# Battleship Game
# CST 205
# CpuPlayer Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason

from media import *
from autoGuess import *
from ship import Ship
from board import Board
from javax.swing import JOptionPane
import random

# Display an option dialog with given title (string), message (string), and options (list); returns index of selected option
def getOption(title,message,options):
  return JOptionPane.showOptionDialog(None,message,title,JOptionPane.DEFAULT_OPTION,JOptionPane.QUESTION_MESSAGE,None,options,options[0])

class CpuPlayer:
  
  def __init__(self, name=''):
    self._name = name
    self._board = Board('CPU Board')
    self._listOfShips = []
    self._guesses = []
    
  def getName(self):
    return self._name
    
  def getBoard(self):
    return self._board
    
  def getLife(self):
    return len(self._listOfShips)
  
  def removeShip(self, ship):
    i = 0
    for myShip in self._listOfShips:
      if myShip == ship:
        del self._listOfShips[i]
        return true
      else:
        i += 1
    return false
        
  # Prompt the user to guess a coordinate until a valid, un-guessed coordinate is entered; return validated coordinate
  def makeGuess(self,hitCoord, usedCoord):
    #calls autoGuess function makeGuess
    makeGuess(hitCoord, usedCoord)
        
      
  def setupLocalBoard(self, listOfShips):
    self._listOfShips = listOfShips
        
    show(self._board.getBoard())
    
    # Make a copy of the listOfShips
    shipsToPlace = list(self._listOfShips)
    while len(shipsToPlace) > 0:
      ship = shipsToPlace[0]
      
      coordinate = 0
      while not coordinate:
        coordinate = requestString('On what square will the bow of your %s be? ' % ship.getDescription())
        coordinate = self._board.validateCoordinate(coordinate)
        if not coordinate:
          showInformation('That coordinate does not exist on the board, please try again ')
               
      directionChoices = ['Up', 'Down', 'Left', 'Right']
      direction = getOption("", "In which direction is the stern of your %s?" % ship.getDescription(), directionChoices)
      
      if direction == 0:
        direction = 'up'
      elif direction == 1:
        direction = 'down'
      elif direction == 2:
        direction = 'left'
      elif direction == 3:
        direction = 'right'
      
      if self._board.validateSpaceForShip(ship, coordinate, direction):
        if self._board.placeShip(ship, coordinate, direction):
          repaint(self._board.getBoard())
          showInformation('Your %s has been placed on the board' % ship.getDescription())
          del shipsToPlace[0]
        else: 
          showInformation('There is an existing ship in the way, please try a different location ')
      else:
        showInformation('There is not enough room on the board in that direction, please try a different location ')
          
    return
    
  # Set up a board with predefined ship locations for easier testing
  def setupTestPlayer(self,listOfShips):
    # Set up player with fewer ships to manually place
    listOfShips = []
    listOfShips.append(Ship(2,'destroyer'))
    listOfShips.append(Ship(3,'submarine'))
	listOfShips.append(Ship(3,'cruiser'))
	listOfShips.append(Ship(4,'battleship'))
    listOfShips.append(Ship(5,'carrier'))
    self.setupLocalBoard(listOfShips)
    direction = ['up', 'down', 'left', 'right']
	xAxis = "ABCDEFG"
	yMax = 10
	yMin = 1
	self._listOfShips = listOfShips
	#initialize coordinates
	xCoord = ''
	yCoord = 0
	ranDirection = ''
	# Automatically place ships
    for i in range(0,len(listOfShips)):
	  shipSpace = false
	  #check for space on board
	  while shipSpace == false:
		#select random coordinates to place ships
	    xCoord = random.choice(xAxis)
	    yCoord = random.randint(yMin,yMax)
	    ranDirection = random.choice(direction)
		shipSpace = validateSpaceForShip(listOfShips[i], xCoord + str(yCoord),ranDirection)
	  #place ship on board
      shipPlacedFlag = self._board.placeShip(listOfShips[i], xCoord + str(yCoord),ranDirection)
    repaint(self._board.getBoard())
    return
