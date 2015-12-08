# Battleship Game
# CST 205
# Player Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason



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
    
  