"""GUI Process
Gregory Brooks(gb510), Matt Coates(mc955) 2018
Includes gist (https://gist.github.com/friendzis/4e98ebe2cf29c0c2c232)
by friendzis & scls19fr
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

                if isinstance(new_packet_window,Usb_command):
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

        # Add slots and signals manually

        # Configure plots
        self.plot_temp_L = self.graphicsLayoutWidgetTemp_L.addPlot(title='Temperature',
            axisItems={ 'bottom': TimeAxisItem(orientation="bottom")})
        self.plot_temp_H = self.graphicsLayoutWidgetTemp_H.addPlot(title='Temperature',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind_L = self.graphicsLayoutWidgetWind_L.addPlot(title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind_H = self.graphicsLayoutWidgetWind_H.addPlot(title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv_L = self.graphicsLayoutWidgetUV_L.addPlot(title='UV Intensity',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv_H = self.graphicsLayoutWidgetUV_H.addPlot(title='UV Intensity',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light_L = self.graphicsLayoutWidgetLight_L.addPlot(title='Light Intensity',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light_H = self.graphicsLayoutWidgetLight_H.addPlot(title='Light Intensity',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})


        all_graphs =    [self.plot_temp_L, self.plot_temp_H,
                        self.plot_wind_L, self.plot_wind_H,
                        self.plot_uv_L, self.plot_uv_H,
                        self.plot_light_L, self.plot_light_H]
        for nr, obj in enumerate(all_graphs):
            # Apply operation to every graph
            pass
            #obj.repaint()

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