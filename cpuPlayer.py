# Battleship Game
# CST 205
# CpuPlayer Class
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason

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
  
  def removeShip(self, ship):
    i = 0
    for myShip in self._listOfShips:
      if myShip == ship:
        del self._listOfShips[i]
        return true
      else:
        i += 1
    return false
        
  # Use autoGuess Seek and Destroy algorithm to select a target to guess
  def makeGuess(self):
    #calls autoGuess function makeGuess
    hitList = self._board.getHitList()
    guess = autoGuess(hitList, self._guesses)
    self._guesses.append(guess)
    return guess
      
  def setupLocalBoard(self, listOfShips):
    self._listOfShips = listOfShips

    yAxis = "ABCDEFGHIJ"
    xMax = 10
    xMin = 1
    
    #initialize coordinates
    yCoord = ''
    xCoord = 0
    runDirection = ['left', 'right', 'up', 'down']
    # Automatically place ships
    for i in range(0,len(listOfShips)):
      shipPlaced = false 
      while shipPlaced == false:
        shipSpace = false
        #check for space on board
        while shipSpace == false:
        #select random coordinates to place ships
          yCoord = random.choice(yAxis)
          xCoord = random.randint(xMin,xMax)
          direction = random.randint(0,len(runDirection)-1)
          shipSpace = self._board.validateSpaceForShip(listOfShips[i], yCoord + str(xCoord),runDirection[direction])
        #place ship on board
        shipPlaced = self._board.placeShip(listOfShips[i], yCoord + str(xCoord),runDirection[direction])
    #repaint(self._board.getBoard())
    return

############# Code for auto guess function #############
yAxis ="ABCDEFGHIJ"
yChoices = []
for i in range(0,len(yAxis),2):
  yChoices.append(yAxis[i])
xMax = 10
xMin = 1
def randomCoord(switchFlag):
  # looking for flag to determine y axis is odd or x axis
  if switchFlag == false: #skips xAxis
    yCoord=random.choice(yAxis)
    xCoord = random.choice(range(xMin,xMax,2))
    if xCoord == 0:
      xCoord = 1
    target = yCoord + str(xCoord)
  else: #skips yAxis
    yCoord = random.choice(yChoices)
    xCoord = random.randint(xMin,xMax)
    target = yCoord + str(xCoord)
  
  return target

# If a single hit has been made, randomLevel2() will guess around that point until another hit is made
#searches around a hit area for another occupied location
# takes in list current hit locations and used locations. 
#Calls randomCoord as backup if no cases are matched
#returns new target coordinate
def randomLevel2(hitCoord, usedCoord,switchFlag):
  #pulls current hitCoord to separate y and x values
   currentCoord  = hitCoord[0]
   yCoord = currentCoord[0]
   yIndex = yAxis.index(yCoord)
   xCoord = int(currentCoord[1])
   #verifies x+1 will not go off the board and the new coord has not already been used
   if xCoord != xMax and (yCoord +str(xCoord+1) not in usedCoord):
     target = yCoord +str(xCoord+1)
     return target
   #verifies y+1 will not go off the board and the new coord has not already been used
   elif yIndex != (len(yAxis)-1) and (yAxis[yIndex+1] +str(xCoord) not in usedCoord):
     target = yAxis[yIndex+1] +str(xCoord)
     return target
   #verifies x-1 will not go off the board and the new coord has not already been used
   elif xCoord != xMin and (yCoord +str(xCoord-1) not in usedCoord):
     target = yCoord +str(xCoord-1)
     return target
   #verifies y-1 will not go off the board and the new coord has not already been used
   elif yIndex != 0 and (yAxis[yIndex-1] +str(xCoord) not in usedCoord):
     target = yAxis[yIndex-1] +str(xCoord)
     return target
   #used if no cases match
   else:
     return randomCoord(switchFlag)

