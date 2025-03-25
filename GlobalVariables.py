import threading
import requests
import os
from bs4 import BeautifulSoup
import subprocess

class GlobalVariables:
	isClose=False
	"""docstring for GlobalVariables"""
	def __init__(self):
		self.apktoolPath="./tools/apktool_2.9.2.jar"
		self.dex2jarPath="./tools/dex2jar/d2j-dex2jar.sh"
		self.dex2jarPathWin = ".\\tools\\dex2jar\\d2j-dex2jar.bat"
		self.jdGUIPath="./tools/jd-gui-1.6.6.jar"
		self.signJar="./tools/uber-apk-signer-1.3.0.jar"
		self.outputDir="./apps"
		self.snapshotDir="./snapshots"
		self.burpCertName="burpcert.crt"
		self.burpCertPath="./tools/{}".format(self.burpCertName)
		self.mobSFURL="http://localhost:8000"
		self.fridaServer="frida-server-16.1.11-android-x86"
		self.fridaServerFileName="./tools/{}".format(self.fridaServer)
		self.fridumpPath="./tools/fridump/fridump.py"
		self.fridumpOutput="./dump/strings.txt"
		self.fridasslunpinscript1="./tools/fridascript/UniversalSSLUnpinning.js"
		self.androidtmpdir="/data/local/tmp/"
		self.mobSFAPIKey=""
		self.isWindowsOS=False

		if os.name == 'nt':
			self.isWindowsOS = True
		if not os.path.exists(self.outputDir):
			os.mkdir(self.outputDir)
		if not os.path.exists(self.snapshotDir):
			os.mkdir(self.snapshotDir)

	def InitializeMobSFVariables(self):
		isSuccess=False
		try:
			response=requests.get("{}/api_docs".format(self.mobSFURL), timeout=10)
			soup = BeautifulSoup(response.text, "lxml")
			self.mobSFAPIKey=soup.find("p", { "class" : "lead" }).find("strong").find("code").text
			isSuccess=True
		except:
			print ("Failed to initiate conection with MobSF!!")
		return isSuccess

	def ExecuteCommand(self, cmd, isADB=True, syncCall=True):
		command = ""
		output = ""
		if isADB:
			command = "adb " + cmd
		else:
			command = cmd
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		if syncCall:
			output = p.communicate()[0].decode("utf-8", errors="ignore")
			p_status = p.wait()
		return output
