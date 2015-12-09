setLibPath("D:\\Heather\\Documents\\School\\CSIT\\2015 Fall B - CST 205\\battleship")
from player import Player
from ship import Ship
from board import Board
from utility import *
from random import randint

# Prompt the user for player type and create and return a human Player object or computer AI object with boards set up
def createPlayer():
  # Create list of ships to place on boards
  listOfShips = [Ship(5,"aircraft carrier"),Ship(4,"battleship"),Ship(3,"submarine"),Ship(3,"cruiser"),Ship(2,"destroyer")]

  # Determine if the player is human (0) or a computer (1)
  #playerType = getOption("Player Type","Is this player a human or a computer?",["Human","Computer"])
  playerType = 0
  
  if playerType == 0: # Human player
    # Get player's name
    playerName = requestString("What is your name?")
    
    # Set player's name to empty string if cancel is clicked
    if playerName == None:
      playerName = ""
      
    # Create player object  
    player = Player(playerName)
    
    # Prompt player to set up their local board
    #player.setupLocalBoard(listOfShips)
    player.setupTestPlayer(listOfShips)
    
  #elif playerType == 1: # AI (computer) player
    
  #else: # Option pane was closed
  #  return None
    
  return player

def battle():

  # Create the players, stored in a list for easier turn-taking
  players = [createPlayer(), createPlayer()]
  
  # Exit if either player wasn't created
  if players[0] == None or players[1] == None:
    return
  
  # Randomly pick a player to go first
  n = randint(0,1)
  
  while True:
    # Set current player and opponent
    player = players[n]
    opponent = players[abs(n-1)]
  
    # Get player's guess
    guess = player.makeGuess()
    
    # Display the player's guess
    printNow(player.getName() + " fired at " + str(guess) + ".")
    
    # Check if the player guessed correctly
    strike = opponent.getLocalBoard().fireAt(guess)
    
    if strike == 0:  # The guess was wrong
      # Update player's board
      player.getLocalBoard().markMiss(guess)
      
      # Print message
      printNow(player.getName() + " missed!")
      
    
    else:            # The guess was correct
      # Take 1 hit point away from the hit ship
      strike.takeHit()
      
      # Update the player's board
      player.getLocalBoard().markHit(guess)
      
      # Check if ship was sunk, display appropriate message
      if strike.isSunk():  # The ship is sunk
        printNow(player.getName() + " sunk " + opponent.getName() + "'s " + strike.getDescription() + "!")
      else:                # The ship is hit, but not sunk
        printNow(player.getName() + " hit " + opponent.getName() + "'s " + strike.getDescription() + "!")
    
    # Increment n to swap players next turn
    n = abs(n-1)
    
    break  