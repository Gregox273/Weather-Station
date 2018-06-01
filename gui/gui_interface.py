"""GUI Process
Gregory Brooks(gb510), Matt Coates(mc955) 2018
Includes gist (https://gist.github.com/friendzis/4e98ebe2cf29c0c2c232)
by friendzis & scls19fr
and code by Jean-François Fabre & ömer sarı (https://stackoverflow.com/questions/39308042/sqlite3-database-tables-export-in-csv)
# Code for second axis on UV graphs by lambcutlet (https://stackoverflow.com/questions/48590354/pyqtgraph-plotwidget-multiple-y-axis-plots-in-wrong-area)
"""
from PyQt4 import QtCore, QtGui#, QtWebKit
from PyQt4.QtCore import QThread, SIGNAL, QTimer
from multiprocessing import Pipe, Process
from .frontend import *
from .frontend.main_window import Ui_WeatherStation
from .packets import *
from .fir_filter import fir_filter
import sys
import os
import time
#from timeit import default_timer as timer
#from math import floor
import pyqtgraph as pg
import datetime
import sqlite3
import numpy as np
import csv

script_dir = os.path.dirname(__file__)
x_wind = np.array([7,14,4,13,18,6,5,18,5,4,11,4,3,2])
y_wind = np.array([4,5.7,2.8,6.6,12.9,5.9,3.5,12,1.3,2.1,4.7,2.3,1.6,2])
z_wind = np.polyfit(x_wind, y_wind, 3)
f_wind = np.poly1d(z_wind)

