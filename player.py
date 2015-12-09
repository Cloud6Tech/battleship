# Battleship Game
# CST 205
# Player Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason

from media import *
from ship import Ship
from board import Board
from javax.swing import JOptionPane

# Display an option dialog with given title (string), message (string), and options (list); returns index of selected option
def getOption(title,message,options):
  return JOptionPane.showOptionDialog(None,message,title,JOptionPane.DEFAULT_OPTION,JOptionPane.QUESTION_MESSAGE,None,options,options[0])

class Player:
  
  def __init__(self, name=''):
    self._name = name
    self._localBoard = Board('local')
    self._remoteBoard = Board('remote')
    self._listOfShips = []
    self._guesses = []
    
  def getName(self):
    return self._name
    
  def getLocalBoard(self):
    return self._localBoard
    
  def getRemoteBoard(self):
    return self._remoteBoard
    
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
  def makeGuess(self):
    prompt = "Pick a target."
    while True:
      # Prompt the user
      guess = requestString(prompt)
    
      # Verify that the coordinate is valid, return validated coordinate
      if guess == None:
        # Cancel was clicked, return None
        return None
      elif self._remoteBoard.validateCoordinate(guess) == False:
        # Coodinate is invalid, reprompt
        prompt = "That target is invalid. Pick a target."
      elif guess in self._guesses:
        # Coordinate was already guessed, reprompt
        prompt = "You have already fired at that target."
      else:  
        # Coordinate is valid and not already guessed
        self._guesses.append(guess)
        return guess
        
      
  def setupLocalBoard(self, listOfShips):
    self._listOfShips = listOfShips
        
    show(self._localBoard.getBoard())
    
    # Make a copy of the listOfShips
    shipsToPlace = list(self._listOfShips)
    while len(shipsToPlace) > 0:
      ship = shipsToPlace[0]
      
      coordinate = 0
      while not coordinate:
        coordinate = requestString('On what square will the bow of your %s be? ' % ship.getDescription())
        coordinate = self._localBoard.validateCoordinate(coordinate)
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
      
      if self._localBoard.validateSpaceForShip(ship, coordinate, direction):
        if self._localBoard.placeShip(ship, coordinate, direction):
          repaint(self._localBoard.getBoard())
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
    #listOfShips = []
    #listOfShips.append(Ship(2,'destroyer'))
    #listOfShips.append(Ship(3,'submarine'))
    #listOfShips.append(Ship(5,'carrier'))
    #self.setupLocalBoard(listOfShips)
    
    # Automatically place ships
    self._listOfShips = listOfShips
    for i in range(0,len(listOfShips)):
      self._localBoard.placeShip(listOfShips[i],'A' + str(i+1),'down')
    repaint(self._localBoard.getBoard())
    return