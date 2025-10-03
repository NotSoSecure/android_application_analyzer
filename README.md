# Android Application Analyzer

The tool is used to analyze the content of the android application in local storage.
 <br /> <br />
Install the dependency using following command 
- `chmod +x setup.sh`
- `./setup.sh`

Use the following command to run the tool using python3
- `python -m venv android_application_analyzer` 
- `android_application_analyzer\Scripts\activate` 
- `pip install -r requirements.txt` 
- `python main.py` 


# Note
In order to run "Fridump" and "Frida universal ssl unpinning"
 script, Frida client must be installed on base machine <br /> <br />

It will list down all the devices connected to the device as shown in Figure:
![Usage](Usage/1.png)
<br /> <br />
It will start fetching logcat logs for the selected device as shown in Figure:
![Usage](Usage/2.png)
<br /> <br />
In order to analyze the application, select it from dropdown list as shown in Figure:
![Usage](Usage/3.png)
<br /> <br />
To analyze the file content of the application, Select the file as shown in Figure:
![Usage](Usage/4.png)
<br /> <br />
Analyze the sensitive information logcat logs as shown in Figure:
![Usage](Usage/5.png)
<br /> <br />
In order to view application source in JD-GUI, click on "jdgui" button as shown in Figure:
![Usage](Usage/6.png)
<br /> <br />
If the mobSF configured in the system and in order to open application with MobSF click on "mobSF" button as shown in Figure:
![Usage](Usage/7.png)
<br /> <br />
In order to decompile application using apktool, click on "apktool" button as shown in Figure:
![Usage](Usage/8.png)
<br /> <br />
In order to take application sandbox backup for future reference, click on "snapshot" button as shown in Figure:
![Usage](Usage/9.png)
<br /> <br />
Frida universal SSL unpinning and fridump support as shown in Figure:
![Usage](Usage/10.png)
<br /> <br />

# Future Enhancement

- [x] Strings command on “so or library” file
- [x] Compatible with python3
- [ ] Deep search :- Find all the files of the application from the entire storage
- [x] Snapshot button :- Copy entire application directory for future reference
- [x] The dropdown list of the application instead of Text Box 
- [x] Snapshot button :- Copy entire application directory for future reference
- [x] The dropdown list of the application instead of Text Box
- [x] One clikc application decompile using apktool
- [x] One click JD GUI application navigation
- [x] Universal Frida SSL Script to bypass ssl pinning
- [x] Run Fridump tool to check sensitive information in application memory
- [x] One click reinstall the APK using (uninstall app -> apktool rebuild app -> sign.jar (sign apk)-> install app)
- [x] One click mobSF analysis (prerequisite: mobSF installation required) 
      Note: as of now update the mobSF endpoint in GlobalVariables.py and "mobSFURL" variable

<br />
# References

- https://stackoverflow.com/questions/11524586/accessing-logcat-from-android-via-python
- https://payatu.com/wp-content/uploads/2016/01/diva-beta.tar.gz
- https://pythonspot.com/pyqt5/
- https://github.com/iBotPeaches/Apktool/releases
- https://github.com/java-decompiler/jd-gui/releases
- https://github.com/pxb1988/dex2jar/releases
- https://github.com/appium/sign/tree/master/dist
- https://github.com/frida/frida/releases/download/12.8.10/frida-server-12.8.10-android-x86.xz
- https://github.com/Nightbringer21/fridump
- https://codeshare.frida.re/@pcipolloni/universal-android-ssl-pinning-bypass-with-frida/

