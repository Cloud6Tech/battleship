# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# sounds.py

from media import *

class SoundEffect:

  def __init__(self, filePath):
    self._sound = makeSound(filePath)
    
  def playStart(self):
    blockingPlay(self._sound)
    return
  
  def playStop(self):
    stopPlaying(self._sound)
    return