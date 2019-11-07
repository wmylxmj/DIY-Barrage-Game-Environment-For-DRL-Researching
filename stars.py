# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:46:22 2019

@author: wmy
"""

import pygame
from config import GameConfigure
from pygame.sprite import Sprite
from pygame.sprite import Group
import random

class Star(Sprite, GameConfigure):
    
    def __init__(self, window):
        '''初始化星星'''
        Sprite.__init__(self)
        GameConfigure.__init__(self)
        self.window = window
        self.resource = 'texture/star/00001.png'
        self.image = pygame.image.load(self.resource)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, self.windowWidth)
        self.rect.centery = random.randint(0, self.windowHeight)
        self.y = float(self.rect.y)
        self.moveSpeed = self.starMoveSpeed
        pass
    
    def update(self):
        '''更新星星位置信息'''
        if(self.y < self.windowHeight):
            self.y += self.moveSpeed
            self.rect.y = self.y
            pass
        else:
            self.rect.centerx = random.randint(0, self.windowWidth)
            self.y = 0
            self.rect.y = self.y
            pass
        pass
    
    def blitme(self):
        '''画出星星'''
        self.window.blit(self.image, self.rect)
        pass
    
    pass


class StarGroup(Group, GameConfigure):
    
    def __init__(self, window):
        Group.__init__(self)
        GameConfigure.__init__(self)
        self.window = window
        for i in range(self.numStars):
            newStar = Star(window)
            self.add(newStar)
            pass
        pass
    
    def run(self):
        '''显示星空'''
        self.update()
        for star in self.sprites():
            star.blitme()
            pass
        pass
    
    pass