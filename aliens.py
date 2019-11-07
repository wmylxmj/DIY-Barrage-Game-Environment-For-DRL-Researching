# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:01:24 2019

@author: wmy
"""

import pygame
from config import GameConfigure
from pygame.sprite import Sprite
import random
import math
from effect import BoomEffect
from pygame.sprite import Group

class Alien(Sprite, GameConfigure):
    
    def __init__(self, window, target, resource):
        Sprite.__init__(self)
        GameConfigure.__init__(self)
        self.window = window
        self.target = target
        self.resource = resource
        self.image = pygame.image.load(resource)
        self.rect = self.image.get_rect()
        # fire init
        self.fireCount = 0
        self.fireInterval = 75
        # number of lives
        self.hp = 10
        # active flag
        self.activeFlag = False
        # boom effect
        self.boomEffect = BoomEffect(self.window)
        # bullets
        self.bullets = Group()
        pass
    
    def update(self):
        # boom effect
        if self.hp <= 0:
            self.boomEffect.setCenter(self.rect.centerx, self.rect.centery)
            self.boomEffect.startFlag = True
            pass
        self.boomEffect.update()
        pass
    
    def blitme(self):
        # blite alien
        if self.activeFlag and self.hp > 0:
            self.window.blit(self.image, self.rect)
            pass
        # boom effect
        self.boomEffect.blitme()
        if self.activeFlag:
            self.window.blit(self.image, self.rect)
            pass
        pass
        
    pass


class AlienBullet(Sprite, GameConfigure):
    
    def __init__(self, alien, resource, decisionPointResource):
        Sprite.__init__(self)
        GameConfigure.__init__(self)
        self.alien = alien
        self.target = self.alien.target
        self.resource = resource
        # init image
        self.image = pygame.image.load(resource)
        self.imageRect = self.image.get_rect()
        self.window = self.alien.window
        self.decisionPointResource = decisionPointResource
        # init decision point
        self.decisionPoint = pygame.image.load(decisionPointResource)
        self.decisionPointRect = self.decisionPoint.get_rect()
        pass
    
    def update(self):
        if self.imageRect.top >= self.windowHeight or \
        self.imageRect.right <= 0 or self.imageRect.left >= self.windowWidth or \
        self.imageRect.bottom <= 0:
            self.alien.bullets.remove(self)
            pass
        pass
    
    def blitme(self):
        self.window.blit(self.image, self.imageRect)
        pass
    
    pass

