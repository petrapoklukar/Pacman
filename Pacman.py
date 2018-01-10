import pygame, sys
from pygame.locals import *
import csv
from functools import reduce 

# importing the csv game matrix
gameMatrix = []
with open('GameMatrixCSV.csv', 'r') as csvfile:
    gameMatrixCsv = csv.reader(csvfile, delimiter=',')
    for row in gameMatrixCsv:
        gameMatrix.append(row)

# importing the csv drawing matrix
drawingMatrix = []
with open('DrawingMatrixCSV.csv', 'r') as csvfile:
    drawingMatrixCSV = csv.reader(csvfile, delimiter=',')
    for row in drawingMatrixCSV:
        drawingMatrix.append(row)

# drawing the walls
def drawWalls():
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


# Shortcut function for displaying text. It creates Surface and Rect objects for given text and recenters it.
def makeText(text, color, bgcolor, centerx, centery):
    textSurf = fontObj.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.center = (centerx, centery)
    return (textSurf, textRect)


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
def displayScore(scoreValue ='0'):
    scoreSurf, scoreRect = makeText(scoreValue, (0, 0, 0), (204,204,0), 660, 92)
    displaySurface.blit(scoreSurf, scoreRect)


# TODO:
# - resize the score value
# - display the dots
# - implement the game logic


# Main loop will start here some day
global FPSCLOCK, displaySurface, fontObj,nLives, scoreValue

pygame.init()
displaySurface = pygame.display.set_mode((760, 620))
pygame.display.set_caption('Pacman')

scoreValue, nLives = 0, 3
fontObj = pygame.font.Font('freesansbold.ttf', 25)

# Drawing functions
drawWalls()
menuButtons()
displayLives()
displayScore()

clock = pygame.time.Clock()
fps = 60

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            # deactivates the pygame library and terminate the program
            pygame.quit() 
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
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


    pygame.display.update()
    clock.tick(fps)
