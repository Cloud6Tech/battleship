# Battleship Game
# CST 205
# Player Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason

from media import *
from board import Board

class Player:
  
  def __init__(self, name=''):
    self._name = name
    self._localBoard = Board('local')
    self._remoteBoard = Board('remote')
    self._life = 0
    self._listOfShips = []
    
  def getName(self):
    return self._name
    
  def getLocalBoard(self):
    return self._localBoard
    
  def getRemoteBoard(self):
    return self._remoteBoard
    
  def makeGuess(self):
    # Prompt the user to guess a coordinate until a valid coordinate is entered
    prompt = "Pick a target."
    while True:
      # Prompt the user
      guess = requestString(prompt)
    
      # Verify that the coordinate is valid, return validated coordinate
      if self._remoteBoard.decodeCoordinate(guess) != (0,0):
        return guess
      # If the coordinate is invalid, reprompt
      else:
        prompt = "That target is invalid. Pick a target."
      
  def setupLocalBoard(self, listOfShips):
    self._listOfShips = listOfShips
    self._life = len(self._listOfShips)
    
    
    show(self._localBoard.getBoard())
    
    # Make a copy of the listOfShips
    shipsToPlace = list(self._listOfShips)
    while len(shipsToPlace) > 0:
      ship = shipsToPlace[0]
      coordinate = requestString('What square is the bow of your %s?' % ship.getDescription())
      
      direction = 0
      while not direction:
        direction = requestString('Which direction is the stern of your %s' % ship.getDescription())
        if direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right':
          pass
        else:
          showInformation('Please type "up", "down", "left", or "right"')
          direction = 0
      
      if self._localBoard.placeShip(ship, coordinate, direction):
        repaint(self._localBoard.getBoard())
        showInformation('Your %s has been placed on the board' % ship.getDescription())
        del shipsToPlace[0]
          
    return
    
  # Set up a board with predefined ship locations for easier testing
  def setupTestPlayer(self, listOfShips):
    self._listOfShips = listOfShips
    self._life = len(self._listOfShips)
    
    shipsToPlace = list(self._listOfShips)
    
    for i in range(0,len(shipsToPlace)):
      self._localBoard.placeShip(shipsToPlace[i],'A' + str(i+1),'down')
    repaint(self._localBoard.getBoard())