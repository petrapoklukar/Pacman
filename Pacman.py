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


# drawing the menu on the right-hand side
def menuButtons():
    # drawing the menu
    pygame.draw.rect(displaySurface, (204,204,0), (565, 5, 755, 610))

    # Lives and Score text
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    scoreSurfaceObj = fontObj.render('Score', True, (0, 0, 255))
    scoreRectObj = scoreSurfaceObj.get_rect()
    scoreRectObj.center = (660, 50)
    displaySurface.blit(scoreSurfaceObj, scoreRectObj)

    livesSurfaceObj = fontObj.render('Lives', True, (0, 0, 255))
    livesRectObj = livesSurfaceObj.get_rect()
    livesRectObj.center = (660, 160)
    displaySurface.blit(livesSurfaceObj, livesRectObj)

    # lives images
    livesImage = pygame.image.load('Pacman.png')
    livesImage = pygame.transform.scale(livesImage, (50, 50))
    displaySurface.blit(livesImage, (600, 180))
    displaySurface.blit(livesImage, (640, 180))
    displaySurface.blit(livesImage, (680, 180))

    # TODO:
    # - add buttons and their functionality
    # - add actual score number


# Main loop
# def main():
pygame.init()
displaySurface = pygame.display.set_mode((760, 620))
pygame.display.set_caption('Pacman')

# Drawing functions
drawWalls()
menuButtons()


clock = pygame.time.Clock()
fps = 60

button = pygame.Rect(100, 100, 50, 50)
# creates a rect object
# The rect method is similar to a list but with a few added perks
# for example if you want the position of the button you can simpy type
# button.x or button.y or if you want size you can type button.width or
# height. you can also get the top, left, right and bottom of an object
# with button.right, left, top, and bottom

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            # deactivates the pygame library and terminate the program
            pygame.quit() 
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() # gets mouse position
            print(mouse_pos)

            # checks if mouse position is over the button
            # note this method is constantly looking for collisions
            # the only reason you dont see an evet activated when you
            #hover over the button is because the method is bellow the
            # mousedown event if it were outside it would be called the
            # the moment the mouse hovers over the button

            if button.collidepoint(mouse_pos):
                # pritns current location of mouse
                print('button was pressed at {0}'.format(mouse_pos))

    pygame.display.update()
    clock.tick(fps)
