#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder
import time
import json
import os

class KackHed():
  def __init__(self):
    with open('locations.json') as json_file:
      self.location = json.load(json_file)
    with open('num2letter.json') as json_file:
      self.num2letter = json.load(json_file)

    if os.path.exists("/dev/ttyACM0"):
      port = "/dev/ttyACM0"
    elif os.path.exists("/dev/ttyACM1"):
      port = "/dev/ttyACM1"
    else:
      print("NO DEVICE FOUND!")

    self.p = printcore(port, 115200)
    self.home()    
    return

  def home(self):
    print("Starting homing sequence")
    gcode = ["G90"]
    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)
    time.sleep(0.5)

  def compileCode(self, lines):
    gcode = gcoder.LightGCode(lines)
    while not self.p.online:
      time.sleep(0.1)
    return gcode

  def run_loop(self):
    while not self.p.online:
      time.sleep(0.1)
    self.send_letter()
    time.sleep(5)
    self.p.disconnect()
    return

  def send_gcode(self, gcode):
    self.p.startprint(gcode)
    return

  """
  def send_random_letter(self):
    import random
    num = str(random.randint(1,10))
    letter = self.num2letter[num]
    print(f"Going to letter: {letter}")

    coordinates = self.location[letter]
    print(f"At coordinates: {coordinates}")

    gcode = self.coordinates2gcode(coordinates)
    print(f"Using gcode: {gcode}")

    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)
    return
    """
    
  def coordinates2gcode(self, coordinates):
    x = coordinates[0]
    y = coordinates[1] 
    
    # soft limits on possible points
    if x < 3 or x > 210 or y < 5 or y > 235:
      print("Uh oh spaggetio :(")
      return
    line = f"G0 X{coordinates[0]} Y{coordinates[1]}"
    return line

  def send_letter(self):
    letter = "goodbye"
    print(f"Going to letter: {letter}")

    coordinates = self.location[letter]
    print(f"At coordinates: {coordinates}")

    gcode = [self.coordinates2gcode(coordinates)]
    print(f"Using gcode: {gcode}")

    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)
    return

def __main__():
  kackhed = KackHed()
  kackhed.run_loop()

__main__()
