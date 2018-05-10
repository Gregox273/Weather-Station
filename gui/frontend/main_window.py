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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(577, 456)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.main_tab_widget.setGeometry(QtCore.QRect(10, 10, 551, 371))
        self.main_tab_widget.setTabPosition(QtGui.QTabWidget.West)
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
        self.tabLive_view = QtGui.QWidget()
        self.tabLive_view.setObjectName(_fromUtf8("tabLive_view"))
        self.main_tab_widget.addTab(self.tabLive_view, _fromUtf8(""))
        self.tabHistoric_view = QtGui.QWidget()
        self.tabHistoric_view.setObjectName(_fromUtf8("tabHistoric_view"))
        self.main_tab_widget.addTab(self.tabHistoric_view, _fromUtf8(""))
        self.tabTerminal = QtGui.QWidget()
        self.tabTerminal.setObjectName(_fromUtf8("tabTerminal"))
        self.textBrowserTerminal = QtGui.QTextBrowser(self.tabTerminal)
        self.textBrowserTerminal.setGeometry(QtCore.QRect(80, 70, 256, 192))
        self.textBrowserTerminal.setOpenLinks(True)
        self.textBrowserTerminal.setObjectName(_fromUtf8("textBrowserTerminal"))
        self.main_tab_widget.addTab(self.tabTerminal, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSerial = QtGui.QMenu(self.menubar)
        self.menuSerial.setObjectName(_fromUtf8("menuSerial"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setCheckable(True)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionLive_Sensor_Data = QtGui.QAction(MainWindow)
        self.actionLive_Sensor_Data.setCheckable(True)
        self.actionLive_Sensor_Data.setChecked(True)
        self.actionLive_Sensor_Data.setObjectName(_fromUtf8("actionLive_Sensor_Data"))
        self.actionDownload_from_SD = QtGui.QAction(MainWindow)
        self.actionDownload_from_SD.setCheckable(True)
        self.actionDownload_from_SD.setChecked(True)
        self.actionDownload_from_SD.setObjectName(_fromUtf8("actionDownload_from_SD"))
        self.menuSerial.addAction(self.actionConnect)
        self.menuSerial.addSeparator()
        self.menuSerial.addAction(self.actionLive_Sensor_Data)
        self.menuSerial.addAction(self.actionDownload_from_SD)
        self.menubar.addAction(self.menuSerial.menuAction())

        self.retranslateUi(MainWindow)
        self.main_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabLive_view), _translate("MainWindow", "Live View", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabHistoric_view), _translate("MainWindow", "Historic View", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tabTerminal), _translate("MainWindow", "Terminal", None))
        self.menuSerial.setTitle(_translate("MainWindow", "Serial", None))
        self.actionConnect.setText(_translate("MainWindow", "Connect", None))
        self.actionLive_Sensor_Data.setText(_translate("MainWindow", "Display Live Sensor Data", None))
        self.actionDownload_from_SD.setText(_translate("MainWindow", "Download Data from SD", None))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

