
### ----------------------------------------------- ###
# - IMPORTING PACKAGES AND DATA
### ----------------------------------------------- ###

import pygame, sys
from pygame.locals import *
import csv
from functools import reduce 
import datetime
import numpy as np
from pygame import gfxdraw

# importing the csv game matrix
gameMatrix = np.genfromtxt('GameMatrixCSV.csv',delimiter=",")


# importing the csv drawing matrix
drawingMatrix = []
with open('DrawingMatrixCSV.csv', 'r') as csvfile:
    drawingMatrixCSV = csv.reader(csvfile, delimiter=',')
    for row in drawingMatrixCSV:
        drawingMatrix.append(row)

### ----------------------------------------------- ###
# - CLASSES
### ----------------------------------------------- ###

class MovingObject:
    def __init__(self, positionX, positionY):
        self.posX = positionX
        self.posY = positionY
        self.pos = np.array((positionX, positionY))


class Pacman(MovingObject):
    def __init__(self, positionX, positionY, nLives = 3, curDirection = np.array((-1, 0))):
        MovingObject.__init__(self, positionX, positionY)
        self.matrixPos = np.floor_divide(self.pos, 20) # current matrix position, default (col, row) = (14, 23)
        self.matrixPosRow = self.matrixPos[1]
        self.matrixPosCol = self.matrixPos[0]

        self.nLives = nLives
        self.curDirection = curDirection # the actual Pacman's direction 
        self.newDirection = curDirection # the requested Pacman's direction

class Ghost(MovingObject):
    def __init__(self, positionX, positionY, pacmanPosX, pacmanPosY):
        MovingObject.__init__(self, positionX, positionY)
        self.pacmanPosX = pacmanPosX
        self.pacmanPosY = pacmanPosY
        self.pacmanPos = (pacmanPosX, pacmanPosY)


### ----------------------------------------------- ###
# - DRAWING FUNCTIONS
### ----------------------------------------------- ###

### - HELPER FUNCTIONS - ###

# Helper function for drawing circles
def drawCircle(posX, posY, radius, color):
    global displaySurace
    pygame.gfxdraw.aacircle(displaySurface, posX, posY, radius, color) 
    pygame.gfxdraw.filled_circle(displaySurface, posX, posY, radius, color) 


# Helper function for calling all drawing functions
def updateScreen(scoreValue = 0):
    drawWalls()
    menuButtons()
    displayLives()
    displayScore(scoreValue)

# Helper function for displaying text. It creates Surface and Rect objects for given text and recenters it.
def makeText(text, color, bgcolor, centerx, centery):
    textSurf = fontObj.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.center = (centerx, centery)
    return (textSurf, textRect)

### --- ###


