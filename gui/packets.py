"""Packet Definitions
Gregory Brooks, Matt Coates 2018"""

import struct
from PyQt4 import QtCore,QtGui
import json
import datetime
from enum import Enum

# Log packet identifier definitions
class Identifier(Enum):
    Temperature = 0x01
    UV = 0x02
    Light = 0x04
    Windspeed = 0x08
    Air_quality = 0x18
    GPS = 0x81

# Command packet identifiers
class Command(Enum):
    Request_dump = 0x11
    Start_tx = 0x81
    Stop_tx  = 0x18
    RTC_update   = 0x88

# Important Constants:
STD_PCKT_LEN = 7   # Number of bytes in a standard ADC reading packet
GPS_PCKT_LEN = 20  # Number of bytes in GPS packet
PCKT_LEN = {Identifier.Temperature: STD_PCKT_LEN,
            Identifier.UV: STD_PCKT_LEN,
            Identifier.Light: STD_PCKT_LEN,
            Identifier.Windspeed: STD_PCKT_LEN,
            Identifier.Air_quality: STD_PCKT_LEN,
            Identifier.GPS: GPS_PCKT_LEN}  # List of packet lengths

ID_POSITION = 4  # Byte position of log packet ID (zero indexed)

WAKEUP_BYTE = 0xAA




class Std_Packet(object):
    """Standard log packet, containing timestamp, id and sensor reading"""
    def __init__(self, input_struct=bytes(STD_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<IBH', self.data_struct[0:STD_PCKT_LEN])
        self.timestamp = meta_data[0] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.id = meta_data[1]  # Identifier, single byte (uint8)
        self.payload = meta_data[2]  # Sensor reading (uint16)

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         textbox.insertPlainText("Timestamp: {} ({}s)\n".format(self.time_date,self.timestamp))
         textbox.insertPlainText("Identifier: {}\n".format(self.id.name))
         textbox.insertPlainText("Payload: {}\n".format(self.payload))

class GPS_Packet(object):
    """Log of GPS output (from NMEA strings)"""
    def __init__(self, input_struct=bytes(GPS_PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<IBiiHIB', self.data_struct[0:GPS_PCKT_LEN])
        self.timestamp = meta_data[0] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.id = meta_data[1]
        self.latitude = meta_data[2]
        self.longitude = meta_data[3]
        self.height = meta_data[4]
        self.gps_time = meta_data[5]
        self.gps_time_date = datetime.datetime.fromtimestamp(self.gps_time).\
            strftime('%H:%M:%S %d-%m-%Y')
        self.num_sat = meta_data[6]

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         textbox.insertPlainText("Timestamp: {} ({})\n".format(self.time_date,self.timestamp))
         textbox.insertPlainText("Identifier: {}\n".format(self.id.name))
         textbox.insertPlainText("Latitude: {}°N\n".format(self.latitude))
         textbox.insertPlainText("Longitude: {}°E\n".format(self.longitude))
         textbox.insertPlainText("Height: {}m\n".format(self.height))
         textbox.insertPlainText("GPS Time: {} ({}s)\n".format(self.gps_time_date,self.gps_time))
         textbox.insertPlainText("# of Satellites: {}\n".format(self.num_sat))

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
class Usb_conn:
    """Command (from GUI to USB process) to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn