"""GUI Process
Gregory Brooks(gb510), Matt Coates(mc955) 2018
Includes gist (https://gist.github.com/friendzis/4e98ebe2cf29c0c2c232)
by friendzis & scls19fr
"""
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import QThread, SIGNAL, QTimer
from multiprocessing import Pipe, Process
from .frontend import *
from .frontend.main_window import Ui_WeatherStation
from .packets import *
import sys
import os
import time
from timeit import default_timer as timer
from math import floor
import pyqtgraph as pg
import datetime
import sqlite3
import numpy as np

script_dir = os.path.dirname(__file__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def int2dt(ts):
    return(datetime.datetime.utcfromtimestamp(float(ts)))

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int2dt(value).strftime("%H:%M:%S\n%-j/%-m/%Y") for value in values]

class MainThd(QThread):
    def __init__(self, window_pipe, usb_pipe, log_pipe):
        QThread.__init__(self)
        self.window_pipe = window_pipe
        self.usb_pipe = usb_pipe
        self.log_pipe = log_pipe

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            if self.log_pipe.poll(0.05):
                new_packet_from_log = self.log_pipe.recv()
                self.emit(SIGNAL('new_packet(PyQt_PyObject)'),new_packet_from_log)

            if self.window_pipe.poll(0.05):
                new_packet_window = self.window_pipe.recv()

                if isinstance(new_packet_window,Usb_command)\
                    or isinstance(new_packet_window, Cmd_Packet):
                        self.usb_pipe.send(new_packet_window)