# Level three of search and destroy, called if at least two hits have been made; guesses along a common axis between the first and last coordinate in the list
# Arguments: list of current known hits, list of already-used coordinates, axis switchFlag
# Checks two hit points to verify if x or y is repeated then moves either + or - along the axis until the target ship is dead     
def randomLevel3(hitCoord, usedCoord, switchFlag):
  
  # Pull out first hit coord from the hit list and separate x and y 
  coordHit0  = hitCoord[0]
  yCoordHit0 = coordHit0[0]
  yIndexHit0 = yAxis.index(yCoordHit0)
  xCoordHit0 = int(coordHit0[1])
  
  # Pull out last hit coord from the hit list and separate x and y
  coordHit1  = hitCoord[len(hitCoord)-1]
  yCoordHit1 = coordHit1[0]
  yIndexHit1 = yAxis.index(yCoordHit1)
  xCoordHit1 = int(coordHit1[1])
  
  # If y1 is larger than y0, guesses will move from y0 to y1 along xAxis
  if yIndexHit0 < yIndexHit1:
    # Verify two points are on the same axis, yIndexHit1 hit coord is not on upper edge of board range, and new target coord has not been used
    if xCoordHit0 == xCoordHit1 and yIndexHit1 != (len(yAxis)-1) and (yAxis[yIndexHit1+1] + str(xCoordHit0) not in usedCoord):
      # New target will be one space to the right of the higher hit coordinate
      target = yAxis[yIndexHit1+1] +str(xCoordHit0)
      return target
    # Otherwise, verify two points are on the same axis, yIndexHit0 hit coord is not on lower edge of board range, and new target coord has not been used
    elif xCoordHit0 == xCoordHit1 and yIndexHit0 != (0) and (yAxis[yIndexHit0-1] +str(xCoordHit0) not in usedCoord):
      # New target will be one space above the smaller hit coordinate
      target = yAxis[yIndexHit0-1] + str(xCoordHit0)
      return target
  
  # If y0 is larger than y1, guesses will move in opposite direction along xAxis. 
  elif yIndexHit0 > yIndexHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used. 
    if xCoordHit0 == xCoordHit1 and yIndexHit0 != (len(yAxis)-1) and (yAxis[yIndexHit0+1] +str(xCoordHit0) not in usedCoord):
       target = yAxis[yIndexHit0+1] +str(xCoordHit0)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif xCoordHit0 == xCoordHit1 and yIndexHit1 != (0) and (yAxis[yIndexHit1-1] +str(xCoordHit0) not in usedCoord):
       target = yAxis[yIndexHit1-1] +str(xCoordHit0)
       return target
  #checks to see if y0 is smaller than y1. if true the will move in smallest to larget along xAxis
  elif xCoordHit0 < xCoordHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    if yCoordHit0 == yCoordHit1 and xCoordHit1 != xMax and (yCoordHit0 +str(xCoordHit1+1) not in usedCoord):
       target = yCoordHit0 +str(xCoordHit1+1)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif yCoordHit0 == yCoordHit1 and xCoordHit0 != xMin and (yCoordHit0 +str(xCoordHit0-1) not in usedCoord):
       target = yCoordHit0 +str(xCoordHit0-1)
       return target
  #if x0 is larger than x1. If true then the algorithm will grow in opposite direction along y axis.
  elif xCoordHit0 > xCoordHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    if yCoordHit0 == yCoordHit1 and xCoordHit0 != xMax and (yCoordHit0 +str(xCoordHit0+1) not in usedCoord):
       target = yCoordHit0 +str(xCoordHit0+1)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif yCoordHit0 == yCoordHit1 and xCoordHit1 != xMin and (yCoordHit0 +str(xCoordHit1-1) not in usedCoord):
       target = yCoordHit0 +str(xCoordHit1-1)
       return target
  else:
    return randomLevel2(hitCoord, usedCoord,switchFlag)
  
# Main AI control. 
# Arguments: list of current known hits, list of already-used coordinates
# Returns coordinate in string form, i.e. "A1"
def autoGuess(hitCoord, usedCoord):
  # Set intial target postion
  target = "A2"
  
  # Set starting x position for switchFlag check
  lastX = 1
  
  # Initialize switch flag to false
  switchFlag = false
  
  # If used coord list is not empty, get the last x coordinate used
  if len(usedCoord) > 0:
    lastCoord = usedCoord[len(usedCoord)-1]
    lastX = lastCoord[1]
  
  # If last X is positive, set switch flag to True, allowing yAxis to switch between even squares
  if int(lastX)%2 == 0:
    switchFlag = true
    
  # If hit list is empty then AI will select every other square until a hit is made
  if len(hitCoord) < 1:
    # Pick a random target that has not been guessed
    while target in usedCoord:
      target = randomCoord(switchFlag)
    return target
  
  # If a single hit has been made, randomLevel2() will guess around that point until another hit is made
  elif len(hitCoord) == 1:
    # Pick a target that near the hit target that has not been guessed
    while target in usedCoord:
      target = randomLevel2(hitCoord, usedCoord, switchFlag)
    return target
    
  # If at least two hits have been made, randomLevel3() will guess along a common axis between the first and last coordinate in the list
  elif len(hitCoord) > 1:
    # Pick a target on the common axis that has not been guessed
    while target in usedCoord:
      target = randomLevel3(hitCoord, usedCoord, switchFlag)
      # Final catch for null string caused by adjacent vertical ships; go back to randomLevel2() logic
      if target == None:
        target = randomLevel2(hitCoord, usedCoord, switchFlag)
    return target