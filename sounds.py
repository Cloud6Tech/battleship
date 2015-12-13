# Battleship Game
# CST 205
# SoundEffect Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason
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