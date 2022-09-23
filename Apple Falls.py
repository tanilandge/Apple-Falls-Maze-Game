import pygame
import time
import random
import os
import csv
import sys
from level1 import sprite, Player, Enemy, levelOne  # import level 1
from level2 import sprite, Player, Enemy, levelTwo  # import level 2
from level3 import sprite, Player, Enemy, levelThree  # import level 3

# define colours
MISTRYROSE = (208, 217, 168)
RED = (215, 43, 43)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (247, 233, 197)
BROWN = (131, 105, 83)
LIGHTRED = (240, 120, 100)
GREEN = (140, 217, 168)

# setup maze constants
CELLWIDTH = 40  # width of cell

# set up pygame window
WIDTH = 800
HEIGHT = 800
FPS = 11

# initalise pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(YELLOW)
pygame.display.set_caption("Apple Falls")
FONTNAME = 'freesansbold.ttf'
clock = pygame.time.Clock()
pygame.display.update()

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, 'img')
playerImg = pygame.image.load(os.path.join(imgFolder, 'apple9.png')).convert()
enemyImg = pygame.image.load(os.path.join(imgFolder, 'snail2.png')).convert()


class GameScreen():  # create game settings
    def __init__(self, level):
        self.page = 1
        self.userType = ''
        self.playerName = ''
        self.level = level
        self.playerLives = 3

    def drawMenu(self):  # enter player name
        font = pygame.font.Font(FONTNAME, 40)
        textSurface = font.render('Apple Falls', True, LIGHTRED)
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH // 2, 50)
        screen.blit(textSurface, textRect)
        font = pygame.font.Font(FONTNAME, 25)
        text = font.render('Click on the box to type player name:', True, LIGHTRED)
        screen.blit(text, [100, 140])
        text = font.render('Press enter when you are done', True, LIGHTRED)
        screen.blit(text, [100, 240])

    def displayInstructions(self):  # display Instructions
        pygame.init()
        screen.fill(YELLOW)
        font = pygame.font.Font(FONTNAME, 30)
        text = font.render("Instructions:", True, LIGHTRED)
        screen.blit(text, [10, 90])
        font = pygame.font.Font(FONTNAME, 20)
        text = font.render("Collect the all pellets in the mazes to win the game!", True, LIGHTRED)
        screen.blit(text, [10, 140])
        text = font.render("Use the 'w', 's', 'd', 'a' keys to move up, down, right, left respectively", True, LIGHTRED)
        screen.blit(text, [10, 190])
        text = font.render("You have 3 lives", True, LIGHTRED)
        screen.blit(text, [10, 240])
        text = font.render("Avoid the snails or else you lose a life", True, LIGHTRED)
        screen.blit(text, [10, 290])
        text = font.render("Use powerups to help you", True, LIGHTRED)
        screen.blit(text, [10, 340])
        text = font.render("Powerups freeze the snails for 3 seconds", True, LIGHTRED)
        screen.blit(text, [10, 390])
        text = font.render("There are three levels to complete", True, LIGHTRED)
        screen.blit(text, [10, 440])
        text = font.render("Press Enter to begin", True, LIGHTRED)
        screen.blit(text, [10, 490])
        pygame.display.update()
        self.moveToNextScreen()
        self.page += 1

    def moveToNextScreen(self):  # check if user has pressed enter to move to next screen
        done = False
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                elif event.type == pygame.QUIT:
                    self.page = 7
                    done = True

    def playerNameLengthErrorMessage(self):  # error message when the user types a name that is too long
        font2 = pygame.font.Font(FONTNAME, 30)
        error = font2.render('Player name is too long', True, RED)
        screen.blit(error, (250, 340))
        error = font2.render('Please choose a shorter name', True, RED)
        screen.blit(error, (200, 390))

    def wrongReturningPlayerNameErrorMessage(self):  # error message when a returning user types a name that is new
        font2 = pygame.font.Font(FONTNAME, 25)
        error = font2.render("That is a new player name and not a returning player's name", True, RED)
        screen.blit(error, (30, 340))
        error = font2.render('Press Enter to try again', True, RED)
        screen.blit(error, (250, 390))
        pygame.display.update()
        self.moveToNextScreen()

    def wrongNewPlayerNameErrorMessage(self):  # error message when a new user types a name that is already taken
        font2 = pygame.font.Font(FONTNAME, 25)
        error = font2.render("That name has already been taken, use a different name", True, RED)
        screen.blit(error, (30, 340))
        error = font2.render('Press Enter to try again', True, RED)
        screen.blit(error, (250, 390))
        pygame.display.update()
        self.moveToNextScreen()

    def blankNewPlayerNameErrorMessage(self):  # error message when the user presses enter without writing a name
        font2 = pygame.font.Font(FONTNAME, 25)
        error = font2.render("You have not entered a name, please enter a name", True, RED)
        screen.blit(error, (80, 340))
        error = font2.render('Press Enter to try again', True, RED)
        screen.blit(error, (250, 390))
        pygame.display.update()
        self.moveToNextScreen()

    def checkPlayerNameIsValid(self):  # checks that the player name is valid
        self.checkHighScoresFileExists()
        playerNameIsValid = True
        fastestTimeFile2 = open('highscores.csv', 'rt')
        playerNames, playerScores = self.getHighScoresFile()
        if self.userType == 'R':
            if self.playerName == '':
                playerNameIsValid = False
                self.blankNewPlayerNameErrorMessage()
            elif self.playerName not in playerNames:
                playerNameIsValid = False
                self.wrongReturningPlayerNameErrorMessage()
        else:
            if self.playerName in playerNames:
                playerNameIsValid = False
                self.wrongNewPlayerNameErrorMessage()
            elif self.playerName == '':
                playerNameIsValid = False
                self.blankNewPlayerNameErrorMessage()
        return playerNameIsValid

    def inputPlayerName(self):  # makes the input box for where the player inputs their name
        font = pygame.font.Font(FONTNAME, 30)
        inputBox = pygame.Rect(100, 185, 140, 32)
        boxInactiveColour = pygame.Color(LIGHTRED)
        boxActiveColour = pygame.Color(RED)
        colour = boxInactiveColour
        text = ''
        currentlyWriting = False
        removeName = False
        self.drawMenu()

        done = False
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.page = 6
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:  # if user clicked
                    if inputBox.collidepoint(event.pos):  # if the box was clicked
                        currentlyWriting = True  # user wants to write
                        colour = boxActiveColour
                    else:  # user clicked the mouse but away from the box
                        currentlyWriting = False  # user is not currently trying to write
                        # Change the current colour of the input box to show it has been clicked on
                        colour = boxInactiveColour

                # if user is trying to write and a key has been pressed
                if event.type == pygame.KEYDOWN:
                    if currentlyWriting == True and removeName == False:
                        if event.key == pygame.K_RETURN:
                            self.playerName = text
                            playerNameIsValid = self.checkPlayerNameIsValid()
                            if playerNameIsValid == False:
                                self.page = self.page - 1
                            elif playerNameIsValid == True:
                                self.page = 3
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                    elif removeName == True:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]

            screen.fill(YELLOW)
            if inputBox.w > 400:
                self.playerNameLengthErrorMessage()
                removeName = True
            else:
                removeName = False
            # Render the current text.
            txt_surface = font.render(text, True, colour)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)  # max(200, txt_surface.get_width()+10)
            inputBox.w = width
            # Blit the text and the inputBox rect.
            pygame.draw.rect(screen, MISTRYROSE, (inputBox.x, inputBox.y, inputBox.w, 32))
            screen.blit(txt_surface, (inputBox.x + 5, inputBox.y + 5))
            pygame.draw.rect(screen, colour, inputBox, 2)

            self.drawMenu()
            pygame.display.flip()

    def checkToStartGameAgain(self):  # check if user wants to start game again after finishing or quit
        pygame.init()
        done = False
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.page = 0
                        done = True
                    elif event.key == pygame.K_x:
                        self.page = 6
                        done = True

    def checkHighScoresFileExists(self):  # make sure a file of highscores exists otherwise make a new highscores file
        try:
            file2 = open('highscores.csv', 'rt')
        except:
            file2 = open('highscores.csv', 'wt')

    def getHighScoresFile(self):  # get the contents of the highscores file
        file2 = open('highscores.csv', 'rt')
        contents = []
        for item in file2:
            contents.append(item.strip())
        file2.close()
        playerNames = []
        playerScores = []
        orderedPlayerScores = []
        orderedPlayerNames = []
        for i in range(0, len(contents)):
            name1 = contents[i]
            for count in range(0, len(name1)):
                if name1[count] == ',':
                    name2 = str(name1[0:count])
                    playerNames.append(name2)
                    score = str(name1[count + 1:len(name1)])
                    playerScores.append(int(score))
                    orderedPlayerScores.append(int(score))
                    break
        orderedPlayerScores.sort()
        for count in range(0, len(playerScores)):
            position = playerScores.index(orderedPlayerScores[count])
            orderedPlayerNames.append(playerNames[position])
        return orderedPlayerNames, orderedPlayerScores

    def displayNewHighScore(self, mins, sec, score):  # if theres a highscore display the highscore
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(YELLOW)
        inputBox = pygame.Rect(220, 120, 350, 80)
        pygame.draw.rect(screen, LIGHTRED, (inputBox.x + 5, inputBox.y + 5, inputBox.w + 5, 80))
        pygame.draw.rect(screen, MISTRYROSE, (inputBox.x, inputBox.y, inputBox.w, 80))
        font = pygame.font.Font(FONTNAME, 40)
        textSurface = font.render('Apple Falls', True, LIGHTRED)
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH // 2, 50)
        screen.blit(textSurface, textRect)
        font = pygame.font.Font(FONTNAME, 40)
        text = font.render('New High Score!', True, LIGHTRED)
        screen.blit(text, [240, 140])
        font = pygame.font.Font(FONTNAME, 70)
        text = font.render(str(score), True, LIGHTRED)
        screen.blit(text, [330, 290])
        font = pygame.font.Font(FONTNAME, 30)
        time = "Time Lapsed = {0}:{1}".format(int(mins), int(sec))
        text = font.render(str(time), True, LIGHTRED)
        screen.blit(text, [260, 440])
        font2 = pygame.font.Font(FONTNAME, 30)
        message = font2.render("Press Enter to start again or 'X' to quit", True, LIGHTRED)
        screen.blit(message, (130, 540))
        pygame.display.update()
        self.checkToStartGameAgain()

    def displayScore(self, mins, sec, score):  # display final score
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(YELLOW)
        inputBox = pygame.Rect(250, 205, 300, 80)
        pygame.draw.rect(screen, MISTRYROSE, (inputBox.x, inputBox.y, inputBox.w, 70))
        font = pygame.font.Font(FONTNAME, 40)
        textSurface = font.render('Apple Falls', True, LIGHTRED)
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH // 2, 50)
        screen.blit(textSurface, textRect)
        font = pygame.font.Font(FONTNAME, 40)
        text = font.render('Your Score is:', True, LIGHTRED)
        screen.blit(text, [260, 220])
        font = pygame.font.Font(FONTNAME, 70)
        text = font.render(str(score), True, LIGHTRED)
        screen.blit(text, [330, 290])
        font = pygame.font.Font(FONTNAME, 30)
        time = "Time Lapsed = {0}:{1}".format(int(mins), int(sec))
        text = font.render(str(time), True, LIGHTRED)
        screen.blit(text, [260, 440])
        font2 = pygame.font.Font(FONTNAME, 30)
        message = font2.render("Press Enter to start again or 'X' to quit", True, LIGHTRED)
        screen.blit(message, (130, 540))
        pygame.display.update()
        self.checkToStartGameAgain()

    def recordScore(self, score):  # record the players score
        newHighScore = False
        playerNames, playerScores = self.getHighScoresFile()
        if self.userType == 'R':
            position = playerNames.index(self.playerName)
            if score > playerScores[position]:
                playerNames.pop(position)
                playerScores.pop(position)
                newHighScore = True
            else:
                return score, newHighScore
        playerScores.append(score)
        playerScores.sort()
        position = playerScores.index(score)
        playerNames.insert(position, self.playerName)

        file1 = open('highscores.csv', 'wt')
        for count in range(0, len(playerScores)):
            file1.write(playerNames[count] + ',' + str(playerScores[count]) + '\n')
        file1.close()
        return score, newHighScore

    def checkUserInput(self):  # make sure the user chooses an option
        pygame.init()
        done = False
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.page = 6
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.userType = 'R'
                        self.page = 2
                        done = True
                    elif event.key == pygame.K_n:
                        self.userType = 'N'
                        self.page = 2
                        done = True
                    else:
                        font2 = pygame.font.Font(FONTNAME, 30)
                        error = font2.render("Please press either 'N' or 'R'", True, RED)
                        screen.blit(error, (170, 340))
                        pygame.display.update()

    def checkIfReturningUser(self):  # check if it is a new player or new player
        screen.fill(YELLOW)
        font = pygame.font.Font(FONTNAME, 40)
        textSurface = font.render('Apple Falls', True, LIGHTRED)
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH // 2, 50)
        screen.blit(textSurface, textRect)
        font = pygame.font.Font(FONTNAME, 25)
        text = font.render('Are you a new player or returning player?', True, LIGHTRED)
        screen.blit(text, [100, 140])
        text = font.render('Press "N" for new player or "R" for returning player', True, LIGHTRED)
        screen.blit(text, [100, 190])
        pygame.display.update()
        self.checkUserInput()

    def displayLevel1Maze(self):  # display the level one maze
        maze = levelOne(self.playerLives)
        score, livesLeft = maze.mainLoop()
        return score, livesLeft

    def displayLevel2Maze(self):  # display the level two maze
        maze = levelTwo(self.playerLives)
        score, livesLeft = maze.mainLoop()
        return score, livesLeft

    def displayLevel3Maze(self):  # display the level three maze
        maze = levelThree(self.playerLives)
        score, livesLeft = maze.mainLoop()
        return score, livesLeft

    def movingToNextLevel(self):  # display the 'next level' message
        screen.fill(YELLOW)
        font = pygame.font.Font(FONTNAME, 40)
        textSurface = font.render('Apple Falls', True, LIGHTRED)
        screen.blit(textSurface, [400, 50])
        font = pygame.font.Font(FONTNAME, 25)
        text = font.render('Well Done! You have completed this level', True, LIGHTRED)
        screen.blit(text, [250, 140])
        text = font.render('Press Enter to start the next level', True, LIGHTRED)
        screen.blit(text, [250, 190])
        pygame.display.update()
        self.moveToNextScreen()

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        return mins, sec
        # print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),int(sec)))

    def main(self):  # main
        totalScore = 0
        done = False
        while not done:
            if self.page == 0:
                return done
            elif self.page == 1:
                self.checkIfReturningUser()
            elif self.page == 2:
                self.inputPlayerName()
            elif self.page == 3:
                self.displayInstructions()
                start_time = time.time()
            elif self.page == 4:
                if self.level == 1:
                    score, livesLeft = self.displayLevel1Maze()
                    self.playerLives = livesLeft
                    if self.playerLives > 0:
                        self.level += 1
                        totalScore += score
                        self.movingToNextLevel()
                    elif self.playerLives == -1:
                        self.page = 7
                    else:
                        totalScore += score
                        self.page += 1
                elif self.level == 2:
                    score, livesLeft = self.displayLevel2Maze()
                    self.playerLives = livesLeft
                    if self.playerLives > 0:
                        self.level += 1
                        totalScore += score
                        self.movingToNextLevel()
                    elif self.playerLives == -1:
                        self.page = 7
                    else:
                        totalScore += score
                        self.page += 1
                elif self.level == 3:
                    score, livesLeft = self.displayLevel3Maze()
                    self.playerLives = livesLeft
                    totalScore += score
                    if self.playerLives == -1:
                        self.page = 7
                    else:
                        self.page += 1
            elif self.page == 5:
                end_time = time.time()
                time_lapsed = end_time - start_time
                mins, sec = self.time_convert(time_lapsed)
                # print("Time Lapsed = {0}:{1}".format(int(mins),int(sec)))
                score, newHighScore = self.recordScore(totalScore)
                if newHighScore == True:
                    self.displayNewHighScore(mins, sec, score)
                else:
                    self.displayScore(mins, sec, score)
            else:
                done = True
                return done


done = False
level = 1  # start with level 1
while done == False:
    del sys.modules['level1']  # delete the imported levels
    del sys.modules['level2']
    del sys.modules['level3']
    from level1 import sprite, Player, Enemy, levelOne # import again so that the data from the previous time this level was run is not being used agaim
    from level2 import sprite, Player, Enemy, levelTwo
    from level3 import sprite, Player, Enemy, levelThree

    gameScreen = GameScreen(level)  # make the game screen class
    done = gameScreen.main()  # if the user quits the game screen then the game quit
pygame.quit()
