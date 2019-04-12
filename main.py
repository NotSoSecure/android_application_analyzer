# Author : sanjay@notsosecure.com
#
# main.py: Initiator file for the project.
#
# Project : Android Application Analyzer

import sqlite3
import os
from CmdExecutor import *
from gui import *
from banner import *
from logcat import *
import urllib
import html

class Main:
	def __init__(self, mainWin):
		self.mainWin=mainWin
		self.cmdExecutor=CmdExecutor()

	def GetDeviceList(self):
		deviceList=[]
		isFirstElement=True
		for device in (self.cmdExecutor.ExecuteCommand("devices -l").strip()).split("\n"):
			try:
				iStart=device.find("model:")
				if iStart != -1:
					iEnd=device.find(" ", iStart)
					deviceList.append((device[iStart: iEnd]).strip())
			except:
				"No device found"
		return deviceList

	def GetApplicationList(self, device):
		appList=[]
		cmd="-s "+device+" shell ls \"/data/data/\""
		for app in (self.cmdExecutor.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				appList.append(app.strip())
			except:
				"App not found"
		return appList

	def GetApplicationContent(self, device, appName):
		appContents=[]
		cmd="-s "+device+" shell ls \"/data/data/"+appName+"/\""
		for appContent in (self.cmdExecutor.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				appContents.append(appContent.strip())
			except:
				"No app content found"
		return appContents

	'''def IsDirectory(self, device, path):
		cmd="-s "+device+" shell cat \""+path+"\""
		cmdOutput=self.cmdExecutor.ExecuteCommand(cmd).strip()
		if cmdOutput.find("Is a directory") != -1:
			return True
		return False'''

	def BuildFileStructure(self, device, appName, dirPath):
		cmd="-s "+device+" shell ls -R \"/data/data/"+appName+"/"+dirPath+"/\""
		fileList=[]
		directory=""
		for dirContent in (self.cmdExecutor.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				dirContent=dirContent.strip()
				if dirContent:
					if dirContent.find(":") != -1 and len(dirContent) == dirContent.find(":")+1:
						directory = dirContent[:-1]
					else:
						file=directory+"/"+dirContent
						fileList.append(file.replace("//","/"))
			except:
				"No file found"
		return fileList

	def GetFileContent(self, device, path):
		path=path.replace(" ", "\\ ").replace("//","/")
		cmd="-s "+device+" shell cat \""+path+"\""
		return self.cmdExecutor.ExecuteCommand(cmd).strip()

	def DownloadDBFile(self, device, filePath, outputPath):
		filePath=filePath.replace(" ", "\\ ").replace("//","/")
		cmd="-s "+device+" pull "+filePath+" \""+outputPath+"\""
		self.cmdExecutor.ExecuteCommand(cmd)

	def GetAllTables(self, dbPath):
		tables=[]
		con = sqlite3.connect(dbPath)
		cursor = con.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		for table_name in cursor.fetchall():
			tables.append(table_name[0])
		return tables

	def GetTableData(self, dbPath, tableName):
		rows=[]
		con = sqlite3.connect(dbPath)
		cursor = con.cursor()
		cursor.execute("SELECT * FROM " + tableName)

		colnames = cursor.description
		row=''
		for colname in colnames:
			row+=colname[0] + " | "
		rows.append(row)

		for row in cursor.fetchall():
			rows.append(row)
		return rows

	def ListApplication(self):
		appList=self.GetApplicationList(self.mainWin.cmbDevice.currentText())
		self.mainWin.lstApps.clear()
		for app in appList:
			self.mainWin.lstApps.addItem(QListWidgetItem(app))

	def ListApplicationContent(self):
		items = self.mainWin.lstApps.selectedItems()
		if len(items) == 1:
			deviceName=self.mainWin.cmbDevice.currentText()
			appName=str(items[0].text())
			appContents=self.GetApplicationContent(deviceName, appName)
			self.mainWin.lstAppDirs.clear()
			for appContent in appContents:
				self.mainWin.lstAppDirs.addItem(QListWidgetItem(appContent))
		else:
			print ("Multiple Item Selected")

	def ListFileFromDir(self):
		if len(self.mainWin.lstApps.selectedItems()) == 1 and len(self.mainWin.lstAppDirs.selectedItems()) == 1:
			deviceName=self.mainWin.cmbDevice.currentText()
			appName=str(self.mainWin.lstApps.selectedItems()[0].text())
			appDirName=str(self.mainWin.lstAppDirs.selectedItems()[0].text())

			appDirFiles=self.BuildFileStructure(deviceName, appName, appDirName)
			self.mainWin.lstAppDirFiles.clear()
			for file in appDirFiles:
				self.mainWin.lstAppDirFiles.addItem(QListWidgetItem(file))
		else:
			print ("Multiple Item Selected")

	def DisplayFileContent(self):
		mainWin.chkLogcat.setChecked(False)
		if len(self.mainWin.lstAppDirFiles.selectedItems()) == 1:
			deviceName=self.mainWin.cmbDevice.currentText()
			filePath=(self.mainWin.lstAppDirFiles.selectedItems()[0].text())
			fileContent=self.GetFileContent(deviceName, filePath).strip()
			if fileContent.find("SQLite format 3") == 0:
				if not os.path.exists("dbs"):
					os.makedirs("dbs")
				fileName=filePath[filePath.rfind('/')+1:]
				dbPath="./dbs/"+fileName
				self.DownloadDBFile(deviceName, filePath, dbPath)
				tableList=self.GetAllTables(dbPath)
				self.mainWin.txtFileContent.setText("SQLiteDB : "+dbPath)
				for table in tableList:
					self.mainWin.txtFileContent.append("\n\n\nTable => " + table.format(type(str), repr(str)))
					rows=self.GetTableData(dbPath, table)
					isFirstRow=True
					for columns in rows:
						rowData=""
						for column in columns:
							try:
								rowData+=column.format(type(str), repr(str))
								if not isFirstRow:
									rowData+=" | "
							except:
								rowData+=str(column)
								if not isFirstRow:
									rowData+=" | "
						isFirstRow=False
						dataLen = len(rowData)
						if dataLen > 174:
							dataLen = 174
						self.mainWin.txtFileContent.append("-"*dataLen)
						self.mainWin.txtFileContent.append(rowData)
						self.mainWin.txtFileContent.append("-"*dataLen)
			elif fileContent.find("ELF") == 1:
				if not os.path.exists("lib"):
					os.makedirs("lib")
				fileName=filePath[filePath.rfind('/')+1:]
				libPath="./lib/"+fileName
				self.DownloadDBFile(deviceName, filePath, libPath)
				self.mainWin.txtFileContent.setText("Performed \"strings\" command on : ELF lib :" + libPath + "\n\n")
				self.mainWin.txtFileContent.append(self.cmdExecutor.ExecuteCommand("strings " + libPath, False))
			else:
				self.mainWin.txtFileContent.setText(fileContent)
				
		else:
			print ("Multiple Item Selected")
		if mainWin.chkHtmlDecode.isChecked():
			text=html.unescape(self.mainWin.txtFileContent.toPlainText())
			self.mainWin.txtFileContent.setText(text)

		if mainWin.chkURLDecode.isChecked():
			text=self.mainWin.txtFileContent.toPlainText()
			text=text.encode('ascii', 'ignore') 
			self.mainWin.txtFileContent.setText(text)

	def DisplayLogcat(self):
		if mainWin.chkLogcat.isChecked():
			mainWin.chkURLDecode.setVisible(False)
			mainWin.chkHtmlDecode.setVisible(False)
			mainWin.txtFileContent.setVisible(False)
			mainWin.txtLogcat.setVisible(True)
		else:
			mainWin.chkHtmlDecode.setVisible(True)
			mainWin.chkURLDecode.setVisible(True)
			mainWin.txtFileContent.setVisible(True)
			mainWin.txtLogcat.setVisible(False)

	def DecodeHTMLEntity(self):
		text=self.mainWin.txtFileContent.toPlainText()
		if mainWin.chkHtmlDecode.isChecked():
			text=html.unescape(text)
			self.mainWin.txtFileContent.setText(text) 
		else:
			self.DisplayFileContent()

	def DecodeURL(self):
		text=self.mainWin.txtFileContent.toPlainText()
		if mainWin.chkURLDecode.isChecked():
			text=text.encode('ascii', 'ignore') 
			self.mainWin.txtFileContent.setText(text)
		else:
			self.DisplayFileContent()
		

if __name__ == "__main__":
    print (getBanner())
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Gui()
    mainWin.show()

    main=Main(mainWin)
    deviceList=main.GetDeviceList()
    if len(deviceList) > 0:
	    for device in deviceList:
	    	mainWin.cmbDevice.addItem(device)

	    mainWin.cmbDevice.currentIndexChanged.connect(lambda: main.ListApplication())
	    mainWin.lstApps.itemClicked.connect(lambda: main.ListApplicationContent())
	    mainWin.lstAppDirs.itemClicked.connect(lambda: main.ListFileFromDir())
	    mainWin.lstAppDirFiles.itemClicked.connect(lambda: main.DisplayFileContent())
	    mainWin.chkLogcat.stateChanged.connect(lambda: main.DisplayLogcat())
	    mainWin.chkHtmlDecode.stateChanged.connect(lambda: main.DecodeHTMLEntity())
	    mainWin.chkURLDecode.stateChanged.connect(lambda: main.DecodeURL())
	    mainWin.chkLogcat.setChecked(True)
	    mainWin.chkHtmlDecode.setVisible(False)
	    mainWin.chkURLDecode.setVisible(False)
	    mainWin.txtFileContent.setVisible(False)
	    logcat=Logcat(mainWin, mainWin.cmbDevice.currentText())
	    logcat.start()
	    main.ListApplication()
	    sys.exit( app.exec_() )
    else:
    	print ("No emulator found. Re-run the applicaiton after connecting device\n\n")





