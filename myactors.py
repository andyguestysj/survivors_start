from pgzero.builtins import Actor, keyboard, keys
import math, sys, random
from constants import *

class MyActor(Actor):
  def __init__(self,img,x,y,speed):
    self.myimg = img
    self.imgno = 1
    myimg = f'{self.myimg}_{self.imgno}'
    super().__init__(myimg, (x,y))    
    self.vposx, self.vposy = x, y
    self.dx, self.dy = 0, 0
    self.speed = speed
    self.timer = 0    
    self.olddx = -100
    self.olddirection = -100

  def update(self):

    self.timer += 1

    if (self.dx < 0): 
      direction = 4
    elif (self.dx == 0): 
      if (self.dy < 0):
        direction = 10
      elif (self.dy >= 0):
        direction = 1            
    else:
      direction = 7

    if (self.olddirection != direction):
      self.imgno = direction

    if (self.timer==10):
      self.timer = 0
      if (self.olddirection == direction):
        self.imgno +=1
        if ((self.imgno==4) or (self.imgno==7) or (self.imgno==10) or (self.imgno==13)):
          self.imgno -= 3   

    self.image = f'{self.myimg}_{self.imgno}'
    self.olddx = self.dx
    self.olddirection = direction


    # Return vector representing amount of movement that should occur
    self.dx = self.dx * self.speed
    self.dy = self.dy * self.speed

    self.vposx += self.dx
    self.vposx = max(0+PLAYER_W,min(self.vposx, LEVEL_W-PLAYER_W))    
    self.vposy += self.dy
    self.vposy = max(0+PLAYER_H,min(self.vposy, LEVEL_H-PLAYER_H))

  def draw(self, offset_x, offset_y):
    self.pos = (self.vposx - offset_x, self.vposy - offset_y)
    super().draw()

class Player(MyActor):
  def __init__(self, x, y):
    self.img = "princess"
    self.health = 100
    super().__init__(self.img,x,y,5)

  def update(self):
    # Return vector representing amount of movement that should occur
    self.dx, self.dy = 0, 0
    if keyboard.a:
        self.dx = -1
    elif keyboard.d:
        self.dx = 1
    if keyboard.w:
        self.dy = -1
    elif keyboard.s:
        self.dy = 1

    super().update()

  def hurt(self,damage):
    self.health -= damage
    if (self.health<=0):
      print("game over")
      
      
class Monster(MyActor):
  def __init__(self, img, posx, posy,spd):
    super().__init__(img, posx, posy, spd)
    self.alive = True
    
  def update(self,player):
    # Return vector representing amount of movement that should occur    
    super().update()   
    if (self.colliderect(player)):
      player.hurt(10)
      self.alive = False
      

class Bat(Monster):
  def __init__(self, screencoords):

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    side = random.randint(0,3)    
    
    if (side == LEFT):
      posx = max(screencoords[LEFT] - 50, 0)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])      
    elif (side == TOP): 
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = max(screencoords[TOP] - 50, 0)
    elif (side == RIGHT): 
      posx = min(screencoords[RIGHT] + 50, LEVEL_W)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])
    elif (side == BOTTOM):
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = min(screencoords[BOTTOM] + 50, LEVEL_H)

    super().__init__("bat", posx, posy, 1)
    
  def update(self,player): 

    if (self.vposx > player.vposx):
      self.dx = -1
    elif (self.vposx < player.vposx):
      self.dx = 1
    else:
        self.dx = 0
    if (self.vposy > player.vposy):
      self.dy = -0.5
    elif (self.vposx < player.vposy):
      self.dy = 0.5
    else:
      self.dy = 0

    super().update(player)   


   
