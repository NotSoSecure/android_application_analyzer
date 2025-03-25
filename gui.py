import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QRect
from GlobalVariables import *

class Gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1100, 700))
        self.setWindowTitle("Android Application Analyzer") 
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)  

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
        globalVariables=GlobalVariables()
        defaultSize = 40
        topMargin = 5
        funBtnStartPost = 65
        variation = 0
        if globalVariables.isWindowsOS:
            defaultSize = 25
            topMargin = 10
            funBtnStartPost = 70
            variation = 5

        self.device_lable = QLabel(centralWidget)
        self.device_lable.setGeometry(QRect(10, topMargin, 85, defaultSize))
        self.device_lable.setText("Select Device")
        self.cmbDevice = QComboBox(centralWidget)
        self.cmbDevice.setGeometry(QRect(95, topMargin, 400, defaultSize))
        self.cmbDevice.setObjectName(("cmbDevice")) 

        self.app_label = QLabel(centralWidget)
        self.app_label.setGeometry(QRect(510, topMargin, 110, defaultSize))
        self.app_label.setText("Select Application")
        self.cmbApp = QComboBox(centralWidget)
        self.cmbApp.setGeometry(QRect(620, topMargin, 375 - variation, defaultSize))
        self.cmbApp.setObjectName(("cmbDevice")) 

        self.btnReloadApps = QPushButton(centralWidget)
        self.btnReloadApps.setGeometry(QRect(920, 35 + variation, 75 - variation, defaultSize))
        self.btnReloadApps.setText(("Reload"))

        self.btnSnapshot = QPushButton(centralWidget)
        self.btnSnapshot.setGeometry(QRect(995, topMargin, 100, defaultSize))
        self.btnSnapshot.setText(("Snapshot"))

        self.appDirs = QLabel(centralWidget)
        self.appDirs.setGeometry(QRect(10, 40, 250, defaultSize))
        self.appDirs.setText("Select Directory")
        self.lstAppDirs = QListWidget(centralWidget)
        self.lstAppDirs.setGeometry(QRect(10, 75-variation, 250, 145))

        self.appDirFiles = QLabel(centralWidget)
        self.appDirFiles.setGeometry(QRect(270, 40, 480, defaultSize))
        self.appDirFiles.setText("Select File")
        self.lstAppDirFiles = QListWidget(centralWidget)
        self.lstAppDirFiles.setGeometry(QRect(270, 75-variation, 720, 145))

        self.btnJDGUI = QPushButton(centralWidget)
        self.btnJDGUI.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))
        self.btnJDGUI.setText(("jdgui"))

        funBtnStartPost = funBtnStartPost + 40
        self.btnMobSF = QPushButton(centralWidget)
        self.btnMobSF.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))
        self.btnMobSF.setText(("mobSF"))

        funBtnStartPost = funBtnStartPost + 40
        self.btnAPKTool = QPushButton(centralWidget)
        self.btnAPKTool.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))
        self.btnAPKTool.setText(("apktool"))

        funBtnStartPost = funBtnStartPost + 40
        self.btnReinstall = QPushButton(centralWidget)
        self.btnReinstall.setGeometry(QRect(995, funBtnStartPost, 100, defaultSize))
        self.btnReinstall.setText(("re-install"))
      
        self.btnFridaSSLUnPin = QPushButton(centralWidget)
        self.btnFridaSSLUnPin.setGeometry(QRect(720, 220+variation, 120-variation, defaultSize))
        self.btnFridaSSLUnPin.setText(("frida-sslunpin"))

        self.btnFridump = QPushButton(centralWidget)
        self.btnFridump.setGeometry(QRect(840, 220+variation, 100-variation, defaultSize))
        self.btnFridump.setText(("fridump"))

        self.lblFileContent = QLabel(centralWidget)
        self.lblFileContent.setGeometry(QRect(10, 230, 250, defaultSize))
        self.lblFileContent.setText("File Content")
      
        self.chkURLDecode = QCheckBox(centralWidget)
        self.chkURLDecode.setGeometry(QRect(100, 230, 130, defaultSize))
        self.chkURLDecode.setText("URLDecode")

        self.chkHtmlDecode = QCheckBox(centralWidget)
        self.chkHtmlDecode.setGeometry(QRect(200, 230, 130, defaultSize))
        self.chkHtmlDecode.setText("HTMLDecode")

        self.chkHideDefaultApp = QCheckBox(centralWidget)
        self.chkHideDefaultApp.setGeometry(QRect(625-variation, 35, 180, defaultSize))
        self.chkHideDefaultApp.setText("Hide Default Application")
      
        self.chkSplitConfig = QCheckBox(centralWidget)
        self.chkSplitConfig.setGeometry(QRect(940+variation*3, 230, 75, defaultSize))
        self.chkSplitConfig.setText(("split-config"))

        self.chkLogcat = QCheckBox(centralWidget)
        self.chkLogcat.setGeometry(QRect(1020+variation*3, 230, 75, defaultSize))
        self.chkLogcat.setText("Logcat")
        
        self.txtFileContent = QTextEdit(centralWidget)
        self.txtFileContent.setGeometry(QRect(10, 260, 1080, 430))

        self.txtLogcat = QTextEdit(centralWidget)
        self.txtLogcat.setGeometry(QRect(10, 260, 1080, 430))

    def closeEvent(self, event):
        GlobalVariables.isClose=True
