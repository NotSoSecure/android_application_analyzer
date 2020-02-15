import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QRect
from GlobalVariables import *

class Gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1100, 700))
        self.setWindowTitle("Android Local stroage analyzer") 
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)  

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.device_lable = QLabel(centralWidget)
        self.device_lable.setGeometry(QRect(10, 5, 85, 40))
        self.device_lable.setText("Select Device")
        self.cmbDevice = QComboBox(centralWidget)
        self.cmbDevice.setGeometry(QRect(95, 5, 400, 40))
        self.cmbDevice.setObjectName(("cmbDevice")) 

        self.app_label = QLabel(centralWidget)
        self.app_label.setGeometry(QRect(510, 5, 110, 40))
        self.app_label.setText("Select Application")
        self.cmbApp = QComboBox(centralWidget)
        self.cmbApp.setGeometry(QRect(620, 5, 375, 40))
        self.cmbApp.setObjectName(("cmbDevice")) 

        self.btnSnapshot = QPushButton(centralWidget)
        self.btnSnapshot.setGeometry(QRect(995, 10, 100, 30))
        self.btnSnapshot.setText(("Snapshot"))

        self.appDirs = QLabel(centralWidget)
        self.appDirs.setGeometry(QRect(10, 40, 250, 30))
        self.appDirs.setText("Select Directory")
        self.lstAppDirs = QListWidget(centralWidget)
        self.lstAppDirs.setGeometry(QRect(10, 70, 250, 150))

        self.appDirFiles = QLabel(centralWidget)
        self.appDirFiles.setGeometry(QRect(270, 40, 480, 30))
        self.appDirFiles.setText("Select File")
        self.lstAppDirFiles = QListWidget(centralWidget)
        self.lstAppDirFiles.setGeometry(QRect(270, 70, 720, 150))

        self.btnJDGUI = QPushButton(centralWidget)
        self.btnJDGUI.setGeometry(QRect(995, 65, 100, 40))
        self.btnJDGUI.setText(("jdgui"))

        self.btnMobSF = QPushButton(centralWidget)
        self.btnMobSF.setGeometry(QRect(995, 105, 100, 40))
        self.btnMobSF.setText(("mobSF"))

        self.btnAPKTool = QPushButton(centralWidget)
        self.btnAPKTool.setGeometry(QRect(995, 145, 100, 40))
        self.btnAPKTool.setText(("apktool"))

        self.btnReinstall = QPushButton(centralWidget)
        self.btnReinstall.setGeometry(QRect(995, 185, 100, 40))
        self.btnReinstall.setText(("re-install"))
      
        self.btnFridaSSLUnPin = QPushButton(centralWidget)
        self.btnFridaSSLUnPin.setGeometry(QRect(780, 220, 120, 40))
        self.btnFridaSSLUnPin.setText(("frida-sslunpin"))

        self.btnFridump = QPushButton(centralWidget)
        self.btnFridump.setGeometry(QRect(895, 220, 100, 40))
        self.btnFridump.setText(("fridump"))

        self.lblFileContent = QLabel(centralWidget)
        self.lblFileContent.setGeometry(QRect(10, 230, 250, 30))
        self.lblFileContent.setText("File Content")
      
        self.chkURLDecode = QCheckBox(centralWidget)
        self.chkURLDecode.setGeometry(QRect(100, 230, 130, 30))
        self.chkURLDecode.setText("URLDecode")

        self.chkHtmlDecode = QCheckBox(centralWidget)
        self.chkHtmlDecode.setGeometry(QRect(200, 230, 130, 30))
        self.chkHtmlDecode.setText("HTMLDecode")

        self.chkHideDefaultApp = QCheckBox(centralWidget)
        self.chkHideDefaultApp.setGeometry(QRect(625, 35, 180, 30))
        self.chkHideDefaultApp.setText("Hide Default Application")

        self.chkLogcat = QCheckBox(centralWidget)
        self.chkLogcat.setGeometry(QRect(1020, 230, 75, 30))
        self.chkLogcat.setText("Logcat")
        
        self.txtFileContent = QTextEdit(centralWidget)
        self.txtFileContent.setGeometry(QRect(10, 260, 1080, 430))

        self.txtLogcat = QTextEdit(centralWidget)
        self.txtLogcat.setGeometry(QRect(10, 260, 1080, 430))

    def closeEvent(self, event):
        GlobalVariables.isClose=True
