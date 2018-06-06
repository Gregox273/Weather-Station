"""Handle incoming serial data (logging and parsing).
Gregory Brooks (gb510), Matt Coates(mc955) 2018
"""
import serial
from multiprocessing import Pipe
#import sys
import struct
from .packets import *
import time


def run(gui_pipe, log_pipe, gui_exit, args):
    if args.file:
        while not gui_exit.is_set():
            time.sleep(0.5)
    else:
        ser = serial.Serial(port = args.port, baudrate = args.baud, write_timeout = 0, timeout = 0.05)  # Open serial port
        time.sleep(3)  # Give arduino time to reset
        if args.debug:
            print("Debug mode activated, incoming serial:")

            # Open session log
            out = open('session_log.bin','wb')

        serial_buffer = bytearray()

        BUF_ID = None
        BUF_LEN = None
        BUF_LOG = None  # True if log, false if event

        if args.debug:
            # Trigger sd dump
            cmd = Cmd_Packet(REQUEST_DUMP)
            ser.write(cmd.to_binary())

        while not gui_exit.is_set():
            # Main loop
            if gui_pipe.poll():
                # Receive incoming commands from the gui process
                cmd = gui_pipe.recv()
                if isinstance(cmd,Usb_command):
                    if cmd.conn and not ser.is_open:
                        # Connect
                        ser.open()
                    elif not cmd.conn and ser.is_open:
                        # Disconnect
                        ser.close()
                elif isinstance(cmd,Cmd_Packet):
                    # Send to the arduino
                    if ser.is_open:
                        ser.write(cmd.to_binary())
            if ser.is_open:
                if int(ser.in_waiting) > 4094:
                    print("USB buffer full!")
                byte_in = ser.read()
                if not byte_in:
                    # Timeout, clear buffer and continue while loop
                    serial_buffer = bytearray()
                    BUF_ID = None
                    BUF_LEN = None
                    BUF_LOG = None
                    continue

                else:
                    serial_buffer.extend(byte_in)
                    if len(serial_buffer) > ID_POSITION and BUF_ID == None:
                        # Check ID
                        BUF_ID = serial_buffer[ID_POSITION]
                        if BUF_ID in LOG_PCKT_LIST:
                            BUF_LEN = LOG_PCKT_LIST[BUF_ID][1]
                            BUF_LOG = True
                        elif BUF_ID in EVENT_PCKT_LIST:
                            BUF_LEN = EVENT_PCKT_LIST[BUF_ID][1]
                            BUF_LOG = False
                        else:
                            # Unrecognised packet, clear the buffer
                            serial_buffer = bytearray()
                            BUF_ID = None
                            BUF_LEN = None
                            BUF_LOG = None

                    if BUF_LEN:
                        if len(serial_buffer) >= BUF_LEN:
                            if BUF_LOG:
                                # Log packet
                                message = Log_Packet.construct(serial_buffer[0:BUF_LEN])

                            elif BUF_LOG == False:
                                # Event packet
                                message = Event_Packet.construct(serial_buffer[0:BUF_LEN])

                            if gui_exit.is_set():
                                break  # End process
                            elif args.debug:
                                out.write(message.data_struct)
                                print(message.data_struct)
                            else:
                                log_pipe.send(message)

                            # Clear buffer
                            serial_buffer = bytearray()
                            BUF_ID = None
                            BUF_LEN = None
                            BUF_LOG = None

            else:
                time.sleep(0.1)
