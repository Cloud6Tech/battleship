# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# ship.py

from media import *

class Ship:

  def __init__(self, size, description):
    # Number of hits a ship can take, and number of squares it takes up on the board
    self._size = size
    # Ship's initial life is equal to its size
    self._life = size
    # A name for the ship... for "Your battleship has been destroyed!"
    self._description = description
    # List of coordinates where ship is on board, used to remove ship from board's hitList
    self._coords = []
  
  def getDescription(self):
    return self._description
    
  def getSize(self):
    return self._size  
    
  def setCoord(self,coordinate):
    self._coords.append(coordinate)
    
  def getCoord(self):
    return self._coords
  
  # If ship's _life is less than 0, return true; else return false
  def isSunk(self):
    if self._life > 0:
      return false
    else:
      return true    

  # Reduce _life by 1
  def takeHit(self):
    self._life -= 1
