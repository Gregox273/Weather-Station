"""Handle incoming serial data (logging and parsing).
Gregory Brooks (gb510), Matt Coates(mc955) 2018
"""
import serial
from multiprocessing import Pipe
#import sys
import struct
from .packets import *
import time
import argparse


def run(gui_pipe, log_pipe, gui_exit):
    # Process arguments
    parser = argparse.ArgumentParser(description= \
        'Connect to weather station on given serial port (default /dev/ttyACM0)')
    parser.add_argument('--port', dest='port', type=str, nargs='?', \
        default='/dev/ttyACM0', help='Serial port to use')

    parser.add_argument('--baud', dest='baud', type=int, nargs='?', \
        default=115200, help='Baud rate')

    parser.add_argument("-d", "--debug", help="print incoming serial",
                    action="store_true")

    args = parser.parse_args()
    ser = serial.Serial(port = args.port, baudrate = args.baud, write_timeout = 3, timeout = 800/args.baud)  # Open serial port
    # timeout is time taken to send 100 bytes at baudrate
    time.sleep(3)  # Give arduino time to reset
    if args.debug:
        print("Debug mode activated, incoming serial:")
        
        # Open session log
        out = open('session_log.bin','wb') 
    
    serial_buffer = bytearray()

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
            byte_in = ser.read()
            if not byte_in:
                # Timeout, clear buffer and continue while loop
                serial_buffer = bytearray()
                continue
            if args.debug:
                # In debug mode, print incoming bytes to terminal
                # and also to the session log file
                #print(byte_in.decode('utf-8'), end='')
                out.write(byte_in)
                print(byte_in)
            else:
                serial_buffer.extend(byte_in)
                if len(serial_buffer) > ID_POSITION:
                    # Check ID
                    id = serial_buffer[ID_POSITION]
                    if id in LOG_PCKT_LIST:
                        length = LOG_PCKT_LIST.get(id)[1]
                        if len(serial_buffer) >= length:
                            message = Log_Packet(serial_buffer[0:length])
                            gui_pipe.send(message)
                            log_pipe.send(message)
                    elif id in EVENT_PCKT_LIST:
                        length = EVENT_PCKT_LIST.get(id)[1]
                        if len(serial_buffer) >= length:
                            message = Event_Packet(serial_buffer[0:length])
                            gui_pipe.send(message)
                            log_pipe.send(message)
                    else:
                        # Unrecognised packet, empty buffer
                        serial_buffer = bytearray()


        else:
            time.sleep(0.2)
