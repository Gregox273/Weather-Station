"""Packet Definitions
Gregory Brooks, Matt Coates 2018"""

import struct
from PyQt4 import QtCore,QtGui
import json
import datetime
from enum import Enum

# Important Constants:
LOG_PCKT_LEN = 7    # Number of bytes in a standard ADC reading packet
EVENT_PCKT_LEN = 5  # Number of bytes in a log packet

ID_POSITION = 4  # Byte position of log packet ID (zero indexed)

WAKEUP_BYTE = 0xAA  # Command packet prefix

LOG_PCKT_LIST = {"Temperature":[0x01, LOG_PCKT_LEN], # Raw ADC
                "UV": [0x02, LOG_PCKT_LEN],           # Raw ADC
                "Light": [0x04, LOG_PCKT_LEN],        # Raw ADC
                "Low_Light": [0x08, LOG_PCKT_LEN],   # Raw ADC
                "V_Low_Light": [0x10, LOG_PCKT_LEN],  # Raw ADC
                "Windspeed": [0x20, LOG_PCKT_LEN],    # Frequency
                "Supply_V": [0x40, LOG_PCKT_LEN]      # mV
}  # List of log packets {"Name": [id, length in bytes]}

EVENT_PCKT_LIST = { "RTC_Error": [0x80, EVENT_PCKT_LEN],       # Communication with DS1307 failed
                    "RTC_Update": [0x81, EVENT_PCKT_LEN],      # RTC Time updated
                    "Idle_Update": [0x82, EVENT_PCKT_LEN],      # Idle time between measurement cycles updated
                    "Payload_Error": [0x83, EVENT_PCKT_LEN],    # Payload of a command couldn't be determined
                    "Unknown_Command": [0x84, EVENT_PCKT_LEN],  # Unknown command received
                    "Tx_Enable": [0x85, EVENT_PCKT_LEN],        # Live transmission of data enabled
                    "Tx_Disable": [0x86, EVENT_PCKT_LEN],       # Live transmission of data disabled
                    "SD_Dump": [0x87, EVENT_PCKT_LEN]          # SD card dumped to host computer
}  # List of event packets {"Name": [id, length in bytes]}

CMD_PACKET_LIST = { "Request_dump": [0x11, 2],     # Request sd card data dump
                    "Start_tx": [0x81, 2],         # Start sending live sensor data
                    "Stop_tx": [0x18, 2],          # Stop sending lve sensor data
                    "RTC_update": [0x88, 6],       # Current unix time in s
                    "Idle_time_update": [0x44, 6]  # Desired idle time in us
}  # List of command packets {"Name": [id, length in bytes]}


class Log_Packet(object):
    """Log packet, containing timestamp, id and sensor reading"""
    def __init__(self, input_struct=bytes(LOG_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<IBH', self.data_struct[0:LOG_PCKT_LEN])
        self.timestamp = meta_data[0] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.id = meta_data[1]  # Identifier, single byte (uint8)
        self.payload = meta_data[2]  # Sensor reading (uint16)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         ldict = LOG_PCKT_LIST
         name = list(ldict.keys())[list(ldict.values()(0)).index(self.id)]
         textbox.insertPlainText("Log Packet: ({})\n".format(name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))
         textbox.insertPlainText("Payload: {}\n".format(self.payload))

class Event(object):
    """Event packet"""
    def __init__(self,input_struct=bytes(EVENT_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<IB', self.data_struct[0:EVENT_PCKT_LEN])
        self.timestamp = meta_data[0] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.id = meta_data[1]  # Identifier, single byte (uint8)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         edict = EVENT_PCKT_LIST
         name = list(edict.keys())[list(edict.values()(0)).index(self.id)]
         textbox.insertPlainText("Log Packet: ({})\n".format(name))
         textbox.insertPlainText("Event: ({})\n".format(self.id.name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))

class Cmd_Packet(object):
    """Base PC to datalogger command packet"""
    def __init__(self, cmd):
        self.cmd = cmd

    def to_binary(self):
        self.packed_bytes = struct.pack('<BB', WAKEUP_BYTE, self.cmd)
        return self.packed_bytes

class RTC_packet(Cmd_Packet):
    """Packet for PC to send time update to weather station's RTC"""
    def __init__(self, cmd, time):
        Packet.__init__(self, cmd)
        self.time = time

    def to_binary(self):
        self.packed_bytes = struct.pack('<BBI', WAKEUP_BYTE, self.cmd, self.time)
        return self.packed_bytes

### Internal to ground station ###
class Usb_conn(object):
    """Command (from GUI to USB process) to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn