"""Packet Definitions
Gregory Brooks, Matt Coates 2018"""

import struct
from PyQt4 import QtCore,QtGui
import json
import datetime

PCKT_LEN = 128  # Number of bytes in a packet

class Packet(object):
    """Weather Station Packet, contains snapshot of all sensor readings"""
    def __init__(self, input_struct=bytes(PCKT_LEN)):
        self.data_struct = input_struct
        meta_data = struct.unpack('<I', self.data_struct[0:4])
        self.timestamp = meta_data[0] # Seconds (UNIX), 4 byte uint
        self.time_date = datetime.datetime.fromtimestamp(self.timestamp).\
            strftime('%H:%M:%S %d-%m-%Y')


        # Get Message Metadata
        # meta_data = struct.unpack('<BBI', self.data_struct[0:6])
        # self.log_type = meta_data[0]
        # self.toad_id = meta_data[1]
        # self.systick = meta_data[2]  # systicks
        # self.systick_freq = 10000  # Hz
        # self.timestamp = self.systick / self.systick_freq  # s

    def printout(self,textbox):
        # Method to print packet to terminal within the GUI
         textbox.moveCursor(QtGui.QTextCursor.End)
         textbox.ensureCursorVisible()
         textbox.insertPlainText("Timestamp: {}\n".format(self.time_date))
#         textbox.insertPlainText("Toad ID: {}\n".format(self.toad_id))
#         textbox.insertPlainText("Systicks: {}\n".format(self.systick))


