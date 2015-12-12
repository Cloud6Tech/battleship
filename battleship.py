#setLibPath("D:\\Heather\\Documents\\School\\CSIT\\2015 Fall B - CST 205\\battleship")
#setLibPath('C:\\Users\\Jason Lloyd\\Dropbox\\School\\CSUMB\\CST205\\Final Project\\battleship\\')
setLibPath('C:\\Users\\Bretterbear\\Documents\\GitHub\\battleship')

from player import Player
from ship import Ship
from board import Board
from sounds import SoundEffect
#from utility import *
from random import randint
from time import sleep

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
    
    # Return without creating player if cancel was clicked
    if playerName == None:
      return
      
    # Create player object  
    player = Player(playerName)
    
    # Prompt player to set up their local board
    player.setupLocalBoard(listOfShips)
    #player.setupTestPlayer(listOfShips)
    
  #elif playerType == 1: # AI (computer) player
    
  # Update the title of the game board Picture object with the player's name
  player.getBoard().getBoard().setTitle(playerName + "'s Fleet")
    
  return player

def battle():

  # Create the soundEffects to be used in the program
  #Change this to reflect your sound directory in order to make audio work
  soundDirectory = 'C:\\Users\\Bretterbear\\Documents\\GitHub\\battleship\\SoundFiles'
  
  sndDeploy = SoundEffect(soundDirectory + '\\deployEffect.wav')
  sndDefeat = SoundEffect(soundDirectory + '\\defeatEffect.wav')
  sndFire = SoundEffect(soundDirectory + '\\fireEffect.wav')
  sndHit = SoundEffect(soundDirectory + '\\hitEffect.wav')
  sndMiss = SoundEffect(soundDirectory + '\\missedEffect.wav')
  sndSink = SoundEffect(soundDirectory + '\\sinkEffect.wav')
  sndVictory = SoundEffect(soundDirectory + '\\victoryEffect.wav')
  
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
    board = players[n].getBoard()
    repaint(board.getBoard())
  
    # Get player's guess; guessed coordinate will be validated
    guess = player.makeGuess()
    
    # If makeGuess returned None, player clicked cancel; exit
    if guess == None:
      return
    
    # Display the player's guess and give audio feedback
    printNow(player.getName() + " fired at " + str(guess) + ".")
    sndFire.playStart()
    sleep(1)
    
    # Check if the player guessed correctly

    ship = opponent.getBoard().fireAt(guess)
    
    if ship == 0:  # The guess was wrong
      # Update player's board
      player.getBoard().markMiss(guess, 'upper')
      
      # Update opponent's board
      opponent.getBoard().markMiss(guess, 'lower')
      
      # Print message and play audio
      printNow(player.getName() + " missed!")
      sndMiss.playStart()
      sleep(1)
    
    else:
      # The guess was correct
      # Take 1 hit point away from the hit ship
      ship.takeHit()
      sndHit.playStart()
      sleep(1)
      # Update the player's board
      player.getBoard().markHit(guess, 'upper')
      
      # Update the opponent's board
      opponent.getBoard().markHit(guess, 'lower')
      
      # Check if ship was sunk, display appropriate message
      if ship.isSunk():  # The ship is sunk
        printNow(player.getName() + " sunk " + opponent.getName() + "'s " + ship.getDescription() + "!")
        sndSink.playStart()
        sleep(1)
        # Remove ship from opponent's list of ships
        opponent.removeShip(ship)
        # Check if opponent has lost, print message and exit if so
        if opponent.getLife() == 0:
          printNow(player.getName() + " wins!")
          sndVictory.playStart()
          sleep(1)
          return
      else:                # The ship is hit, but not sunk
        printNow(player.getName() + " hit " + opponent.getName() + "'s " + ship.getDescription() + "!")
    
    # Increment n to swap players next turn
    n = abs(n-1)