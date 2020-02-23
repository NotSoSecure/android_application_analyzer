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
		self.isSuNeeded = True
		self.device=""

	def ComposeCmd(self, cmd):
		commandPath=""
		if self.isSuNeeded:
			commandPath="-s {} shell \"su -c {}\"".format(self.device, cmd)
		else:
			commandPath="-s {} shell {}".format(self.device, cmd)
		return commandPath
	
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

	def GetApplicationList(self):
		self.isSuNeeded = True
		cmd=self.ComposeCmd("ls '/data/data/'")
		output=self.globalVariables.ExecuteCommand(cmd)
		if output.lower().find("unknown id")==0:
			self.isSuNeeded = False
		else:
			self.isSuNeeded = True
		cmd=self.ComposeCmd("ls '/data/data/'")
		appList=[]	
		for app in (self.globalVariables.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				appList.append(app.strip())
			except:
				"App not found"
		return appList

	def GetDirContent(self, dir, appContents, appendPath=False):
		cmd=self.ComposeCmd("ls '{}'".format(dir))
		for appContent in (self.globalVariables.ExecuteCommand(cmd).strip()).split("\n"):
			try:
				if appendPath:
					appContents.append(dir.replace("\"","")+appContent.strip())
				else:
					appContents.append(appContent.strip())
			except:
				"No app content found"

	def GetApplicationContent(self, appName):
		appContents=[]
		self.GetDirContent("/data/data/{}".format(appName), appContents)
		cmd="{} | grep {}".format(self.ComposeCmd("ls /sdcard/Android/data/"), self.mainWin.cmbApp.currentText())
		appDir=self.globalVariables.ExecuteCommand(cmd).strip()
		if appDir != "":
			self.GetDirContent("/sdcard/Android/data/"+appName+"/", appContents, True)
		return appContents

	'''def IsDirectory(self, path):
		cmd=self.ComposeCmd("cat '"+path+"'")
		cmdOutput=self.globalVariables.ExecuteCommand(cmd).strip()
		if cmdOutput.find("Is a directory") != -1:
			return True
		return False'''

	def BuildFileStructure(self, appName, dirPath):
		if (dirPath.find("/sdcard") == 0):
			cmd=self.ComposeCmd("ls -R '"+dirPath+"'")
		else:
			cmd=self.ComposeCmd("ls -R '/data/data/"+appName+"/"+dirPath+"'")
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

	def GetFileContent(self, path):
		path=path.replace(" ", "\\ ").replace("//","/")
		cmd=self.ComposeCmd("cat '"+path+"'")
		return self.globalVariables.ExecuteCommand(cmd).strip()

	def DownloadDBFile(self, filePath, outputPath):
		filePath=filePath.replace(" ", "\\ ").replace("//","/")
		if self.isSuNeeded:
			cmd="{} > '{}'".format(self.ComposeCmd("cat '"+filePath+"'"),outputPath)
		else:
			cmd="-s "+self.device+" pull "+filePath+" \""+outputPath+"\""
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

	def HideDefaultApplication(self):
		if mainWin.chkHideDefaultApp.isChecked():
			self.ListApplication(True)
		else:
			self.ListApplication(False)

	def ListApplication(self, isHide=False):
		self.device=self.mainWin.cmbDevice.currentText()
		appList=self.GetApplicationList()
		self.mainWin.cmbApp.clear()
		for app in appList:
			if isHide:
				if app.find("com.android") == 0 or app.find("com.google") == 0:
					continue
				else:
					self.mainWin.cmbApp.addItem(app)
			else:
				self.mainWin.cmbApp.addItem(app)

	def ListApplicationContent(self):
		appName=self.mainWin.cmbApp.currentText()
		appContents=self.GetApplicationContent(appName)
		self.mainWin.lstAppDirs.clear()
		for appContent in appContents:
			self.mainWin.lstAppDirs.addItem(QListWidgetItem(appContent))

	def ListFileFromDir(self):
		if len(self.mainWin.lstAppDirs.selectedItems()) == 1:
			appName=self.mainWin.cmbApp.currentText()
			appDirName=str(self.mainWin.lstAppDirs.selectedItems()[0].text())

			appDirFiles=self.BuildFileStructure(appName, appDirName)
			self.mainWin.lstAppDirFiles.clear()
			for file in appDirFiles:
				self.mainWin.lstAppDirFiles.addItem(QListWidgetItem(file))
		else:
			print ("Multiple Item Selected")

	def DisplayFileContent(self):
		mainWin.chkLogcat.setChecked(False)
		if len(self.mainWin.lstAppDirFiles.selectedItems()) == 1:
			filePath=(self.mainWin.lstAppDirFiles.selectedItems()[0].text())
			fileContent=self.GetFileContent(filePath).strip()
			if fileContent.find("SQLite format 3") == 0:
				if not os.path.exists("dbs"):
					os.makedirs("dbs")
				fileName=filePath[filePath.rfind('/')+1:]
				dbPath="./dbs/"+fileName
				self.DownloadDBFile(filePath, dbPath)
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
				self.DownloadDBFile(filePath, libPath)
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
		cmd="{} | grep {}".format(self.ComposeCmd("ls '/data/app/'"), apkName)
		appDir=self.globalVariables.ExecuteCommand(cmd).strip()
		if self.isSuNeeded:
			self.globalVariables.ExecuteCommand("{} > {}/{}.apk".format(self.ComposeCmd("cat /data/app/{}/base.apk".format(appDir)), self.globalVariables.outputDir, apkName))
		else:
			self.globalVariables.ExecuteCommand("-s {} pull /data/app/{}/base.apk {}/{}.apk".format(self.device, appDir, self.globalVariables.outputDir, apkName))
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
		self.globalVariables.ExecuteCommand("-s {} uninstall {}".format(self.device, apkName))
		self.globalVariables.ExecuteCommand("-s {} install {}/{}/dist/{}.s.apk".format(self.device, self.globalVariables.outputDir, apkName, apkName))
	
	def RunSnapshot(self):
		apkName=self.mainWin.cmbApp.currentText()
		outputDir="{}/{}_{}".format(self.globalVariables.snapshotDir, apkName, str(datetime.now()).replace(" ", "_"))
		if not os.path.exists(outputDir):
			os.mkdir(outputDir)
		cmd="{} | grep {}".format(self.ComposeCmd("ls '/data/app/'"), apkName)
		appDir=self.globalVariables.ExecuteCommand(cmd).strip()
		self.globalVariables.ExecuteCommand("-s {} pull /data/data/{}/ {}/data_data".format(self.device, apkName, outputDir))
		self.globalVariables.ExecuteCommand("-s {} pull /data/app/{}/ {}/data_app".format(self.device, appDir, outputDir))

	def StartFridaServer(self):
		cmd="{} | grep {}".format(self.ComposeCmd("ps"), self.globalVariables.fridaServer)
		output = self.globalVariables.ExecuteCommand(cmd)
		if output.find(self.globalVariables.fridaServer) < 0:
			self.globalVariables.ExecuteCommand("-s {} push {} {}".format(self.device, self.globalVariables.fridaServerFileName, self.globalVariables.androidtmpdir))
			self.globalVariables.ExecuteCommand(self.ComposeCmd("\"cd {} && chmod 755 {}\"".format(self.globalVariables.androidtmpdir, self.globalVariables.fridaServer)))
			self.globalVariables.ExecuteCommand(self.ComposeCmd("\"cd {} && ./{} &\"".format(self.globalVariables.androidtmpdir, self.globalVariables.fridaServer)), True, False)
		
	def RunFridump(self):
		self.StartFridaServer()
		try:
			self.globalVariables.ExecuteCommand("python {} -U -s {}".format(self.globalVariables.fridumpPath, self.mainWin.cmbApp.currentText()), False)

			mainWin.chkLogcat.setChecked(False)
			output=''
			with open(self.globalVariables.fridumpOutput) as f:
				for line in f:
					output += line
			self.mainWin.txtFileContent.setText(output)
		except:
			print ("Please check the application is running!!")

	def RunUniversalFridaSSLUnPinning(self):
		self.StartFridaServer()
		self.globalVariables.ExecuteCommand("-s {} push {} {}{}".format(self.device, self.globalVariables.burpCertPath, self.globalVariables.androidtmpdir, self.globalVariables.burpCertName))
		self.globalVariables.ExecuteCommand("frida -U -f {} -l {} --no-pause".format(self.mainWin.cmbApp.currentText(), self.globalVariables.fridasslunpinscript1), False, False)

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
	    mainWin.chkHideDefaultApp.stateChanged.connect(lambda: main.HideDefaultApplication())
	    mainWin.chkLogcat.stateChanged.connect(lambda: main.DisplayLogcat())
	    mainWin.chkHtmlDecode.stateChanged.connect(lambda: main.DecodeHTMLEntity())
	    mainWin.chkURLDecode.stateChanged.connect(lambda: main.DecodeURL())
	    mainWin.btnAPKTool.clicked.connect(lambda: main.RunAPKTool())
	    mainWin.btnJDGUI.clicked.connect(lambda: main.RunJDGUITool())
	    mainWin.btnMobSF.clicked.connect(lambda: main.RunMobSFTool())
	    mainWin.btnSnapshot.clicked.connect(lambda: main.RunSnapshot())
	    mainWin.btnReinstall.clicked.connect(lambda: main.RunReinstallAPK())
	    mainWin.btnFridaSSLUnPin.clicked.connect(lambda: main.RunUniversalFridaSSLUnPinning())
	    mainWin.btnFridump.clicked.connect(lambda: main.RunFridump())
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





