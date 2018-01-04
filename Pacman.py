import pygame, sys
from pygame.locals import *
import csv


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

pygame.init()
DISPLAYSURF = pygame.display.set_mode((560, 620))
pygame.display.set_caption('Pacman')

# drawing the walls
blueCol = 0, 0, 255
for i in range(0, len(drawingMatrix)):
    for j in range(0, len(drawingMatrix[0])):
        currentPos = drawingMatrix[i][j]
        # corners
        if currentPos[0:2] == 'TL': # top left
            if currentPos == 'TLO' or len(currentPos) == 2: # top left outer
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(5 + j * 20, 20 + i * 20), (5 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20)], 3)
            if currentPos == 'TLI' or len(currentPos) == 2: # top left inner
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(15 + j * 20, 20 + i * 20), (15 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
        if currentPos[0:2] == 'TR': # top right
            if currentPos == 'TRO' or len(currentPos) == 2: # top right outer
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(j * 20, 5 + i * 20), (15 + j * 20, 5 + i * 20), (15 + j * 20, 20 + i * 20)], 3)
            if currentPos == 'TRI' or len(currentPos) == 2: # top right inner
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(j * 20, 15 + i * 20), (5 + j * 20, 15 + i * 20), (5 + j * 20, 20 + i * 20)], 3)
        if currentPos[0:2] == 'BL': # bottom left
            if currentPos == 'BLO' or len(currentPos) == 2: # bottom left outer
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(5 + j * 20, i * 20), (5 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
            if currentPos == 'BLI' or len(currentPos) == 2: # bottom left inner
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(15 + j * 20, i * 20), (15 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20)], 3)
        if currentPos[0:2] == 'BR': # bottom right
            if currentPos == 'BRO' or len(currentPos) == 2: # bottom right outer
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(15 + j * 20, i * 20), (15 + j * 20, 15 + i * 20), (0 + j * 20, 15 + i * 20)], 3)
            if currentPos == 'BRI' or len(currentPos) == 2: # bottom right inner
                pygame.draw.lines(DISPLAYSURF, blueCol, False, [(5 + j * 20, i * 20), (5 + j * 20, 5 + i * 20), (j * 20, 5 + i * 20)], 3)
        # connecting lines
        if currentPos[0:2] == 'CH': # connecting horizontal
            if currentPos == 'CHT' or len(currentPos) == 2: # connecting horizontal top
                pygame.draw.line(DISPLAYSURF, blueCol, (0 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20), 3)
            if currentPos == 'CHB' or len(currentPos) == 2: # connecting horizonal bottom
                pygame.draw.line(DISPLAYSURF, blueCol, (0 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20), 3)
        if currentPos[0:2] == 'CV': # connecting vertical
            if currentPos == 'CVR' or len(currentPos) == 2: # connecting vertical right
                pygame.draw.line(DISPLAYSURF, blueCol, (15 + j * 20, 0 + i * 20), (15 + j * 20, 20 + i * 20), 3)
            if currentPos == 'CVL' or len(currentPos) == 2: # connecting vertical left
                pygame.draw.line(DISPLAYSURF, blueCol, (5 + j * 20, 0 + i * 20), (5 + j * 20, 20 + i * 20), 3)
        if currentPos == 'LO': # left open
            pygame.draw.lines(DISPLAYSURF, blueCol, False, [(0 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20),
                                                            (20 + j * 20, 15 + i * 20), (0 + j * 20, 15 + i * 20)], 3)
        if currentPos == 'RO': # right open
            pygame.draw.lines(DISPLAYSURF, blueCol, False, [(20 + j * 20, 5 + i * 20), (0 + j * 20, 5 + i * 20),
                                                            (0 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20)], 3)
        # ghost house entrance
        if currentPos == '8':
            pygame.draw.line(DISPLAYSURF, (255, 255, 255), (0 + j * 20, 10 + i * 20), (20 + j * 20, 10 + i * 20), 3)
        # short connecting lines at the teleport points
        if currentPos == 'SL': # short bottom
            pygame.draw.line(DISPLAYSURF, blueCol, (0 + j * 20, 15 + i * 20), (5 + j * 20, 15 + i * 20), 3)
            pygame.draw.line(DISPLAYSURF, blueCol, (0 + j * 20, 5 + i * 20), (5 + j * 20, 5 + i * 20), 3)
        if currentPos == 'SR':
            pygame.draw.line(DISPLAYSURF, blueCol, (15 + j * 20, 15 + i * 20), (20 + j * 20, 15 + i * 20), 3)
            pygame.draw.line(DISPLAYSURF, blueCol, (15 + j * 20, 5 + i * 20), (20 + j * 20, 5 + i * 20), 3)



# main game loop
while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            # deactivates the pygame library and terminate the program
            pygame.quit() 
            sys.exit()
        # draws the surface object DISPLAYSURF
        pygame.display.update()
