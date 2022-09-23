import pygame
import random
import os

#define colours
MISTRYROSE = (208, 217, 168)
RED = (215, 43, 43)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (247, 233, 197)
BROWN = (131,105,83)
LIGHTRED = (240,120,100)
GREEN = (140, 217, 168)

#setup maze constants
CELLWIDTH = 80 #width of cell

#set up pygame window
WIDTH = 800
HEIGHT = 800
FPS = 10

#initalise pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Falls")
FONTNAME = 'freesansbold.ttf'
clock = pygame.time.Clock()
pygame.display.update()

#set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, 'img')
playerImg = pygame.image.load(os.path.join(imgFolder, 'apple9.png')).convert()
enemyImg = pygame.image.load(os.path.join(imgFolder, 'snail.png')).convert()

#set up superclass sprite
class sprite:
  def __init__(self, x, y, spriteImg):
      pygame.sprite.Sprite.__init__(self)
      self.image = spriteImg
      self.image.set_colorkey((255, 255, 255))
      self.rect = self.image.get_rect()
      self.x = x
      self.y = y
      self.rect.center = (x, y)
      
#set up subclass Player to inherit from the superclass 'sprite'
class Player(sprite, pygame.sprite.Sprite):
  def __init__(self, x, y, spriteImg, availablePowerUps):
      sprite.__init__(self, x, y, spriteImg)
      spriteImg = playerImg
      self.collectedPelletsCoordinates = [] #stores the coordinates of the pellets that have been collected in a list
      self.availablePowerUps = availablePowerUps
      #self.numOfLives = 3
      self.score = 0
      
  def moveLeft(self, x, y): #move player sprite left
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,32,37), 0)
      self.rect.x -= CELLWIDTH
      self.x = self.rect.x
  
  def moveRight(self, x, y): #move player sprite right
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,32,37), 0)
      self.rect.x += CELLWIDTH
      self.x = self.rect.x
  
  def moveUp(self, x, y): #move player sprite upwards
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x ,self.rect.y,32,37), 0)
      self.rect.y -= CELLWIDTH
      self.y = self.rect.y
  
  def moveDown(self, x, y): #move player sprite downwards
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,32,37), 0)
      self.rect.y += CELLWIDTH
      self.y = self.rect.y

  def activatePowerUp(self):
      powerUpActivated = True
      return powerUpActivated

  def collectPellets(self, pelletX, pelletY):#collect Pellet and powerups
      powerUpActivated = False
      if (pelletX,pelletY) not in self.collectedPelletsCoordinates:
        self.collectedPelletsCoordinates.append((pelletX,pelletY))
      if (pelletX,pelletY) in  self.availablePowerUps:
        self.availablePowerUps.remove((pelletX,pelletY))
        powerUpActivated = self.activatePowerUp()
      return powerUpActivated
      
  def returnCollectedPellets(self):
      return self.collectedPelletsCoordinates

  def setCoordinates(self, x, y): #set the player sprite's coordinates
      self.x = x+(CELLWIDTH/2)
      self.y = y+(CELLWIDTH/2)

  def getCoordinates(self):#gets the coordinates of the cell the player is in
      return self.x-(CELLWIDTH/2), self.y-(CELLWIDTH/2)

  def alignPlayerToCell(self, x, y):
      self.x = x + 40
      self.rect.x = x + 20
      self.y = y + 40
      self.rect.y = y+20

  def calculateScore(self):
      player.score = 10 * len(self.returnCollectedPellets()) #each pellet is worth 10 points
      powerUpsUsed =  4 - len(self.availablePowerUps)#calculate how many pellets have been used
      player.score = player.score - (powerUpsUsed * 10)#subtract the powerups point from the pellets
      player.score = player.score + (powerUpsUsed * 30)#powerups are worth 30 points so add toscore
      return player.score

