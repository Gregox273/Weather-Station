"""GUI Process
Gregory Brooks(gb510), Matt Coates(mc955) 2018
"""
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import QThread, SIGNAL,QTimer
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

script_dir = os.path.dirname(__file__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

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

                if isinstance(new_packet_window,Usb_command):
                    self.usb_pipe.send(new_packet_window)


class gcs_main_window(QtGui.QMainWindow, Ui_WeatherStation):
    """Inherit main window generated in QT4 Designer"""
    def __init__(self, usb_pipe, log_pipe, parent=None):

        super().__init__(parent)
        self.setupUi(self)
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # Add slots and signals manually

        # Configure plots
        self.graphicsViewTemp_L.plot([100,101,102],[200,210,220],title="Temperature")  

        # Start update thread
        thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
        self.update_thread = MainThd(thread_end, usb_pipe, log_pipe)
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

def run(usb_pipe, log_pipe, gui_exit):
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    main_window = gcs_main_window(usb_pipe, log_pipe)
    main_window.show()
    app.exec_()
    gui_exit.set()