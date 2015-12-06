# CST 205
# Final
# ship.py

class Ship:

  def __init__(self, size, description):
    self._size = size
    self._life = size
    self._description = description
  
  def getDescription(self):
    return self._description
    
  def getSize(self):
    return self._size  
  
  def isSunk(self):
    if self._life > 0:
      return false
    else:
      return true    

  def takeHit(self):
    self._life -= 1
    return
