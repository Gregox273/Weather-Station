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
        WeatherStation.resize(738, 485)
        self.centralwidget = QtGui.QWidget(WeatherStation)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.widgetButtons = QtGui.QWidget(self.centralwidget)
        self.widgetButtons.setMinimumSize(QtCore.QSize(140, 420))
        self.widgetButtons.setMaximumSize(QtCore.QSize(16777215, 420))
        self.widgetButtons.setObjectName(_fromUtf8("widgetButtons"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widgetButtons)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonDumpSD = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonDumpSD.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonDumpSD.setObjectName(_fromUtf8("pushButtonDumpSD"))
        self.verticalLayout.addWidget(self.pushButtonDumpSD)
        self.line = QtGui.QFrame(self.widgetButtons)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.radioButtonLiveData = QtGui.QRadioButton(self.widgetButtons)
        self.radioButtonLiveData.setMinimumSize(QtCore.QSize(100, 26))
        self.radioButtonLiveData.setObjectName(_fromUtf8("radioButtonLiveData"))
        self.verticalLayout.addWidget(self.radioButtonLiveData)
        self.labelGoingBack = QtGui.QLabel(self.widgetButtons)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelGoingBack.setFont(font)
        self.labelGoingBack.setObjectName(_fromUtf8("labelGoingBack"))
        self.verticalLayout.addWidget(self.labelGoingBack)
        self.spinBoxGoingBack = QtGui.QSpinBox(self.widgetButtons)
        self.spinBoxGoingBack.setMinimumSize(QtCore.QSize(100, 27))
        self.spinBoxGoingBack.setMaximum(999999999)
        self.spinBoxGoingBack.setSingleStep(1)
        self.spinBoxGoingBack.setProperty("value", 1)
        self.spinBoxGoingBack.setObjectName(_fromUtf8("spinBoxGoingBack"))
        self.verticalLayout.addWidget(self.spinBoxGoingBack)
        self.line_3 = QtGui.QFrame(self.widgetButtons)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.label_2 = QtGui.QLabel(self.widgetButtons)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.pushButtonRefreshHistoric = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonRefreshHistoric.setMinimumSize(QtCore.QSize(70, 26))
        self.pushButtonRefreshHistoric.setObjectName(_fromUtf8("pushButtonRefreshHistoric"))
        self.verticalLayout.addWidget(self.pushButtonRefreshHistoric)
        self.labelHistoricFrom = QtGui.QLabel(self.widgetButtons)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelHistoricFrom.setFont(font)
        self.labelHistoricFrom.setObjectName(_fromUtf8("labelHistoricFrom"))
        self.verticalLayout.addWidget(self.labelHistoricFrom)
        self.dateTimeEditHistoricFrom = QtGui.QDateTimeEdit(self.widgetButtons)
        self.dateTimeEditHistoricFrom.setObjectName(_fromUtf8("dateTimeEditHistoricFrom"))
        self.verticalLayout.addWidget(self.dateTimeEditHistoricFrom)
        self.labelHistoricTo = QtGui.QLabel(self.widgetButtons)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelHistoricTo.setFont(font)
        self.labelHistoricTo.setObjectName(_fromUtf8("labelHistoricTo"))
        self.verticalLayout.addWidget(self.labelHistoricTo)
        self.dateTimeEditHistoricTo = QtGui.QDateTimeEdit(self.widgetButtons)
        self.dateTimeEditHistoricTo.setObjectName(_fromUtf8("dateTimeEditHistoricTo"))
        self.verticalLayout.addWidget(self.dateTimeEditHistoricTo)
        self.labelHistoricTo_2 = QtGui.QLabel(self.widgetButtons)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelHistoricTo_2.setFont(font)
        self.labelHistoricTo_2.setObjectName(_fromUtf8("labelHistoricTo_2"))
        self.verticalLayout.addWidget(self.labelHistoricTo_2)
        self.line_2 = QtGui.QFrame(self.widgetButtons)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.pushButtonUpdateRTC = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonUpdateRTC.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonUpdateRTC.setObjectName(_fromUtf8("pushButtonUpdateRTC"))
        self.verticalLayout.addWidget(self.pushButtonUpdateRTC)
        self.pushButtonSetIdle = QtGui.QPushButton(self.widgetButtons)
        self.pushButtonSetIdle.setMinimumSize(QtCore.QSize(100, 26))
        self.pushButtonSetIdle.setObjectName(_fromUtf8("pushButtonSetIdle"))
        self.verticalLayout.addWidget(self.pushButtonSetIdle)
        self.labelIdleTime = QtGui.QLabel(self.widgetButtons)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelIdleTime.setFont(font)
        self.labelIdleTime.setObjectName(_fromUtf8("labelIdleTime"))
        self.verticalLayout.addWidget(self.labelIdleTime)
        self.spinBoxIdleTime = QtGui.QSpinBox(self.widgetButtons)
        self.spinBoxIdleTime.setMinimumSize(QtCore.QSize(100, 27))
        self.spinBoxIdleTime.setMaximum(999999999)
        self.spinBoxIdleTime.setSingleStep(1)
        self.spinBoxIdleTime.setProperty("value", 1)
        self.spinBoxIdleTime.setObjectName(_fromUtf8("spinBoxIdleTime"))
        self.verticalLayout.addWidget(self.spinBoxIdleTime)
        self.gridLayout_3.addWidget(self.widgetButtons, 0, 1, 1, 1, QtCore.Qt.AlignTop)
        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.main_tab_widget.setMinimumSize(QtCore.QSize(300, 300))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.main_tab_widget.setFont(font)
        self.main_tab_widget.setTabPosition(QtGui.QTabWidget.West)
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setMovable(True)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
        self.tabOverview = QtGui.QWidget()
        self.tabOverview.setObjectName(_fromUtf8("tabOverview"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabOverview)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.graphicsLayoutWidgetTemp_O = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetTemp_O.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetTemp_O.setObjectName(_fromUtf8("graphicsLayoutWidgetTemp_O"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetTemp_O, 0, 0, 1, 1)
        self.graphicsLayoutWidgetUV_O = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetUV_O.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetUV_O.setObjectName(_fromUtf8("graphicsLayoutWidgetUV_O"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetUV_O, 1, 0, 1, 1)
        self.graphicsLayoutWidgetLight_O = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetLight_O.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetLight_O.setObjectName(_fromUtf8("graphicsLayoutWidgetLight_O"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetLight_O, 1, 1, 1, 1)
        self.graphicsLayoutWidgetWind_O = GraphicsLayoutWidget(self.tabOverview)
        self.graphicsLayoutWidgetWind_O.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetWind_O.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetWind_O.setObjectName(_fromUtf8("graphicsLayoutWidgetWind_O"))
        self.gridLayout_2.addWidget(self.graphicsLayoutWidgetWind_O, 0, 1, 1, 1)
        self.main_tab_widget.addTab(self.tabOverview, _fromUtf8(""))
        self.tabTemperature = QtGui.QWidget()
        self.tabTemperature.setObjectName(_fromUtf8("tabTemperature"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabTemperature)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsLayoutWidgetTemp = GraphicsLayoutWidget(self.tabTemperature)
        self.graphicsLayoutWidgetTemp.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetTemp.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetTemp.setObjectName(_fromUtf8("graphicsLayoutWidgetTemp"))
        self.verticalLayout_2.addWidget(self.graphicsLayoutWidgetTemp)
        self.main_tab_widget.addTab(self.tabTemperature, _fromUtf8(""))
        self.tabWind = QtGui.QWidget()
        self.tabWind.setObjectName(_fromUtf8("tabWind"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabWind)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.graphicsLayoutWidgetWind = GraphicsLayoutWidget(self.tabWind)
        self.graphicsLayoutWidgetWind.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetWind.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetWind.setObjectName(_fromUtf8("graphicsLayoutWidgetWind"))
        self.verticalLayout_3.addWidget(self.graphicsLayoutWidgetWind)
        self.main_tab_widget.addTab(self.tabWind, _fromUtf8(""))
        self.tabLight = QtGui.QWidget()
        self.tabLight.setObjectName(_fromUtf8("tabLight"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabLight)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.graphicsLayoutWidgetLight = GraphicsLayoutWidget(self.tabLight)
        self.graphicsLayoutWidgetLight.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetLight.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetLight.setObjectName(_fromUtf8("graphicsLayoutWidgetLight"))
        self.verticalLayout_4.addWidget(self.graphicsLayoutWidgetLight)
        self.main_tab_widget.addTab(self.tabLight, _fromUtf8(""))
        self.tabUV = QtGui.QWidget()
        self.tabUV.setObjectName(_fromUtf8("tabUV"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabUV)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.graphicsLayoutWidgetUV = GraphicsLayoutWidget(self.tabUV)
        self.graphicsLayoutWidgetUV.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsLayoutWidgetUV.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsLayoutWidgetUV.setObjectName(_fromUtf8("graphicsLayoutWidgetUV"))
        self.verticalLayout_5.addWidget(self.graphicsLayoutWidgetUV)
        self.main_tab_widget.addTab(self.tabUV, _fromUtf8(""))
        self.tabTerminal = QtGui.QWidget()
        self.tabTerminal.setObjectName(_fromUtf8("tabTerminal"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tabTerminal)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.tabWidgetSubTerminal = QtGui.QTabWidget(self.tabTerminal)
        self.tabWidgetSubTerminal.setObjectName(_fromUtf8("tabWidgetSubTerminal"))
        self.tabAllPackets = QtGui.QWidget()
        self.tabAllPackets.setObjectName(_fromUtf8("tabAllPackets"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tabAllPackets)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.textBrowserTerminal = QtGui.QTextBrowser(self.tabAllPackets)
        self.textBrowserTerminal.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTerminal.setOpenLinks(True)
        self.textBrowserTerminal.setObjectName(_fromUtf8("textBrowserTerminal"))
        self.verticalLayout_7.addWidget(self.textBrowserTerminal)
        self.tabWidgetSubTerminal.addTab(self.tabAllPackets, _fromUtf8(""))
        self.tabLogPackets = QtGui.QWidget()
        self.tabLogPackets.setObjectName(_fromUtf8("tabLogPackets"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.tabLogPackets)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.textBrowserTerminalLogs = QtGui.QTextBrowser(self.tabLogPackets)
        self.textBrowserTerminalLogs.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTerminalLogs.setOpenLinks(True)
        self.textBrowserTerminalLogs.setObjectName(_fromUtf8("textBrowserTerminalLogs"))
        self.verticalLayout_8.addWidget(self.textBrowserTerminalLogs)
        self.tabWidgetSubTerminal.addTab(self.tabLogPackets, _fromUtf8(""))
        self.tabEventPackets = QtGui.QWidget()
        self.tabEventPackets.setObjectName(_fromUtf8("tabEventPackets"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tabEventPackets)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.textBrowserTerminalEvents = QtGui.QTextBrowser(self.tabEventPackets)
        self.textBrowserTerminalEvents.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTerminalEvents.setOpenLinks(True)
        self.textBrowserTerminalEvents.setObjectName(_fromUtf8("textBrowserTerminalEvents"))
        self.verticalLayout_9.addWidget(self.textBrowserTerminalEvents)
        self.tabWidgetSubTerminal.addTab(self.tabEventPackets, _fromUtf8(""))
        self.verticalLayout_6.addWidget(self.tabWidgetSubTerminal)
        self.main_tab_widget.addTab(self.tabTerminal, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.main_tab_widget, 0, 0, 1, 1)
        WeatherStation.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WeatherStation)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        WeatherStation.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(WeatherStation)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        WeatherStation.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(WeatherStation)
        self.actionConnect.setCheckable(True)
        self.actionConnect.setChecked(True)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionLive_Sensor_Data = QtGui.QAction(WeatherStation)
        self.actionLive_Sensor_Data.setCheckable(True)
        self.actionLive_Sensor_Data.setChecked(True)
        self.actionLive_Sensor_Data.setObjectName(_fromUtf8("actionLive_Sensor_Data"))
        self.actionDownload_from_SD = QtGui.QAction(WeatherStation)
        self.actionDownload_from_SD.setCheckable(True)
        self.actionDownload_from_SD.setChecked(True)
        self.actionDownload_from_SD.setObjectName(_fromUtf8("actionDownload_from_SD"))
        self.actionWipe_SD_Card = QtGui.QAction(WeatherStation)
        self.actionWipe_SD_Card.setObjectName(_fromUtf8("actionWipe_SD_Card"))
        self.actionSave_Terminal = QtGui.QAction(WeatherStation)
        self.actionSave_Terminal.setObjectName(_fromUtf8("actionSave_Terminal"))
        self.actionExport_Database = QtGui.QAction(WeatherStation)
        self.actionExport_Database.setObjectName(_fromUtf8("actionExport_Database"))
        self.menuFile.addAction(self.actionWipe_SD_Card)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Terminal)
        self.menuFile.addAction(self.actionExport_Database)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(WeatherStation)
        self.main_tab_widget.setCurrentIndex(0)
        self.tabWidgetSubTerminal.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WeatherStation)

    def retranslateUi(self, WeatherStation):
        WeatherStation.setWindowTitle(_translate("WeatherStation", "Weather Station -gb510, mc955", None))
        self.pushButtonDumpSD.setText(_translate("WeatherStation", "Dump SD", None))
        self.radioButtonLiveData.setText(_translate("WeatherStation", "Show Live Data", None))
        self.labelGoingBack.setText(_translate("WeatherStation", "Going back:", None))
        self.spinBoxGoingBack.setSuffix(_translate("WeatherStation", "min", None))
        self.label_2.setText(_translate("WeatherStation", "Historic Data:", None))
        self.pushButtonRefreshHistoric.setText(_translate("WeatherStation", "Refresh", None))
        self.labelHistoricFrom.setText(_translate("WeatherStation", "From:", None))
        self.dateTimeEditHistoricFrom.setDisplayFormat(_translate("WeatherStation", "HH:mm dd/MM/yyyy", None))
        self.labelHistoricTo.setText(_translate("WeatherStation", "To:", None))
        self.dateTimeEditHistoricTo.setDisplayFormat(_translate("WeatherStation", "HH:mm dd/MM/yyyy", None))
        self.labelHistoricTo_2.setText(_translate("WeatherStation", "(system times)", None))
        self.pushButtonUpdateRTC.setText(_translate("WeatherStation", "Update RTC", None))
        self.pushButtonSetIdle.setText(_translate("WeatherStation", "Set Idle Time", None))
        self.labelIdleTime.setText(_translate("WeatherStation", "Idle time:", None))
        self.spinBoxIdleTime.setSuffix(_translate("WeatherStation", "s", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabOverview), _translate("WeatherStation", "Overview", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabTemperature), _translate("WeatherStation", "Temp", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabWind), _translate("WeatherStation", "Windspeed", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabLight), _translate("WeatherStation", "Light", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabUV), _translate("WeatherStation", "UV", None))
        self.tabWidgetSubTerminal.setTabText(self.tabWidgetSubTerminal.indexOf(self.tabAllPackets), _translate("WeatherStation", "All Packets (Raw)", None))
        self.tabWidgetSubTerminal.setTabText(self.tabWidgetSubTerminal.indexOf(self.tabLogPackets), _translate("WeatherStation", "Log Packets", None))
        self.tabWidgetSubTerminal.setTabText(self.tabWidgetSubTerminal.indexOf(self.tabEventPackets), _translate("WeatherStation", "Event Packets", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabTerminal), _translate("WeatherStation", "Terminal", None))
        self.menuFile.setTitle(_translate("WeatherStation", "File", None))
        self.actionConnect.setText(_translate("WeatherStation", "Connect", None))
        self.actionLive_Sensor_Data.setText(_translate("WeatherStation", "Display Live Sensor Data", None))
        self.actionDownload_from_SD.setText(_translate("WeatherStation", "Download Data from SD", None))
        self.actionWipe_SD_Card.setText(_translate("WeatherStation", "Wipe SD Card", None))
        self.actionSave_Terminal.setText(_translate("WeatherStation", "Save Terminal", None))
        self.actionExport_Database.setText(_translate("WeatherStation", "Export Database", None))

from pyqtgraph import GraphicsLayoutWidget

class WeatherStation(QtGui.QMainWindow, Ui_WeatherStation):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

