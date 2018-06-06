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

# Data Log IDs
ID_TEMP = 0x01
ID_UV = 0x02
ID_LIGHT = 0x04
ID_LOW_LIGHT = 0x8
ID_V_LOW_LIGHT = 0x10
ID_WIND = 0x20
ID_VCC = 0x40

# Event Log IDs
RTC_ERROR = 0x80
RTC_UPDATE = 0x81
IDLE_UPDATE = 0x82
PAYLOAD_ERROR = 0x83
UNKNOWN_COMMAND = 0x84
TX_ENABLE = 0x85
TX_DISABLE = 0x86
SD_DUMP = 0x87
SD_WIPE = 0x88
SD_END = 0x90


LOG_PCKT_LIST = {ID_TEMP :["Temperature", LOG_PCKT_LEN],  # Raw ADC
                 ID_UV: ["UV", LOG_PCKT_LEN],           # Raw ADC
                 ID_LIGHT: ["Light", LOG_PCKT_LEN],        # Raw ADC
                 ID_LOW_LIGHT: ["Low_Light", LOG_PCKT_LEN],    # Raw ADC
                 ID_V_LOW_LIGHT: ["V_Low_Light", LOG_PCKT_LEN],  # Raw ADC
                 ID_WIND: ["Windspeed", LOG_PCKT_LEN],    # Frequency
                 ID_VCC: ["Supply_V", LOG_PCKT_LEN]      # mV
}  # List of log packets {id: ["Name", length in bytes]}
log_pckt_names = [i[0] for i in list(LOG_PCKT_LIST.values())]

EVENT_PCKT_LIST = { RTC_ERROR: ["RTC_Error", EVENT_PCKT_LEN],        # Communication with DS1307 failed
                    RTC_UPDATE: ["RTC_Update", EVENT_PCKT_LEN],       # RTC Time updated
                    IDLE_UPDATE: ["Idle_Update", EVENT_PCKT_LEN],      # Idle time between measurement cycles updated
                    PAYLOAD_ERROR: ["Payload_Error", EVENT_PCKT_LEN],    # Payload of a command couldn't be determined
                    UNKNOWN_COMMAND: ["Unknown_Command", EVENT_PCKT_LEN],  # Unknown command received
                    TX_ENABLE: ["Tx_Enable", EVENT_PCKT_LEN],        # Live transmission of data enabled
                    TX_DISABLE: ["Tx_Disable", EVENT_PCKT_LEN],       # Live transmission of data disabled
                    SD_DUMP: ["SD_Dump", EVENT_PCKT_LEN],          # SD card dumped to host computer
                    SD_WIPE: ["SD_Wipe", EVENT_PCKT_LEN],          # SD card wiped
                    SD_END: ["SD_Dump_End", EVENT_PCKT_LEN]       # End of SD dump (TIMESTAMP INVALID!)
}  # List of event packets {id: ["Name", length in bytes]}
event_pckt_names = [i[0] for i in list(EVENT_PCKT_LIST.values())]

REQUEST_DUMP = 0x11
START_TX = 0x81
STOP_TX = 0x18
RTC_UPDATE_CMD = 0x88
IDLE_UPDATE_CMD = 0x44
SD_WIPE_CMD = 0x28

CMD_PCKT_LIST = { REQUEST_DUMP: ["Request_dump", 2],     # Request sd card data dump
                  START_TX: ["Start_tx", 2],         # Start sending live sensor data
                  STOP_TX: ["Stop_tx", 2],          # Stop sending lve sensor data
                  RTC_UPDATE_CMD: ["RTC_update", 6],       # Current unix time in s
                  IDLE_UPDATE_CMD: ["Idle_time_update", 6], # Desired idle time in us
                  SD_WIPE_CMD: ["SD_Wipe",2]            # Wipe the SD card
}  # List of command packets {id: ["Name", length in bytes]}
cmd_pckt_names = [i[0] for i in list(CMD_PCKT_LIST.values())]


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
BEGIN_DUMP = 1

class Usb_command(object):
    """Command (from GUI to USB process) to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn