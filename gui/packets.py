"""Packet Definitions
Gregory Brooks, Matt Coates 2018"""

import struct
from PyQt4 import QtCore,QtGui
import json
import datetime

# Important Constants:

# Nominal Supply Voltage
V_SUPPLY = 5.0

# Amplifier Gains
TEMP_GAIN = 5.0164
UV_GAIN = 5.0142
V_LOW_LIGHT_GAIN = 33.9525

# Resistor Values
LIGHT_RES = 995.823
LOW_LIGHT_RES = 32876.6


LOG_PCKT_LEN = 7    # Number of bytes in a standard ADC reading packet
EVENT_PCKT_LEN = 5  # Number of bytes in a log packet

ID_POSITION = 0  # Byte position of log packet ID (zero indexed)

WAKEUP_BYTE = 0xAA  # Command packet prefix

LIGHT_ID = 0x04
LOW_LIGHT_ID = 0x08
V_LOW_LIGHT_ID = 0x10


LOG_PCKT_LIST = {0x01 :["Temperature", LOG_PCKT_LEN],  # Raw ADC
                 0x02: ["UV", LOG_PCKT_LEN],           # Raw ADC
                 LIGHT_ID: ["Light", LOG_PCKT_LEN],        # Raw ADC
                 LOW_LIGHT_ID: ["Low_Light", LOG_PCKT_LEN],    # Raw ADC
                 V_LOW_LIGHT_ID: ["V_Low_Light", LOG_PCKT_LEN],  # Raw ADC
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
                    0x87: ["SD_Dump", EVENT_PCKT_LEN],          # SD card dumped to host computer
                    0x88: ["SD_Wipe", EVENT_PCKT_LEN],          # SD card wiped
                    0x90: ["SD_Dump_End", EVENT_PCKT_LEN]       # End of SD dump (TIMESTAMP INVALID!)
}  # List of event packets {id: ["Name", length in bytes]}
event_pckt_names = [i[0] for i in list(EVENT_PCKT_LIST.values())]

CMD_PCKT_LIST = { 0x11: ["Request_dump", 2],     # Request sd card data dump
                  0x81: ["Start_tx", 2],         # Start sending live sensor data
                  0x18: ["Stop_tx", 2],          # Stop sending lve sensor data
                  0x88: ["RTC_update", 6],       # Current unix time in s
                  0x44: ["Idle_time_update", 6], # Desired idle time in us
                  0x28: ["SD_Wipe",2]            # Wipe the SD card
}  # List of command packets {id: ["Name", length in bytes]}
cmd_pckt_names = [i[0] for i in list(CMD_PCKT_LIST.values())]


# class Log_Packet(object):
#     """Log packet, containing timestamp, id and sensor reading"""
#     def __init__(self, input_struct=bytes(LOG_PCKT_LEN)):
#         self.data_struct = input_struct
#         meta_data = struct.unpack('<BIH', self.data_struct[0:LOG_PCKT_LEN])
#         self.id = meta_data[0]  # Identifier, single byte (uint8)
#         self.timestamp = meta_data[1] # Seconds (UNIX), 4 byte uint
#         self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
#             strftime('%H:%M:%S %d-%m-%Y')
#         self.payload = meta_data[2]  # Sensor reading (uint16)
#
#     @classmethod
#     def construct(cls, id, timestamp, payload):
#     """Construct class by direct field entries"""
#         packed_bytes = struct.pack('<BIH', id, timestamp, payload)
#         return cls(packed_bytes)

class Log_Packet(object):
    """Log packet, containing timestamp, id and sensor reading"""
    def __init__(self, id, timestamp, payload, packed=None):
        if packed:
            self.data_struct = packed
        else:
            self.data_struct = struct.pack('<BIH', id, timestamp, payload)
        self.id = id  # Identifier, single byte (uint8)
        self.timestamp = timestamp  # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.payload = payload  # Sensor reading (uint16)

    @classmethod
    def construct(cls, input_struct=bytes(LOG_PCKT_LEN)):
        """Construct class from binary data"""
        meta_data = struct.unpack('<BIH', input_struct[0:LOG_PCKT_LEN])
        return cls(meta_data[0], meta_data[1], meta_data[2], input_struct)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         name = LOG_PCKT_LIST.get(self.id)[0]
         textbox.insertPlainText("Log Packet: ({})\n".format(name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))
         textbox.insertPlainText("Payload: {}\n\n".format(self.payload))
         textbox.moveCursor(QtGui.QTextCursor.End)

# class Event(object):
#     """Event packet"""
#     def __init__(self,input_struct=bytes(EVENT_PCKT_LEN)):
#         self.data_struct = input_struct
#         meta_data = struct.unpack('<BI', self.data_struct[0:EVENT_PCKT_LEN])
#         self.id = meta_data[0]  # Identifier, single byte (uint8)
#         self.timestamp = meta_data[1] # Seconds (UNIX), 4 byte uint
#         self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
#             strftime('%H:%M:%S %d-%m-%Y')
#
#     @classmethod
#     def construct(cls, id, timestamp):
#     """Construct class by direct field entries"""
#         packed_bytes = struct.pack('<BI', id, timestamp)
#         return cls(packed_bytes)

class Event_Packet(object):
    """Event packet"""
    def __init__(self, id, timestamp, packed=None):
        if packed:
            self.data_struct = packed
        else:
            self.data_struct = struct.pack('<BI', id, timestamp)
        self.id = id  # Identifier, single byte (uint8)
        self.timestamp = timestamp  # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')

    @classmethod
    def construct(cls, input_struct=bytes(EVENT_PCKT_LEN)):
        """Construct class from binary data"""
        meta_data = struct.unpack('<BI', input_struct[0:EVENT_PCKT_LEN])
        return cls(meta_data[0], meta_data[1], input_struct)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         name = EVENT_PCKT_LIST.get(self.id)[0]
         textbox.insertPlainText("Event: ({})\n".format(name))
         textbox.insertPlainText("Timestamp: {} ({}s)\n\n".format(self.time_date,self.timestamp))
         textbox.moveCursor(QtGui.QTextCursor.End)

class Cmd_Packet(object):
    """Base PC to datalogger command packet"""
    def __init__(self, cmd):
        self.cmd = cmd

    def to_binary(self):
        self.packed_bytes = struct.pack('<BB', WAKEUP_BYTE, self.cmd)
        return self.packed_bytes

class RTC_Packet(Cmd_Packet):
    """Packet for PC to send time update to weather station's RTC"""
    def __init__(self, cmd, time):
        Cmd_Packet.__init__(self, cmd)
        self.time = time

    def to_binary(self):
        self.packed_bytes = struct.pack('<BBI', WAKEUP_BYTE, self.cmd, self.time)
        return self.packed_bytes

class Idle_Time_Packet(Cmd_Packet):
    """Packet for PC to send time update to weather station's RTC"""
    def __init__(self, cmd, idle_time):
        Cmd_Packet.__init__(self, cmd)
        self.idle_time = idle_time

    def to_binary(self):
        self.packed_bytes = struct.pack('<BBI', WAKEUP_BYTE, self.cmd, self.idle_time)
        return self.packed_bytes

############ Internal to ground station ############
class Usb_command(object):
    """Command (from GUI to USB process) to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn