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

class Alien1(Alien):
    
    def __init__(self, window, target):
        self.resource = 'texture/alien/00001.png'
        Alien.__init__(self, window, target, self.resource)
        # init the location
        self.rect.centerx = random.randint(-50, self.windowWidth + 50)
        self.rect.bottom = self.window.get_rect().top - 50
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.targetx = random.randint(100, self.windowWidth - 100)
        self.targety = random.randint(25, 250)
        # hp
        self.hp = 25
        pass
    
    def fire(self):
        if self.fireCount >= self.fireInterval and self.activeFlag and self.hp > 0:
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
                self.targetx = random.randint(max(100, self.target.decisionPointRect.centerx - 400), \
                                              min(self.windowWidth - 100, self.target.decisionPointRect.centerx + 400))
                pass
            if self.targetx > self.rect.centerx:
                self.x += 2
            elif self.targetx < self.rect.centerx:
                self.x -= 2
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
        self.movex = self.target.decisionPointRect.centerx - self.alien.rect.centerx
        self.movey = self.target.decisionPointRect.centery - self.alien.rect.centery
        # location
        self.decisionPointRect.centerx = alien.rect.centerx
        self.decisionPointRect.bottom = alien.rect.bottom
        self.y = float(self.decisionPointRect.centery)
        self.x = float(self.decisionPointRect.centerx)
        self.imageRect.centerx = self.decisionPointRect.centerx
        self.imageRect.centery = self.decisionPointRect.centery
        # speed
        self.speed = 2
        pass
    
    def update(self):
        '''更新子弹位置信息'''
        self.y += self.speed * \
        float(self.movey) / math.sqrt(self.movex**2 + self.movey**2)
        self.x += self.speed * \
        float(self.movex) / math.sqrt(self.movex**2 + self.movey**2)
        self.decisionPointRect.centery = self.y
        self.decisionPointRect.centerx = self.x
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


class Stage1(GameConfigure):
    
    def __init__(self, window, ship):
        GameConfigure.__init__(self)
        self.window = window
        self.ship = ship
        self.aliens = Group()
        self.done = False
        self.aliensCreated = False
        self.aliensActived = False
        # 残余子弹
        self.bulletsRemains = Group()
        self.boomEffectsRemains = Group()
        pass
    
    def creatAliens(self):
        for i in range(10):
            newAlien = Alien1(self.window, self.ship)
            self.aliens.add(newAlien)
            pass
        self.aliensCreated = True
        pass
    
    def activeAliens(self):
        for alien in self.aliens.sprites():
            alien.activeFlag = True
            pass
        self.aliensActived = True
        pass
    
    def update(self):
        self.aliens.update()
        if self.aliensCreated and self.aliensActived:
            done = True
            for alien in self.aliens.sprites():
                if alien.hp > 0:   
                    done = False
                    pass
                else:
                    self.boomEffectsRemains.add(alien.boomEffect)
                    for bullet in alien.bullets.sprites():
                        self.bulletsRemains.add(bullet)
                        pass
                    self.aliens.remove(alien)
                    pass
                pass
            self.done = done
            pass
        for bommEffect in self.boomEffectsRemains:
            if bommEffect.endFlag == True:
                self.boomEffectsRemains.remove(bommEffect)
                pass
            pass
        self.bulletsRemains.update()
        self.boomEffectsRemains.update()
        pass
    
    def blitme(self):
        for alien in self.aliens.sprites():
            alien.blitme()
            pass
        for bullet in self.bulletsRemains.sprites():
            bullet.blitme()
            pass
        for bommEffect in self.boomEffectsRemains.sprites():
            bommEffect.blitme()
            pass
        pass
    
    def run(self):
        self.update()
        self.blitme()
        pass
    
    def isDone(self):
        return self.done
    
    pass
        
    