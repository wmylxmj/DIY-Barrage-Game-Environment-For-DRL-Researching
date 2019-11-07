# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 15:37:06 2019

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
from background import GameBackground
from stars import StarGroup
from ship import Ship
from stages.stage1 import Stage1

class AlienGame(GameConfigure):
    
    def __init__(self):
        GameConfigure.__init__(self)
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Alien Invasion")
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.background = GameBackground(self.window)
        self.stars = StarGroup(self.window)
        self.ship = Ship(self.window)
        self.stages = [Stage1(self.window, self.ship)]
        pass
    
    def eventsProcess(self):
        '''事件处理'''
        for event in pygame.event.get():                
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                self.musicPlayFlag = False
                sys.exit()
                pass
            pass
        if self.AIMode == False:
            pressedKeys = pygame.key.get_pressed()
            # right
            if pressedKeys[pygame.K_RIGHT] and self.ship.aliveFlag:
                self.ship.movingRight = True
                pass
            else:
                self.ship.movingRight = False
                pass
            # left
            if pressedKeys[pygame.K_LEFT] and self.ship.aliveFlag:
                self.ship.movingLeft = True
                pass
            else:
                self.ship.movingLeft = False
                pass
            # up
            if pressedKeys[pygame.K_UP] and self.ship.aliveFlag:
                self.ship.movingUp = True
                pass
            else:
                self.ship.movingUp = False
                pass
            # down
            if pressedKeys[pygame.K_DOWN] and self.ship.aliveFlag:
                self.ship.movingDown = True
                pass
            else:
                self.ship.movingDown = False
                pass
            # shoot
            if pressedKeys[pygame.K_z] and self.ship.aliveFlag:
                self.ship.fireFlag = True
                pass
            else:
                self.ship.fireFlag = False
                pass
            # slow down
            if pressedKeys[pygame.K_LSHIFT] and self.ship.aliveFlag:
                self.ship.speed = self.shipSlowSpeed
                pass
            else:
                self.ship.speed = self.shipNormalSpeed
                pass
            pass
        pass
    
    def computeDamage(self):
        '''计算伤害'''
        if len(self.stages) == 0:
            return
        crashed = pygame.sprite.groupcollide(self.stages[0].aliens, self.ship.bullets, False, True)   
        for alien in self.stages[0].aliens:
            try:
                crashed[alien]
                pass
            except:
                pass
            else:
                bullets = crashed[alien]
                for bullet in bullets:
                    alien.hp -= bullet.attack
                    pass
                pass
            pass
        for battery in self.ship.batterys:
            crashed = pygame.sprite.groupcollide(self.stages[0].aliens, battery.bullets, False, True)   
            for alien in self.stages[0].aliens:
                try:
                    crashed[alien]
                    pass
                except:
                    pass
                else:
                    bullets = crashed[alien]
                    for bullet in bullets:
                        alien.hp -= bullet.attack
                        pass
                    pass
                pass
            pass
        pass
    
    def run(self):
        '''运行游戏'''
        exitCount = 0
        while True:
            self.background.run()
            self.stars.run()
            if len(self.stages) != 0:
                self.stages[0].run()
                if self.stages[0].isDone() == False:
                    if self.stages[0].aliensCreated == False:
                        self.stages[0].creatAliens()
                        pass
                    if self.stages[0].aliensActived == False:
                        self.stages[0].activeAliens()
                        pass
                    pass
                else:  
                    exitCount += 1
                    if exitCount > 500:
                        self.stages.remove(self.stages[0])
                        exitCount = 0
                        pass
                    pass
                pass   
            self.ship.run()
            self.computeDamage()
            self.eventsProcess()
            pygame.display.flip()  
            pass
        pass
    
    pass
    
        
if __name__ == "__main__":
    game = AlienGame()
    game.run()
    pass