import pygame
import math
import random

BLACK     = (  0,  0,  0)
WHITE     = (255,255,255)
GREEN     = (  0,255,  0)
RED       = (255,  0,  0)
BROWN     = (160,82,45)
LIGHTBLUE = (173,216,230)
ORANGE    = (255,165,0)
nice =(10,10,50)

pygame.init()

size = (1920, 1080)
mid = (size[0]/2,size[1]/2)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Doom Engine')
done = False
clock = pygame.time.Clock()

speed = 1
turnSpeed = 0.05

game = True

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Player(object):

    def __init__(self):
        self.position = Point(0, 0)
        self.angle = 0
        self.collision = False
    def Update(self):
        self.MovePlayer()
        ##self.point4rawPlayer()
    def point4rawPlayer(self):
        pygame.draw.line(screen,WHITE,(mid[0],mid[1]),(mid[0],mid[1]+20))
    def MovePlayer(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= turnSpeed
        if keys[pygame.K_RIGHT]:
            self.angle += turnSpeed
        if self.collision == False:
            if keys[pygame.K_UP]:
                self.position.x += math.cos(self.angle) * speed
                self.position.y += math.sin(self.angle) * speed
            if keys[pygame.K_DOWN]:
                self.position.x -= math.cos(self.angle) * speed
                self.position.y -= math.sin(self.angle) * speed
        self.collision = False


    def ProjectedPosition(self):
        newX,newY = 0,0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            newX = self.position.x + math.cos(self.angle) * 5
            newY = self.position.y + math.sin(self.angle) * 5
        if keys[pygame.K_DOWN]:
            newX = self.position.x - math.cos(self.angle) * 5
            newY = self.position.y - math.sin(self.angle) * 5
        return Point(newX,newY)


class Wall(object):
    def __init__(self,vx1,vy1,vx2,vy2):
        self.startPoint = Point(vx1,vy1)
        self.endPoint = Point(vx2,vy2)
        self.isVisible = False
    def DrawWall(self):
        tx1 = self.startPoint.x - player.position.x
        tx2 = self.endPoint.x - player.position.x
        ty1 = self.startPoint.y - player.position.y
        ty2 = self.endPoint.y - player.position.y
        tz1 = tx1 * math.cos(player.angle) + ty1 * math.sin(player.angle)
        tz2 = tx2 * math.cos(player.angle) + ty2 * math.sin(player.angle)
        tx1 = tx1 * math.sin(player.angle) - ty1 * math.cos(player.angle)
        tx2 = tx2 * math.sin(player.angle) - ty2 * math.cos(player.angle)

        if tz1 > 0 or tz2 > 0:

            i2 = Intersect(tx1,tz1, tx2,tz2, -0.000001,0.000001, -200,5)
            i1 = Intersect(tx1,tz1, tx2,tz2,  0.000001,0.000001, 200,5)
            ix1 = i1[0]
            iz1 = i1[1]
            ix2 = i2[0]
            iz2 = i2[1]
            if tz1 <= 0:
                 if iz1 > 0:
                     tx1=ix1
                     tz1=iz1
                 else:
                    tx1=ix2
                    tz1=iz2
            if tz2 <= 0:
                if iz1 > 0:
                     tx2=ix1
                     tz2=iz1
                else:
                     tx2=ix2
                     tz2=iz2

            for i in range(20):
                c1 = 40 * 20
                c2 = 30 * 20
                x1 = -tx1 * c1 / tz1
                y1a = -i * c2 / tz1
                y1b = i * c2 / tz1
                x2 = -tx2 * c1 / tz2
                y2a = -i * c2 / tz2
                y2b = i * c2 / tz2

                pygame.draw.line(screen,BROWN,(mid[0] + x1, mid[1] + y1a),(mid[0] + x2,mid[1] + y2a),10)
                pygame.draw.line(screen,BROWN,(mid[0] + x1, mid[1] + y1b),(mid[0] + x2,mid[1] + y2b),10)

            pygame.draw.line(screen,WHITE,(mid[0] + x1, mid[1] + y1a),(mid[0] + x1,mid[1] + y1b),5)
            pygame.draw.line(screen,WHITE,(mid[0] + x2, mid[1] + y2a),(mid[0] + x2,mid[1] + y2b),5)


def FNcross(x1,y1, x2,y2):
    return x1*y2 - y1*x2

def Intersect(x1,y1, x2,y2, x3,y3, x4,y4):
  x = FNcross(x1,y1, x2,y2)
  y = FNcross(x3,y3, x4,y4)
  det = FNcross(x1-x2, y1-y2, x3-x4, y3-y4)
  x = FNcross(x, x1-x2, y, x3-x4) / (det + 0.00000000000000000000000000000000000001)
  y = FNcross(x, y1-y2, y, y3-y4) / (det + 0.00000000000000000000000000000000000001)
  return (x,y)
def ccw(point1,point2,point3):
    return (point3.y-point1.y)*(point2.x-point1.x) > (point2.y-point1.y)*(point3.x-point1.x)

def LineIntersect(point1,point2,point3,point4):
    keys=pygame.key.get_pressed()
    return ccw(point1,point3,point4) != ccw(point2,point3,point4) and ccw(point1,point2,point3) != ccw(point1,point2,point4)


def Distance(x1,y1,x2,y2):
    return math.fabs( math.sqrt(math.pow(( x2-x1),2) + math.pow(( y2- y1),2)))

player = Player()
def RunGame():
    for walls in level_walls:
        if Distance(player.position.x,player.position.y,walls.startPoint.x,walls.startPoint.y) < 200 or Distance(player.position.x,player.position.y,walls.endPoint.x,walls.endPoint.y) < 200:
            walls.DrawWall()
        if player.collision == False:
            player.collision = LineIntersect(player.position,player.ProjectedPosition(),walls.startPoint,walls.endPoint)
    player.Update()
class EditorCamera(object):
    def __init__(self):
        self.position = Point(size[0]/2,size[1]/2)
        self.speed = 10
    def MoveCamera(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.position.x += self.speed
        if keys[pygame.K_RIGHT]:
            self.position.x -= self.speed
        if keys[pygame.K_UP]:
            self.position.y += self.speed
        if keys[pygame.K_DOWN]:
            self.position.y -= self.speed
scale = 10
level_walls = []
cam = EditorCamera()
def RunEditor():
    SetWallPoints()
    cam.MoveCamera()
    for walls in level_walls:
        pygame.draw.line(screen,RED,(walls.startPoint.x + cam.position.x,walls.startPoint.y + cam.position.y),(walls.endPoint.x + cam.position.x,walls.endPoint.y + cam.position.y),1)
        pygame.draw.circle(screen,RED,(int(round(walls.startPoint.x + cam.position.x)), int(round(walls.startPoint.y + cam.position.y))),2,0)
        pygame.draw.circle(screen,RED,(int(round(walls.endPoint.x + cam.position.x)),int(round(walls.endPoint.y + cam.position.y))),2,0)

    global first
    if first:
        pos = pygame.mouse.get_pos()
        x = int(RoundToMultiple(pos[0],scale))
        y = int(RoundToMultiple(pos[1],scale))
        pygame.draw.line(screen,RED,(firstPoint.x + cam.position.x,firstPoint.y + cam.position.y),(x,y),1)
        pygame.draw.circle(screen,RED,(x,y),3,1)
    else:
        pos = pygame.mouse.get_pos()
        x = int(RoundToMultiple(pos[0],scale))
        y = int(RoundToMultiple(pos[1],scale))
        pygame.draw.circle(screen,GREEN,(x,y),3,1)
    pygame.draw.circle(screen,WHITE,(int(round(player.position.x+cam.position.x)),int(round(player.position.y+cam.position.y))),3,1)
    global click

def SetWallPoints():
    File  = open("level.txt","r+")
    data = File.readlines()
    global level_walls
    level_walls = []
    for line in data:
        words = line.split(",")
        if words != "":
            tempWall = Wall(int(float(words[0])),int(float(words[1])),int(float(words[2])),int(float(words[3])))
            level_walls.append(tempWall)
first = False
click = False
firstPoint = Point(0,0)
secondPoint = Point(0,0)

def DrawWallPoints():
    File  = open("level.txt",'a')
    global first
    global firstPoint
    global secondPoint
    global click
    go = False
    if first == False and click:
        pos = pygame.mouse.get_pos()
        x = int(RoundToMultiple(pos[0],scale))
        y = int(RoundToMultiple(pos[1],scale))
        firstPoint = Point(x - cam.position.x,y - cam.position.y)
        first = True
    elif first and click:
        pos = pygame.mouse.get_pos()
        x = int(RoundToMultiple(pos[0],scale))
        y = int(RoundToMultiple(pos[1],scale))
        secondPoint = Point(x - cam.position.x,y - cam.position.y)
        if firstPoint.x != secondPoint.x or firstPoint.y != secondPoint.y:
            File.write(str(firstPoint.x) +","+str(firstPoint.y)+","+str(secondPoint.x)+","+str(secondPoint.y)+", \n")
        File.close()
        first = False

    click = False

def DeleteWall():
    pos = pygame.mouse.get_pos()
    x = int(RoundToMultiple(pos[0],scale)) - cam.position.x
    y = int(RoundToMultiple(pos[1],scale)) - cam.position.y
    deleteRange = 9
    Point1 = Point(x + deleteRange,y + deleteRange)
    Point2 = Point(x - deleteRange,y - deleteRange)
    Point3 = Point(x - deleteRange,y + deleteRange)
    Point4 = Point(x + deleteRange,y - deleteRange)
    i = 0
    for walls in level_walls:
        if LineIntersect(Point1,Point2,walls.startPoint,walls.endPoint) or LineIntersect(Point3,Point4,walls.startPoint,walls.endPoint):
            level_walls.remove(walls)
        File  = open("level.txt","r+")
        File.truncate()
        data = File.readlines()
        for walls in level_walls:
            File.write(str(walls.startPoint.x) +","+str(walls.startPoint.y)+","+str(walls.endPoint.x)+","+str(walls.endPoint.y)+", \n")

def RoundToMultiple(number,multiple):
    remainder = number % multiple;
    if remainder == 0:
        return number;
    return number + multiple - remainder;

SetWallPoints()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game = not game
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game == False:
                click = True
                if event.button == 1:
                    DrawWallPoints()
                else:
                    DeleteWall()

    screen.fill(nice)
    pygame.mouse.set_visible(False)

    if game:
        RunGame()
    else:
        RunEditor()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
