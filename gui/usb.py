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

    args = parser.parse_args()
    ser = serial.Serial(args.port)  # Open serial port

    while not gui_exit.is_set():
        # Main loop
        time.sleep(0.2)
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

        if ser.is_open:
            # Read in a packet if there are more bytes than the min packet length available
            if ser.in_waiting>=PCKT_LEN[min(PCKT_LEN,key=PCKT_LEN.get)]:
                # Check ID
                data = ser.read(ID_POSITION+1)
                id = data[ID_POSITION]
                data += ser.read(PCKT_LEN[id] - ID_POSITION - 1)  # Size of packet determined from id

                # Handle message
                if id == Identifier.GPS:
                    message = GPS_Packet(data)
                else:
                    message = Packet(data)
                gui_pipe.send(message)
                log_pipe.send(message)