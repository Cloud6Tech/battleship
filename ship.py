# CST 205
# Final
# ship.py

from media import *

class Ship:

  def __init__(self, size, description):
    # Number of hits a ship can take, and number fo squares on the board it takes
    self._size = size
    # At the beginning, the ship's life is equal to it's size
    self._life = size
    # A name for the ship... for "Your battleship has been destroyed!"
    self._description = description
    self._coords = []
  
  def getDescription(self):
    return self._description
    
  def getSize(self):
    return self._size  
    
  def setCoord(self,coordinate):
    self._coords.append(coordinate)
    
  def getCoord(self):
    return self._coords
  
  # isSunk() checks the _life member. If _life is less than 0, the ship is sunk 
  # and the function returns true
  def isSunk(self):
    if self._life > 0:
      return false
    else:
      return true    

  # takeHit reduces the _life member by 1
  def takeHit(self):
    self._life -= 1
    return