class gcs_main_window(QtGui.QMainWindow, Ui_WeatherStation):
    """Inherit main window generated in QT4 Designer"""
    def __init__(self, usb_pipe, log_pipe, conn, cursor, db_filepath, parent=None):

        # Graphs - enable antialiasing
        pg.setConfigOptions(antialias=True,  # Enable antialiasing
                            background=0.8,  # Background fill
                            foreground='k')  # Black foreground (axes etc.)

        super().__init__(parent)
        self.setupUi(self)

        # Configure plots
        # Overview page
        self.plot_temp_O = self.graphicsLayoutWidgetTemp_O.addPlot(
            title='Temperature',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind_O = self.graphicsLayoutWidgetWind_O.addPlot(
            title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light_O = self.graphicsLayoutWidgetLight_O.addPlot(
            title='Light Levels',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv_O = self.graphicsLayoutWidgetUV_O.addPlot(
            title='UV Index',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        # Individual tabs
        self.plot_temp = self.graphicsLayoutWidgetTemp.addPlot(
            title='Temperature',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind = self.graphicsLayoutWidgetWind.addPlot(
            title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light = self.graphicsLayoutWidgetLight.addPlot(
            title='Light Levels',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv = self.graphicsLayoutWidgetUV.addPlot(
            title='UV Index',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        # Update thread, don't start yet
        thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
        self.update_thread = MainThd(thread_end, usb_pipe, log_pipe)
        self.connect(self.update_thread, SIGNAL("new_packet(PyQt_PyObject)"),self.new_packet)

        # Add slots and signals manually:
        self.pushButtonDumpSD.clicked.connect(self.dump_sd)
        self.radioButtonLiveData.clicked.connect(lambda: self.toggle_live_data(self.radioButtonLiveData.isChecked()))
        self.dateTimeEditHistoricFrom.dateTimeChanged.connect(self.historic_plot)
        self.dateTimeEditHistoricTo.dateTimeChanged.connect(self.historic_plot)
        self.pushButtonUpdateRTC.clicked.connect(self.update_rtc)
        self.pushButtonSetIdle.clicked.connect(lambda: self.set_idle(self.spinBoxIdleTime.value()))

        # Add db
        self.db_conn = conn
        self.db_cursor = cursor
        self.db_filepath = db_filepath  # For creating new temporary connections

        # SD dump flag
        self.DUMP_IN_PROGRESS = False

        # Start update thread
        self.update_thread.start(QThread.LowPriority)

    def dump_sd(self):
        self.DUMP_IN_PROGRESS(True)
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Request_dump")]
        cmd = Cmd_Packet(cmd_id)
        self.gui_end.send(cmd)

    def DUMP_IN_PROGRESS(self,arg=None):
        if arg:
            self.DUMP_IN_PROGRESS = arg
        return self.DUMP_IN_PROGRESS

    def update_rtc(self):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("RTC_update")]
        cmd = RTC_Packet(cmd_id, int(round(time.time())))  # Update with current time
        self.gui_end.send(cmd)

    def set_idle(self,idle_time):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Idle_time_update")]
        cmd = Idle_Time_Packet(cmd_id, idle_time)
        self.gui_end.send(cmd)

    def toggle_live_data(self, on):
        if on:
            cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Start_tx")]
        else:
            cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Stop_tx")]
        cmd = Cmd_Packet(cmd_id)
        self.gui_end.send(cmd)

    def new_packet(self, packet):
        # Print to terminal tab
        packet.printout(self.textBrowser_terminal)

        if packet.id in EVENT_PCKT_LIST:
            new_name = EVENT_PCKT_LIST.get(packet.id)[0]
            if new_name == "SD_Dump_End":
                # SD Dump has ended
                self.DUMP_IN_PROGRESS(False)
                return

        if self.radioButtonLiveData.isChecked() and not self.DUMP_IN_PROGRESS():
            # Display live data
            go_back = self.spinBoxGoingBack.value()*60  # Go back this many seconds on live graph
            new_name = LOG_PCKT_LIST.get(packet.id)[0]

            if new_name == "Temperature":
                # Fetch temperatures
                self.update_temp(int(round(time.time())) - go_back, 2147483647)
                # self.db_cursor.execute(
                #     'SELECT timestamp, payload_16 from log_table WHERE timestamp >= {t} AND id == {i})'.\
                #     format(t = ) - go_back, i = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Temperature")]))
                # temperatures = self.db_cursor.fetchall()
                # temperatures = np.asarray(temperatures)
                #
                # self.plot_temp_O.plot(temperatures, clear = True,pen=(255,0,0))
                # self.plot_temp.plot(temperatures, clear = True,pen=(255,0,0))

            elif new_name == "Windspeed":
                # Fetch wind speed
                #self.update_wind(int(round(time.time())) - go_back, 2147483647)
                pass

            elif new_name in ("Light, Low_Light, V_Low_Light"):
                # Fetch Light
                #self.update_light(int(round(time.time())) - go_back, 2147483647)
                pass

            elif new_name == "UV":
                # Fetch UV
                #self.update_UV(int(round(time.time())) - go_back, 2147483647)
                pass

    def update_temp(self,start,end):
        # Fetch temperatures and plot them
        self.db_cursor.execute(
            'SELECT timestamp, payload_16 from log_table WHERE timestamp BETWEEN {t_s} AND {t_e} AND id == {i})'.\
            format(t_s = start, t_e = end, i = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Temperature")]))
        temperatures = self.db_cursor.fetchall()
        temperatures = np.asarray(temperatures)

        self.plot_temp_O.plot(temperatures, clear = True,pen=(255,0,0))
        self.plot_temp.plot(temperatures, clear = True,pen=(255,0,0))

    def historic_plot(self):
        if not self.radioButtonLiveData.isChecked():
            # Plot data in historic mode
            start = int(round(self.dateTimeEditHistoricFrom.dateTime.toMSecsSinceEpoch()/1000))
            end = int(round(self.dateTimeEditHistoricTo.dateTime.toMSecsSinceEpoch()/1000))
            self.update_temp(start,end)
            #self.update_light(start,end)
            #etc.

    def set_text(self,text,lineedit):
        lineedit.setText(str(text))
        lineedit.home(False)  # Return cursor to start so most significant digits displayed

    def terminal_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
        file = open(name,'w')
        text = self.textBrowser_terminal.toPlainText()
        file.write(text)
        file.close()

def run(usb_pipe, log_pipe, gui_exit,db_filepath):
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))

    db_conn = sqlite3.connect(db_filepath)
    db_cursor = db_conn.cursor()

    main_window = gcs_main_window(usb_pipe, log_pipe, db_conn, db_cursor,db_filepath)
    main_window.show()

    app.exec_()

    db_conn.close()
    gui_exit.set()
