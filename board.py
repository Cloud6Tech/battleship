# CST 205
# Final
# Board.py

import string

class Board:
  def __init__(self, description):
    self._description = description
    self._size = 10
    
    self._layout = {}
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._layout[x + str(y)] = 0
  
  def getDescription(self):
    return self._description
    
  
  def decodeCoordinate(self, id):
    # ord('A') = 65. ord() - 64 will convert the row letter to a number between 1 - the size of the board
    row = ord(id[0]) - 64
    column = int(id[1:])
    if row > self._size or column > self._size:
      row = 0
      column = 0
    return (row, column)
  
  def encodeCoordinate(self, x, y):
    row = chr(x + 64)
    column = str(y)
    return row + column
  
  def fireAt(self, coordinate):
      if self.decodeCoordinate(coordinate) != (0,0):
        return self._layout[coordinate]
      else:
        return 0                 
                          
  def placeShip(self, ship, coordinate, growDirection):
    size = ship.getSize()
    
    (origX,origY) = self.decodeCoordinate(coordinate)
    
    # Check to make sure the ship will fit on the board
    if growDirection == 'left':
      if origY - size < 0:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'right':
      if origY + size > self._size:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'up':
      if origX - size < 0:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'down':
      if origX + size > self._size:
        showWarning('There isn\'t enough space on the board')
        return false
    else:
      return false
    
    # Check to make sure all squares needed are empty
    # Empty list of coordinates. As coordinates are checked, add them to this list
    listOfEmptyCoordinates = []
    
    for i in range(size):
      if growDirection == 'left':
        x = origX
        y = origY - i
      elif growDirection == 'right':
        x = origX
        y = origY + i 
      elif growDirection == 'up':
        x = origX - i
        y = origY
      elif growDirection == 'down':
        x = origX + i
        y = origY
      
      # If true, there is something in (x,y) already
      if self._layout[self.encodeCoordinate(x,y)]:
        showWarning('There is a ship in the way')
        return false
      else:
        listOfEmptyCoordinates.append(self.encodeCoordinate(x,y))
    
    for i in listOfEmptyCoordinates:
      self._layout[i] = ship
    
    return true