SUPPLY_V_ID = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Supply_V")]

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
        return [int2dt(value).strftime("%H:%M:%S\n%-d/%-m/%Y") for value in values]

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
    def __init__(self, usb_pipe, log_pipe, db_filepath, parent=None):

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
        self.plot_temp_O.setLabel('left', 'Temperature', units='°C')
        # self.plot_temp_O.setLabel('bottom', 'Timestamp')

        self.plot_wind_O = self.graphicsLayoutWidgetWind_O.addPlot(
            title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind_O.setLabel('left', 'Wind Speed', units='m/s')
        # self.plot_wind_O.setLabel('bottom', 'Timestamp')

        self.plot_light_O = self.graphicsLayoutWidgetLight_O.addPlot(
            title='Light Levels',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light_O.setLabel('left', 'Light Intensity', units='lx')
        # self.plot_light_O.setLogMode(x=False, y=True)
        # self.plot_light_O.setLabel('bottom', 'Timestamp')

        self.plot_uv_O = self.graphicsLayoutWidgetUV_O.addPlot(
            title='UV Index',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv_O.setLabel('left', 'UV Index')
        # self.plot_uv_O.setLabel('bottom', 'Timestamp')

        # Individual tabs
        self.plot_temp = self.graphicsLayoutWidgetTemp.addPlot(
            title='Temperature',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_temp.setLabel('left', 'Temperature', units='°C')
        # self.plot_temp.setLabel('bottom', 'Timestamp')

        self.plot_wind = self.graphicsLayoutWidgetWind.addPlot(
            title='Wind Speed',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_wind.setLabel('left', 'Wind Speed', units='m/s')
        # self.plot_wind.setLabel('bottom', 'Timestamp')

        self.plot_light = self.graphicsLayoutWidgetLight.addPlot(
            title='Light Levels',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_light.setLabel('left', 'Light Intensity', units='lx')
        # self.plot_light.setLogMode(x=False, y=True)
        # self.plot_light.setLabel('bottom', 'Timestamp')

        self.plot_uv = self.graphicsLayoutWidgetUV.addPlot(
            title='UV Index',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot_uv.setLabel('left', 'UV Index')
        # self.plot_uv.setLabel('bottom', 'Timestamp')

        # Second y axis for UV Graphs
        # self.p2_uv_O = pg.ViewBox()
        # self.p2_uv = pg.ViewBox()
        # self.p2_plot_O = pg.PlotCurveItem()
        # self.p2_plot = pg.PlotCurveItem()
        # self.p2_uv_O.addItem(self.p2_plot_O)
        # self.p2_uv.addItem(self.p2_plot)
        # self.plot_uv_O.showAxis('right')
        # self.plot_uv.showAxis('right')
        # self.plot_uv_O.scene().addItem(self.p2_uv_O)
        # self.plot_uv.scene().addItem(self.p2_uv)
        # self.plot_uv_O.getAxis('right').linkToView(self.p2_uv_O)
        # self.plot_uv.getAxis('right').linkToView(self.p2_uv)
        # self.p2_uv_O.setXLink(self.plot_uv_O)
        # self.p2_uv.setXLink(self.plot_uv)

        # self.plot_uv_O.vb.sigResized.connect(lambda: self.updateViewsUV(self.plot_uv_O,self.p2_uv_O))
        # self.plot_uv.vb.sigResized.connect(lambda: self.updateViewsUV(self.plot_uv, self.p2_uv))

        # Power axis for UV graphs
        # self.plot_uv_O.setLabel('right', 'UV Power', units="W/m^2")
        # self.plot_uv.setLabel('right', 'UV Power', units="W/m^2")

        # Update thread, don't start yet
        thread_end,self.gui_end = Pipe(duplex=False)  # So that QThread and gui don't use same pipe end at same time
        self.update_thread = MainThd(thread_end, usb_pipe, log_pipe)
        self.connect(self.update_thread, SIGNAL("new_packet(PyQt_PyObject)"),self.new_packet)

        # Add slots and signals manually:
        self.pushButtonDumpSD.clicked.connect(self.dump_sd)
        self.radioButtonLiveData.clicked.connect(lambda: self.toggle_live_data(self.radioButtonLiveData.isChecked()))
        self.pushButtonRefreshHistoric.clicked.connect(self.historic_plot)
        self.dateTimeEditHistoricFrom.dateTimeChanged.connect(self.historic_plot)
        self.dateTimeEditHistoricTo.dateTimeChanged.connect(self.historic_plot)
        self.pushButtonUpdateRTC.clicked.connect(self.update_rtc)
        self.pushButtonSetIdle.clicked.connect(lambda: self.set_idle(self.spinBoxIdleTime.value()))

        self.actionWipe_SD_Card.triggered.connect(self.wipe_sd)
        self.actionSave_Terminal.triggered.connect(self.terminal_save)
        self.actionExport_Database.triggered.connect(self.export_db)
        self.actionConnect.triggered.connect(self.toggle_con)

        #self.tabWidgetSubTerminal.currentChanged.connect(self.update_terminal_tab)

        # Add db
        self.db_filepath = db_filepath

        # SD dump flag
        self.DUMP_IN_PROGRESS = False

        # Filtering flag
        #self.FILTER = True

        # Start update thread
        self.update_thread.start(QThread.LowPriority)

    # def update_terminal_tab(self):
    #     if self.tabWidgetSubTerminal.currentIndex() == 1:
    #         # Log packet tab
    #             cmd = 'SELECT id, timestamp, payload_16 from log_table WHERE id IN ({log_ids}) ORDER BY timestamp ASC'.format(log_ids=",".join(["?"]*len(LOG_PCKT_LIST.keys())))
    #             from_db = self.run_db(cmd, list(LOG_PCKT_LIST.keys()))
    #             for i in from_db:
    #                 pckt = Log_Packet(i[0],i[1],i[2])
    #                 pckt.printout(self.textBrowserTerminalLogs)
    #
    #     elif self.tabWidgetSubTerminal.currentIndex() == 2:
    #         # Event packet tab
    #         cmd = 'SELECT id, timestamp, payload_16 from log_table WHERE id IN ({ev_ids}) ORDER BY timestamp ASC'.format(ev_ids=",".join(["?"]*len(EVENT_PCKT_LIST.keys())))
    #         from_db = self.run_db(cmd, list(EVENT_PCKT_LIST.keys()))
    #         for i in from_db:
    #             pckt = Event_Packet(i[0],i[1],i[2])
    #             pckt.printout(self.textBrowserTerminalEvents)

    def updateViewsUV(self, graph, p2):
        p2.setGeometry(graph.vb.sceneBoundingRect())
        #self.p2_uv.setGeometry(self.plot_uv_O.vb.sceneBoundingRect())

    def dump_sd(self):
        self.dump_in_progress(True)
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index("Request_dump")]
        cmd = Cmd_Packet(cmd_id)
        self.gui_end.send(cmd)

    def dump_in_progress(self,arg=None):
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
            self.send_cmd("Start_tx")
        else:
            self.historic_plot()
            self.send_cmd("Stop_tx")

    def new_packet(self, packet):
        # Print to terminal tab
        packet.printout(self.textBrowserTerminal)
        if packet.id in LOG_PCKT_LIST:
            packet.printout(self.textBrowserTerminalLogs)
            if packet.id == SUPPLY_V_ID:
                self.lcdNumberBattV.display(packet.payload/1000)
        #self.update_terminal_tab()


        if packet.id in EVENT_PCKT_LIST:
            packet.printout(self.textBrowserTerminalEvents)
            new_name = EVENT_PCKT_LIST.get(packet.id)[0]
            if new_name == "SD_Dump_End":
                # SD Dump has ended
                self.dump_in_progress(False)
                return None

        elif self.radioButtonLiveData.isChecked(): # and not self.dump_in_progress():
            # Display live data
            go_back = self.spinBoxGoingBack.value()*60  # Go back this many seconds on live graph
            new_name = LOG_PCKT_LIST.get(packet.id)[0]
            if new_name == "Temperature":
                # Fetch temperatures
                self.update_temp(int(round(time.time())) - go_back, 2147483647)  # Until unix time overflow

            elif new_name == "Windspeed":
                # Fetch wind speed
                self.update_wind(int(round(time.time())) - go_back, 2147483647)
                pass

            elif new_name in ("Light, Low_Light, V_Low_Light"):
                # Fetch Light
                self.update_light(int(round(time.time())) - go_back, 2147483647)
                pass

            elif new_name == "UV":
                # Fetch UV
                self.update_UV(int(round(time.time())) - go_back, 2147483647)
                pass

    def run_db(self,cmd,args=None):
        conn = sqlite3.connect(self.db_filepath,timeout=20)
        c = conn.cursor()
        if args:
            c.execute(cmd,args)
        else:
            c.execute(cmd)
        val = c.fetchall()
        conn.close()
        return val

    def update_temp(self,start,end):
        # Fetch temperatures and plot them
        cmd = 'SELECT timestamp, payload_16 from log_table WHERE timestamp BETWEEN {t_s} AND {t_e} AND id == {i} ORDER BY timestamp ASC'.\
            format(t_s = start, t_e = end, i = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Temperature")])
        temperatures = self.run_db(cmd)
        if temperatures:
            # If not empty
            temperatures = np.asarray(temperatures)
            temperatures = temperatures.astype(float)
            temperatures[:,1] = ((temperatures[:,1]*V_SUPPLY)/(1024.0*TEMP_GAIN))*100.0 - 50.0
            filtering = self.spinBoxFiltering.value()
            if filtering > 0:
                print("filtering")
                temperatures[:,1] = fir_filter(temperatures[:,1],filtering)
            else:
                print("not filtering")
            self.plot_temp_O.plot(temperatures, clear = True,pen=(255,0,0))
            self.plot_temp.plot(temperatures, clear = True,pen=(255,0,0))

    def update_UV(self,start,end):
        # Fetch UV measurements and plot them
        cmd = 'SELECT timestamp, payload_16 from log_table WHERE timestamp BETWEEN {t_s} AND {t_e} AND id == {i} ORDER BY timestamp ASC'.\
            format(t_s = start, t_e = end, i = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("UV")])
        uv_readings = self.run_db(cmd)
        if uv_readings:
            # If not empty
            uv_readings = np.asarray(uv_readings)
            uv_readings = uv_readings.astype(float)

            uv_vout = uv_readings[:,1]*V_SUPPLY/(1024.0*UV_GAIN)
            uv_index = uv_vout/(4.3*0.026)
            #uv_power = uv_vout*10000.0/(4.3*113)
            uv_index = np.column_stack((uv_readings[:,0], uv_index))
            #uv_power = np.column_stack((uv_readings[:,0], uv_power))
            #uv_power = np.asarray(uv_power)

            filtering = self.spinBoxFiltering.value()
            if filtering > 0:
                uv_index[:,1] = fir_filter(uv_index[:,1],filtering)

            self.plot_uv_O.plot(uv_index, clear = True,pen=(0,0,255))
            #self.plot_uv_O.plot(uv_power, pen=(255,0,255))
            self.plot_uv.plot(uv_index, clear = True,pen=(0,0,255))
            #self.plot_uv.plot(uv_power, pen=(255,0,255))

            # self.p2_uv_O.addItem(pg.PlotCurveItem(uv_readings[:,0],uv_power, pen=(255,0,255)))
            # self.p2_uv.addItem(pg.PlotCurveItem(uv_readings[:,0],uv_power, pen=(255,0,255)))
            # self.p2_plot_O.setData(uv_readings[:,0],uv_power, pen=(255,0,255))
            # self.p2_plot.setData(uv_readings[:,0],uv_power, pen=(255,0,255))

    def update_light(self,start,end):
        # Fetch light levels and plot them
        cmd = 'SELECT id, timestamp, payload_16 from log_table WHERE timestamp BETWEEN {t_s} AND {t_e} AND (id == {i1} OR id == {i2} OR id == {i3})  ORDER BY timestamp ASC'.\
            format(t_s = start, t_e = end, i1 = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Light")], i2 = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Low_Light")], i3 = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("V_Low_Light")])
        light = self.run_db(cmd)
        if light:
            # If not empty
            light = [self.convert_light(i) for i in light if self.convert_light(i)]
            light = np.asarray(light)
            light = light.astype(float)

            filtering = self.spinBoxFiltering.value()
            if filtering > 0:
                light[:,1] = fir_filter(light[:,1],filtering)

            self.plot_light_O.plot(light, clear = True,pen=(100,100,0))
            self.plot_light.plot(light, clear = True,pen=(100,100,0))

    def convert_light(self,meas):
        if meas[2] > 20 and meas[2] < 673:
            if meas[0] == LIGHT_ID:
                return (meas[1],10**7 * (meas[2]/1024) * V_SUPPLY/LIGHT_RES)  # lx
            elif meas[0] == LOW_LIGHT_ID:
                return (meas[1],10**7 * (meas[2]/1024) * V_SUPPLY/LOW_LIGHT_RES)  # lx
            elif meas[0] == V_LOW_LIGHT_ID:
                return (meas[1],10**7 * (meas[2]/1024) * V_SUPPLY/(V_LOW_LIGHT_GAIN*LOW_LIGHT_RES))  # lx
        else:
            return False# if meas[0] == LIGHT_ID:
        #     if meas[2] > 20 and meas[2] < 673:
        #
        #     else:
        #         return False
        # elif meas[0] == LOW_LIGHT_ID:
        #     if meas[2] > 20 and meas[2] < 673:
        #         return (meas[0],meas[1],(meas[2]/1024) * V_SUPPLY/LIGHT_RES)  # Photocurrent in A
        #     else:
        #         return False
        # elif meas[0 == V_LOW_LIGHT_ID:
        #     if meas[2] > and meas[2] < :
        #         return (meas[0],meas[1],(meas[2]/1024) * V_SUPPLY/LIGHT_RES)  # Photocurrent in A
        #     else:
        #         return False
        # else:
        #     return False

    def update_wind(self,start,end):
        # Fetch light levels and plot them
        cmd = 'SELECT timestamp, payload_16 from log_table WHERE timestamp BETWEEN {t_s} AND {t_e} AND id == {i} ORDER BY timestamp ASC'.\
            format(t_s = start, t_e = end, i = list(LOG_PCKT_LIST.keys())[log_pckt_names.index("Windspeed")])
        wind = self.run_db(cmd)
        if wind:
            # If not empty
            wind = np.asarray(wind)
            wind = wind.astype(float)
            wind[:,1] = f_wind(wind[:,1])  # m/s
            # Set negative values to 0
            wind[:,1] = np.where(wind[:,1] < 0, 0, wind[:,1])

            filtering = self.spinBoxFiltering.value()
            if filtering > 0:
                wind[:,1] = fir_filter(wind[:,1],filtering)

            self.plot_wind_O.plot(wind, clear = True,pen=(0,0,0))
            self.plot_wind.plot(wind, clear = True,pen=(0,0,0))

    def historic_plot(self):
        if not self.radioButtonLiveData.isChecked():
            # Plot data in historic mode
            start = int(round(self.dateTimeEditHistoricFrom.dateTime().toTime_t()))
            end = int(round(self.dateTimeEditHistoricTo.dateTime().toTime_t()))
            self.update_temp(start,end)
            self.update_UV(start,end)
            self.update_light(start,end)
            self.update_wind(start,end)

    def set_text(self,text,lineedit):
        lineedit.setText(str(text))
        lineedit.home(False)  # Return cursor to start so most significant digits displayed

    def terminal_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
        file = open(name,'w')
        file.write(self.textBrowserTerminal.toPlainText())
        file.close()

    def wipe_sd(self):
        choice = QtGui.QMessageBox.question(self, 'Wipe SD Card',
                                            "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.send_cmd("SD_Wipe")
        else:
            pass

    def export_db(self):
        conn = sqlite3.connect(self.db_filepath,timeout=20)
        c = conn.cursor()

        # First check whether database is empty
        c.execute("SELECT exists(SELECT 1 from log_table);")
        n = c.fetchall()
        if n[0][0] == 0:
            # Empty table
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Database is empty!")
            msg.setWindowTitle("Export Database")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            #msg.buttonClicked.connect(msgbtn)

            msg.exec_()
           # print "value of pressed message box button:", retval
        else:
            name = QtGui.QFileDialog.getSaveFileName(self,'Export Database')
            if not name.lower().endswith('.csv'):
                name = name + '.csv'
            file = open(name,'w',newline="")
            conn.row_factory = sqlite3.Row
            crsr=conn.execute("SELECT * From log_table")
            row=crsr.fetchone()
            titles=row.keys()

            data = c.execute("SELECT * FROM log_table")

            writer = csv.writer(file,delimiter=';')
            writer.writerow(titles)  # keys=title you're looking for
            # write the rest
            writer.writerows(data)

            file.close()
            conn.close()

    def toggle_con(self):
        if self.actionConnect.isChecked():
            # Connect
            self.gui_end.send(Usb_command(True))
        else:
            # Disconnect
            self.gui_end.send(Usb_command(False))

    def send_cmd(self,name):
        cmd_id = list(CMD_PCKT_LIST.keys())[cmd_pckt_names.index(name)]
        cmd = Cmd_Packet(cmd_id)
        self.gui_end.send(cmd)

    def closeEvent(self, event):
        self.send_cmd("Stop_tx")  # Stop transmitting live data when gui is closed
        event.accept() # let the window close


def run(usb_pipe, log_pipe, gui_exit,db_filepath):
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))


    main_window = gcs_main_window(usb_pipe, log_pipe,db_filepath)
    main_window.show()

    app.exec_()
    gui_exit.set()

    # Might need to keep log->gui pipe empty here if it causes problems
    #(cf. loggign process keeping usb pipe clear)
