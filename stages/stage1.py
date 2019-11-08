# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:07:38 2019

@author: wmy
"""

import sys
sys.path.append("..")
from aliens import Alien, AlienBullet
import pygame
from config import GameConfigure
from pygame.sprite import Sprite
import random
import math
from effect import BoomEffect
from pygame.sprite import Group
from stage import Stage

class Alien1(Alien):
    
    def __init__(self, window, target):
        self.resource = 'texture/alien/00001.png'
        Alien.__init__(self, window, target, self.resource)
        # init the location
        self.rect.centerx = random.randint(-50, self.windowWidth + 50)
        self.rect.bottom = random.randint(-75, -15)
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.targetx = random.randint(50, self.windowWidth - 50)
        self.targety = random.randint(25, 250)
        # hp
        self.hp = 25
        # fire init
        self.fireCount = 0
        self.fireInterval = 75
        pass
    
    def fire(self):
        if self.fireCount >= self.fireInterval and self.activeFlag \
        and self.hp > 0 and self.target.aliveFlag == True:
            newBullet = AlienBullet1(self)
            self.bullets.add(newBullet)
            self.fireCount = 0
            pass
        self.fireCount += 1
        pass
    
    def update(self):
        # fire
        if self.activeFlag and self.rect.top >= 0:
            self.fire()
            pass
        # bullets
        self.bullets.update()
        # move
        if self.activeFlag:
            if (self.targety - self.rect.centery) < 2 and (self.targety - self.rect.centery) > -2:
                self.targety = random.randint(25, 250)
                pass
            if self.targety > self.rect.centery:
                self.y += 0.5
                pass
            elif self.targety < self.rect.centery:
                self.y -= 0.5
                pass
            if (self.targetx - self.rect.centerx) < 2 and (self.targetx - self.rect.centerx) > -2:
                if self.target.aliveFlag:
                    self.targetx = random.randint(max(50, self.target.rect.centerx - 450), \
                                                  min(self.windowWidth - 50, self.target.rect.centerx + 450))
                    pass
                else:
                    self.targetx = random.randint(50, self.windowWidth - 50)
                    pass
                pass
            if self.targetx > self.rect.centerx:
                self.x += 1
            elif self.targetx < self.rect.centerx:
                self.x -= 1
                pass
            self.rect.centery = self.y
            self.rect.centerx = self.x
            pass
        # boom effect
        if self.hp <= 0:
            self.boomEffect.setCenter(self.rect.centerx, self.rect.centery)
            self.boomEffect.startFlag = True
            pass
        self.boomEffect.update()
        pass
    
    def blitme(self):
        # blite bullets
        for bullet in self.bullets.sprites():
            bullet.blitme()
            pass
        # blite alien
        if self.activeFlag and self.hp > 0:
            self.window.blit(self.image, self.rect)
            pass
        # boom effect
        self.boomEffect.blitme()
        pass
    
    pass


class AlienBullet1(AlienBullet):
    
    def __init__(self, alien):
        self.resource = 'texture/alien/bullet/00001.png'
        self.decisionPointResource = 'texture/alien/bullet/decisionpoint/00002.png'
        AlienBullet.__init__(self, alien, self.resource, self.decisionPointResource)
        self.movex = self.target.rect.centerx - self.alien.rect.centerx
        self.movey = self.target.rect.centery - self.alien.rect.centery
        # location
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        self.y = float(self.rect.centery)
        self.x = float(self.rect.centerx)
        self.imageRect.centerx = self.rect.centerx
        self.imageRect.centery = self.rect.centery
        # speed
        self.speed = 2
        pass
    
    def update(self):
        '''更新子弹位置信息'''
        self.y += self.speed * \
        float(self.movey) / math.sqrt(self.movex**2 + self.movey**2)
        self.x += self.speed * \
        float(self.movex) / math.sqrt(self.movex**2 + self.movey**2)
        self.rect.centery = self.y
        self.rect.centerx = self.x
        self.imageRect.centerx = self.x
        self.imageRect.centery = self.y
        # delete
        if self.imageRect.top >= self.windowHeight or \
        self.imageRect.right <= 0 or self.imageRect.left >= self.windowWidth or \
        self.imageRect.bottom <= 0:
            self.alien.bullets.remove(self)
            pass
        pass
    
    pass


class Stage1(Stage):
    
    def __init__(self, window, ship):
        Stage.__init__(self, window, ship)
        pass
    
    def creatAliens(self):
        for i in range(10):
            newAlien = Alien1(self.window, self.ship)
            self.aliens.add(newAlien)
            pass
        self.aliensCreated = True
        pass
    
    pass
        
    