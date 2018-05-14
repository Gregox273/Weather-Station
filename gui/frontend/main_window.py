# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WeatherStation(object):
    def setupUi(self, WeatherStation):
        WeatherStation.setObjectName(_fromUtf8("WeatherStation"))
        WeatherStation.resize(606, 469)
        self.centralwidget = QtGui.QWidget(WeatherStation)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.main_tab_widget.setMinimumSize(QtCore.QSize(300, 300))
        self.main_tab_widget.setTabPosition(QtGui.QTabWidget.West)
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
        self.tabLive_view = QtGui.QWidget()
        self.tabLive_view.setObjectName(_fromUtf8("tabLive_view"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabLive_view)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.graphicsViewUV_L = PlotWidget(self.tabLive_view)
        self.graphicsViewUV_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewUV_L.setObjectName(_fromUtf8("graphicsViewUV_L"))
        self.gridLayout_2.addWidget(self.graphicsViewUV_L, 1, 0, 1, 1)
        self.graphicsViewWind_L = PlotWidget(self.tabLive_view)
        self.graphicsViewWind_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewWind_L.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsViewWind_L.setObjectName(_fromUtf8("graphicsViewWind_L"))
        self.gridLayout_2.addWidget(self.graphicsViewWind_L, 0, 1, 1, 1)
        self.graphicsViewLight_L = PlotWidget(self.tabLive_view)
        self.graphicsViewLight_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewLight_L.setObjectName(_fromUtf8("graphicsViewLight_L"))
        self.gridLayout_2.addWidget(self.graphicsViewLight_L, 1, 1, 1, 1)
        self.graphicsViewTemp_L = PlotWidget(self.tabLive_view)
        self.graphicsViewTemp_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewTemp_L.setObjectName(_fromUtf8("graphicsViewTemp_L"))
        self.gridLayout_2.addWidget(self.graphicsViewTemp_L, 0, 0, 1, 1)
        self.main_tab_widget.addTab(self.tabLive_view, _fromUtf8(""))
        self.tabHistoric_view = QtGui.QWidget()
        self.tabHistoric_view.setObjectName(_fromUtf8("tabHistoric_view"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabHistoric_view)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.graphicsViewTemp_H = PlotWidget(self.tabHistoric_view)
        self.graphicsViewTemp_H.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewTemp_H.setObjectName(_fromUtf8("graphicsViewTemp_H"))
        self.gridLayout_3.addWidget(self.graphicsViewTemp_H, 0, 0, 1, 1)
        self.graphicsViewWind_H = PlotWidget(self.tabHistoric_view)
        self.graphicsViewWind_H.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewWind_H.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsViewWind_H.setObjectName(_fromUtf8("graphicsViewWind_H"))
        self.gridLayout_3.addWidget(self.graphicsViewWind_H, 0, 1, 1, 1)
        self.graphicsViewUV_H = PlotWidget(self.tabHistoric_view)
        self.graphicsViewUV_H.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewUV_H.setObjectName(_fromUtf8("graphicsViewUV_H"))
        self.gridLayout_3.addWidget(self.graphicsViewUV_H, 1, 0, 1, 1)
        self.graphicsViewLight_H = PlotWidget(self.tabHistoric_view)
        self.graphicsViewLight_H.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsViewLight_H.setObjectName(_fromUtf8("graphicsViewLight_H"))
        self.gridLayout_3.addWidget(self.graphicsViewLight_H, 1, 1, 1, 1)
        self.main_tab_widget.addTab(self.tabHistoric_view, _fromUtf8(""))
        self.tabTerminal = QtGui.QWidget()
        self.tabTerminal.setObjectName(_fromUtf8("tabTerminal"))
        self.gridLayout = QtGui.QGridLayout(self.tabTerminal)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowserTerminal = QtGui.QTextBrowser(self.tabTerminal)
        self.textBrowserTerminal.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTerminal.setOpenLinks(True)
        self.textBrowserTerminal.setObjectName(_fromUtf8("textBrowserTerminal"))
        self.gridLayout.addWidget(self.textBrowserTerminal, 0, 0, 1, 1)
        self.main_tab_widget.addTab(self.tabTerminal, _fromUtf8(""))
        self.verticalLayout.addWidget(self.main_tab_widget)
        WeatherStation.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WeatherStation)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 606, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSerial = QtGui.QMenu(self.menubar)
        self.menuSerial.setObjectName(_fromUtf8("menuSerial"))
        WeatherStation.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(WeatherStation)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        WeatherStation.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(WeatherStation)
        self.actionConnect.setCheckable(True)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionLive_Sensor_Data = QtGui.QAction(WeatherStation)
        self.actionLive_Sensor_Data.setCheckable(True)
        self.actionLive_Sensor_Data.setChecked(True)
        self.actionLive_Sensor_Data.setObjectName(_fromUtf8("actionLive_Sensor_Data"))
        self.actionDownload_from_SD = QtGui.QAction(WeatherStation)
        self.actionDownload_from_SD.setCheckable(True)
        self.actionDownload_from_SD.setChecked(True)
        self.actionDownload_from_SD.setObjectName(_fromUtf8("actionDownload_from_SD"))
        self.menuSerial.addAction(self.actionConnect)
        self.menuSerial.addSeparator()
        self.menuSerial.addAction(self.actionLive_Sensor_Data)
        self.menuSerial.addAction(self.actionDownload_from_SD)
        self.menubar.addAction(self.menuSerial.menuAction())

        self.retranslateUi(WeatherStation)
        self.main_tab_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(WeatherStation)

    def retranslateUi(self, WeatherStation):
        WeatherStation.setWindowTitle(_translate("WeatherStation", "Weather Station -gb510, mc955", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabLive_view), _translate("WeatherStation", "Live View", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabHistoric_view), _translate("WeatherStation", "Historic View", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabTerminal), _translate("WeatherStation", "Terminal", None))
        self.menuSerial.setTitle(_translate("WeatherStation", "Serial", None))
        self.actionConnect.setText(_translate("WeatherStation", "Connect", None))
        self.actionLive_Sensor_Data.setText(_translate("WeatherStation", "Display Live Sensor Data", None))
        self.actionDownload_from_SD.setText(_translate("WeatherStation", "Download Data from SD", None))

from pyqtgraph import PlotWidget

class WeatherStation(QtGui.QMainWindow, Ui_WeatherStation):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

