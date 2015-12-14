# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# board.py

from media import *
import string

class Board:
  def __init__(self, description = ''):
    self._description = description
    self._size = 10       # By default the board is 10 x 10. Update _size for a different board
    self._squareSize = 31 # pixel width of square
    self._hitList = []    # list of coordinates that have been hit but not sunk
    
    # Initialize the boards as a dictionary of 100 squares: 'A1', 'A2', 'A3', ... 'J8', 'J9', 'J10'
    # Default value is 0, will store ship objects
    # Upper board
    self._upperLayout = {}
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._upperLayout[x + str(y)] = 0
    # Lower board
    self._lowerLayout = {} 
    for x in string.uppercase[:self._size]:
      for y in range(1,self._size+1):
        self._lowerLayout[x + str(y)] = 0
    self._board = self.createBigBoard()
     
  def getDescription(self):
    return self._description
    
  def getHitList(self):
    return self._hitList
  
  def getBoard(self):
    return self._board
 
  # Create and return a single game board Picture object
  def createBoard(self):
    # Get dimensions
    squareEdgeLength = self._squareSize
    squares = self._size + 1
    boardWidth = squareEdgeLength * squares
    boardHeight = boardWidth
    
    # Set background color
    background = blue
    
    # Create empty canvas with above background color
    board = makeEmptyPicture(boardWidth,boardHeight,blue)
  
    # Draw vertical lines
    for x in range(squares):
      verticalEdge = x * squareEdgeLength
      addLine(board, verticalEdge, 0, verticalEdge, boardHeight, white)
  
    # Draw horizontal lines
    for y in range(squares):  
      horizontalEdge = y * squareEdgeLength
      addLine(board, 0, horizontalEdge, boardWidth, horizontalEdge, white)
  
    # Populate squares
    for x in range(squares):
      for y in range(squares):
        # Get square boundaries
        verticalEdge = x * squareEdgeLength
        horizontalEdge = y * squareEdgeLength
        
        # Label with numbers across the first row (x-axis labels)
        if y == 0 and x > 0:
          addText(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength * 2 / 3, str(x), white)
        
        # Label with letters down the first column (y-axis labels)
        elif x == 0 and y > 0:
          addText(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength * 2 / 3, chr(y + 64), white)
        
        # Draw peg circles everywhere else (except the top left square)
        elif x > 0 and y > 0:
          addOval(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength/3, 10, 10, white)
          
    return board
  
  # Create and return a double game board Picture object
  def createBigBoard(self):
    # Get dimensions
    squareEdgeLength = self._squareSize
    squares = self._size + 1
    boardWidth = squareEdgeLength * squares
    boardHeight = squareEdgeLength * (squares * 2 + 1)
    
    # Get starting y-value for bottom board
    topBoardHeight = squareEdgeLength * squares
    bottomBoardStart = topBoardHeight + squareEdgeLength
    
    # Set background color  
    background = blue
    
    # Create empty canvas with above background color
    board = makeEmptyPicture(boardWidth, boardHeight, background)
  
    # Draw horizontal lines
    for y in range(squares * 2 + 1):
      horizontalEdge = y * squareEdgeLength
      addLine(board, 0, horizontalEdge, boardWidth, horizontalEdge, white)
  
    # Draw vertical lines
    for x in range(squares):
      verticalEdge = x * squareEdgeLength
      addLine(board, verticalEdge, 0, verticalEdge, topBoardHeight, white)
      addLine(board, verticalEdge, bottomBoardStart, verticalEdge, boardHeight, white) 
  
    # Populate squares
    for x in range(squares):
      for y in range(squares * 2 + 1):
        # Get square boundaries
        verticalEdge = x * squareEdgeLength
        horizontalEdge = y * squareEdgeLength
        textXBegin = verticalEdge + squareEdgeLength/3
        textYBegin = horizontalEdge + squareEdgeLength * 2 / 3
        
        # Label with numbers across the first row (x-axis labels)
        if (y == 0 or y == 12) and x > 0:
          addText(board, textXBegin, textYBegin, str(x), white)
        
        # Label with letters down the first column for the first board (y-axis labels)
        elif x == 0 and y > 0 and y < 11:
          addText(board, textXBegin, textYBegin, chr(y+64), white)
        
        # Label with letters down the first column for the second board (y-axis labels)
        elif x == 0 and y > 12:
          addText(board, textXBegin, textYBegin, chr(y-12+64), white)
        
        # Draw peg circles everywhere else (except the top left square of each board)
        elif x > 0 and y > 0:
          if y != 11:
            addOval(board, verticalEdge + squareEdgeLength/3, horizontalEdge + squareEdgeLength/3, 10, 10, white)
        
    return board
  
  # Validate coordinate; return a working coordinate or False
  def validateCoordinate(self, coordinate):
    # Make sure coordinate not empty
    if coordinate:
      # Convert coordinate to an uppercase string
      dataToValidate = str(coordinate).upper()
      
      # Check for valid first char; should be letter for row
      firstChar = ord(dataToValidate[0])
      # If ord() < 64 or > 90, firstChar is not A - Z
      if firstChar < 64 or firstChar > 90:  # ord() < 64 or > 90 means it's not A - Z
        dataToValidate = false
      # Else if firstChar is A-Z, check to see if given letter label is on the board
      elif firstChar - 64 > self._size:
        dataToValidate = false
    
      # Try to convert string remainder to int and check against board range
      try:
        # If remaining characters are int, check that int is within board size
        if int(dataToValidate[1:]) > self._size or int(dataToValidate[1:]) <= 0:
          dataToValidate = false
      # If int() above fails, remaining string characters are not numeric
      except:
        dataToValidate = false
    # Else coordinate is empty
    else:
      dataToValidate = false 
    
    return dataToValidate

  # Given a string of a coordinate (ex: 'F5', 'B10', etc.) return (row, column) int pair
  # Return (0,0) if the coordinate is invalid
  def decodeCoordinate(self, id):
    # Validate coordinate
    goodCoordinate = self.validateCoordinate(id)
    
    # If coordinate is valid, get x and y int values
    if goodCoordinate:
      # ord('A') = 65 so ord() - 64 will convert the row letter to a number between 1 and the size of the board
      row = ord(goodCoordinate[0]) - 64
      # Convert everything after the first character into an int
      column = int(goodCoordinate[1:])
      
    # Else if the coordinate is invalid, return (0,0)
    else:
      row = 0
      column = 0
    
    # Return the (row, column) pair
    return (row, column)
  
  #encodeCoordinate()
  # Given an (row, column) int pair, return a string version of the coordinate (ex: 'F4', 'A3', 'C10')
  def encodeCoordinate(self, row, column):
    # chr() converts an int to it's ASCII character. 65 is A, 66 is B, etc.
    r = chr(row + 64)
    
    # Convert the int given to a string
    c = str(column)    
    
    return r + c
  
  # Check that ship can be placed in given location
  # Args: ship object, the starting coordinate, and which direction to fill the remaining ship
  # Return: true if there is enough space on the board, else false
  def validateSpaceForShip(self, ship, coordinate, growDirection):
    # Get ship size
    size = ship.getSize()
    
    # Get the starting coordinate in (row,col) form
    (row,col) = self.decodeCoordinate(coordinate)
    
    if (row, col) != (0,0): # Coordinate is valid
      # Offset row index to access lower board
      row += self._size + 2
    
      # Count squares in grow direction to check that ship fits on board
      if growDirection == 'left':
        if col - size < 0:
          # Not enough room to the left
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'right':
        if col + size - 1 > self._size:
          # Not enough room to the right
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'up':
        if row - size < self._size + 2:
          # Not enough room above
          returnValue = false
        else:
          returnValue = true
      elif growDirection == 'down':
        if row + size - 1 > ((self._size + 1) * 2):
          # Not enough room below
          returnValue = false
        else:
          returnValue = true
      else: # growDirection is invalid
        returnValue = false
    else: # Coordinate is invalid
      returnValue = false
    
    return returnValue
  
  # Add ship object to self._lowerLayout list
  # Args: ship object, the starting coordinate, and which direction to fill the remaining ship
  # Return: true if the ship placement was successful, else false
  def placeShip(self, ship, coordinate, growDirection):
    # Get ship size
    sizeOfShip = ship.getSize()
    
    # Empty list of coordinates; as coordinates are found to be empty, add them to this list
    # Used to make sure all needed squares are empty
    listOfEmptyCoordinates = []
    
    # Get the starting coordinate in (row,col) form
    (row, col) = self.decodeCoordinate(coordinate)

    # For all squares needed to place the ship, check that they are empty (0 value)
    for i in range(sizeOfShip):
      # Find the row or column int coordinate of the adjacent square in the given direction
      if growDirection == 'left':
        r = row
        c = col - i
      elif growDirection == 'right':
        r = row
        c = col + i 
      elif growDirection == 'up':
        r = row - i
        c = col
      elif growDirection == 'down':
        r = row + i
        c = col
              
      # Encode coordinate and check self._lowerLayout for empty square
      if self._lowerLayout[self.encodeCoordinate(r,c)]:
        # Ship already exists at coordinate
        return false
      else:
        # Empty square; add coordinate to list of empty coordinates
        listOfEmptyCoordinates.append(self.encodeCoordinate(r,c))
    
    # Check that there are as many empty coordinates as the ship's size requires
    if len(listOfEmptyCoordinates) != ship.getSize():
      showWarning('An unknown error occured!')
      return false
    
    # All the squares needed are empty; place ship at validated coordinates
    for i in listOfEmptyCoordinates:
      # Add ship to lowerLayout list
      self._lowerLayout[i] = ship
      
      # Store coordinate in ship object as well for use in clearHitList()
      ship.setCoord(i)
      
      # Draw ship on board by making square background grey
      self.drawShipOnSquare(i)
    
    # Return true for successful placement
    return true
  
  # Update the picture object self._board by turning the square at given coordinate string gray  
  def drawShipOnSquare(self, coordinate):
    # Get the starting coordinate in (row,col) form
    (row, column) = self.decodeCoordinate(coordinate)
    
    # Offset row index to access lower board
    row += self._size + 2

    # Color the square background gray
    addRectFilled(self._board, self._squareSize * column + 1, self._squareSize * row + 1, self._squareSize - 1, self._squareSize - 1, gray)
    
    # Redraw the blue circle in the middle of the square  
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, blue)
    
    # Draw a white outline around the blue circle
    addOval(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, white)
    
    return
  
  # Draw a colored peg in given color at the given coordinate string
  def addPegToSquare(self, coordinate, color, boardName):
    # Get the starting coordinate in (row,col) form
    (row, column) = self.decodeCoordinate(coordinate)
    
    # Offset row index to access lower board
    if boardName == 'lower':
      row += self._size + 2
      
      # Draw circle in given color at given coordinate
    addOvalFilled(self._board, self._squareSize * column + self._squareSize/3, self._squareSize * row + self._squareSize/3, 10, 10, color)
    
    return
  
  # Given a coordinate in string form, return ship object at self._lowerLayout[coordinate]; if no ship, return 0
  def fireAt(self, coordinate):
    # Validate coordinate, then return ship or 0
    if self.validateCoordinate(coordinate):
      return self._lowerLayout[coordinate]
    else:
      return 0   

  # Draw a red-colored peg at given coordinate string, add coordinate to self._hitList
  def markHit(self, coordinate, boardName):
      self.addPegToSquare(coordinate,red, boardName)
      if boardName == "upper":
        self._hitList.append(coordinate)
        
  # Draw a white-colored peg at given coordinate string
  def markMiss(self, coordinate, boardName):
    self.addPegToSquare(coordinate,white, boardName)
    
  # Given ship object, remove its coords from self._hitList
  def clearHitList (self,ship):
    for coord in ship.getCoord():
      if coord in self._hitList:
        self._hitList.remove(coord)