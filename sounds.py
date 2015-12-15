# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# sounds.py

from media import *
from time import *

class SoundEffect:

  def __init__(self, filePath):
    self._sound = makeSound(filePath)
    
  def playStart(self):
    play(self._sound)
    return
	
  def playLooping(self, bTime, eTime):
    if (eTime-bTime > getDuration(self._sound)):
      play(self._sound)
      return clock()
    else:
      return bTime
  
  def playStop(self):
    stopPlaying(self._sound)
    return
	
  def getDur(self):
    dur = getDuration(self._sound)
    return dur