#set up subclass Enemy to inherit from the superclass 'sprite'
class Enemy(sprite, pygame.sprite.Sprite):
  def __init__(self, x, y, spriteImg):
      sprite.__init__(self, x, y, spriteImg)
      spriteImg = enemyImg
      self.prevCell = (x,y)
      self.startingPosition = (x, y)
      self.firstMovement = True

  def addPellets(self, x ,y): #draws pellets
      pygame.draw.circle(screen, BROWN, (x, y),7)

  def addPowerUp(self, x , y): #draws powerups
      pygame.draw.circle(screen, BLACK, (x, y),6)

  def moveLeft(self, xValue, drawPellets, drawPowerUp): #move enemy sprite left
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,77,70), 0)
      if drawPellets == True:
        self.addPellets(self.x, self.y)
      if drawPowerUp == True:
        self.addPowerUp(self.x, self.y)
      xValue -= CELLWIDTH
      self.rect.x  -= CELLWIDTH
      self.x = xValue+(CELLWIDTH/2)
  
  def moveRight(self, xValue, drawPellets, drawPowerUp): #move enemy sprite right
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,77,70), 0)
      if drawPellets == True:
        self.addPellets(self.x, self.y)
      if drawPowerUp == True:
        self.addPowerUp(self.x, self.y)
      xValue += CELLWIDTH
      self.rect.x  += CELLWIDTH
      self.x = xValue+(CELLWIDTH/2)
  
  def moveUp(self, yValue, drawPellets, drawPowerUp): #move enemy sprite upwards
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x ,self.rect.y,77,70), 0)
      if drawPellets == True:
        self.addPellets(self.x, self.y)
      if drawPowerUp == True:
        self.addPowerUp(self.x, self.y)
      yValue -= CELLWIDTH
      self.rect.y  -= CELLWIDTH
      self.y = yValue+(CELLWIDTH/2)
      
  def moveDown(self, yValue, drawPellets, drawPowerUp): #move enemy sprite downwards
      pygame.draw.rect(screen, MISTRYROSE, (self.rect.x,self.rect.y,77,70), 0)
      if drawPellets == True:
        self.addPellets(self.x, self.y)
      if drawPowerUp == True:
        self.addPowerUp(self.x, self.y)
      yValue += CELLWIDTH
      self.rect.y  += CELLWIDTH
      self.y = yValue+(CELLWIDTH/2)

  def getNextCell(self, direction, cellsAvailable):#returns coordinates of the cell the enemy is in
      nextCell = str(cellsAvailable[direction])
      if nextCell[4] == ',':
        nextCellX = nextCell[1:4]
        if len(nextCell) == 10:
          nextCellY = nextCell[6:9]
        else:
          nextCellY = nextCell[6:8]
      else:
        nextCellX = nextCell[1:3]
        if len(nextCell) == 10:
          nextCellY = nextCell[5:9]
        elif len(nextCell) == 9:
          nextCellY = nextCell[5:8]
        else:
          nextCellY = nextCell[5:7]
      return int(nextCellX), int(nextCellY)

  def getCoordinates(self):#gets the coordinates of the cell the player is in
      return self.x-40, self.y-40
      
  def enemyMovement(self, NeighbouringCells): #makes the enemy move randomly around the maze
      xValue = self.x-40 #the coordinates of the sprite is slighlt off from the cell's coordinates because the image of the sprite should be centered in the middle of the cell so xValue represents the cell that the sprite is in
      yValue = self.y-40
      for count in range(0, len(NeighbouringCells)):#get the sublist of neighbouring cells from the list cells
                if NeighbouringCells[count][0] == (xValue,yValue):
                  break
      cellsAvailable = NeighbouringCells[count]
      direction = random.randint(1,len(NeighbouringCells[count])-1)#choose a random neighbouring cell that is available
      if self.firstMovement == False: #if it is the first time the enemy is moving
        while NeighbouringCells[count][direction] == self.prevCell: #check the cell chosen is  not a cell that was just visited
          direction = random.randint(1,len(NeighbouringCells[count])-1)
        self.prevCell = (xValue, yValue)
      else:
        self.firstMovement = False #it is no longer the first time the enemy is moving
      nextCellX, nextCellY = self.getNextCell(direction, cellsAvailable)#get the coordinates of the cell chosen

      drawPellets = True
      drawPowerUp = False
      pellets = player.returnCollectedPellets()
      if (self.getCoordinates()) in pellets:
          drawPellets = False
      if (self.x-40, self.y-40) in player.availablePowerUps:
        drawPowerUp = True
        
      if nextCellX > xValue: #if the x coordinate of the neighbouring cell is larger then move right
        self.moveRight(xValue, drawPellets, drawPowerUp)
      elif nextCellX < xValue:
         self.moveLeft(xValue, drawPellets, drawPowerUp)
      elif nextCellY > yValue:
        self.moveDown(yValue, drawPellets, drawPowerUp)
      elif nextCellY < yValue:
        self.moveUp(yValue, drawPellets, drawPowerUp)
        
