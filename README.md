# Android Application Analyzer

The tool is used to analyze the content of the android application in local storage.
 <br /> <br />
Install the dependency using following command 
- `pip3 install -r requirement.txt`

Use the following command to run the tool 
- `python3 main.py` 
<br /> <br />

It will list down all the devices connected to the device as shown in Figure:
![Usage](Usage/1.png)
<br /> <br />
It will start fetching logcat logs for the selected device as shown in Figure:
![Usage](Usage/2.png)
<br /> <br />
To analyze the file content of the application, Select the file as shown in Figure:
![Usage](Usage/3.png)
<br /> <br />
Analyze the sensitive information logcat logs as shown in Figure:
![Usage](Usage/4.png)
<br /> <br />

# Future Enhancement

- [x] Strings command on “so or library” file
- [x] Compatible with python3
- [ ] Deep search :- Find all the files of the application from the entire storage
- [ ] Right click save menu :- To Save the file content for future reference
- [ ] Snapshot button :- Copy entire application directory for future reference
- [ ] The dropdown list of the application instead of Text Box 

<br /> <br />
# References

- https://stackoverflow.com/questions/11524586/accessing-logcat-from-android-via-python
- https://payatu.com/wp-content/uploads/2016/01/diva-beta.tar.gz
- https://pythonspot.com/pyqt5/

