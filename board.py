# CST 205
# Final
# Board.py

from media import *
import string

class Board:
  def __init__(self, description = ''):
    self._description = description
    # By default the board is 10 x 10. Update _size for a different board
    self._size = 10
    self._squareSize = 31
    # Initialize the board as a dictionary of 100 squares
    # 'A1', 'A2', 'A3', ... 'J8', 'J9', 'J10'
    # Each index returns a 0, until a ship is placed in it or a shot is fired
    self._layout = {}
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._layout[x + str(y)] = 0
    self._board = self.createBoard()
     
  # createBoard()
  # Args: none
  # Actions: creates a picture object of the game board
  # Returns: the picture object created
  def createBoard(self):
    squareEdgeLength = self._squareSize
    squares = self._size + 1
    boardWidth = squareEdgeLength * squares
    boardHeight = boardWidth
    background = blue
    board = makeEmptyPicture(boardWidth,boardHeight,blue)
  
    # Drawing Vertical Lines
    for x in range(squares):
      verticalEdge = x * squareEdgeLength
      addLine(board, verticalEdge, 0, verticalEdge, boardHeight, white)
  
    # Drawing Horizontal Lines
    for y in range(squares):  
      horizontalEdge = y * squareEdgeLength
      addLine(board, 0, horizontalEdge, boardWidth, horizontalEdge, white)
  
    # Now populate each square
    for x in range(squares):
      for y in range(squares):
        verticalEdge = x * squareEdgeLength
        horizontalEdge = y * squareEdgeLength
        # Add the numbers across the first row
        if y == 0 and x > 0:
          addText(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength * 2 / 3, str(x), white)
        # Add the letters down the first column
        elif x == 0 and y > 0:
          addText(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength * 2 / 3, chr(y + 64), white)
        # Add peg circles everywhere else (except the top left square)
        elif x > 0 and y > 0:
          addOval(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength/3, 10, 10, white)
          
    return board
    
  # Returns the Description of the board
  # May be silly
  def getDescription(self):
    return self._description
    
  # decodeCoordinate()
  # Args: a string of a coordinate: 'F5', 'B10', etc
  # Returns: an (x, y) int pair for the row and column
  # also returns (0,0) if the coordinate is too large for the board
  def decodeCoordinate(self, id):
    # ord('A') = 65. ord() - 64 will convert the row letter to a number between 1 - the size of the board
    row = ord(id[0]) - 64
    # Takes everything after the first character and convert into an int
    column = int(id[1:])
    # Make sure the row and column are withing the board's size. If they are beyond the board, return (0,0)
    if row > self._size or column > self._size:
      row = 0
      column = 0
    # Return the (x, y) pair
    return (row, column)
  
  #encodeCoordinate()
  # Args: an (x, y) int pair
  # Returns: a string version of the coordinate. ex: 'F4', 'A3', 'C10'
  def encodeCoordinate(self, x, y):
    # chr() converts an int to it's ASCII character. 65 is A, 66 is B, etc
    row = chr(x + 64)
    # Just convert the int given to a string
    column = str(y)
    return row + column
  
  # fireAt()
  # Args: coordinate in string form
  # Returns: what exists at _layout[coordinate] (either a ship or a 0)
  def fireAt(self, coordinate):
      # Test to make sure the coordinate is on the board first
      if self.decodeCoordinate(coordinate) != (0,0):
        return self._layout[coordinate]
      else:
        return 0                 
  
  # placeShip()
  # Args: ship object, the starting coordinate, and which way to place the remaining ship
  # Returns: true if the ship placement was successful. False if not
  def placeShip(self, ship, coordinate, growDirection):
    # Use size to determine if the board can handle the ship
    size = ship.getSize()
    
    # Save the starting coordinate in (x,y) form
    (origX,origY) = self.decodeCoordinate(coordinate)
    
    # Check to make sure the ship will fit on the board
    if growDirection == 'left':
      if origY - size < 0:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'right':
      if origY + size - 1 > self._size:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'up':
      if origX - size < 0:
        showWarning('There isn\'t enough space on the board')
        return false
    elif growDirection == 'down':
      if origX + size - 1 > self._size:
        showWarning('There isn\'t enough space on the board')
        return false
    else:
      return false
    
    # If we got through the if above, the ship can fit on the board.
    # Now we have to check to make sure all squares needed are empty
    
    # Empty list of coordinates. As coordinates are found to be empty, add them to this list
    listOfEmptyCoordinates = []
    
    # For all the squares needed to place the ship, check that they are empty '0'
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
      # Now we have (x,y) to check. encode it and check _layout
      # If true, there is something in (x,y) already
      if self._layout[self.encodeCoordinate(x,y)]:
        showWarning('There is a ship in the way')
        return false
      else:
        # Empty square! add to our list
        listOfEmptyCoordinates.append(self.encodeCoordinate(x,y))
    
    # If we get here and listOfEmptyCoordinates does not equal getSize(), then something weird happened
    if len(listOfEmptyCoordinates) != ship.getSize():
      showWarning('An unknown error occured!!')
      return false
    
    # If we got here, all the squares needed are empty. Now we can finally add the ship to the board
    for i in listOfEmptyCoordinates:
      self._layout[i] = ship
      self.drawShipOnSquare(i)
    
    return true
  
  # markSquare()
  # Args: a string of a coordinate. ex: 'F5', and a mark ('hit' | 'miss')
  # Actions: marks the dictionary at index of the coordinate as 'hit' or 'miss'
  # Returns: true if the action succeeded, false if not   
  def markSquare(self, coordinate, action):
    if self.decodeCoordinate(coordinate) != (0,0):
      self._layout[coordinate] = action
      return true
    else:
      return false

  # addPegToSquare()
  # Args: string of coordinate and a color
  # Actions: draws a colored peg in the coordinate given
  def addPegToSquare(self, coordinate, color):
    (row, column) = self.decodeCoordinate(coordinate)
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, color)
    return
  
  # markHit()
  # Args: string of coordinate
  # Actions: draw a red-colored peg in the coordinate given, update dictionary at index of the coordinate as 'hit'
  def markHit(self, coordinate):
      self.markSquare(coordinate,'hit')
      self.addPegToSquare(coordinate,red)
  
  # markMiss()
  # Args: string of coordinate
  # Actions: draw a white-colored peg in the coordinate given, update dictionary at index of the coordinate as 'miss'
  def markMiss(self, coordinate):
      self.markSquare(coordinate,'miss')
      self.addPegToSquare(coordinate,white)
  
  # drawShipOnSquare()
  # Args: coordinate in string form
  # Actions: updates the picture object self._board, turning the coordinate given gray  
  def drawShipOnSquare(self, coordinate):
    (row, column) = self.decodeCoordinate(coordinate)
    # Turn the square gray
    addRectFilled(self._board, self._squareSize * column + 1, self._squareSize * row + 1, self._squareSize - 1, self._squareSize - 1, gray)
    # Put the blue circle in the middle of the square back  
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, blue)
    # Give the circle a white outline
    addOval(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, white)
    return
    
  def getBoard(self):
    return self._board
  