#set up sprites
player = Player(60,120, playerImg, [(340, 400), (20,800), (740,80), (740,800)])
enemy3 = Enemy(60,840, enemyImg)
enemy4 = Enemy(780,840, enemyImg)
allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(enemy3)
allSprites.add(enemy4)

#set up screen
class levelOne():
    #build the grid
    def __init__(self, numOfLives):
        self.numOfLives = numOfLives
        x = 0
        y = 0
        CELLWIDTH = 80
        grid = []
        self.NeighbouringCells = []
        pygame.init()
        size = [1000,1000]
        self.size = size
        self.screen = pygame.display.set_mode(size)
        screen.fill(YELLOW)
        for i in range(1, 11):
            x = 20
            y = y + 80
            for j in range(1, 11):
                grid.append((x,y))
                self.NeighbouringCells.append([(x,y)])
                pygame.draw.line(screen, WHITE, [x,y], [x + CELLWIDTH, y])
                pygame.draw.line(screen, WHITE, [x + CELLWIDTH, y], [x + CELLWIDTH, y + CELLWIDTH])
                pygame.draw.line(screen, WHITE, [x + CELLWIDTH, y + CELLWIDTH], [x, y + CELLWIDTH])
                pygame.draw.line(screen, WHITE, [x, y + CELLWIDTH], [x, y])
                x = x + 80
        x,y = 20,80
        self.recordNeighbouringCell(grid)
        self.clock = pygame.time.Clock()
        
    def pushUp(self,x, y):
        pygame.draw.rect(screen, MISTRYROSE, (x + 2, y - CELLWIDTH + 2, 78, 158), 0)
        self.addPellets(x,y)
        pygame.display.update()

    def pushDown(self,x, y):
        pygame.draw.rect(screen, MISTRYROSE, (x+2, y +2, 78, 158), 0)
        self.addPellets(x,y)
        pygame.display.update()

    def pushLeft(self,x, y):
        pygame.draw.rect(screen, MISTRYROSE, (x - CELLWIDTH + 2, y + 2, 158, 78), 0)
        self.addPellets(x,y)
        pygame.display.update()
    
    def pushRight(self,x, y):
        pygame.draw.rect(screen, MISTRYROSE, (x +2, y + 2, 158, 78), 0)
        self.addPellets(x,y)
        pygame.display.update()

    def backtrackingCell(self,x, y): #used to recolour path after single cell
        self.addPellets(x,y)
        pygame.display.update()

    def goDown(self,x,y, push): #overrwrite the coordinates if the program goes down
        if push == True:
          self.pushDown(x,y)
        y =y + CELLWIDTH
        return x, y
        
    def goUp(self,x,y, push):#overrwrite the coordinates if the program goes up
        if push == True:
          self.pushUp(x,y)
        y = y - CELLWIDTH
        return x, y

    def goRight(self,x,y, push):#overrwrite the coordinates if the program goes right
        if push == True:
          self.pushRight(x,y)
        x = x + CELLWIDTH
        return x, y

    def goLeft(self,x,y, push):#overrwrite the coordinates if the program goes left
        if push == True:
          self.pushLeft(x,y)
        x = x - CELLWIDTH
        return x, y

    def recordNeighbouringCell(self, grid): #records the neighbouring cells
      self.carveOutMaze(20, 80, grid)
      for count in range(0, len(self.NeighbouringCells)):
        for i in range(0, len(self.NeighbouringCells)):
            if self.NeighbouringCells[i][0] in self.NeighbouringCells[count] and count != i:
              if self.NeighbouringCells[count][0] not in self.NeighbouringCells[i]:
                self.NeighbouringCells[i].append(self.NeighbouringCells[count][0])
      self.addPowerUps()

    def moveToNeighbouringCell(self, directionAvailable, x, y): #chooses an available neighbourimg cell to move to and draws it into the grid
      push = True
      cellChosen = (random.choice(directionAvailable))#choose a random direction
      if cellChosen == 'right':
            x,y = self.goRight(x,y, push)

      elif cellChosen == 'left':
            x,y = self.goLeft(x,y, push)
                
      elif cellChosen == "down":
            x,y = self.goDown(x,y, push)

      elif cellChosen == "up":
            x,y = self.goUp(x,y, push)
      return x,y

    def moveThroughDeadend(self, visited,  lastVisited, x, y, grid): #overwrites deadend by pushing into another neighbouring cell
        push = True
        if (x , y - CELLWIDTH) == lastVisited[-2]: #if prev cell is above current cell
            if (x, y + CELLWIDTH) in grid: #and the cell below the current cell is in the grid
              x1,y1 = self.goDown(x,y, push)#overwrite the cell downwards
            elif (x + CELLWIDTH, y) in grid:
              x1,y1 = self.goRight(x,y, push)
            else:
              x1,y1 = self.goLeft(x,y, push)

        elif (x , y + CELLWIDTH) == lastVisited[-2]: #if prev cell is below current cell
            if (x, y - CELLWIDTH) in grid:
               x1,y1 = self.goUp(x,y, push)
            elif (x + CELLWIDTH, y) in grid:
              x1,y1 = self.goRight(x,y, push)
            else:
              x1,y1 = self.goLeft(x,y, push)

        elif (x + CELLWIDTH, y) == lastVisited[-2]: #if prev cell is to the right current cell
            if (x - CELLWIDTH, y) in grid:
              x1,y1 = self.goLeft(x,y, push)
            elif (x, y + CELLWIDTH) in grid:
              x1,y1 = self.goDown(x,y, push)
            else:
              x1,y1 = self.goUp(x,y, push)

        elif(x - CELLWIDTH, y) == lastVisited[-2]: #if prev cell is to the left current cell
            if (x + CELLWIDTH, y) in grid:
              x1,y1 = self.goRight(x,y, push)
            elif (x, y + CELLWIDTH) in grid:
              x1,y1 = self.goDown(x,y, push)
            else:
              x1,y1 = self.goUp(x,y, push)

        self.addPellets(x1,y1)#add pellet into dead end
        return x1, y1 #return coordinates of dead end

    def removeDeadendsAtTheStart(self):#removes any dead ends at the start 
        if len(self.NeighbouringCells[0]) == 2:
            x1,y1 = self.goUp(20,160, True)
            x1,y1 = self.goRight(20, 80, True)
            self.addPellets(100,80)
            if (20, 160) not in self.NeighbouringCells[0]:
              self.NeighbouringCells[0].append((20, 160))
            else:
              self.NeighbouringCells[0].append((100, 80))

    def addPellets(self, x ,y): #draws pellets
        pygame.draw.circle(screen, BROWN, (x+40, y+40),7)

    def addPowerUps(self): #draws powerups
        pygame.draw.circle(screen, BLACK, (380, 440),9) 
        pygame.draw.circle(screen, BLACK, (60, 840),9)
        pygame.draw.circle(screen, BLACK, (780, 120),9)
        pygame.draw.circle(screen, BLACK, (780, 840),9)
        pygame.display.update()
        
    def carveOutMaze(self,x ,y, grid):
        visited = []
        stack = []
        lastVisited = []
        push = True
        stack.append((x,y))
        visited.append((x,y))
        lastVisited.append((x,y))
        while len(stack) > 0:
            for count in range(0, len(self.NeighbouringCells)): # find coordinate of cell in list
                if self.NeighbouringCells[count][0] == (x,y):
                  index = count
                  break
                
            directionAvailable = []
            if (x + CELLWIDTH, y) not in visited and (x + CELLWIDTH, y) in grid:
                directionAvailable.append('right')
            if (x - CELLWIDTH, y) not in visited and (x - CELLWIDTH, y) in grid:
                directionAvailable.append('left')
            if (x , y + CELLWIDTH) not in visited and (x, y + CELLWIDTH) in grid:
                directionAvailable.append('down')
            if (x , y - CELLWIDTH) not in visited and (x, y - CELLWIDTH) in grid:
                directionAvailable.append('up')

            if len(directionAvailable) > 0:
                #if there are cells to move to then move to one of the neighbouring cells
                x,y = self.moveToNeighbouringCell(directionAvailable, x, y)
                #update the lists and stacks containing the cells
                visited.append((x, y))
                stack.append((x, y))
                lastVisited.append((x,y))
                self.NeighbouringCells[index].append((x,y))
                
            elif len(directionAvailable) == 0:
                if (x,y) == visited[-1]:
                    x1, y1 = self.moveThroughDeadend(visited,  lastVisited, x, y, grid)#overwrite dead end
                    lastVisited.append((x1, y1))
                    if (x1, y1) not in self.NeighbouringCells[index]:
                       self.NeighbouringCells[index].append((x1, y1))
                     
                x,y = stack.pop() #if no cells are avialable to pop from the stack
                self.backtrackingCell(x, y)
                lastVisited.append((x,y))
            self.removeDeadendsAtTheStart() #remove any deadends at the starting position

    def movePlayer(self): #move player based on what key is presses
      push = False
      powerUpActivated = False
      keys = pygame.key.get_pressed()
      xValue, yValue = player.getCoordinates()# get player coordinates
      for count in range(0, len(self.NeighbouringCells)):#get the sublist of neighbouring cells from the list cells
                if self.NeighbouringCells[count][0] == (xValue,yValue):
                  break     
      if keys[pygame.K_w]: #if player wants to move up
            newX, newY = self.goUp(xValue, yValue, push) #find the coordinates of the cell above the current cell
            if (newX, newY) in self.NeighbouringCells[count]: #if the cell above is one of the availble cells             
              player.moveUp(xValue, yValue)#movethe player sprite up to the cell above
              player.setCoordinates(newX, newY)#set the players new coordinates
              powerUpActivated = player.collectPellets(newX, newY)
      elif keys[pygame.K_s]: #if player wants to move down
            newX, newY = self.goDown(xValue, yValue, push)
            if (newX, newY) in self.NeighbouringCells[count]:
              player.moveDown(xValue, yValue)
              player.setCoordinates(newX, newY)#set the players new coordinates
              powerUpActivated =player.collectPellets(newX, newY)
      elif keys[pygame.K_a]: #if player wants to move left
            newX, newY = self.goLeft(xValue, yValue, push)
            if (newX, newY) in self.NeighbouringCells[count]:
              player.moveLeft(xValue, yValue)
              player.setCoordinates(newX, newY)#set the players new coordinates
              powerUpActivated =player.collectPellets(newX, newY)
      elif keys[pygame.K_d]: #if player wants to move right
            newX, newY = self.goRight(xValue, yValue, push)
            if (newX, newY) in self.NeighbouringCells[count]:
              player.moveRight(xValue, yValue)
              player.setCoordinates(newX, newY)#set the players new coordinates
              powerUpActivated =player.collectPellets(newX, newY)
      return powerUpActivated

    def displayLifeLost(self): #shows game over when the player and enemy meet
      pygame.init()
      font = pygame.font.Font(FONTNAME, 30)
      textSurface = font.render('YOU HAVE LOST A LIFE', True, RED)
      textRect = textSurface.get_rect()
      textRect.center = (WIDTH // 2, 20)
      screen.blit(textSurface, textRect)
      pygame.display.update()
      pygame.time.wait(3000)
      pygame.draw.rect(screen, YELLOW, (180, 5, WIDTH // 2, 30), 0)
      pygame.display.update()

    def displayGameOver(self): #shows game over when the player and enemy meet
      pygame.init()
      font = pygame.font.Font(FONTNAME, 30)
      textSurface = font.render('GAME OVER', True, RED)
      textRect = textSurface.get_rect()
      textRect.center = (WIDTH // 2, 20)
      screen.blit(textSurface, textRect)
      pygame.display.update()
      pygame.time.wait(3000)

    def displayYouWon(self): #shows you won when all the pellets are collected
      pygame.init()
      font = pygame.font.Font(FONTNAME, 30)
      textSurface = font.render('YOU WON', True, RED)
      textRect = textSurface.get_rect()
      textRect.center = (WIDTH // 2, 20)
      screen.blit(textSurface, textRect)
      pygame.display.update()
      pygame.time.wait(3000)

    def displayLives(self):
      pygame.draw.rect(screen, YELLOW, (890,290,50,40), 0)
      font = pygame.font.Font(FONTNAME, 25)
      text = font.render('Lives left:',True, LIGHTRED)
      screen.blit(text, [845, 240])
      if self.numOfLives == 1:
          text = font.render('1',True, LIGHTRED)
      elif self.numOfLives == 2:
          text = font.render('2',True, LIGHTRED)
      elif self.numOfLives == 3:
          text = font.render('3',True, LIGHTRED)
      else:
          text = font.render('0',True, LIGHTRED)
      screen.blit(text, [890, 290])
      pygame.display.update()

    def displayLevelNumber(self):
      font = pygame.font.Font(FONTNAME, 25)
      text = font.render('Level 1',True, LIGHTRED)
      screen.blit(text, [860, 140])
      pygame.display.update()

    def displayPowerUpIsActivated(self):
      font = pygame.font.Font(FONTNAME, 30)
      textSurface = font.render('POWERUP ACTIVATED', True, RED)
      textRect = textSurface.get_rect()
      textRect.center = (WIDTH // 2, 20)
      screen.blit(textSurface, textRect)
      pygame.display.update()

    def deActivatePowerUp(self):
      pygame.draw.rect(screen, YELLOW, (180, 5, WIDTH // 2, 30), 0)

    def mainLoop(self):# Game Loop
      timeTaken = 0
      powerUpActivated = False
      self.done = False
      push = False
      player.collectPellets(20, 80)
      self.displayLevelNumber()
      self.displayLives()
      while not self.done:
        dt = clock.tick(FPS) / 1000
        timeTaken = timeTaken + dt
        allSprites.draw(screen)
        # Player movement
        powerUpActivated = self.movePlayer() 

        #Enemy movement
        if timeTaken > 0.5 and powerUpActivated == False:  # Allows enemy to move once every 0.3 seconds as long as as a powerup is not activated
          timeTaken = 0          #resets time
          #Enemy movement
          enemy3.enemyMovement(self.NeighbouringCells)
          enemy4.enemyMovement(self.NeighbouringCells)
          self.deActivatePowerUp()
          
        elif powerUpActivated == True: #if a powerup is activated
          timeTaken = -2.5 #3 seconds have to pass for the time to get more than 0.3 for the enemies to move
          self.displayPowerUpIsActivated()
          powerUpActivated = False #powerup has finished activating

        allSprites.draw(screen) #redraw sprites in new positions

        #if the player has collected all the pellets then 'You won' screen
        if len(player.returnCollectedPellets()) == 100:
          self.deActivatePowerUp()
          self.displayYouWon()
          self.done = True

        elif  player.getCoordinates() == enemy3.getCoordinates() or player.getCoordinates() == enemy4.getCoordinates():
          self.numOfLives -= 1
          self.deActivatePowerUp()
          self.displayLives()
          if self.numOfLives == 0:
            self.displayGameOver()
            self.done = True
          else:
            player.alignPlayerToCell(20,80)
            self.displayLifeLost()
        
        pygame.display.flip()
        
        #Redraw Screen
        allSprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            score = player.calculateScore()
            return score, -1

      
      score = player.calculateScore()
      return score, self.numOfLives


