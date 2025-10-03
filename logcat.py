import queue
import threading
import subprocess
import time

from gui import *
from GlobalVariables import *
from PySide6.QtCore import QThread


class AsynchronousFileRead(QThread):
    def __init__(self, fd, queueobj):
        assert isinstance(queueobj, queue.Queue)
        assert callable(fd.readline)
        super().__init__()
        self._fd = fd
        self._queue = queueobj

    def run(self):
        """Read lines from fd and push them into the queue."""
        for line in iter(self._fd.readline, ''):
            QThread.msleep(10)
            if GlobalVariables.isClose:
                break
            self._queue.put(line)

    def eof(self):
        """Check if no more content is expected."""
        return not self.isRunning() and self._queue.empty()


class Logcat(QThread):
    def __init__(self, mainWin, device):
        super().__init__()
        self.mainWin = mainWin
        self.device = device

    def run(self):
        cmd = f"adb -s {self.device} logcat"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        self.stdout_queue = queue.Queue()
        self.stdout_reader = AsynchronousFileRead(process.stdout, self.stdout_queue)
        self.stdout_reader.start()

        time.sleep(1)
        while not self.stdout_reader.eof():
            if GlobalVariables.isClose:
                break

            line = ""
            while not self.stdout_queue.empty():
                line += self.stdout_queue.get().decode(encoding='unicode_escape')

            if line:
                # Appending log output to QTextEdit in GUI
                self.mainWin.txtLogcat.append(line.strip())

            time.sleep(1)

        print("Wait to stop logcat.....")
        self.stdout_reader.join()