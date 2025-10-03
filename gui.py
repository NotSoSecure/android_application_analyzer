import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, QRect
from GlobalVariables import *

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1100, 700))
        self.setWindowTitle("Android Application Analyzer")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        quit_action = QtGui.QAction("Quit", self)
        quit_action.triggered.connect(self.close)

        globalVariables = GlobalVariables()
        defaultSize = 40
        topMargin = 5
        funBtnStartPost = 65
        variation = 0
        if globalVariables.isWindowsOS:
            defaultSize = 25
            topMargin = 10
            funBtnStartPost = 70
            variation = 5

        # Device label + combobox
        self.device_lable = QLabel("Select Device", centralWidget)
        self.device_lable.setGeometry(QRect(10, topMargin, 85, defaultSize))
        self.cmbDevice = QComboBox(centralWidget)
        self.cmbDevice.setGeometry(QRect(95, topMargin, 400, defaultSize))
        self.cmbDevice.setObjectName("cmbDevice")

        # Application label + combobox
        self.app_label = QLabel("Select Application", centralWidget)
        self.app_label.setGeometry(QRect(510, topMargin, 110, defaultSize))
        self.cmbApp = QComboBox(centralWidget)
        self.cmbApp.setGeometry(QRect(620, topMargin, 375 - variation, defaultSize))
        self.cmbApp.setObjectName("cmbApp")

        # Reload / Snapshot
        self.btnReloadApps = QPushButton("Reload", centralWidget)
        self.btnReloadApps.setGeometry(QRect(920, 35 + variation, 75 - variation, defaultSize))

        self.btnSnapshot = QPushButton("Snapshot", centralWidget)
        self.btnSnapshot.setGeometry(QRect(995, topMargin, 100, defaultSize))

        # Directories
        self.appDirs = QLabel("Select Directory", centralWidget)
        self.appDirs.setGeometry(QRect(10, 40, 250, defaultSize))
        self.lstAppDirs = QListWidget(centralWidget)
        self.lstAppDirs.setGeometry(QRect(10, 75 - variation, 250, 145))

        self.appDirFiles = QLabel("Select File", centralWidget)
        self.appDirFiles.setGeometry(QRect(270, 40, 480, defaultSize))
        self.lstAppDirFiles = QListWidget(centralWidget)
        self.lstAppDirFiles.setGeometry(QRect(270, 75 - variation, 720, 145))

        # Tool buttons
        self.btnJDGUI = QPushButton("jdgui", centralWidget)
        self.btnJDGUI.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))

        funBtnStartPost += 40
        self.btnMobSF = QPushButton("mobSF", centralWidget)
        self.btnMobSF.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))

        funBtnStartPost += 40
        self.btnAPKTool = QPushButton("apktool", centralWidget)
        self.btnAPKTool.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))

        funBtnStartPost += 40
        self.btnReinstall = QPushButton("re-install", centralWidget)
        self.btnReinstall.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))

        # Frida buttons
        self.btnFridaSSLUnPin = QPushButton("frida-sslunpin", centralWidget)
        self.btnFridaSSLUnPin.setGeometry(QRect(720, 220 + variation, 120 - variation, defaultSize))

        self.btnFridump = QPushButton("fridump", centralWidget)
        self.btnFridump.setGeometry(QRect(840, 220 + variation, 100 - variation, defaultSize))

        # File content section
        self.lblFileContent = QLabel("File Content", centralWidget)
        self.lblFileContent.setGeometry(QRect(10, 230, 250, defaultSize))

        self.chkURLDecode = QCheckBox("URLDecode", centralWidget)
        self.chkURLDecode.setGeometry(QRect(100, 230, 130, defaultSize))

        self.chkHtmlDecode = QCheckBox("HTMLDecode", centralWidget)
        self.chkHtmlDecode.setGeometry(QRect(200, 230, 130, defaultSize))

        self.chkHideDefaultApp = QCheckBox("Hide Default Application", centralWidget)
        self.chkHideDefaultApp.setGeometry(QRect(625 - variation, 35, 180, defaultSize))

        self.chkSplitConfig = QCheckBox("split-config", centralWidget)
        self.chkSplitConfig.setGeometry(QRect(940 + variation * 3, 230, 75, defaultSize))

        self.chkLogcat = QCheckBox("Logcat", centralWidget)
        self.chkLogcat.setGeometry(QRect(1020 + variation * 3, 230, 75, defaultSize))

        # Text areas
        self.txtFileContent = QTextEdit(centralWidget)
        self.txtFileContent.setGeometry(QRect(10, 260, 1080, 430))

        self.txtLogcat = QTextEdit(centralWidget)
        self.txtLogcat.setGeometry(QRect(10, 260, 1080, 430))

    def closeEvent(self, event):
        GlobalVariables.isClose = True
        event.accept()  # make sure window closes properly
