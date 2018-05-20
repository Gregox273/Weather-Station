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
        WeatherStation.resize(738, 469)
        self.centralwidget = QtGui.QWidget(WeatherStation)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.main_tab_widget.setMinimumSize(QtCore.QSize(300, 300))
        self.main_tab_widget.setTabPosition(QtGui.QTabWidget.West)
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
        self.tabOverview = QtGui.QWidget()
        self.tabOverview.setObjectName(_fromUtf8("tabOverview"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabOverview)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.graphicsLayoutWidgetUV_L = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetUV_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetUV_L.setObjectName(_fromUtf8("graphicsLayoutWidgetUV_L"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetUV_L, 1, 0, 1, 1)
        self.graphicsLayoutWidgetTemp_L = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetTemp_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetTemp_L.setObjectName(_fromUtf8("graphicsLayoutWidgetTemp_L"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetTemp_L, 0, 0, 1, 1)
        self.graphicsLayoutWidgetLight_L = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetLight_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetLight_L.setObjectName(_fromUtf8("graphicsLayoutWidgetLight_L"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetLight_L, 1, 1, 1, 1)
        self.graphicsLayoutWidgetWind_L = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetWind_L.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetWind_L.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetWind_L.setObjectName(_fromUtf8("graphicsLayoutWidgetWind_L"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetWind_L, 0, 1, 1, 1)
        self.main_tab_widget.addTab(self.tabOverview, _fromUtf8(""))
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
        self.tabSerial = QtGui.QWidget()
        self.tabSerial.setObjectName(_fromUtf8("tabSerial"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabSerial)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.textBrowserSerial = QtGui.QTextBrowser(self.tabSerial)
        self.textBrowserSerial.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserSerial.setOpenLinks(True)
        self.textBrowserSerial.setObjectName(_fromUtf8("textBrowserSerial"))
        self.gridLayout_4.addWidget(self.textBrowserSerial, 0, 0, 1, 1)
        self.main_tab_widget.addTab(self.tabSerial, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.main_tab_widget, 0, 0, 1, 1)
        self.widgetButtons = QtGui.QWidget(self.centralwidget)
        self.widgetButtons.setMinimumSize(QtCore.QSize(140, 200))
        self.widgetButtons.setMaximumSize(QtCore.QSize(16777215, 200))
        self.widgetButtons.setObjectName(_fromUtf8("widgetButtons"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widgetButtons)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonDumpSD = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonDumpSD.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonDumpSD.setObjectName(_fromUtf8("pushButtonDumpSD"))
        self.verticalLayout.addWidget(self.pushButtonDumpSD)
        self.radioButtonLiveData = QtGui.QRadioButton(self.widgetButtons)
        self.radioButtonLiveData.setMinimumSize(QtCore.QSize(100, 26))
        self.radioButtonLiveData.setObjectName(_fromUtf8("radioButtonLiveData"))
        self.verticalLayout.addWidget(self.radioButtonLiveData)
        self.pushButtonUpdateRTC = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonUpdateRTC.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonUpdateRTC.setObjectName(_fromUtf8("pushButtonUpdateRTC"))
        self.verticalLayout.addWidget(self.pushButtonUpdateRTC)
        self.pushButtonSetIdle = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonSetIdle.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonSetIdle.setObjectName(_fromUtf8("pushButtonSetIdle"))
        self.verticalLayout.addWidget(self.pushButtonSetIdle)
        self.spinBoxIdleTime = QtGui.QSpinBox(self.widgetButtons)
        self.spinBoxIdleTime.setMinimumSize(QtCore.QSize(100, 27))
        self.spinBoxIdleTime.setMaximum(999999999)
        self.spinBoxIdleTime.setSingleStep(100)
        self.spinBoxIdleTime.setProperty("value", 1000)
        self.spinBoxIdleTime.setObjectName(_fromUtf8("spinBoxIdleTime"))
        self.verticalLayout.addWidget(self.spinBoxIdleTime)
        self.gridLayout_3.addWidget(self.widgetButtons, 0, 1, 1, 1, QtCore.Qt.AlignTop)
        WeatherStation.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WeatherStation)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 25))
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
        self.main_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WeatherStation)

    def retranslateUi(self, WeatherStation):
        WeatherStation.setWindowTitle(_translate("WeatherStation", "Weather Station -gb510, mc955", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabOverview), _translate("WeatherStation", "Overview", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabTerminal), _translate("WeatherStation", "Terminal", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabSerial), _translate("WeatherStation", "Serial", None))
        self.pushButtonDumpSD.setText(_translate("WeatherStation", "Dump SD", None))
        self.radioButtonLiveData.setText(_translate("WeatherStation", "Show Live Data", None))
        self.pushButtonUpdateRTC.setText(_translate("WeatherStation", "Update RTC", None))
        self.pushButtonSetIdle.setText(_translate("WeatherStation", "Set Idle Time", None))
        self.spinBoxIdleTime.setSuffix(_translate("WeatherStation", "ms", None))
        self.menuSerial.setTitle(_translate("WeatherStation", "Serial", None))
        self.actionConnect.setText(_translate("WeatherStation", "Connect", None))
        self.actionLive_Sensor_Data.setText(_translate("WeatherStation", "Display Live Sensor Data", None))
        self.actionDownload_from_SD.setText(_translate("WeatherStation", "Download Data from SD", None))

from pyqtgraph import GraphicsLayoutWidget

class WeatherStation(QtGui.QMainWindow, Ui_WeatherStation):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

