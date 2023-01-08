#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder
import time
import json
import os
import requests

class KackHed():
  def __init__(self):
    self.xmin = 3
    self.xmax = 210
    self.ymin = 5
    self.ymax = 235
    self.xmiddle = (self.xmin + self.xmax)/2
    self.ymiddle = (self.ymin + self.ymax)/2

    self.last_letter = " "
    self.last_word_state = ""
    self.new_website_letter = ""

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
    gcode = [f"G90", "G0 X100 Y75"]
    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)
    time.sleep(2)

  def compileCode(self, lines):
    gcode = gcoder.LightGCode(lines)
    while not self.p.online:
      time.sleep(0.1)
    return gcode

  def set_word_state(self):
    self.last_word_state
    x = requests.get('https://cfong71.wixsite.com/mysite/_functions/word')
    self.word_state = x.json()['word']
    print(self.word_state)
    
    diff = len(self.word_state) - len(self.last_word_state)
    if diff > 0:
      print("Case 1")
      self.new_website_letter = self.word_state[-1]
      self.new_website_letter = self.new_website_letter.upper()
    elif diff < 0:
      print("Case 2")
      self.new_website_letter = "." 
    elif len(self.word_state) == 0:
      print("Case 3")
      self.new_website_letter = "."
    else:
      print("Case 4")
      self.new_website_letter = ""

    self.last_word_state = self.word_state

    return

  def run_loop(self):
    self.set_word_state()

    print(self.word_state)

    if self.new_website_letter != "":
      while not self.p.online:
        time.sleep(0.1)
      print(f"Going to print the letter: {self.new_website_letter}")
      if self.last_letter == self.new_website_letter:
        self.repeat_letter(self.new_website_letter)
      else:
        self.send_letter(self.new_website_letter)
      self.last_letter = self.new_website_letter

    return

  def send_gcode(self, gcode):
    self.p.startprint(gcode)
    return

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
    
  def coordinates2gcode(self, coordinates):
    x = coordinates[0]
    y = coordinates[1] 
    
    # soft limits on possible points
    if x < self.xmin or x > self.xmax or y < self.ymin or y > self.ymax:
      print("Uh oh spaggetio :(")
      return
    line = f"G0 X{coordinates[0]} Y{coordinates[1]}"
    return line

  def send_letter(self, letter):
    print(f"Going to letter: {letter}")

    coordinates = self.location[letter]
    print(f"At coordinates: {coordinates}")

    gcode = [self.coordinates2gcode(coordinates)]
    print(f"Using gcode: {gcode}")

    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)

    self.last_letter = letter
    return

  def repeat_letter(self, letter):
    if letter == ".":
      return
    print(f"repeating letter: {letter}")

    coordinates = self.location[letter]
    x = coordinates[0]
    y = coordinates[1]
    print(f"At coordinates: {coordinates}")

    if x < self.xmiddle:
      if y < self.ymiddle:
        #circle left down J
        gcode = [f"G2 X{x} Y{y} I10 J10"]
      else:
        #circle left up
        gcode = [f"G3 X{x} Y{y} I10 J-10"]
        pass
    else:
      if y < self.ymiddle:
        #circle right down
        gcode = [f"G2 X{x} Y{y} I-10 J10"]
        pass
      else:
        #circle right up
        gcode = [f"G2 X{x} Y{y} I-10 J-10"]
        pass

    print(f"Using gcode: {gcode}")

    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)

    self.last_letter = letter
    
    return

  def send_word(self, word):
    word = word.replace(" ", "")
    word = word.upper()
    for letter in word:
      if letter == self.last_letter:
        self.repeat_letter(letter)
      else:
        self.send_letter(letter)
      time.sleep(4)

  def dwell(self, milliseconds):
    print("Dwelling for {milliseconds} milliseconds")
    gcode = [f"G4 P{milliseconds}"]
    compiled = self.compileCode(gcode)
    self.send_gcode(compiled)
    return


def __main__():
  kackhed = KackHed()
  while 1:
    kackhed.run_loop()
  
  kackhed.p.disconnect()

__main__()
