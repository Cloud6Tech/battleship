# Final Project: Battleship Game
# Group Seven: Brett Hansen, Jason Lloyd, Matthew Mason, Heather McCabe
# Last modified: Dec 13, 2015
# battleship.py

# Set the directory for imports and sound files
showInformation('Please select the folder containing the library files.')
libPath = pickAFolder()
setLibPath(libPath)
soundDirectory = libPath + '\\SoundFiles\\'

# Import modules/libraries
from player import Player
from cpuPlayer import CPUPlayer
from ship import Ship
from board import Board
from sounds import SoundEffect
from random import randint
from time import sleep

# Create and return a human Player object (type = 0) or computer AI object (type = 1) with boards set up
def createPlayer(playerType):
  # Create list of ships to place on boards
  # Format: Ship(length,type)
  listOfShips = [Ship(5,"aircraft carrier"),Ship(4,"battleship"),Ship(3,"submarine"),Ship(3,"cruiser"),Ship(2,"destroyer")]

  # Set player name and create player object using appropriate class for type
  if playerType == 0: # Human player
    # Get player's name
    playerName = requestString("What is your name?")
    
    # Return without creating player if cancel was clicked
    if playerName == None:
      return
      
    # Create player object  
    player = Player(playerName)
       
  elif playerType == 1: # AI (computer) player
    # Set player's name
    playerName = 'CPU'
    
    # Create CPUPlayer object
    player = CPUPlayer(playerName)
       
  # Prompt human Player to set up board or automatically set up CPUPlayer Board
  player.setupLocalBoard(listOfShips)
  
  # Exit without returning player object if player canceled during ship placement
  if len(player._listOfShips) == 0:
    return
      
  # Update the title of the game board Picture object with the player's name
  player.getBoard().getBoard().setTitle(playerName + "'s Fleet")
    
  return player

# Play a game of Battleship
def battle():

  # Create the soundEffects to be used in the program
  sndDeploy = SoundEffect(soundDirectory + '\\deployEffect.wav')
  sndDefeat = SoundEffect(soundDirectory + '\\defeatEffect.wav')
  sndFire = SoundEffect(soundDirectory + '\\fireEffect.wav')
  sndHit = SoundEffect(soundDirectory + '\\hitEffect.wav')
  sndMiss = SoundEffect(soundDirectory + '\\missedEffect.wav')
  sndSink = SoundEffect(soundDirectory + '\\sinkEffect.wav')
  sndVictory = SoundEffect(soundDirectory + '\\victoryEffect.wav')
  
  # Create the players, stored in a list for easier turn-taking
  # player[0] is human, player[1] is AI/computer
  players = [createPlayer(0), createPlayer(1)]
  
  # Exit if either player wasn't created
  if players[0] == None or players[1] == None:
    return
  
  # Randomly pick a player to go first
  n = randint(0,1)
  
  while True:
    # Set current player and opponent
    player = players[n]
    opponent = players[abs(n-1)]
    
    # Show board if current player is human
    if isinstance(player,Player):
      repaint(players[n].getBoard().getBoard())
  
    # Get player's guess (guessed coordinate will be validated)
    guess = player.makeGuess()
    
    # Player clicked cancel; exit game
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
      
      # Update display of human player's board
      if isinstance(player,Player):
        repaint(player.getBoard().getBoard())
      elif isinstance(opponent,Player):
        repaint(opponent.getBoard().getBoard())
            
      # Print message and play audio
      printNow(player.getName() + " missed!")
      sndMiss.playStart()
      sleep(1)
    
    else: # The guess was correct
      # Update the player's board
      player.getBoard().markHit(guess, 'upper')
      
      # Update the opponent's board
      opponent.getBoard().markHit(guess, 'lower')
      
      # Update display of human player's board
      if isinstance(player,Player):
        repaint(player.getBoard().getBoard())
      elif isinstance(opponent,Player):
        repaint(opponent.getBoard().getBoard())
        
      # Take 1 hit point away from the hit ship
      ship.takeHit()
      
      # Print message and play sound
      printNow(player.getName() + " hit " + opponent.getName() + "'s " + ship.getDescription() + "!")
      sndHit.playStart()
      sleep(1)
            
      # Check if ship was sunk
      if ship.isSunk():
        # Print message and play audio
        printNow(player.getName() + " sunk " + opponent.getName() + "'s " + ship.getDescription() + "!")
        sndSink.playStart()
        sleep(1)
        
        # Remove ship from opponent's list of ships
        opponent.removeShip(ship)
        
        # Clear hit list in player's board - used for CPU makeGuess()
        player.getBoard().clearHitList()
        
        # Check if opponent has lost
        if opponent.getLife() == 0:
          # Print message, play sound, and exit
          printNow(player.getName() + " wins!")
          sndVictory.playStart()
          sleep(1)
          return
    
    # Increment n to swap players next turn
    n = abs(n-1)