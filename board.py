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
    self._hitList = []
    # Initialize the board as a dictionary of 100 squares
    # 'A1', 'A2', 'A3', ... 'J8', 'J9', 'J10'
    # Each index returns a 0, until a ship is placed in it or a shot is fired
    self._upperLayout = {}
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._upperLayout[x + str(y)] = 0
    self._lowerLayout = {}
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._lowerLayout[x + str(y)] = 0
    self._board = self.createBigBoard()
     
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
  
  def createBigBoard(self):
    squareEdgeLength = self._squareSize
    squares = self._size + 1
    topBoardHeight = squareEdgeLength * squares
  
    bottomBoardStart = topBoardHeight + squareEdgeLength
  
    boardWidth = squareEdgeLength * squares
    boardHeight = squareEdgeLength * (squares * 2 + 1)
    background = blue
    board = makeEmptyPicture(boardWidth, boardHeight, background)
  
    # Draw Horizontal Lines
    for y in range(squares * 2 + 1):
      horizontalEdge = y * squareEdgeLength
      addLine(board, 0, horizontalEdge, boardWidth, horizontalEdge, white)
  
    # Draw Vertical Lines
    for x in range(squares):
      verticalEdge = x * squareEdgeLength
      addLine(board, verticalEdge, 0, verticalEdge, topBoardHeight, white)
      addLine(board, verticalEdge, bottomBoardStart, verticalEdge, boardHeight, white) 
  
    # Now populate each square
    for x in range(squares):
      for y in range(squares * 2 + 1):
        verticalEdge = x * squareEdgeLength
        horizontalEdge = y * squareEdgeLength
        textXBegin = verticalEdge + squareEdgeLength/3
        textYBegin = horizontalEdge + squareEdgeLength * 2 / 3
        # Add the numbers across the first row
        if (y == 0 or y == 12) and x > 0:
          addText(board, textXBegin, textYBegin, str(x), white)
        elif x == 0 and y > 0 and y < 11:
          addText(board, textXBegin, textYBegin, chr(y+64), white)
        elif x == 0 and y > 12:
          addText(board, textXBegin, textYBegin, chr(y-12+64), white)
        elif x > 0 and y > 0:
          if y == 11:
            pass
          else:
            addOval(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength/3, 10, 10, white)
        
    return board
  
  
  # Returns the Description of the board
  # May be silly
  def getDescription(self):
    return self._description
  
  # validateCoordinate()
  # Args: a coordinate in string form
  # Returns: A working coordinate or False depending upon 
  #  if the coordinate is in good form
  def validateCoordinate(self, coordinate):
    # Test if coordinate not empty
    if coordinate:
      # Convert whatever we have to an uppercase string
      dataToValidate = str(coordinate).upper()
      # Test the first char. 
      # ord() < 64 or > 90 means it's not A - Z
      firstChar = ord(dataToValidate[0])
      if firstChar < 64 or firstChar > 90:
        dataToValidate = false
      # Now check to see if that row is on the board
      elif firstChar - 64 > self._size:
        dataToValidate = false
    
      # Try to convert the remaining string to an int, and 
      # see if it's on the board.
      try:
        if int(dataToValidate[1:]) >  self._size:
          dataToValidate = false
      # If int() above fails, we don't have a numeric string.
      except:
        dataToValidate = false
    else:
      dataToValidate = false 
    return dataToValidate

  # decodeCoordinate()
  # Args: a string of a coordinate: 'F5', 'B10', etc
  # Returns: an (x, y) int pair for the row and column
  # also returns (0,0) if the coordinate is too large for the board
  def decodeCoordinate(self, id):
    goodCoordinate = self.validateCoordinate(id)
    if goodCoordinate:
      # ord('A') = 65. ord() - 64 will convert the row letter to a number between 1 - the size of the board
      row = ord(goodCoordinate[0]) - 64
      # Takes everything after the first character and convert into an int
      column = int(goodCoordinate[1:])
      # Make sure the row and column are withing the board's size. If they are beyond the board, return (0,0)
    else:
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
  # fireAT() now inspects the lower board, which is where the player put their ships
  def fireAt(self, coordinate):
      # Test to make sure the coordinate is on the board first
      if self.validateCoordinate(coordinate) != False:
        return self._lowerLayout[coordinate]
      else:
        return 0                 

  # Args: ship object, the starting coordinate, and which way to place the remaining ship
  # Returns: true if there is enough space on the board, false if not
  # validateSpaceForShip() now works on the lower board, so an offset is needed
  def validateSpaceForShip(self, ship, coordinate, growDirection):
 
    # Use size to determine if the board can handle the ship
    size = ship.getSize()
    # Save the starting coordinate in (row,col) form
    (row,col) = self.decodeCoordinate(coordinate)
    if (row, col) != (0,0):
      # Need to modify row because of the combined board
      row += self._size + 2
    
      # Check to make sure the ship will fit on the board
      if growDirection == 'left':
        if col - size < 0:
          # Not enough room on the left
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'right':
        if col + size - 1 > self._size:
          # Not enough room on the right
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'up':
        if row - size < self._size + 2:
          # Not enough room going up
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'down':
        if row + size - 1 > ((self._size + 1) * 2):
          # Not enough room going down
          returnValue = false
        else:
          returnValue = true
      # If we are here, returnValue is not recognized
      else:
        returnValue = false
    else:
      returnValue = false
    return returnValue
  
  # placeShip()
  # Args: ship object, the starting coordinate, and which way to place the remaining ship
  # Returns: true if the ship placement was successful. False if not
  def placeShip(self, ship, coordinate, growDirection):
    sizeOfShip = ship.getSize()
    # We have to check to make sure all squares needed are empty
    # Empty list of coordinates. As coordinates are found to be empty, add them to this list
    listOfEmptyCoordinates = []
    
    (row, col) = self.decodeCoordinate(coordinate)
    # For all the squares needed to place the ship, check that they are empty '0'
    for i in range(sizeOfShip):
      if growDirection == 'left':
        x = row
        y = col - i
      elif growDirection == 'right':
        x = row
        y = col + i 
      elif growDirection == 'up':
        x = row - i
        y = col
      elif growDirection == 'down':
        x = row + i
        y = col
      # Now we have (x,y) to check. encode it and check _layout
      # If true, there is something in (x,y) already
      if self._lowerLayout[self.encodeCoordinate(x,y)]:
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
      self._lowerLayout[i] = ship
      self.drawShipOnSquare(i)
    
    return true
  
  # markSquare()
  # Args: a string of a coordinate. ex: 'F5', and a mark ('hit' | 'miss')
  # Actions: marks the dictionary at index of the coordinate as 'hit' or 'miss'
  # Returns: true if the action succeeded, false if not   
  def markSquare(self, coordinate, action, boardName ):
    if self.decodeCoordinate(coordinate) != (0,0) and (boardName == 'upper' or boardName == 'lower'):
      if boardName == 'lower':
        self._lowerLayout[coordinate] = action
      else:
        self._upperLayout[coordinate] = action
      return true
    else:
      return false

  # addPegToSquare()
  # Args: string of coordinate and a color
  # Actions: draws a colored peg in the coordinate given
  def addPegToSquare(self, coordinate, color, boardName):
    (row, column) = self.decodeCoordinate(coordinate)
    if boardName == 'lower':
      row += self._size + 2
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, color)
    return
  
  # markHit()
  # Args: string of coordinate
  # Actions: draw a red-colored peg in the coordinate given, update dictionary at index of the coordinate as 'hit'
  def markHit(self, coordinate, boardName):
      self.markSquare(coordinate,'hit', boardName)
      self.addPegToSquare(coordinate,red, boardName)
      if boardName == "upper":
        self._hitList.append(coordinate)
  #clearHitLit()
  #clears hit list of all items 
  def clearHitList (self):
    del self._hitList[:]
  
  #def getHitList
  #returns hitList  
  def getHitList(self):
    hitList = self._hitList
    return hitList

  # markMiss()
  # Args: string of coordinate
  # Actions: draw a white-colored peg in the coordinate given, update dictionary at index of the coordinate as 'miss'
  def markMiss(self, coordinate, boardName):
      self.markSquare(coordinate,'miss', boardName)
      self.addPegToSquare(coordinate,white, boardName)
  
  
  
  # drawShipOnSquare()
  # Args: coordinate in string form
  # Actions: updates the picture object self._board, turning the coordinate given gray  
  def drawShipOnSquare(self, coordinate):
    (row, column) = self.decodeCoordinate(coordinate)
    #Offset Row because ships go on lower board
    row += self._size + 2
    # Turn the square gray
    addRectFilled(self._board, self._squareSize * column + 1, self._squareSize * row + 1, self._squareSize - 1, self._squareSize - 1, gray)
    # Put the blue circle in the middle of the square back  
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, blue)
    # Give the circle a white outline
    addOval(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, white)
    return
    
  def getBoard(self):
    return self._board
  