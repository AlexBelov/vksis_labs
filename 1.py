from serial import *
from threading import Thread
import sys
import os
import logging

# socat -d -d pty,raw,echo=1 pty,raw,echo=1

logging.basicConfig(filename='info.log',level=logging.INFO)

if len(sys.argv) < 1:
  quit()
pts = sys.argv[1]
if len(sys.argv) == 3:
  baud = sys.argv[2]
else:
  baud = 9600

logger = logging.getLogger("Port " + pts)

class Receiver(Thread):
  def __init__(self, serialPort, pts):
    Thread.__init__(self)
    self.serialPort = serialPort
  def run(self):
    text = ""
    while(True):
      text = serialPort.readline()
      if text:
        print ("message: " + text.rstrip('\n'))
        logger.info("Receive message {}".format(text.rstrip('\n')))

class Sender(Thread):
  def __init__(self, serialPort):
    Thread.__init__(self)
    self.serialPort = serialPort
  def run(self):
    text = ""
    while(True):
      text = raw_input("") + "\n"
      if text == "exit\n":
        self.serialPort.close()
        logger.info("Exit {}".format(self.serialPort.portstr))
        os._exit(0)
      self.serialPort.write(text)
      logger.info("Send message {}".format(text.rstrip('\n')))

serialPort = Serial("/dev/pts/" + pts, baudrate=baud)

logger.info("Run port {} with speed {}".format(pts, baud))

send = Sender(serialPort)
receive = Receiver(serialPort, pts)
send.start()
receive.start()

# Use serialPort.setBaudrate("115200")
