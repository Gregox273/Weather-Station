"""GUI Process
Gregory Brooks(gb510), Matt Coates(mc955) 2018
"""
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import QThread, SIGNAL,QTimer
from multiprocessing import Pipe, Process
from .frontend import *
from .frontend.toad_gui import Ui_main_window
from .packets import *
import sys
import os
import time
from timeit import default_timer as timer
from math import floor

script_dir = os.path.dirname(__file__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MainThd(QThread):
    def __init__(self, window_pipe, usb_pipe):
        QThread.__init__(self)
        self.window_pipe = window_pipe
        self.usb_pipe = usb_pipe

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            if self.usb_pipe.poll(0.01):
                new_packet_usb = self.usb_pipe.recv()
                self.emit(SIGNAL('new_packet(PyQt_PyObject)'),new_packet_usb)

            if self.window_pipe.poll(0.01):
                new_packet_window = self.window_pipe.recv()

                if isinstance(new_packet_window,Usb_command):
                    self.usb_pipe.send(new_packet_window)


class gcs_main_window(QtGui.QMainWindow, Ui_main_window):
    """Inherit main window generated in QT4 Designer"""
    def __init__(self, usb_pipe, parent=None):

        super().__init__(parent)
        self.setupUi(self)

        # Add slots and signals manually

        # Start update thread
        thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
        self.update_thread = MainThd(thread_end, usb_pipe)
        self.connect(self.update_thread, SIGNAL("new_packet(PyQt_PyObject)"),self.new_packet)
        self.update_thread.start(QThread.LowPriority)


    def new_packet(self, packet):
        # Print to terminal tab
        packet.printout(self.textBrowser_terminal)

    def set_text(self,text,lineedit):
        lineedit.setText(str(text))
        lineedit.home(False)  # Return cursor to start so most significant digits displayed

    def terminal_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
        file = open(name,'w')
        text = self.textBrowser_terminal.toPlainText()
        file.write(text)
        file.close()

def run(usb_pipe, gui_exit):
    app = QtGui.QApplication(sys.argv)
    main_window = gcs_main_window(usb_pipe)
    main_window.show()
    app.exec_()
    gui_exit.set()

###OLD STUFF BELOW###


#

#
#
#
#
#
# class MainThd(QThread):
#     def __init__(self, window_pipe, usb_pipe):
#         QThread.__init__(self)
#         self.window_pipe = window_pipe
#         self.usb_pipe = usb_pipe
#
#     def __del__(self):
#         self.wait()
#
#     def run(self):
#         while True:
#             if self.usb_pipe.poll(0.01):
#                 new_packet_usb = self.usb_pipe.recv()
#                 self.emit(SIGNAL('new_packet(PyQt_PyObject)'),new_packet_usb)
#
#             if self.window_pipe.poll(0.01):
#                 new_packet_window = self.window_pipe.recv()
#
#                 if isinstance(new_packet_window,Usb_command):
#                     self.usb_pipe.send(new_packet_window)
#
#
# class WebView(QtWebKit.QWebView):
#     def __init__(self, parent=None):
#         super(WebView, self).__init__(parent)
#         self.page().mainFrame().addToJavaScriptWindowObject("WebView", self)
#
#     def contextMenuEvent(self, event):
#         pass
#
# class gcs_main_window(QtGui.QMainWindow, Ui_main_window):
#     """Inherit main window generated in QT4 Designer"""
#     def __init__(self, usb_pipe, parent=None):
#
#         super().__init__(parent)
#         self.setupUi(self)
#
#         # Add map
#         self.map_view = WebView()
#         self.splitter.insertWidget(0,self.map_view)
#         self.map_view.setObjectName(_fromUtf8("map_view"))
#
#         self.map_view.page().mainFrame().addToJavaScriptWindowObject("TOAD Map", self)
#         rel_path = 'leaflet_map/map.html'
#         abs_file_path = os.path.abspath(os.path.join(script_dir,rel_path))
#         self.map_view.load(QtCore.QUrl.fromLocalFile(abs_file_path))
#         #self.map_view.loadFinished.connect(self.on_map_load)
#
#         # Add slots and signals manually
#         self.car_frame.pushButton_conn.clicked.connect(self.toggle_con)
#         #self.balloon_frame.start_apogee.clicked.connect(self.start_apogee)
#         self.actionSave_Terminal.triggered.connect(self.terminal_save)
#         self.actionRefresh.triggered.connect(self.refresh_map)
#
#         self.actionCentre_on_Balloon.triggered.connect(self.centre_on_balloon)
#         self.actionCentre_on_Chase_Car.triggered.connect(self.centre_on_car)
#         self.actionFollow_Balloon.triggered.connect(self.follow_balloon)
#         self.actionFollow_Chase_Car.triggered.connect(self.follow_car)
#
#         # Start update thread
#         thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
#         self.update_thread = MainThd(thread_end, usb_pipe)
#         self.connect(self.update_thread, SIGNAL("new_packet(PyQt_PyObject)"),self.new_packet)
#         self.update_thread.start(QThread.LowPriority)
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.tick)
#         self.timer.start(100)
#
#     def refresh_map(self):
#         self.map_view.load(QtCore.QUrl.fromLocalFile(os.path.abspath(os.path.join(script_dir,'leaflet_map/map.html'))))
#
#     def toggle_con(self):
#         if self.car_frame.pushButton_conn.isChecked():
#             # Connect
#             self.car_frame.pushButton_conn.setText("Disconnect")
#             self.gui_end.send(Usb_command(True))
#         else:
#             # Disconnect
#             self.car_frame.pushButton_conn.setText("Connect")
#             self.gui_end.send(Usb_command(False))
#
#
#     def centre_on_balloon(self):
#         self.map_view.page().mainFrame().evaluateJavaScript("map.setView(balloon.getLatLng());")
#
#     def centre_on_car(self):
#         self.map_view.page().mainFrame().evaluateJavaScript("map.setView(chase_car.getLatLng());")
#
#     def follow_balloon(self):
#         # Uncheck 'Follow Chase Car' if we want to centre on balloon
#         self.actionFollow_Chase_Car.setChecked(False)
#         self.centre_on_balloon()
#
#     def follow_car(self):
#         # Uncheck 'Follow Balloon' if we want to centre on chase car
#         self.actionFollow_Balloon.setChecked(False)
#         self.centre_on_car()
#
#     def fill_fields_pvt(self,frame,packet):
#         self.set_text(packet.timestamp,frame.lineEdit_timestamp_pvt)
#
#         self.set_text("{} ({})".format(packet.fixString(),packet.fix_type),frame.LineEdit_fixtype)
#
#         self.set_text("{} ({})".format(packet.validString(),packet.valid),frame.LineEdit_validity)
#
#         #Set UTC time
#         date_time_obj = QtCore.QDateTime(packet.year, packet.month, packet.day,
#                                          packet.hour,packet.minute,packet.second)
#         frame.DateTimeEdit.setDateTime(date_time_obj)
#
#         self.set_text(packet.num_sv,frame.LineEdit_num_sv)
#
#     def fill_fields_psu(self,frame,packet):
#         self.set_text(packet.timestamp,frame.lineEdit_timestamp_psu)
#
#         #self.set_text(packet.charging,frame.LineEdit_charging)
#         if packet.charging:
#             self.set_text("Yes",frame.LineEdit_charging)
#         else:
#             self.set_text("No",frame.LineEdit_charging)
#
#         self.set_text(packet.charge_current,frame.LineEdit_charge_current)
#
#         self.set_text(packet.charge_temperature,frame.LineEdit_charge_temp)
#
#
#     def fill_fields_pos(self,frame,packet):
#         self.set_text(packet.timestamp, frame.tframe.lineEdit_timestamp_pos)
#
#         self.set_text(packet.lat,frame.tframe.lineEdit_lat)
#
#         self.set_text(packet.lon, frame.tframe.lineEdit_lon)
#
#         self.set_text(packet.height,frame.tframe.lineEdit_height)
#
#         self.set_text(packet.num_sat, frame.tframe.lineEdit_num_sat)
#
#         self.set_text(packet.batt_v, frame.tframe.lineEdit_batt_v)
#
#         self.set_text(packet.mcu_temp, frame.tframe.lineEdit_mcu_temp)
#
#     # Reduce CPU usage by only moving markers after some time has passed
#     balloon_prev_time = timer()
#     car_prev_time = timer()
#
#     def tick(self):
#         self.set_text(int(floor(timer() - self.car_prev_time)), self.car_frame.tframe.lineEdit_timesince)
#         self.set_text(int(floor(timer() - self.balloon_prev_time)), self.balloon_frame.tframe.lineEdit_timesince)
#
#
#     def new_packet(self, packet):
#         # Print to terminal tab
#         packet.printout(self.textBrowser_terminal)
#
#         if packet.toad_id == TOAD_MASTER:
#             toad_frame_x = self.car_frame
#             id_no = 0
#         elif packet.toad_id == TOAD_SLAVE:
#             toad_frame_x = self.balloon_frame
#             id_no = 1
#
#         if packet.log_type == MESSAGE_PVT:
#             self.fill_fields_pvt(self.car_frame, packet)
#         elif packet.log_type == MESSAGE_PSU:
#             self.fill_fields_psu(self.car_frame, packet)
#         elif packet.log_type == MESSAGE_POSITION:
#             self.fill_fields_pos(toad_frame_x, packet)
#             if self.balloon_frame.start_apogee.isChecked() \
#                 and packet.toad_id == TOAD_SLAVE \
#                 and int(packet.height) > 1000*float(self.balloon_frame.lineEdit_apogee.text()) :
#                 self.set_text(int(packet.height)/1000, self.balloon_frame.lineEdit_apogee)
#
#             # Update map marker
#             if packet.toad_id == TOAD_SLAVE and abs(timer() - self.balloon_prev_time) > 5:
#                 self.balloon_prev_time = timer()
#                 self.map_view.page().mainFrame().evaluateJavaScript("balloon.setLatLng([{},{}]);".format(packet.lat,packet.lon))
#                 if self.actionFollow_Balloon.isChecked():
#                     self.centre_on_balloon()
#             elif packet.toad_id == TOAD_MASTER and abs(timer() - self.car_prev_time) > 5:
#                 self.car_prev_time = timer()
#                 self.map_view.page().mainFrame().evaluateJavaScript("chase_car.setLatLng([{},{}]);".format(packet.lat,packet.lon))
#                 if self.actionFollow_Chase_Car.isChecked():
#                     self.centre_on_car()
# #     def trilat_rx(self, packet):
# #         if isinstance(packet,Position_fix):
# #             e_disp = packet.e_coord - self.origin[0]
# #             n_disp = packet.n_coord - self.origin[1]
# #             u_disp = packet.u_coord - self.origin[2]  # Altitude - pad altitude
# #             alt_disp = int(round(u_disp))
# #             self.altimeter.display(alt_disp)
# #
# #             self.set_text(e_disp,self.dxLineEdit)
# #             self.set_text(n_disp,self.dyLineEdit)
# #             self.set_text(u_disp,self.dzLineEdit)
# #
# #             llh = convert_ENU_to_llh([packet.e_coord, packet.n_coord, packet.u_coord])
# #             self.set_text(llh[0],self.latitudeLineEdit)
# #             self.set_text(llh[1],self.longitudeLineEdit)
# #
# #             if not self.first_trilat_rx_packet:
# #                 dx = packet.e_coord - self.trilat_rx_prev_packet.e_coord  # m
# #                 dy = packet.n_coord - self.trilat_rx_prev_packet.n_coord  # m
# #                 dz = packet.u_coord - self.trilat_rx_prev_packet.u_coord  # m
# #                 dt = packet.itow_s - self.trilat_rx_prev_packet.itow_s    # s
# #
# #                 self.set_text(dx/dt,self.dxdtLineEdit)
# #                 self.set_text(dy/dt,self.dydtLineEdit)
# #                 self.set_text(dz/dt,self.dzdtLineEdit)
# #
# #                 speed = ( (dx/dt)**2 + (dy/dt)**2 + (dz/dt)**2 )**0.5
# #                 self.set_text(speed,self.lineEdit_speed)
# #
# #             if packet.u_coord > self.apogee:
# #                 # New max alt
# #                 self.apogee = packet.u_coord
# #                 self.max_alt_value.display(int(round(self.apogee - self.origin[2])))
# #
# #             self.trilat_rx_prev_packet = packet
# #             self.first_trilat_rx_packet = False
# #
# #             # Update map markers including u_disp in the bubble
# #             self.map_view.page().mainFrame().evaluateJavaScript("toad_marker_1.setLatLng([{},{}]); \
# # toad_marker_2.setLatLng([{},{}]); \
# # toad_marker_3.setLatLng([{},{}]); \
# # toad_marker_4.setLatLng([{},{}]); \
# # toad_marker_5.setLatLng([{},{}]); \
# # toad_marker_6.setLatLng([{},{}]); \
# # marker_dart.setLatLng([{},{}]);   \
# # marker_dart.bindPopup(\"TOAD Dart (height above pad: {} m)\").openPopup();"
# #             .format(self.balloon_frame.frame.lineEdit_lat.text(),self.balloon_frame.frame.lineEdit_lon.text(),
# #                     self.frame_toad_2.frame.lineEdit_lat.text(),self.frame_toad_2.frame.lineEdit_lon.text(),
# #                     self.frame_toad_3.frame.lineEdit_lat.text(),self.frame_toad_3.frame.lineEdit_lon.text(),
# #                     self.frame_toad_4.frame.lineEdit_lat.text(),self.frame_toad_4.frame.lineEdit_lon.text(),
# #                     self.frame_toad_5.frame.lineEdit_lat.text(),self.frame_toad_5.frame.lineEdit_lon.text(),
# #                     self.frame_toad_6.frame.lineEdit_lat.text(),self.frame_toad_6.frame.lineEdit_lon.text(),
# #                     llh[0],llh[1], u_disp))
# #             #self.map_view.page().mainFrame().evaluateJavaScript("marker_dart.setLatLng([{},{}]);".format(llh[0],llh[1]))
# #             #self.map_view.page().mainFrame().evaluateJavaScript("marker_dart.bindPopup(\"TOAD Dart (height above pad: {} m)\").openPopup();".format(u_disp))
#
#     def set_text(self,text,lineedit):
#         lineedit.setText(str(text))
#         lineedit.home(False)  # Return cursor to start so most significant digits displayed
#
#     def terminal_save(self):
#         name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
#         file = open(name,'w')
#         text = self.textBrowser_terminal.toPlainText()
#         file.write(text)
#         file.close()
#
# def run(usb_pipe, gui_exit):
#     app = QtGui.QApplication(sys.argv)
#     main_window = gcs_main_window(usb_pipe)
#     main_window.show()
#     #sys.exit(app.exec_())
#     app.exec_()
#     gui_exit.set()
