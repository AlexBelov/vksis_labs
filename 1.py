from serial import *
from threading import Thread
import sys

if len(sys.argv) < 1:
  quit()
pts = sys.argv[1]
if len(sys.argv) == 3:
  baud = sys.argv[2]
else:
  baud = 9600

class Receiver(Thread):
    def __init__(self, serialPort):
        Thread.__init__(self)
        self.serialPort = serialPort
    def run(self):
        text = ""
        while (text != "exit\n"):
            text = serialPort.readline()
            print ("\n machine1: " + text)
        self.serialPort.close()

class Sender(Thread):
    def __init__(self, serialPort):
        Thread.__init__(self)
        self.serialPort = serialPort
    def run(self):
        text = ""
        while(text != "exit\n"):
            text = raw_input("Type your message>>") + "\n"
            self.serialPort.write(text)
        self.serialPort.close()

serialPort = Serial("/dev/pts/" + pts, baudrate=baud)

send = Sender(serialPort)
receive = Receiver(serialPort)
send.start()
receive.start()
