# Battleship Game
# CST 205
# autoGuess function
# Team: Jason Lloyd Heather Mccabe, Brett, Matthew Mason
################   Note ##################################
###### makesGuess currently requires xAxis to be provided as a string and yAxis to be provided as minY and maxY.
###### Can be changed when integrated with main game

from media import *
import random

#selects every other square on the board and returns a random coordinate value
def randomCoord(switchFlag):
  xAxis ="ABCDEFGHIJ"
  yMax = 10
  yMin = 1
  # looking for flag to determine x axis is odd or y axis
  if switchFlag == false: #skips yAxis
    xCoord=random.choice(xAxis)
    yCoord = random.choice(range(yMin,yMax,2))
    if yCoord == 0:
      yCoord = 1
    target = xCoord + str(yCoord)
  else: #skips xAxis
    xCoord=random.choice(xAxis[0,10,2])
    yCoord = random.randint(yMin,yMax)
    target = xCoord + str(yCoord)
    
  return target
#searches around a hit area for another occupied location
# takes in list current hit locations and used locations. 
#Calls randomCoord as backup if no cases are matched
#returns new target coordinate
def randomLevel2(hitCoord, usedCoord,switchFlag):
  #pulls current hitCoord to separate x and y values
   currentCoord  = hitCoord[0]
   xCoord = currentCoord[0]
   xIndex = xAxis.index(xCoord)
   yCoord = int(currentCoord[1])
   #verifies y+1 will not go off the board and the new coord has not already been used
   if yCoord != yMax and (xCoord +str(yCoord+1) not in usedCoord):
     target = xCoord +str(yCoord+1)
     return target
   #verifies x+1 will not go off the board and the new coord has not already been used
   elif xIndex != (len(xAxis)-1) and (xAxis[xIndex+1] +str(yCoord) not in usedCoord):
     target = xAxis[xIndex+1] +str(yCoord)
     return target
   #verifies y-1 will not go off the board and the new coord has not already been used
   elif yCoord != yMin and (xCoord +str(yCoord-1) not in usedCoord):
     target = xCoord +str(yCoord-1)
     return target
   #verifies x-1 will not go off the board and the new coord has not already been used
   elif xIndex != 0 and (xAxis[xIndex-1] +str(yCoord) not in usedCoord):
     target = xAxis[xIndex-1] +str(yCoord)
     return target
   #used if no cases match
   else:
     return randomCoord(switchFlag)

#level three of search and destory.
#takes 3 parameters current hit list, used coordinate list, calls level two if not parameters match.
#checks two hit point to verify if x or y is repeated then moves either + or - along the axis until the target ship is dead     
def randomLevel3(hitCoord, usedCoord,switchFlag):
  #pulls out first hit coord from the hit list and separates x and y 
  coordHit0  = hitCoord[0]
  xCoordHit0 = coordHit0[0]
  xIndexHit0 = xAxis.index(xCoordHit0)
  yCoordHit0 = int(coordHit0[1])
  #pulls out last hit coord from the hit list and separates x and y
  coordHit1  = hitCoord[len(hitCoord)-1]
  xCoordHit1 = coordHit1[0]
  xIndexHit1 = xAxis.index(xCoordHit1)
  yCoordHit1 = int(coordHit1[1])
  
  #checks to see if x0 is larger that x1 so the will move in smallest to larget along yAxis
  if xIndexHit0 < xIndexHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used. 
    if yCoordHit0 == yCoordHit1 and xIndexHit1 != (len(xAxis)-1) and (xAxis[xIndexHit1+1] +str(yCoordHit0) not in usedCoord):
       target = xAxis[xIndexHit1+1] +str(yCoordHit0)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used. 
    elif yCoordHit0 == yCoordHit1 and xIndexHit0 != (0) and (xAxis[xIndexHit0-1] +str(yCoordHit0) not in usedCoord):
       target = xAxis[xIndexHit0-1] +str(yCoordHit0)
       return target
  #if x0 is larger than x1. if true then the algorithm will grow in opposite direction along yAxis. 
  elif xIndexHit0 > xIndexHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used. 
    if yCoordHit0 == yCoordHit1 and xIndexHit1 != (len(xAxis)-1) and (xAxis[xIndexHit0+1] +str(yCoordHit0) not in usedCoord):
       target = xAxis[xIndexHit0+1] +str(yCoordHit0)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif yCoordHit0 == yCoordHit1 and xIndexHit0 != (0) and (xAxis[xIndexHit1-1] +str(yCoordHit0) not in usedCoord):
       target = xAxis[xIndexHit1-1] +str(yCoordHit0)
       return target
  #checks to see if x0 is smaller than x1. if true the will move in smallest to larget along yAxis
  elif yCoordHit0 < yCoordHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    if xCoordHit0 == xCoordHit1 and yCoordHit1 != yMax and (xCoordHit0 +str(yCoordHit1+1) not in usedCoord):
       target = xCoordHit0 +str(yCoordHit1+1)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif xCoordHit0 == xCoordHit1 and yCoordHit1 != yMin and (xCoordHit0 +str(yCoordHit0-1) not in usedCoord):
       target = xCoordHit0 +str(yCoordHit0-1)
       return target
  #if y0 is larger than y1. If true then the algorithm will grow in opposite direction along x axis.
  elif yCoordHit0 > yCoordHit1:
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    if xCoordHit0 == xCoordHit1 and yCoordHit1 != yMax and (xCoordHit0 +str(yCoordHit0+1) not in usedCoord):
       target = xCoordHit0 +str(yCoordHit0+1)
       return target
    # verifies to point are on the same axis and checks to ensure new target coord will stay on the board and has not been used.
    elif xCoordHit0 == xCoordHit1 and yCoordHit1 != yMin and (xCoordHit0 +str(yCoordHit1-1) not in usedCoord):
       target = xCoordHit0 +str(yCoordHit1-1)
       return target
  else:
    return randomLevel2(hitCoord, usedCoord,switchFlag)
  
#main AI control. Takes two parameters: current hit list and used coordinates
#Make guess returns coordinate in string "A1"
def autoGuess(hitCoord, usedCoord):
  #set intial target postion
  target = "A2"
  #set starting y position for swithFlag check
  lastY = 1
  #initialize switch flag as false
  switchFlag=false
  #check if used coord list is empty. And set last y coordinate used. 
  if len(usedCoord) > 0:
    lastCoord = usedCoord[len(usedCoord)-1]
    lastY = lastCoord[1]
  #In not then the lastY coord will be checked
  #if last Y is positive switch flag will be set to to true allowing xAxis to switch between even squares
  if int(lastY)%2 == 0:
    swithFlag = true
  #if hit list is empty then AI will select every other square until a hit is made
  if len(hitCoord) == 0:
    #will not return a target if porvided coord is in used list
    while target in usedCoord:
      target = randomCoord(switchFlag)
    return target
  #if single hit is made the second level will look around the point until another hit is made
  elif len(hitCoord) == 1:
    #will not return a target if porvided coord is in used list
    while target in usedCoord:
      target = randomLevel2(hitCoord, usedCoord,switchFlag)
    return target
  #if more than two hits third level search will move along a common axis between the first and last coordinate in the list
  elif len(hitCoord) > 1:
    #will not return a target if porvided coord is in used list
    while target in usedCoord:
      target = randomLevel3(hitCoord, usedCoord,switchFlag)
    return target
   