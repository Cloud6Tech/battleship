# Final Project: Battleship Game
# CST 205
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 14, 2015
# CPUPlayer.py

from media import *
from ship import Ship
from board import Board
import random

class CPUPlayer:
  
  def __init__(self, name=''):
    self._name = name
    self._board = Board('CPU_Board')
    self._listOfShips = []
    self._guesses = []
 
  def getName(self):
    return self._name
    
  def getBoard(self):
    return self._board
    
  def getLife(self):
    return len(self._listOfShips)
  
  # Remove a ship from listOfShips (called when a ship is sunk)
  def removeShip(self, ship):
    if ship in self._listOfShips:
      self._listOfShips.remove(ship)
      return true
    else:
      return false
        
  # Use autoGuess() 'Seek and Destroy' algorithm to select a target to guess
  def makeGuess(self):
    hitList = self._board.getHitList()
    guess = autoGuess(hitList, self._guesses)
    self._guesses.append(guess)
    return guess
      
  # Automatically place ships on board
  def setupLocalBoard(self, listOfShips):
    # Save list of ships
    self._listOfShips = listOfShips

    # Set board axis ranges
    yAxis = "ABCDEFGHIJ"
    xMax = 10
    xMin = 1
    
    # Initialize coordinates
    yCoord = ''
    xCoord = 0
    runDirection = ['left', 'right', 'up', 'down']
    
    # Place ships
    for i in range(0,len(listOfShips)):
      shipPlaced = false 
      while shipPlaced == false:
        
        # Select random coordinates and directions until a set is found that allows space for the ship
        shipHasSpace = false
        while shipHasSpace == false:
          yCoord = random.choice(yAxis)
          xCoord = random.randint(xMin,xMax)
          direction = random.randint(0,len(runDirection)-1)
          shipHasSpace = self._board.validateSpaceForShip(listOfShips[i], yCoord + str(xCoord),runDirection[direction])
        
        # Place ship on board
        shipPlaced = self._board.placeShip(listOfShips[i], yCoord + str(xCoord),runDirection[direction])

    return

############# 'Seek and Destroy': code for autoGuess() #############
# Axis labels
yAxis ="ABCDEFGHIJ"
xMax = 10
xMin = 1

# Level One: Called if hit list is empty; guesses every other square until a hit is made
# Argument: axis switchFlag 
# Returns target coordinate as string
def randomCoord(switchFlag):
  # switchFlag determines which axis will have guessed values skipped
  # Every other square is skipped, reducing random move option from 100 to 50
  if switchFlag == false: # Skip even x-axis values with y-axis 'ACEGI' values
    # Pick a random value from the list of every-other y-value
    yCoord = random.choice('ACEGI')
    
    # Pick a random odd value on the x-axis
    xCoord = random.choice(range(xMin,xMax,2))

    # Create coordinate string
    target = yCoord + str(xCoord)
  else: # Skip odd x-axis values with y-axis 'BDFHJ' values
    # Pick a random value from the list of every-other y-value
    yCoord = random.choice('BDFHJ')
    
    # Pick a random even value on the x-axis
    xCoord = random.choice(range(2,xMax+1,2))

    # Create coordinate string
    target = yCoord + str(xCoord)
  
  return target

# Level Two: Called if exactly one hit has been made; guesses around that point until another hit is made
# Arguments: list of current known hits, list of already-used coordinates, axis switchFlag
# Returns target coordinate in string form
def randomLevel2(hitCoord, usedCoord,switchFlag):
  # Get current hitCoord and separate y and x values
   currentCoord  = hitCoord[0]
   yCoord = currentCoord[0]
   yIndex = yAxis.index(yCoord)
   xCoord = int(currentCoord[1:])
   
   # Verify x+1 is on the board and new target coord has not already been used
   if xCoord != xMax and (yCoord +str(xCoord+1) not in usedCoord):
     # Target coordinate will be one space to the right of hit coordinate
     target = yCoord +str(xCoord+1)
     return target
   # Else verify y+1 is on the board and new target coord has not already been used
   elif yIndex != (len(yAxis)-1) and (yAxis[yIndex+1] +str(xCoord) not in usedCoord):
     # Target coordinate will be one space below hit coordinate
     target = yAxis[yIndex+1] +str(xCoord)
     return target
   # Else verify x-1 is on the board and new target coord has not already been used
   elif xCoord != xMin and (yCoord +str(xCoord-1) not in usedCoord):
     # Target coordinate will be one space to the left of hit coordinate
     target = yCoord +str(xCoord-1)
     return target
   # Else verify y-1 is on the board and new target coord has not already been used
   elif yIndex != 0 and (yAxis[yIndex-1] +str(xCoord) not in usedCoord):
     # Target coordinate will be one space above hit coordinate
     target = yAxis[yIndex-1] +str(xCoord)
     return target
   # Else if everything fails, go to randomCoord() logic
   else:
     return randomCoord(switchFlag)