# drawing the walls and the dots
def drawWalls():
    displaySurface = pygame.display.set_mode((760, 620))
    # pygame.draw.rect(displaySurface, (0, 0, 0), (0, 0, 560, 620))

    blueCol = 0, 0, 255
    for i in range(0, len(drawingMatrix)):
        for j in range(0, len(drawingMatrix[0])):
            currentPos = drawingMatrix[i][j]
            # corners
            if currentPos[0:2] == 'TL': # top left
                if currentPos == 'TLO' or len(currentPos) == 2: # top left outer
                    pygame.draw.lines(displaySurface, blueCol, False, [(5 + j * 20, 20 + i * 20), (5 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20)], 3)
                if currentPos == 'TLI' or len(currentPos) == 2: # top left inner
                    pygame.draw.lines(displaySurface, blueCol, False, [(15 + j * 20, 20 + i * 20), (15 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
            if currentPos[0:2] == 'TR': # top right
                if currentPos == 'TRO' or len(currentPos) == 2: # top right outer
                    pygame.draw.lines(displaySurface, blueCol, False, [(j * 20, 5 + i * 20), (15 + j * 20, 5 + i * 20), (15 + j * 20, 20 + i * 20)], 3)
                if currentPos == 'TRI' or len(currentPos) == 2: # top right inner
                    pygame.draw.lines(displaySurface, blueCol, False, [(j * 20, 15 + i * 20), (5 + j * 20, 15 + i * 20), (5 + j * 20, 20 + i * 20)], 3)
            if currentPos[0:2] == 'BL': # bottom left
                if currentPos == 'BLO' or len(currentPos) == 2: # bottom left outer
                    pygame.draw.lines(displaySurface, blueCol, False, [(5 + j * 20, i * 20), (5 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
                if currentPos == 'BLI' or len(currentPos) == 2: # bottom left inner
                    pygame.draw.lines(displaySurface, blueCol, False, [(15 + j * 20, i * 20), (15 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20)], 3)
            if currentPos[0:2] == 'BR': # bottom right
                if currentPos == 'BRO' or len(currentPos) == 2: # bottom right outer
                    pygame.draw.lines(displaySurface, blueCol, False, [(15 + j * 20, i * 20), (15 + j * 20, 15 + i * 20), (0 + j * 20, 15 + i * 20)], 3)
                if currentPos == 'BRI' or len(currentPos) == 2: # bottom right inner
                    pygame.draw.lines(displaySurface, blueCol, False, [(5 + j * 20, i * 20), (5 + j * 20, 5 + i * 20), (j * 20, 5 + i * 20)], 3)
            # connecting lines
            if currentPos[0:2] == 'CH': # connecting horizontal
                if currentPos == 'CHT' or len(currentPos) == 2: # connecting horizontal top
                    pygame.draw.line(displaySurface, blueCol, (0 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20), 3)
                if currentPos == 'CHB' or len(currentPos) == 2: # connecting horizonal bottom
                    pygame.draw.line(displaySurface, blueCol, (0 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20), 3)
            if currentPos[0:2] == 'CV': # connecting vertical
                if currentPos == 'CVR' or len(currentPos) == 2: # connecting vertical right
                    pygame.draw.line(displaySurface, blueCol, (15 + j * 20, 0 + i * 20), (15 + j * 20, 20 + i * 20), 3)
                if currentPos == 'CVL' or len(currentPos) == 2: # connecting vertical left
                    pygame.draw.line(displaySurface, blueCol, (5 + j * 20, 0 + i * 20), (5 + j * 20, 20 + i * 20), 3)
            if currentPos == 'LO': # left open
                pygame.draw.lines(displaySurface, blueCol, False, [(0 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20),
                                                                (20 + j * 20, 15 + i * 20), (0 + j * 20, 15 + i * 20)], 3)
            if currentPos == 'RO': # right open
                pygame.draw.lines(displaySurface, blueCol, False, [(20 + j * 20, 5 + i * 20), (0 + j * 20, 5 + i * 20),
                                                                (0 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
            # ghost house entrance
            if currentPos == '8':
                pygame.draw.line(displaySurface, (255, 255, 255), (0 + j * 20, 10 + i * 20), (20 + j * 20, 10 + i * 20), 3)
            # short connecting lines at the teleport points
            if currentPos == 'SL': # short bottom
                pygame.draw.line(displaySurface, blueCol, (0 + j * 20, 15 + i * 20), (5 + j * 20, 15 + i * 20), 3)
                pygame.draw.line(displaySurface, blueCol, (0 + j * 20, 5 + i * 20), (5 + j * 20, 5 + i * 20), 3)
            if currentPos == 'SR':
                pygame.draw.line(displaySurface, blueCol, (15 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20), 3)
                pygame.draw.line(displaySurface, blueCol, (15 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20), 3)
            # dots
            if currentPos == '1':
                drawCircle(30 + (j - 1) * 20, 30 + (i - 1) * 20, 2, (255,255,255))
            if currentPos == '2':
                drawCircle(30 + (j - 1) * 20, 30 + (i - 1) * 20, 5, (255,255,255)) 


# drawing the menu on the right-hand side
def menuButtons():
    global pauseSurface, pauseRect, newGameSurface, newGameRect, autoplaySurface, autoplayRect, quitSurface, quitRect
    
    # the yellow menu rectangle
    pygame.draw.rect(displaySurface, (204,204,0), (565, 5, 755, 610))

    # displaying score, lives and game buttons 
    scoreSurfaceObj, scoreRectObj = makeText('Score', (0, 0, 255), (204,204,0), 660, 52)
    displaySurface.blit(scoreSurfaceObj, scoreRectObj)
    
    livesSurfaceObj, livesRectObj = makeText('Lives', (0, 0, 255), (204,204,0), 660, 184)
    displaySurface.blit(livesSurfaceObj, livesRectObj)

    # Store the option buttons and their rectangles in OPTIONS.
    pauseSurface, pauseRect = makeText('Pause', (0, 0, 255), (215,215,0), 660, 325)
    pygame.draw.rect(displaySurface, (150, 150, 0), (pauseRect.left - 5, pauseRect.top - 5, pauseRect.width + 10, pauseRect.height + 10))
    displaySurface.blit(pauseSurface, pauseRect)

    newGameSurface, newGameRect = makeText('New Game', (0, 0, 255), (215,215,0), 660, 375)
    pygame.draw.rect(displaySurface, (150, 150, 0), (newGameRect.left - 5, newGameRect.top - 5, newGameRect.width + 10, newGameRect.height + 10))
    displaySurface.blit(newGameSurface, newGameRect)

    autoplaySurface, autoplayRect = makeText('Autoplay', (0, 0, 255), (215,215,0), 660, 425)
    pygame.draw.rect(displaySurface, (150, 150, 0), (autoplayRect.left - 5, autoplayRect.top - 5, autoplayRect.width + 10, autoplayRect.height + 10))
    displaySurface.blit(autoplaySurface, autoplayRect)

    quitSurface, quitRect = makeText('Quit :(', (0, 0, 255), (215,215,0), 660, 475)
    pygame.draw.rect(displaySurface, (150, 150, 0), (quitRect.left - 5, quitRect.top - 5, quitRect.width + 10, quitRect.height + 10))
    displaySurface.blit(quitSurface, quitRect)


# displaying life images
def displayLives(nLives = 3):
    livesImage = pygame.image.load('Pacman.png')
    livesImage = pygame.transform.scale(livesImage, (50, 50))

    for i in range(nLives):
        displaySurface.blit(livesImage, (600 + i * 40, 200))


# displaying the actual score (as a string!)
def displayScore(scoreValue = 0):
    scoreValue = str(scoreValue)
    scoreSurf, scoreRect = makeText(scoreValue, (0, 0, 0), (204,204,0), 660, 92)
    displaySurface.blit(scoreSurf, scoreRect)


# checks if there is a dot and updates the score
def checkForDots(rowIndex, colIndex):
    matrixPos = gameMatrix[rowIndex, colIndex]
    if 0 < matrixPos < 3:
        global eatenDots, scoreValue
        eatenDots += 1
        scoreValue += 10 if matrixPos == 1 else 50
        gameMatrix[rowIndex, colIndex] = 0
        drawingMatrix[rowIndex][colIndex] = str(0)
        updateScreen(scoreValue)
        drawCircle(pacman.pos[0], pacman.pos[1], 12, (255, 255, 0))

        # TODO: call chasing function if not matrixPos
        # TODO: declare victory if eatenPoints == 244



### ----------------------------------------------- ###
# - MOVING FUNCTIONS
### ----------------------------------------------- ###

# moving the pacman
def move(pacman):

    def changePosition():
        pacman.pos += pacman.curDirection * 5
        pacman.matrixPos = np.floor_divide(pacman.pos, 20)
    
    # Pacman can change its direction only if it is in the middle of a pile.
    if np.all(np.mod(pacman.pos - 10, np.array((20, 20))) == (0, 0)):
        checkForDots(pacman.matrixPos[1], pacman.matrixPos[0])

        def tunnelPassing(): # changing the coords while in the tunnel
            pacman.pos = np.array((530, 290)) if pacman.curDirection[0] == -1 else np.array((30, 290))
            pacman.matrixPos = np.floor_divide(pacman.pos, 20)
            changePosition()

        # matrix position of the desired direction 
        newMatrixPosCol, newMatrixPosRow  = pacman.matrixPos + pacman.newDirection
        matrixIndex = gameMatrix[newMatrixPosRow, newMatrixPosCol]

        # if there is a wall in the desired direction
        if matrixIndex in {8, 9}:
            # we check if Pacman can perhaps move in the current direction instead of the new one
            nextMatrixPosCol, nextMatrixPosRow  = pacman.matrixPos + pacman.curDirection
            nextMatrixIndex = gameMatrix[nextMatrixPosRow, nextMatrixPosCol]
            if nextMatrixIndex not in {8, 9}:
                if nextMatrixIndex == 5:
                    tunnelPassing()
                else:
                    changePosition()
            else:
                # if Pacman cannot move in the current or desired direction it stops
                pacman.curDirection = np.array((0, 0))
                pacman.newDirection = np.array((0, 0))
        # if there is a tunnel entrance
        elif matrixIndex == 5:
            tunnelPassing()

        # if Pacman can move in the desired direction
        else:
            pacman.curDirection = pacman.newDirection
            changePosition()
            
    # Pacman is not in the middle of the pile so it just moves forward.
    else:
        changePosition()


# TODO:
# - implement the ghosts
# - new game & pause buttons functionality


### ----------------------------------------------- ###
# - MAIN LOOP
### ----------------------------------------------- ###

# Main loop will start here some day
global FPSCLOCK, displaySurface, fontObj,nLives, scoreValue, eatenDots

pygame.init()
displaySurface = pygame.display.set_mode((760, 620))
pygame.display.set_caption('Pacman')

scoreValue, eatenDots, nLives = 0, 0, 3
fontObj = pygame.font.Font('freesansbold.ttf', 25)

# Drawing functions. Each pile has dimensions 20x20 px
updateScreen(scoreValue)

# Initializing Pacman and the Ghosts
pacman = Pacman(290,470)
pygame.draw.circle(displaySurface, (255,255,0), pacman.pos, 12) # pacman

## positions
##self.blinky = Posasti(250, 230, self.pacman.x, self.pacman.y)
##self.pinky = Posasti(290, 290, self.pacman.x, self.pacman.y)
##self.inky = Posasti(270,290)
##self.clyde = Posasti(310,290)

# Timers
clock = pygame.time.Clock()
fps = 100


while True:
    updateScreen(scoreValue)
    drawCircle(pacman.pos[0], pacman.pos[1], 12, (255, 255, 0)) # draw pacman
    move(pacman)

    for event in pygame.event.get():
        if event.type == QUIT:
            # deactivates the pygame library and terminate the program
            pygame.quit() 
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos() # gets mouse position
            print(mousePos)

            # - collidepoint function checks if the mouse position is over the button
            # - Rect objects have attributes x, y, width, height, top, left, right, bottom

            if quitRect.collidepoint(mousePos):
                print('Killing me softly')
                pygame.quit() 
                sys.exit()
                
            if pauseRect.collidepoint(mousePos):
                print('You clicked the pause button dude')

            if newGameRect.collidepoint(mousePos):
                print('You clicked the new  button YO')
                displayScore()
                displayLives()

            if autoplayRect.collidepoint(mousePos):
                print('This will soon be the most wild pacman autoplay ever')

        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                pacman.newDirection = np.array((-1, 0))
            elif event.key == K_RIGHT:
                pacman.newDirection = np.array((1, 0))
            elif event.key == K_DOWN:
                pacman.newDirection = np.array((0, 1))
            elif event.key == K_UP:
                pacman.newDirection = np.array((0, -1))


    pygame.display.update()
    clock.tick(fps)



