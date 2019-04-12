import Queue
import threading
import subprocess
from gui import *
from GlobalVariables import *
import time
from PyQt5.QtCore import QThread

class AsynchronousFileRead(QThread):
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        QThread.__init__(self) 
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            if GlobalVariables.isClose:
                break
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.isRunning() and self._queue.empty()

class Logcat(QThread):
    def __init__(self, mainWin, device):
        self.mainWin = mainWin
        self.device=device
        QThread.__init__(self) 
        #threading.Thread.__init__(self)

    def run(self):
        cmd="adb -s "+self.device+" logcat"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        self.stdout_queue = Queue.Queue()
        self.stdout_reader = AsynchronousFileRead(process.stdout, self.stdout_queue)
        self.stdout_reader.start()
        time.sleep(1)
        while not self.stdout_reader.eof():
            line=''
            if GlobalVariables.isClose:
                break
            
            while not self.stdout_queue.empty():
                line+=self.stdout_queue.get()
            
            if line:
                self.mainWin.txtLogcat.append(line.strip())
            time.sleep(1)
        print "Wait to stop logcat....."
        self.stdout_reader.join()
