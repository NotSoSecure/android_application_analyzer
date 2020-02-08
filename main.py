# Author : sanjay@notsosecure.com
#
# main.py: Initiator file for the project.
#
# Project : Android Application Analyzer

import sqlite3
import os
from datetime import datetime
import urllib
import html
import webbrowser 
from gui import *
from banner import *
from logcat import *
from GlobalVariables import *

class Main:
	def __init__(self, mainWin):
		self.mainWin=mainWin
		self.globalVariables=GlobalVariables()

	def GetDeviceList(self):
		deviceList=[]
		isFirstElement=True
		for device in (self.globalVariables.ExecuteCommand("devices -l").strip()).split("\n"):
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
		#cmd="-s "+device+" shell \"su -c ls '/data/data/'\""
		cmd="-s "+device+" shell ls \"/data/data/\""
		for app in (self.globalVariables.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				appList.append(app.strip())
			except:
				"App not found"
		return appList

	def GetDirContent(self, device, dir, appContents, appendPath=False):
		#cmd="-s "+device+" shell \"su -c ls '/data/data/"+appName+"/'\""
		cmd="-s "+device+" shell ls " + dir
		for appContent in (self.globalVariables.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				if appendPath:
					appContents.append(dir.replace("\"","")+appContent.strip())
				else:
					appContents.append(appContent.strip())
			except:
				"No app content found"

	def GetApplicationContent(self, device, appName):
		appContents=[]
		self.GetDirContent(device, "\"/data/data/"+appName+"/\"", appContents)
		appDir=self.globalVariables.ExecuteCommand("-s {} shell ls /sdcard/Android/data/ | grep {}".format(device, self.mainWin.cmbApp.currentText())).strip()
		if appDir != "":
			print (appDir)
			self.GetDirContent(device, "\"/sdcard/Android/data/"+appName+"/\"", appContents, True)
		return appContents

	'''def IsDirectory(self, device, path):
		#cmd="-s "+device+" shell \"su -c cat "+path+"'\""
		cmd="-s "+device+" shell cat \""+path+"\""
		cmdOutput=self.globalVariables.ExecuteCommand(cmd).strip()
		if cmdOutput.find("Is a directory") != -1:
			return True
		return False'''

	def BuildFileStructure(self, device, appName, dirPath):
		#cmd="-s "+device+" shell \"su -c ls -R '/data/data/"+appName+"/"+dirPath+"/'\""
		if (dirPath.find("/sdcard") == 0):
			cmd="-s "+device+" shell ls -R \""+dirPath+"\""
		else:
			cmd="-s "+device+" shell ls -R \"/data/data/"+appName+"/"+dirPath+"\""
		fileList=[]
		directory=""
		for dirContent in (self.globalVariables.ExecuteCommand(cmd).strip()).split("\n"):
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
		#cmd="-s "+device+" shell \"su -c cat '"+path+"'\""
		cmd="-s "+device+" shell cat \""+path+"\""
		return self.globalVariables.ExecuteCommand(cmd).strip()

	def DownloadDBFile(self, device, filePath, outputPath):
		filePath=filePath.replace(" ", "\\ ").replace("//","/")
		cmd="-s "+device+" pull "+filePath+" \""+outputPath+"\""
		self.globalVariables.ExecuteCommand(cmd)

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
		self.mainWin.cmbApp.clear()
		for app in appList:
			self.mainWin.cmbApp.addItem(app)

	def ListApplicationContent(self):
		deviceName=self.mainWin.cmbDevice.currentText()
		appName=self.mainWin.cmbApp.currentText()
		appContents=self.GetApplicationContent(deviceName, appName)
		self.mainWin.lstAppDirs.clear()
		for appContent in appContents:
			self.mainWin.lstAppDirs.addItem(QListWidgetItem(appContent))

	def ListFileFromDir(self):
		if len(self.mainWin.lstAppDirs.selectedItems()) == 1:
			deviceName=self.mainWin.cmbDevice.currentText()
			appName=self.mainWin.cmbApp.currentText()
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
					print (table)
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
				self.mainWin.txtFileContent.append(self.globalVariables.ExecuteCommand("strings " + libPath, False))
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

	def FetchAPK(self):
		apkName=self.mainWin.cmbApp.currentText()
		appDir=self.globalVariables.ExecuteCommand("-s {} shell ls /data/app/ | grep {}".format(device, apkName)).strip()
		self.globalVariables.ExecuteCommand("-s {} pull /data/app/{}/base.apk {}/{}.apk".format(device, appDir, self.globalVariables.outputDir, apkName))
		return apkName
		
	def RunAPKTool(self):
		apkName=self.FetchAPK()
		self.globalVariables.ExecuteCommand("java -jar {} d {}/{}.apk -f -o {}/{}".format(self.globalVariables.apktoolPath, self.globalVariables.outputDir, apkName, self.globalVariables.outputDir, apkName), False)

	def RunJDGUITool(self):
		apkName=self.FetchAPK()
		self.globalVariables.ExecuteCommand("{} {}/{}.apk -o {}/{}.jar".format(self.globalVariables.dex2jarPath, self.globalVariables.outputDir, apkName, self.globalVariables.outputDir, apkName), False)
		self.globalVariables.ExecuteCommand("java -jar {} {}/{}.jar".format(self.globalVariables.jdGUIPath, self.globalVariables.outputDir, apkName), False, False)

	def RunMobSFTool(self):
		isSuccess=self.globalVariables.InitializeMobSFVariables()
		if isSuccess:
			apkName=self.FetchAPK()
			self.globalVariables.ExecuteCommand("curl -F 'file=@./apps/{}.apk' {}/api/v1/upload -H \"Authorization:{}\"".format(apkName, self.globalVariables.mobSFURL, self.globalVariables.mobSFAPIKey), False, False)
			webbrowser.open_new_tab("{}/recent_scans/".format(self.globalVariables.mobSFURL))

	def RunReinstallAPK(self):
		apkName=self.mainWin.cmbApp.currentText()
		self.globalVariables.ExecuteCommand("java -jar {} b {}/{}/".format(self.globalVariables.apktoolPath, self.globalVariables.outputDir, apkName), False)
		self.globalVariables.ExecuteCommand("java -jar {} {}/{}/dist/{}.apk".format(self.globalVariables.signJar, self.globalVariables.outputDir, apkName, apkName), False)
		self.globalVariables.ExecuteCommand("uninstall {}".format(apkName))
		self.globalVariables.ExecuteCommand("install {}/{}/dist/{}.s.apk".format(self.globalVariables.outputDir, apkName, apkName))
	
	def RunSnapshot(self):
		apkName=self.mainWin.cmbApp.currentText()
		outputDir="{}/{}_{}".format(self.globalVariables.snapshotDir, apkName, str(datetime.now()).replace(" ", "_"))
		if not os.path.exists(outputDir):
			os.mkdir(outputDir)
		appDir=self.globalVariables.ExecuteCommand("-s {} shell ls /data/app/ | grep {}".format(device, apkName)).strip()
		self.globalVariables.ExecuteCommand("-s {} pull /data/data/{}/ {}/data_data".format(device, apkName, outputDir))
		self.globalVariables.ExecuteCommand("-s {} pull /data/app/{}/ {}/data_app".format(device, appDir, outputDir))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('./Usage/icon.png'))
    print (getBanner())
    mainWin = Gui()
    mainWin.show()

    main=Main(mainWin)
    deviceList=main.GetDeviceList()
    if len(deviceList) > 0:
	    for device in deviceList:
	    	mainWin.cmbDevice.addItem(device)

	    mainWin.cmbDevice.currentIndexChanged.connect(lambda: main.ListApplication())
	    mainWin.cmbApp.currentIndexChanged.connect(lambda: main.ListApplicationContent())
	    mainWin.lstAppDirs.itemClicked.connect(lambda: main.ListFileFromDir())
	    mainWin.lstAppDirFiles.itemClicked.connect(lambda: main.DisplayFileContent())
	    mainWin.chkLogcat.stateChanged.connect(lambda: main.DisplayLogcat())
	    mainWin.chkHtmlDecode.stateChanged.connect(lambda: main.DecodeHTMLEntity())
	    mainWin.chkURLDecode.stateChanged.connect(lambda: main.DecodeURL())
	    mainWin.btnAPKTool.clicked.connect(lambda: main.RunAPKTool())
	    mainWin.btnJDGUI.clicked.connect(lambda: main.RunJDGUITool())
	    mainWin.btnMobSF.clicked.connect(lambda: main.RunMobSFTool())
	    mainWin.btnSnapshot.clicked.connect(lambda: main.RunSnapshot())
	    mainWin.btnReinstall.clicked.connect(lambda: main.RunReinstallAPK())
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





