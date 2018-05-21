"""Packet Definitions
Gregory Brooks, Matt Coates 2018"""

import struct
from PyQt4 import QtCore,QtGui
import json
import datetime
#from enum import Enum

# Important Constants:
LOG_PCKT_LEN = 7    # Number of bytes in a standard ADC reading packet
EVENT_PCKT_LEN = 5  # Number of bytes in a log packet

ID_POSITION = 0  # Byte position of log packet ID (zero indexed)

WAKEUP_BYTE = 0xAA  # Command packet prefix

LOG_PCKT_LIST = {0x01 :["Temperature", LOG_PCKT_LEN],  # Raw ADC
                 0x02: ["UV", LOG_PCKT_LEN],           # Raw ADC
                 0x04: ["Light", LOG_PCKT_LEN],        # Raw ADC
                 0x08: ["Low_Light", LOG_PCKT_LEN],    # Raw ADC
                 0x10: ["V_Low_Light", LOG_PCKT_LEN],  # Raw ADC
                 0x20: ["Windspeed", LOG_PCKT_LEN],    # Frequency
                 0x40: ["Supply_V", LOG_PCKT_LEN]      # mV
}  # List of log packets {id: ["Name", length in bytes]}
log_pckt_names = [i[0] for i in list(LOG_PCKT_LIST.values())]

EVENT_PCKT_LIST = { 0x80: ["RTC_Error", EVENT_PCKT_LEN],        # Communication with DS1307 failed
                    0x81: ["RTC_Update", EVENT_PCKT_LEN],       # RTC Time updated
                    0x82: ["Idle_Update", EVENT_PCKT_LEN],      # Idle time between measurement cycles updated
                    0x83: ["Payload_Error", EVENT_PCKT_LEN],    # Payload of a command couldn't be determined
                    0x84: ["Unknown_Command", EVENT_PCKT_LEN],  # Unknown command received
                    0x85: ["Tx_Enable", EVENT_PCKT_LEN],        # Live transmission of data enabled
                    0x86: ["Tx_Disable", EVENT_PCKT_LEN],       # Live transmission of data disabled
                    0x87: ["SD_Dump", EVENT_PCKT_LEN]           # SD card dumped to host computer
}  # List of event packets {id: ["Name", length in bytes]}
event_pckt_names = [i[0] for i in list(EVENT_PCKT_LIST.values())]

CMD_PCKT_LIST = { 0x11: ["Request_dump", 2],     # Request sd card data dump
                  0x81: ["Start_tx", 2],         # Start sending live sensor data
                  0x18: ["Stop_tx", 2],          # Stop sending lve sensor data
                  0x88: ["RTC_update", 6],       # Current unix time in s
                  0x44: ["Idle_time_update", 6]  # Desired idle time in us
}  # List of command packets {id: ["Name", length in bytes]}
cmd_pckt_names = [i[0] for i in list(CMD_PCKT_LIST.values())]


class Log_Packet(object):
    """Log packet, containing timestamp, id and sensor reading"""
    def __init__(self, input_struct=bytes(LOG_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<BIH', self.data_struct[0:LOG_PCKT_LEN])
        self.id = meta_data[0]  # Identifier, single byte (uint8)
        self.timestamp = meta_data[1] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.payload = meta_data[2]  # Sensor reading (uint16)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         name = LOG_PCKT_LIST.get(self.id)[0]
         textbox.insertPlainText("Log Packet: ({})\n".format(name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))
         textbox.insertPlainText("Payload: {}\n".format(self.payload))

class Event(object):
    """Event packet"""
    def __init__(self,input_struct=bytes(EVENT_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<BI', self.data_struct[0:EVENT_PCKT_LEN])
        self.id = meta_data[0]  # Identifier, single byte (uint8)
        self.timestamp = meta_data[1] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')


    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         name = EVENT_PCKT_LIST.get(self.id)[0]
         textbox.insertPlainText("Log Packet: ({})\n".format(name))
         textbox.insertPlainText("Event: ({})\n".format(self.id.name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))

class Cmd_Packet(object):
    """Base PC to datalogger command packet"""
    def __init__(self, cmd):
        self.cmd = cmd

    def to_binary(self):
        self.packed_bytes = struct.pack('>BB', WAKEUP_BYTE, self.cmd)
        return self.packed_bytes

class RTC_Packet(Cmd_Packet):
    """Packet for PC to send time update to weather station's RTC"""
    def __init__(self, cmd, time):
        Cmd_Packet.__init__(self, cmd)
        self.time = time

    def to_binary(self):
        self.packed_bytes = struct.pack('>BBI', WAKEUP_BYTE, self.cmd, self.time)
        return self.packed_bytes

class Idle_Time_Packet(Cmd_Packet):
    """Packet for PC to send time update to weather station's RTC"""
    def __init__(self, cmd, idle_time):
        Cmd_Packet.__init__(self, cmd)
        self.idle_time = idle_time

    def to_binary(self):
        self.packed_bytes = struct.pack('>BBI', WAKEUP_BYTE, self.cmd, self.idle_time)
        return self.packed_bytes

### Internal to ground station ###
class Usb_command(object):
    """Command (from GUI to USB process) to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn