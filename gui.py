import sys
from PyQt5 import QtCore, QtWidgets
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
        self.device_lable.setGeometry(QRect(10, 5, 85, 30))
        self.device_lable.setText("Select Device")
        self.cmbDevice = QComboBox(centralWidget)
        self.cmbDevice.setGeometry(QRect(95, 5, 400, 30))
        self.cmbDevice.setObjectName(("cmbDevice")) 

        self.device_lable = QLabel(centralWidget)
        self.device_lable.setGeometry(QRect(10, 40, 250, 30))
        self.device_lable.setText("Select Application")
        self.lstApps = QListWidget(centralWidget)
        self.lstApps.setGeometry(QRect(10, 70, 250, 150))

        self.appDirs = QLabel(centralWidget)
        self.appDirs.setGeometry(QRect(270, 40, 250, 30))
        self.appDirs.setText("Select Directory")
        self.lstAppDirs = QListWidget(centralWidget)
        self.lstAppDirs.setGeometry(QRect(270, 70, 250, 150))

        self.appDirFiles = QLabel(centralWidget)
        self.appDirFiles.setGeometry(QRect(530, 40, 480, 30))
        self.appDirFiles.setText("Select File")
        self.lstAppDirFiles = QListWidget(centralWidget)
        self.lstAppDirFiles.setGeometry(QRect(530, 70, 560, 150))
      
        self.lblFileContent = QLabel(centralWidget)
        self.lblFileContent.setGeometry(QRect(10, 230, 250, 30))
        self.lblFileContent.setText("File Content")
      
        self.chkURLDecode = QCheckBox(centralWidget)
        self.chkURLDecode.setGeometry(QRect(100, 230, 130, 30))
        self.chkURLDecode.setText("URLDecode")

        self.chkHtmlDecode = QCheckBox(centralWidget)
        self.chkHtmlDecode.setGeometry(QRect(200, 230, 130, 30))
        self.chkHtmlDecode.setText("HTMLDecode")

        self.chkLogcat = QCheckBox(centralWidget)
        self.chkLogcat.setGeometry(QRect(1020, 230, 75, 30))
        self.chkLogcat.setText("Logcat")
        
        self.txtFileContent = QTextEdit(centralWidget)
        self.txtFileContent.setGeometry(QRect(10, 260, 1080, 430))

        self.txtLogcat = QTextEdit(centralWidget)
        self.txtLogcat.setGeometry(QRect(10, 260, 1080, 430))

    def closeEvent(self, event):
        GlobalVariables.isClose=True
