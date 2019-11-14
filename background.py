# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:25:25 2019

@author: wmy
"""

import sys
import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
import random
import numpy as np
import math
import time
from config import GameConfigure

class GameBackground(GameConfigure):
    
    def __init__(self, window):
        GameConfigure.__init__(self)
        self.resource = "texture/background/00001.jpg"
        self.pointer = 0
        self.window = window
        self.image = pygame.image.load(self.resource).convert()
        pass
    
    def update(self):
        self.pointer += 1
        if self.pointer >= self.windowHeight:
            self.pointer = 0
            pass
        pass
    
    def blitme(self):
        self.window.blit(self.image, (0, self.pointer - self.windowHeight))
        self.window.blit(self.image, (0, self.pointer))
        pass
    
    def run(self):
        self.update()
        self.blitme()
        pass
    
    pass