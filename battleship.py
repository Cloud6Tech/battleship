setLibPath("D:\\Heather\\Documents\\School\\CSIT\\2015 Fall B - CST 205\\battleship")
from player import Player
from ship import Ship
from board import Board
from utility import *

# Prompt the user for player type and create and return a human Player object or computer AI object with boards set up
def createPlayer():
  # Create list of ships to place on boards
  listOfShips = [Ship(5,"aircraft carrier"),Ship(4,"battleship"),Ship(3,"submarine"),Ship(3,"cruiser"),Ship(2,"destroyer")]

  # Determine if the player is human (0) or a computer (1)
  playerType = getOption("Player Type","Is this player a human or a computer?",["Human","Computer"])
  
  if playerType == 0: # Human player
    # Get player's name
    playerName = requestString("What is your name?")
    
    # Set player's name to empty string if cancel is clicked
    if playerName == None:
      playerName = ""
      
    # Create player object  
    player = Player(playerName)
    
    # Prompt player to set up their local board
    player.setupLocalBoard(listOfShips)
    
  #elif playerType == 1: # AI (computer) player
    
  else: # Option pane was closed
    return None
    
  return player

def battle():
  
  # Create the players
  player1 = createPlayer()
  player2 = createPlayer()
  
  # Exit if either player wasn't created
  if player1 == None or player2 == None:
    return