# Level Three: Called if at least two hits have been made; guesses along a common axis between the first and last coordinate in the list
# Arguments: list of current known hits, list of already-used coordinates, axis switchFlag
# Checks two hit points to verify if x or y is repeated then moves either + or - along the axis until the target ship is dead     
def randomLevel3(hitCoord, usedCoord, switchFlag):
  # Get first hitCoord and separate y and x values
  coordHit0  = hitCoord[0]
  yCoordHit0 = coordHit0[0]
  yIndexHit0 = yAxis.index(yCoordHit0)
  xCoordHit0 = int(coordHit0[1:])
  
  # Get last hitCoord and separate y and x values
  coordHit1  = hitCoord[len(hitCoord)-1]
  yCoordHit1 = coordHit1[0]
  yIndexHit1 = yAxis.index(yCoordHit1)
  xCoordHit1 = int(coordHit1[1:])
  
  # If y0 < y1, guesses will move down from y1 or up from y0 (along the y-axis)
  if yIndexHit0 < yIndexHit1:
    # Verify both points have same x-value, y1 hit coord is not on upper edge of board range, and new target coord has not been used
    if xCoordHit0 == xCoordHit1 and yIndexHit1 != (len(yAxis)-1) and (yAxis[yIndexHit1+1] + str(xCoordHit0) not in usedCoord):
      # New target will be one space below the y1 hit
      target = yAxis[yIndexHit1+1] +str(xCoordHit0)
      return target
      
    # Else, verify both points have same x-value, y0 hit coord is not on lower edge of board range, and new target coord has not been used
    elif xCoordHit0 == xCoordHit1 and yIndexHit0 != (0) and (yAxis[yIndexHit0-1] +str(xCoordHit0) not in usedCoord):
      # New target will be one space above the y0 hit
      target = yAxis[yIndexHit0-1] + str(xCoordHit0)
      return target
  
  # If y0 > y1, guesses will move down from y0 or up from y1 (along the y-axis)
  elif yIndexHit0 > yIndexHit1:
    # Verify both points have same x-value, y0 is not on upper edge of board range, and new target coord has not been used
    if xCoordHit0 == xCoordHit1 and yIndexHit0 != (len(yAxis)-1) and (yAxis[yIndexHit0+1] +str(xCoordHit0) not in usedCoord):
      # New target will be one space below the y0 hit
      target = yAxis[yIndexHit0+1] +str(xCoordHit0)
      return target
       
    # Else, verify both points have same x-value, y1 is not on the lower edge of board range, and new target coord has not been used
    elif xCoordHit0 == xCoordHit1 and yIndexHit1 != (0) and (yAxis[yIndexHit1-1] +str(xCoordHit0) not in usedCoord):
      # New target will be one space above the y1 hit
      target = yAxis[yIndexHit1-1] +str(xCoordHit0)
      return target
       
  # If x0 < x1, guesses will move right from x1 or left from x0 (along the x-axis)
  elif xCoordHit0 < xCoordHit1:
    # Verify both points have same y-value, x1 is not on the upper edge of board range, and new target coord has not been used
    if yCoordHit0 == yCoordHit1 and xCoordHit1 != xMax and (yCoordHit0 +str(xCoordHit1+1) not in usedCoord):
      # New target will be one space to the right of x1 hit
      target = yCoordHit0 +str(xCoordHit1+1)
      return target
       
    # Else, verify both points have same y-value, x0 is not on the lower edge of board range, and new target coord has not been used
    elif yCoordHit0 == yCoordHit1 and xCoordHit0 != xMin and (yCoordHit0 +str(xCoordHit0-1) not in usedCoord):
      # New target will be one space to the left of x0 hit
      target = yCoordHit0 +str(xCoordHit0-1)
      return target
       
  # If x0 > x1, guesses will move right from x0 or left from x1 (along the x-axis)
  elif xCoordHit0 > xCoordHit1:
    # Verify both points have same y-value, x0 is not on the upper edge of board range, and new target coord has not been used
    if yCoordHit0 == yCoordHit1 and xCoordHit0 != xMax and (yCoordHit0 +str(xCoordHit0+1) not in usedCoord):
      # New target will be one space to the right of x0 hit
      target = yCoordHit0 +str(xCoordHit0+1)
      return target
       
    # Else, verify both points have same y-value, x1 is not on the lower edge of board range, and new target coord has not been used
    elif yCoordHit0 == yCoordHit1 and xCoordHit1 != xMin and (yCoordHit0 +str(xCoordHit1-1) not in usedCoord):
      # New target will be one space to the left of x1 hit
      target = yCoordHit0 +str(xCoordHit1-1)
      return target
      
  # Else if everything fails, go to randomLevel2() logic
  else:
    return randomLevel2(hitCoord, usedCoord,switchFlag)
  
# Main AI guessing control. 
# Arguments: list of current known hits, list of already-used coordinates
# Returns coordinate in string form, i.e. "A1"
def autoGuess(hitCoord, usedCoord):
  # Intialize target variable
  target = ''
  
  # Set starting x position for switchFlag check
  lastX = 1
  
  # Initialize switch flag to false
  switchFlag = false
  
  # If used coord list is not empty, get the last x coordinate used
  if len(usedCoord) > 0:
    lastCoord = usedCoord[len(usedCoord)-1]
    lastX = lastCoord[1]
  
  # If last X is positive, set switch flag to True, allowing yAxis to switch between even squares
  if int(lastX)%2 != 0:
    switchFlag = true
    
  # If hit list is empty then AI will select every other square until a hit is made
  if len(hitCoord) < 1:
    # Pick a random target that has not been guessed
    while target == '' or target in usedCoord:
      target = randomCoord(switchFlag)
    return target
  
  # If a single hit has been made, randomLevel2() will guess around that point until another hit is made
  elif len(hitCoord) == 1:
    # Pick a target that near the hit target that has not been guessed
    while target == '' or target in usedCoord:
      target = randomLevel2(hitCoord, usedCoord, switchFlag)
    return target
    
  # If at least two hits have been made, randomLevel3() will guess along a common axis between the first and last coordinate in the list
  elif len(hitCoord) > 1:
    # Pick a target on the common axis that has not been guessed
    while target == '' or target in usedCoord:
      target = randomLevel3(hitCoord, usedCoord, switchFlag)
      # Final catch for null string caused by adjacent vertical ships; go to randomLevel2() logic
      if target == None:
        target = randomLevel2(hitCoord, usedCoord, switchFlag)
    return target