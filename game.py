import pygame
import time
import random

pygame.init()
HEIGHT = 565
WIDTH = 503
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("D00dle")
bg = pygame.image.load('sheet.jpg')
ddlR = pygame.image.load('doodle-r.png')
ddlL = pygame.image.load('doodle2.png')
gTale = pygame.image.load('green_tale1.png')
bTile = pygame.image.load('blue_tile.png')
enemy1 = pygame.image.load('enemy1.png')
no = pygame.image.load('nothing.png')
st = pygame.image.load('start.png')
ex = pygame.image.load('exit.png')
stg = pygame.image.load('startg.png')
exg = pygame.image.load('exitg.png')
clock = pygame.time.Clock()
tilesPictureArr = list()
tilesPictureArr.append(gTale)
tilesPictureArr.append(bTile)
tilesPictureArr.append(enemy1)
tilesPictureArr.append(no)

class Tile:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._dy = 0
        self._type = 0
        self._jumpCount = 0

    def setID(self, ID):
        self._ID = ID

    def setJumpCount(self, jumpCount):
        self._jumpCount = jumpCount

    def setDy(self, dy):
        self._dy = dy

    def motion(self):
        self._y += (((int(self._jumpCount)) * 0.9) ** 2) / 90
        self._jumpCount -= 1

    def getX(self):
        return self._x

    def getY(self):
        return self._y

