# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# Player.py

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
    self._board = Board('Player Board')
    self._listOfShips = []
    self._guesses = []
    
  def getName(self):
    return self._name
    
  def getBoard(self):
    return self._board
    
  def getLife(self):
    return len(self._listOfShips)
  
  # Remove a ship from listOfShips (called when a ship is sunk); returns true if ship is found and removed, false otherwise  
  def removeShip(self, ship):
    if ship in self._listOfShips:
      self._listOfShips.remove(ship)
      return true
    else:
      return false
        
  # Prompt user to guess a coordinate until valid, un-guessed coordinate is entered; return validated coordinate  
  def makeGuess(self):
    # Prompt the user to guess a coordinate until a valid coordinate is entered
    prompt = self._name + ", pick a target."
    while True:
      # Prompt the user
      guess = requestString(prompt)
    
      # Verify that the coordinate input is valid
      if guess == None:
        # Cancel was clicked, return None
        return None
      elif self._board.validateCoordinate(guess) == False:
        # Coodinate is invalid, reprompt
        prompt = "That target is invalid. Pick a target."
      elif guess in self._guesses:
        # Coordinate was already guessed, reprompt
        prompt = "You have already fired at that target."
      else:  
        # Coordinate is valid and not already guessed, return validated coordinate
        self._guesses.append(guess)
        return guess.upper()
        
      
  # Prompt user to select locations to place ships on board
  def setupLocalBoard(self, listOfShips):
    # Save list of ships
    self._listOfShips = listOfShips
        
    # Show player's board
    show(self._board.getBoard())

    # Loop through ships to place
    i = 0
    while i < len(self._listOfShips):
      ship = self._listOfShips[i]
      
      # Prompt user to enter starting coordinate for placement
      coordinate = false
      while not coordinate:
        coordinate = requestString('On what square will the bow of your %s (length: %s) be? ' % (ship.getDescription(),ship.getSize()))
        
        # Cancel was clicked; clear list of ships and return to exit
        if coordinate == None:
          self._listOfShips[:] = []
          return
          
        # Validate coordinate input
        coordinate = self._board.validateCoordinate(coordinate)
        if not coordinate:
          showInformation('That coordinate does not exist on the board. Please try again.')
               
      # Prompt user to select direction in which to fill ship from starting coordinate
      directionChoices = ['Up', 'Down', 'Left', 'Right']
      direction = getOption("", "In which direction is the stern of your %s?" % ship.getDescription(), directionChoices)
      
      # Translate option dialog return value
      if direction == 0:
        direction = 'up'
      elif direction == 1:
        direction = 'down'
      elif direction == 2:
        direction = 'left'
      elif direction == 3:
        direction = 'right'
      
      # Check if there is space in provided location, then place the ship; else reprompt if ship cannot be placed
      if self._board.validateSpaceForShip(ship, coordinate, direction):
        if self._board.placeShip(ship, coordinate, direction):
          repaint(self._board.getBoard())
          showInformation('Your %s has been placed on the board.' % ship.getDescription())
          i += 1 # Incremement listOfShips index
        else: 
          showInformation('There is an existing ship in the way. Please try a different location.')
          continue
      else:
        showInformation('There is not enough room on the board in that direction. Please try a different location.')
        continue
          
    return