####OLD STUFF TO DELETE###
# #
# # Message Type Definitions
# MESSAGE_PVT         = 1
# MESSAGE_PSU         = 2
# MESSAGE_POSITION    = 4
# MESSAGE_RX_PACKET   = 32
#
# # TOAD ID Definitions
# TOAD_MASTER = 1  # Chase car
# TOAD_SLAVE = 2   # Balloon
#
# # SR Packet Types
# POSITION_PACKET = 128
#
# class Packet(object):
#     """Base class"""
#     def __init__(self, input_struct=bytes(128)):
#         self.data_struct = input_struct
#
#         # Get Message Metadata
#         meta_data = struct.unpack('<BBI', self.data_struct[0:6])
#         self.log_type = meta_data[0]
#         self.toad_id = meta_data[1]
#         self.systick = meta_data[2]  # systicks
#         self.systick_freq = 10000  # Hz
#         self.timestamp = self.systick / self.systick_freq  # s
#
#     def printout(self,textbox):
#         textbox.moveCursor(QtGui.QTextCursor.End)
#         textbox.ensureCursorVisible()
#         textbox.insertPlainText("Log type: {}\n".format(self.log_type))
#         textbox.insertPlainText("Toad ID: {}\n".format(self.toad_id))
#         textbox.insertPlainText("Systicks: {}\n".format(self.systick))
#
#
#
# class Pvt_packet(Packet):
#
#     def __init__(self, input_struct=bytes(128)):
#
#         Packet.__init__(self, input_struct)
#         payload = self.data_struct[6:98]
#         pvt = struct.unpack('<IHBBBBBBIiBBBBiiiiIIiiiiiIIHHIiI', payload)
#         self.i_tow = pvt[0]
#         self.year = pvt[1]
#         self.month = pvt[2]
#         self.day = pvt[3]
#         self.hour = pvt[4]
#         self.minute = pvt[5]
#         self.second = pvt[6]
#         self.valid = pvt[7]
#         self.t_acc = pvt[8]
#         self.nano = pvt[9]
#         self.fix_type = pvt[10]
#         self.flags = pvt[11]
#         self.num_sv = pvt[13]
#         self.lon = pvt[14]/10000000  # degrees
#         self.lat = pvt[15]/10000000  # degrees
#         self.height = pvt[16]/1000  # m
#         self.h_msl = pvt[17]/1000  # m
#         self.h_acc = pvt[18]
#         self.v_acc = pvt[19]
#         self.velN = pvt[20]
#         self.velE = pvt[21]
#         self.velD = pvt[22]
#         self.gspeed = pvt[23]
#         self.head_mot = pvt[24]
#         self.s_acc = pvt[25]
#         self.head_acc = pvt[26]
#         self.p_dop = pvt[27]
#         self.head_veh = pvt[30]
#
#     def validString(self):
#         if self.valid == 1:
#             return 'validDate'
#         elif self.valid == 2:
#             return 'validTime'
#         elif self.valid == 4:
#             return 'fullyResolved'
#         elif self.valid == 8:
#             return 'validMag'
#         else:
#             return 'Invalid!'
#
#     def fixString(self):
#         list = ['no_fix', 'dead_rkn_only', '2D', '3D', 'GNSS+dead_rkn', 'time_only']
#         if self.fix_type > 5 or self.fix_type < 0:
#             return('Invalid!')
#         else:
#             return list[self.fix_type]
#
#     def printout(self,textbox):
#         textbox.moveCursor(QtGui.QTextCursor.End)
#         textbox.ensureCursorVisible()
#         textbox.insertPlainText("\n\n")
#         textbox.insertPlainText("PVT MESSAGE:\n")
#         textbox.insertPlainText("TOAD ID = {}\n".format(self.toad_id))
#         textbox.insertPlainText("Timestamp = {} s\n".format(self.timestamp))
#         textbox.insertPlainText("Log type = {}\n".format(self.log_type))
#         textbox.insertPlainText("i_tow = {} ms\n".format(self.i_tow))
#         textbox.insertPlainText("year = {}\n".format(self.year))
#         textbox.insertPlainText("month = {}\n".format(self.month))
#         textbox.insertPlainText("day = {}\n".format(self.day))
#         textbox.insertPlainText("hour = {}\n".format(self.hour))
#         textbox.insertPlainText("minute = {}\n".format(self.minute))
#         textbox.insertPlainText("second = {}\n".format(self.second))
#         textbox.insertPlainText("valid = {}\n".format(self.valid))
#         textbox.insertPlainText("t_acc = {} ns\n".format(self.t_acc))
#         textbox.insertPlainText("nano = {} ns\n".format(self.nano))
#         textbox.insertPlainText("fix_type = {}\n".format(self.fix_type))
#         textbox.insertPlainText("flags = {}\n".format(self.flags))
#         textbox.insertPlainText("num_sv = {}\n".format(self.num_sv))
#         textbox.insertPlainText("lat = {} degrees\n".format(self.lat))
#         textbox.insertPlainText("lon = {} degrees\n".format(self.lon))
#         textbox.insertPlainText("height = {} m\n".format(self.height))
#         textbox.insertPlainText("h_msl = {} m\n".format(self.h_msl))
#         textbox.insertPlainText("h_acc = {} mm\n".format(self.h_acc))
#         textbox.insertPlainText("v_acc = {} mm\n".format(self.v_acc))
#         textbox.insertPlainText("velN = {} mm/s\n".format(self.velN))
#         textbox.insertPlainText("velE = {} mm/s\n".format(self.velE))
#         textbox.insertPlainText("velD = {} mm/s\n".format(self.velD))
#         textbox.insertPlainText("gspeed = {} mm/s\n".format(self.gspeed))
#         textbox.insertPlainText("head_mot = {} degrees\n".format(self.head_mot))
#         textbox.insertPlainText("s_acc = {} mm/s\n".format(self.s_acc))
#         textbox.insertPlainText("head_acc = {} degrees\n".format(self.head_acc))
#         textbox.insertPlainText("p_dop = {}\n".format(self.p_dop))
#         textbox.insertPlainText("head_veh = {} degrees\n".format(self.head_veh))
#         textbox.moveCursor(QtGui.QTextCursor.End)
#
# class Psu_packet(Packet):
#     def __init__(self, input_struct=bytes(128)):
#         Packet.__init__(self, input_struct)
#         payload = self.data_struct[6:13]
#         psu = struct.unpack('<HHBBB', payload)
#         self.batt_v = psu[1]/1000  # V
#         self.mcu_temp = psu[4]  # Celsius
#         self.charging = psu[3]
#         self.charge_current = psu[0]  # mA
#         self.charge_temperature = psu[2]  # Celsius
#
#     def printout(self,textbox):
#         textbox.moveCursor(QtGui.QTextCursor.End)
#         textbox.ensureCursorVisible()
#         textbox.insertPlainText("\n\n")
#         textbox.insertPlainText("PSU MESSAGE:\n")
#         textbox.insertPlainText("TOAD ID = {}\n".format(self.toad_id))
#         textbox.insertPlainText("Timestamp = {} s\n".format(self.timestamp))
#         textbox.insertPlainText("Log type = {}\n".format(self.log_type))
#         textbox.insertPlainText("battery voltage = {} V\n".format(self.batt_v))
#         textbox.insertPlainText("stm32 temp = {} °C\n".format(self.mcu_temp))
#         textbox.insertPlainText("charging = {}\n".format(self.charging))
#         textbox.insertPlainText("charge current = {} mA\n".format(self.charge_current))
#         textbox.insertPlainText("charge temperature = {} °C\n".format(self.charge_temperature))
#         textbox.moveCursor(QtGui.QTextCursor.End)
#
#
#
# class Position_packet(Packet):
#     def __init__(self, input_struct=bytes(128)):
#         Packet.__init__(self, input_struct)
#         payload = self.data_struct[6:22]
#         pos = struct.unpack('<BiiiBBB', payload)
#
#         self.lon = pos[1]/10000000  # degrees
#         self.lat = pos[2]/10000000  # degrees
#         self.height = pos[3]/1000  # m
#         self.num_sat = pos[4]
#         self.batt_v = pos[5]/10  # V
#         self.mcu_temp = pos[6]  # Celsius
#
#     def printout(self,textbox):
#         textbox.moveCursor(QtGui.QTextCursor.End)
#         textbox.ensureCursorVisible()
#         textbox.insertPlainText("\n\n")
#         textbox.insertPlainText("POSITION PACKET:\n")
#         textbox.insertPlainText("TOAD ID = {}\n".format(self.toad_id))
#         textbox.insertPlainText("Timestamp = {} s\n".format(self.timestamp))
#         textbox.insertPlainText("Log Type = {}\n".format(self.log_type))
#         textbox.insertPlainText("lat = {} degrees\n".format(self.lat))
#         textbox.insertPlainText("lon = {} degrees\n".format(self.lon))
#         textbox.insertPlainText("height = {} m\n".format(self.height))
#         textbox.insertPlainText("num sat = {}\n".format(self.num_sat))
#         textbox.insertPlainText("battery voltage = {} V\n".format(self.batt_v))
#         textbox.insertPlainText("stm32 temp = {} °C\n".format(self.mcu_temp))
#         textbox.moveCursor(QtGui.QTextCursor.End)
#
#
### Internal to ground station ###
class Usb_conn:
    """Command to enable/disable serial connection"""
    def __init__(self,conn):
        self.conn = conn