class Blue_Tile(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        self._type = 1
        self._direction = random.choice([-1, 1])
        self._speed = 3

    def xMotion(self):
        newX = (self._x + self._speed * self._direction)
        if (newX > 426) or (newX < 0):
            self._direction *= -1
        self._x += self._speed * self._direction


class Enemy(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        self._type = 2
        self._xDirection = random.choice([-1, 1])
        self._yDirection = random.choice([-1, 1])
        self._xRange = 5
        self._yRange = 2
        self._xSpeed = 0.6
        self._ySpeed = 0.6

    def xMotion(self):

       if (self._xRange < 0) or (self._xRange > 12):
           self._xDirection *= -1
       self._x += self._xSpeed * self._xDirection
       self._xRange += self._xDirection

       if (self._yRange < 0) or (self._yRange > 7):
           self._yDirection *= -1
       self._y += self._ySpeed * self._yDirection
       self._yRange += self._yDirection

class Gm:
    def __init__(self, x, y, width, height, speed, image, exist, direction):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._speed = speed
        self._image = image
        self._exist = exist
        self._time0 = time.time()
        self._jumpCount = 40
        self._direction = direction
        self._bTileCount = random.uniform(0, 4)
        self._enemyCount = random.uniform(15, 20)
        self._isFalling = False
        self._score = 0

    def setLastTile(self, lastTile):
        self._lastTile = lastTile

    def setTalesArray(self, talesArray):
        self._talesArray = talesArray

    def getDirection(self):
        return self._direction

    def setDirection(self, direction):
        self._direction = direction

    def setPicture(self, image):
        self._image = image

    def GetExist(self):
        return self._exist

    def SetExist(self, exist):
        self._exist = exist

    def getFalling(self):
        return self._isFalling

    def setFalling(self, temp):
        self._isFalling = temp

    def notExist(self):
        self._exist = False

    def turnLeft(self):
        if (self._isFalling == False):
            self._x -= self._speed
            if (self._x < -30):
                self._x = 470

    def turnRight(self):
        if (self._isFalling == False):
            self._x += self._speed
            if (self._x > 470):
                self._x = -30

    def XfallingMotion(self):
        if (self._isFalling == True) and (self._direction):
            self._x -= self._speed
        else:
            if (self._isFalling == True) and not (self._direction):
                 self._x += self._speed
        if self._x > 470:
            self._x = -30
        if self._x < -30:
            self._x = 470

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def newTile(self):
        for tile in self._talesArray:
            if tile._ID == self._lastTile._ID:
                self._lastTile = tile
        if (self._lastTile._y - self._talesArray[-1]._y)**2 < 360000:
            x = random.uniform(1, 419)
            y = self._talesArray[-1]._y - random.uniform(40, 100)
            newTile = Tile(x, y)

            if self._enemyCount <= 0:
                newTile = Enemy(x, self._talesArray[-1]._y - random.uniform(80, 100))
                self._enemyCount = random.uniform(5, 7)
                self._bTileCount -= 1
            else:
                self._enemyCount -= 1
                if self._bTileCount <= 0:
                    newTile = Blue_Tile(x, y)
                    self._bTileCount = random.uniform(0, 15)
                    if self._talesArray[-1]._type == 2:
                        newTile._y = self._talesArray[-1]._y - random.uniform(35, 50)
                else:
                    self._bTileCount -= 1
            newTile.setID(self._talesArray[-1]._ID + 1)
            newTile.setDy(self._lastTile._dy)
            newTile.setJumpCount(self._talesArray[-1]._jumpCount)
            if (self._talesArray[-1]._type == 2):
                newTile._y = self._talesArray[-1]._y - random.uniform(30, 65)
            self._talesArray.append(newTile)

    def motion(self):

        for tile in self._talesArray:
            if (tile._type == 1) or (tile._type == 2) :
                tile.xMotion()

        if self._jumpCount > -81:
            if self._jumpCount < 0:
                for tile in self._talesArray:
                  if ((((self._x - tile._x) ** 2)  + (self._y - tile._y) ** 2) < 5000) and\
                          (tile._type == 2) and (self._y - tile._y > 1)and(self._isFalling == False):
                      self._isFalling = True
                      self._jumpCount = -2
                  if (tile._y - 75 < self._y) and (self._y < tile._y - 56)and\
                          (tile._x - self._width + 12 <  self._x) and\
                          (self._x < tile._x + 66) and (tile._type != 3) and (self._isFalling == False):
                      if (tile._ID == self._lastTile._ID) :
                          self._y = tile._y - self._height + 5
                          self._jumpCount = 40
                          pygame.display.update()
                          self._lastTile = tile
                          return 0
                      else:
                          self._y = tile._y - self._height + 5
                          self._jumpCount = 40
                          pygame.display.update()
                          for j in self._talesArray:
                              if j._ID == self._lastTile._ID:
                                  self._lastTile = j
                          dy = self._lastTile._y - tile._y

                          for i in self._talesArray:
                              i._jumpCount = 40
                              i._dy = dy
                          self._lastTile = tile

                          for k in self._talesArray:
                              if (k._ID == self._lastTile._ID)and(k._type == 2):
                                self._talesArray[self._talesArray.index(k)]._type = 3
                          return 0

                self._y += (((int(self._jumpCount))*0.9) ** 2) / 90.0
                if self._y > HEIGHT:
                    font = pygame.font.Font(None, 50)
                    text = font.render("Game over", True, (0, 0, 0))
                    win.blit(text, [170, 180])
                    pygame.display.update()

            else:
                for tile in self._talesArray:
                    if ((((self._x - tile._x)**2)  + (self._y - tile._y)**2 ) < 5000)\
                            and (tile._type == 2)and(self._isFalling == False):
                       self._isFalling = True
                       self._jumpCount = -2

                if (self._talesArray[-1]._jumpCount > 0) and (self._talesArray[-1]._dy > 0) and (self._isFalling == False):
                    self._y -=  (((int(self._jumpCount))*0.9) ** 2) / 90.0 - (((int(self._jumpCount))*0.9) ** 2) / 90 * self._talesArray[-1]._dy / 200.0
                    for tile in self._talesArray:
                         if tile._jumpCount > 0:
                            tile._y += (((int(tile._jumpCount)) * 0.9) ** 2) / 90.0 * tile._dy / 200.0
                            self._score += (((int(tile._jumpCount)) * 0.9) ** 2) / 90.0 * tile._dy / 200.0
                            tile._jumpCount -= 1
                else:
                    self._y -= (((int(self._jumpCount)) * 0.9) ** 2) / 90.0
            self._jumpCount -= 1
        else:
            self.SetExist(False)

def delUseless(tilesArray):
    lst = list()
    for tile in tilesArray:
        if tile._y > HEIGHT:
            lst.append(tilesArray.index(tile))
    lst.reverse()
    for i in lst:
        del tilesArray[i]

def drawWindow(object):

    win.blit(bg, (0, 0))
    for tile in objects:
        win.blit(tilesPictureArr[tile._type], (tile.getX(), tile.getY()))
    win.blit(ob1._image, (ob1.getX(), ob1.getY()))

    font = pygame.font.Font(None, 30)
    score = str(object._score // 10)
    if len(score) > 3:
        score = score[0:-2]
    text = font.render(score, True, (0, 0, 0))
    win.blit(text, [3, 3])

objects = list()
ob1 = Gm(95, 550, 75, 69, 8, ddlR, True, True)
tile1 = Tile(90, 450)
tile2 = Tile(250, 350)
tile3 = Tile(300, 250)
tile4 = Tile(100, 150)
tile1.setID(1)
tile2.setID(2)
tile3.setID(3)
tile4.setID(4)
ob1.setLastTile(tile1)
objects.append(tile1)
objects.append(tile2)
objects.append(tile3)
objects.append(tile4)

start = 0
enter = 0

while (True):

    pygame.time.delay(5)
    enter = 0
    ob1.setTalesArray(objects)
    ob1.motion()
    drawWindow(ob1)

    keys = pygame.key.get_pressed()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                start = 1
            elif i.key == pygame.K_DOWN:
                start = 0
            elif i.key == pygame.K_SPACE:
                enter = 1
    if start == 1:
        win.blit(st, (290, 100))
        win.blit(exg, (290, 300))
    else:
        win.blit(stg, (290, 100))
        win.blit(ex, (290, 300))
    if (start == 0) and (enter == 1):
        exit()
    if (start == 1) and (enter == 1):

        objects = list()
        ob1 = Gm(260, 495, 75, 69, 8, ddlR, True, True)  #
        tile1 = Tile(250, 500)
        tile2 = Tile(350, 410)
        tile3 = Tile(210, 300)
        tile4 = Tile(150, 145)
        tile1.setID(1)
        tile2.setID(2)
        tile3.setID(3)
        tile4.setID(4)
        ob1.setLastTile(tile1)
        objects.append(tile1)
        objects.append(tile2)
        objects.append(tile3)
        objects.append(tile4)

        while ob1.GetExist():

            clock.tick(500)

            pygame.time.delay(3)

            ob1.setTalesArray(objects)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ob1.notExist()
            keys = pygame.key.get_pressed()
            ob1.motion()
            ob1.newTile()
            delUseless(objects)
            ob1.XfallingMotion()
            if keys[pygame.K_LEFT]:
                if ob1.getDirection():
                    ob1.setPicture(ddlL)
                    ob1.setDirection(False)
                ob1.turnLeft()
            if keys[pygame.K_RIGHT]:
                if not ob1.getDirection():
                    ob1.setPicture(ddlR)
                    ob1.setDirection(True)
                ob1.turnRight()
            drawWindow(ob1)
            pygame.display.update()

        start = 0
    pygame.display.update()




