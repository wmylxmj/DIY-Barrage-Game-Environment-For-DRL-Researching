# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:48:25 2019

@author: wmy
"""

import pygame
from config import GameConfigure
from pygame.sprite import Sprite
import random
import math

class DynamicSpeciallyGoodEffect(Sprite, GameConfigure):
    
    def __init__(self, window, frameInterval=10, resourses=[]):
        '''init'''
        GameConfigure.__init__(self)
        Sprite.__init__(self)
        # picture
        self.images = []
        self.resourses = resourses
        for resourse in resourses:
            image = pygame.image.load(resourse)
            self.images.append(image)
            pass
        # rect
        self.rect = self.images[0].get_rect()
        # window 
        self.window = window
        # frame interval
        self.frameInterval = frameInterval
        # count
        self.lifeCount = frameInterval * len(self.resourses)
        self.count = 0
        # pointer
        self.pointer = 0
        # start flag
        self.startFlag = False
        # done
        self.endFlag = False
        pass
    
    def setCenter(self, centerx, centery):
        self.rect.centerx = centerx
        self.rect.centery = centery
        pass
    
    def reset(self):
        self.count = 0
        self.pointer = 0
        self.startFlag = False
        self.endFlag = False
        pass
    
    def update(self):
        '''update'''
        if self.startFlag:
            self.count += 1
            pass
        if self.count >= self.lifeCount:
            self.endFlag = True
            pass
        pass
    
    def blitme(self):
        '''blit'''
        if self.count < self.lifeCount and self.startFlag == True:
            self.pointer = int(self.count/self.frameInterval)
            self.window.blit(self.images[self.pointer], self.rect)
            pass
        pass
    
    pass


class BoomEffect(DynamicSpeciallyGoodEffect):
    
    def __init__(self, window):
        self.resources = ['texture/boom/00001.png', \
                          'texture/boom/00002.png', \
                          'texture/boom/00003.png']
        self.window = window
        DynamicSpeciallyGoodEffect.__init__(self, window, \
                                            frameInterval=20, \
                                            resourses=self.resources)
        pass
    
    pass
