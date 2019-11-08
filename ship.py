# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:11:54 2019

@author: wmy
"""

from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame
import math
from config import GameConfigure
from effect import BoomEffect

class Ship(Sprite, GameConfigure):
    
    def __init__(self, window):
        '''初始化飞船'''
        GameConfigure.__init__(self)
        Sprite.__init__(self)
        self.window = window
        self.windowRect = self.window.get_rect()
        # load the image
        self.resource = 'texture/ship/00001.png'
        self.image = pygame.image.load(self.resource)
        self.imageRect = self.image.get_rect()
        # load the decision point
        self.decisionPointResource = 'texture/ship/decisionpoint/00001.png'
        self.decisionPoint = pygame.image.load(self.decisionPointResource)
        self.rect = self.decisionPoint.get_rect()
        # init the location
        self.imageRect.centerx = self.windowRect.centerx
        self.imageRect.bottom = self.windowRect.bottom
        self.rect.centerx = self.imageRect.centerx
        self.rect.centery = self.imageRect.centery
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # move flag
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False
        # fire init
        self.fireFlag = False
        self.fireCount = 0
        self.fireInterval = self.shipFireInterval
        self.bulletSpeed = self.shipBulletSpeed
        # init speed 
        self.speed = self.shipNormalSpeed
        # the ship is still alive
        self.aliveFlag = True
        # bullets
        self.bullets = Group()
        # boom effect
        self.boomEffect = BoomEffect(self.window)
        # battery
        self.batterys = Group()
        self.numBatterys = 2
        for i in range(self.numBatterys):
            phase = i*(2*3.1415926)/self.numBatterys
            self.batterys.add(ShipBattery(self, initialPhase=phase))
            pass
        pass
    
    def fire(self):
        '''ship fire update'''
        # ship fire
        if self.aliveFlag==True and self.fireFlag == True and self.fireCount >= self.fireInterval:
            if self.speed == self.shipNormalSpeed:
                # 1
                newBullet = ShipBullet(self)
                self.bullets.add(newBullet)
                # 2
                newBullet = ShipBullet(self)
                newBullet.angle = float(3.1415926/12)             
                self.bullets.add(newBullet)
                # 3
                newBullet = ShipBullet(self)
                newBullet.angle = float(-3.1415926/12)
                self.bullets.add(newBullet)
                # 4
                newBullet = ShipBullet(self)
                newBullet.angle = float(3.1415926/24)
                self.bullets.add(newBullet)
                # 5
                newBullet = ShipBullet(self)
                newBullet.angle = float(-3.1415926/24)
                self.bullets.add(newBullet)
                pass
            else:
                # 1
                newBullet = ShipBullet(self)
                self.bullets.add(newBullet)
                # 2
                newBullet = ShipBullet(self)
                newBullet.x += 24
                self.bullets.add(newBullet)
                # 3
                newBullet = ShipBullet(self)
                newBullet.x -= 24
                self.bullets.add(newBullet)
                # 4
                newBullet = ShipBullet(self)
                newBullet.x += 12
                self.bullets.add(newBullet)
                # 5
                newBullet = ShipBullet(self)
                newBullet.x -= 12
                self.bullets.add(newBullet)
                pass
            self.fireCount = 0
            pass
        self.fireCount += 1
        pass
    
    def update(self):
        '''更新位置'''
        if self.aliveFlag == True:
            speed = self.speed
            if (self.movingRight|self.movingLeft) & (self.movingUp|self.movingDown):
                speed = speed / 1.414
                pass
            if self.movingRight and self.imageRect.right < self.windowRect.right:
                self.centerx += speed
                pass
            if self.movingLeft and self.imageRect.left > 0:
                self.centerx -= speed
                pass
            if self.movingUp and self.imageRect.top > 0:
                self.centery -= speed
                pass
            if self.movingDown and self.imageRect.bottom < self.windowRect.bottom:
                self.centery += speed
                pass
            self.rect.centerx = int(self.centerx)
            self.rect.centery = int(self.centery)
            self.imageRect.centerx = int(self.centerx)
            self.imageRect.centery = int(self.centery)
            # battery 
            self.batterys.update()
            pass
        else:
            # not alive
            self.boomEffect.setCenter(self.rect.centerx, self.rect.centery)
            self.boomEffect.startFlag = True
            pass
        # boom effect
        self.boomEffect.update()
        # fire update
        self.fire()
        # bullets
        self.bullets.update()
        pass
        
    def blitme(self):
        '''画出飞船'''
        # show ship bullets
        for bullet in self.bullets.sprites():
            bullet.blitme()
            pass
        # show ship
        if self.aliveFlag:            
            self.window.blit(self.image, self.imageRect)
            if self.speed == self.shipSlowSpeed:
                self.window.blit(self.decisionPoint, self.rect)
                pass
            # show batterys
            for battery in self.batterys.sprites():
                battery.blitme()
                pass
            pass
        # boom effect
        self.boomEffect.blitme()
        pass 
    
    def run(self):
        self.update()
        self.blitme()
        pass
    
    pass
    

class ShipBullet(Sprite):
    
    def __init__(self, ship):
        '''初始化子弹'''
        Sprite.__init__(self)
        # load information from ship
        self.ship = ship
        self.window = ship.window
        # image init
        self.resource = 'texture/ship/bullet/00001.png'
        self.image = pygame.image.load(self.resource)
        self.rect = self.image.get_rect()
        # init the location
        self.rect.centerx = ship.imageRect.centerx
        self.rect.top = ship.imageRect.top
        # init the shoot angle
        self.angle = 0
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        # init the attack
        self.attack = 1
        pass
    
    def update(self):
        '''更新子弹位置信息'''
        self.y -= self.ship.bulletSpeed * math.cos(self.angle)
        self.rect.y = self.y
        self.x += self.ship.bulletSpeed * math.sin(self.angle)
        self.rect.x = self.x
        # 超出屏幕删除
        if self.rect.bottom < 0:
            self.ship.bullets.remove(self)
            pass
        pass
    
    def blitme(self):
        '''画出子弹'''
        self.window.blit(self.image, self.rect)
        pass
    
    pass
    

class ShipBattery(Sprite, GameConfigure):
    
    def __init__(self, ship, radius=64, initialPhase=0):
        Sprite.__init__(self)
        GameConfigure.__init__(self)
        self.ship = ship
        self.window = self.ship.window
        self.resource = 'texture/ship/battery/00001.png'
        self.image = pygame.image.load(self.resource)
        self.rect = self.image.get_rect()
        self.defaultRadius = radius
        self.radius = self.defaultRadius
        self.initialPhase = initialPhase
        self.phase = initialPhase
        self.circleCenterx = self.ship.rect.centerx
        self.circleCentery = self.ship.rect.centery
        self.angularVelocity = 3.1415926/180
        self.rect.centery = self.ship.rect.centery - self.radius * math.cos(initialPhase)
        self.rect.centerx = self.ship.rect.centerx + self.radius * math.sin(initialPhase)
        self.bullets = Group()
        self.fireInterval = int(self.ship.fireInterval*2)
        self.bulletSpeed = int(self.ship.bulletSpeed/2)
        self.fireCount = 0
        pass
    
    def fire(self):
        '''fire update'''
        # fire
        if self.ship.aliveFlag==True and self.ship.fireFlag == True and \
        self.fireCount >= self.fireInterval:
            newBullet = ShipBatteryBullet(self)
            self.bullets.add(newBullet)
            self.fireCount = 0
            pass
        self.fireCount += 1
        pass
    
    def update(self):
        self.phase += self.angularVelocity
        if self.ship.speed == self.shipNormalSpeed:
            self.radius = self.defaultRadius
            self.angularVelocity = 3.1415926/180
            self.fireInterval = int(self.ship.fireInterval*2)
            self.bulletSpeed = int(self.ship.bulletSpeed/2)
            self.circleCenterx = self.ship.rect.centerx
            self.circleCentery = self.ship.rect.centery
            self.rect.centery = self.circleCentery - self.radius * math.cos(self.phase)
            self.rect.centerx = self.circleCenterx + self.radius * math.sin(self.phase)
            pass
        elif self.ship.speed == self.shipSlowSpeed:
            self.radius = 1.5 * self.defaultRadius
            self.angularVelocity = 3.1415926/120
            self.fireInterval = int(self.ship.fireInterval*1.2)
            self.bulletSpeed = int(self.ship.bulletSpeed/1.2)
            self.rect.centery = self.circleCentery - self.radius * math.cos(self.phase)
            self.rect.centerx = self.circleCenterx + self.radius * math.sin(self.phase)
            pass
        self.fire()
        # update bullets
        self.bullets.update()
        pass
    
    def blitme(self):
        for bullet in self.bullets.sprites():
            bullet.blitme()
            pass
        if self.ship.aliveFlag == True:
            self.window.blit(self.image, self.rect)
            pass
        pass
    
    pass


class ShipBatteryBullet(Sprite):
    
    def __init__(self, battery):
        '''初始化子弹'''
        Sprite.__init__(self)
        # load information from ship
        self.battery = battery
        self.window = battery.window
        # image init
        self.resource = 'texture/ship/battery/bullet/00001.png'
        self.image = pygame.image.load(self.resource)
        self.rect = self.image.get_rect()
        # init the location
        self.rect.centerx = battery.rect.centerx
        self.rect.top = battery.rect.top
        # init the shoot angle
        self.angle = 0
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        # init the attack
        self.attack = 1.5
        pass
    
    def update(self):
        '''更新子弹位置信息'''
        self.y -= self.battery.bulletSpeed * math.cos(self.angle)
        self.rect.y = self.y
        self.x += self.battery.bulletSpeed * math.sin(self.angle)
        self.rect.x = self.x
        # 超出屏幕删除
        if self.rect.bottom < 0:
            self.battery.bullets.remove(self)
            pass
        pass
    
    def blitme(self):
        '''画出子弹'''
        self.window.blit(self.image, self.rect)
        pass
    
    pass
    