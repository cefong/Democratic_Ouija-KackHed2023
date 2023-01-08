#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder
import time
import os

if os.path.exists("/dev/ttyACM0"):
  port = "/dev/ttyACM0"
elif os.path.exists("/dev/ttyACM1"):
  port = "/dev/ttyACM1"
else:
  print("NO DEVICE FOUND!")

p = printcore(port, 115200)

gcode=[i.strip() for i in open('filename.gcode')] # or pass in your own array of gcode lines instead of reading from a file
print(gcode)
print(type(gcode))
gcode = gcoder.LightGCode(gcode)
print(gcode)
# startprint silently exits if not connected yet
while not p.online:
  time.sleep(0.1)

p.startprint(gcode) # this will start a print

time.sleep(5)
p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
