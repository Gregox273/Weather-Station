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

script_dir = os.path.dirname(__file__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def int2dt(ts, ts_mult=1e6):
    return(datetime.datetime.utcfromtimestamp(float(ts)/ts_mult))

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
            if self.usb_pipe.poll(0.01):
                new_packet_usb = self.usb_pipe.recv()
                self.emit(SIGNAL('new_packet(PyQt_PyObject)'),new_packet_usb)

            if self.window_pipe.poll(0.01):
                new_packet_window = self.window_pipe.recv()

                if isinstance(new_packet_window,Usb_command)\
                    or isinstance(new_packet_window, Cmd_Packet):
                        self.usb_pipe.send(new_packet_window)


class gcs_main_window(QtGui.QMainWindow, Ui_WeatherStation):
    """Inherit main window generated in QT4 Designer"""
    def __init__(self, usb_pipe, log_pipe, parent=None):

        # Graphs - enable antialiasing
        pg.setConfigOptions(antialias=True,  # Enable antialiasing
                            background=0.8,  # Background fill
                            foreground='k')  # Black foreground (axes etc.)

        super().__init__(parent)
        self.setupUi(self)

        # Add slots and signals manually:

        # Update thread, don't start yet
        thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
        self.update_thread = MainThd(thread_end, usb_pipe, log_pipe)
        self.connect(self.update_thread, SIGNAL("new_packet(PyQt_PyObject)"),self.new_packet)

        self.pushButtonDumpSD.clicked.connect(self.dump_sd)
        self.pushButtonUpdateRTC.clicked.connect(self.update_rtc)
        self.pushButtonSetIdle.clicked.connect(lambda: self.set_idle(self.spinBoxIdleTime.value()))
        self.radioButtonLiveData.clicked.connect(lambda: self.toggle_live_data(self.radioButtonLiveData.isChecked()))
        # Start update thread
        self.update_thread.start(QThread.LowPriority)

    def dump_sd(self):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Request_dump")]
        cmd = Cmd_Packet(cmd_id)
        self.gui_end.send(cmd)

    def update_rtc(self):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("RTC_update")]
        cmd = RTC_Packet(cmd_id, time.time())  # Update with current time
        self.gui_end.send(cmd)

    def set_idle(self,idle_time):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("RTC_update")]
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

    def set_text(self,text,lineedit):
        lineedit.setText(str(text))
        lineedit.home(False)  # Return cursor to start so most significant digits displayed

    def terminal_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
        file = open(name,'w')
        text = self.textBrowser_terminal.toPlainText()
        file.write(text)
        file.close()

def run(usb_pipe, log_pipe, gui_exit):
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    main_window = gcs_main_window(usb_pipe, log_pipe)
    main_window.show()
    app.exec_()
    gui_exit.set()