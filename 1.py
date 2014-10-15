import serial
import sys

# socat -d -d pty,raw,echo=1 pty,raw,echo=1

if len(sys.argv) < 1:
  quit()
pts = sys.argv[1]
if len(sys.argv) == 3:
  baud = sys.argv[2]
else:
  baud = 9600

s = serial.Serial("/dev/pts/" + pts, baudrate=baud)

while True:
  str = s.readline()
  if str:
    print str
  #s.write("hello/r/n")

