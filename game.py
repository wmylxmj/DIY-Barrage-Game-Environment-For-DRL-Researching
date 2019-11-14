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
import matplotlib.pyplot as plt
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
        self.stageSkipCount = 0
        self.spotAward = 0
        self.actionsDict = {
                '0' :{'left':False, 'right':False, 'up':False, 'down':False, 'shoot':False, 'shift':False}, 
                '1' :{'left':True,  'right':False, 'up':False, 'down':False, 'shoot':False, 'shift':False},
                '2' :{'left':False, 'right':True,  'up':False, 'down':False, 'shoot':False, 'shift':False},
                '3' :{'left':False, 'right':False, 'up':True,  'down':False, 'shoot':False, 'shift':False},
                '4' :{'left':False, 'right':False, 'up':False, 'down':True,  'shoot':False, 'shift':False},
                '5' :{'left':True,  'right':False, 'up':True,  'down':False, 'shoot':False, 'shift':False},
                '6' :{'left':True,  'right':False, 'up':False, 'down':True,  'shoot':False, 'shift':False},
                '7' :{'left':False, 'right':True,  'up':True,  'down':False, 'shoot':False, 'shift':False},
                '8' :{'left':False, 'right':True,  'up':False, 'down':True,  'shoot':False, 'shift':False},
                '9' :{'left':False, 'right':False, 'up':False, 'down':False, 'shoot':True,  'shift':False}, 
                '10':{'left':True,  'right':False, 'up':False, 'down':False, 'shoot':True,  'shift':False},
                '11':{'left':False, 'right':True,  'up':False, 'down':False, 'shoot':True,  'shift':False},
                '12':{'left':False, 'right':False, 'up':True,  'down':False, 'shoot':True,  'shift':False},
                '13':{'left':False, 'right':False, 'up':False, 'down':True,  'shoot':True,  'shift':False},
                '14':{'left':True,  'right':False, 'up':True,  'down':False, 'shoot':True,  'shift':False},
                '15':{'left':True,  'right':False, 'up':False, 'down':True,  'shoot':True,  'shift':False},
                '16':{'left':False, 'right':True,  'up':True,  'down':False, 'shoot':True,  'shift':False},
                '17':{'left':False, 'right':True,  'up':False, 'down':True,  'shoot':True,  'shift':False},
                '18':{'left':False, 'right':False, 'up':False, 'down':False, 'shoot':False, 'shift':True }, 
                '19':{'left':True,  'right':False, 'up':False, 'down':False, 'shoot':False, 'shift':True },
                '20':{'left':False, 'right':True,  'up':False, 'down':False, 'shoot':False, 'shift':True },
                '21':{'left':False, 'right':False, 'up':True,  'down':False, 'shoot':False, 'shift':True },
                '22':{'left':False, 'right':False, 'up':False, 'down':True,  'shoot':False, 'shift':True },
                '23':{'left':True,  'right':False, 'up':True,  'down':False, 'shoot':False, 'shift':True },
                '24':{'left':True,  'right':False, 'up':False, 'down':True,  'shoot':False, 'shift':True },
                '25':{'left':False, 'right':True,  'up':True,  'down':False, 'shoot':False, 'shift':True },
                '26':{'left':False, 'right':True,  'up':False, 'down':True,  'shoot':False, 'shift':True },
                '27':{'left':False, 'right':False, 'up':False, 'down':False, 'shoot':True , 'shift':True }, 
                '28':{'left':True,  'right':False, 'up':False, 'down':False, 'shoot':True , 'shift':True },
                '29':{'left':False, 'right':True,  'up':False, 'down':False, 'shoot':True , 'shift':True },
                '30':{'left':False, 'right':False, 'up':True,  'down':False, 'shoot':True , 'shift':True },
                '31':{'left':False, 'right':False, 'up':False, 'down':True,  'shoot':True , 'shift':True },
                '32':{'left':True,  'right':False, 'up':True,  'down':False, 'shoot':True , 'shift':True },
                '33':{'left':True,  'right':False, 'up':False, 'down':True,  'shoot':True , 'shift':True },
                '34':{'left':False, 'right':True,  'up':True,  'down':False, 'shoot':True , 'shift':True },
                '35':{'left':False, 'right':True,  'up':False, 'down':True,  'shoot':True , 'shift':True }
        }
        self.nActions = len(self.actionsDict)
        self.frameWidthReturn = 400
        self.frameHeightReurn = 200
        self.shipCrashExecute = True
        pass
    
    def reset(self):
        self.background = GameBackground(self.window)
        self.stars = StarGroup(self.window)
        self.ship = Ship(self.window)
        self.stages = [Stage1(self.window, self.ship)]
        self.stageSkipCount = 0
        self.spotAward = 0
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
        if self.AIPlayMode == False:
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
            # restart
            if pressedKeys[pygame.K_SPACE]  and self.ship.aliveFlag==False:
                self.ship.aliveFlag = True
                self.ship.boomEffect.reset()
                if len(self.stages) != 0:
                    for alien in self.stages[0].aliens: 
                        for bullet in alien.bullets:
                            if ((bullet.rect.centerx - self.ship.rect.centerx) ** 2 + \
                            (bullet.rect.centery - self.ship.rect.centery)) < 150**2:                         
                                alien.bullets.remove(bullet)
                                pass
                            pass
                        pass
                    for bullet in self.stages[0].bulletsRemains:
                        if ((bullet.rect.centerx - self.ship.rect.centerx) ** 2 + \
                        (bullet.rect.centery - self.ship.rect.centery)) < 150**2:
                            self.stages[0].bulletsRemains.remove(bullet)
                            pass
                        pass
                    pass
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
            collideList = pygame.sprite.spritecollide(self.ship, alien.bullets, True)
            if len(collideList) != 0:
                if self.shipCrashExecute:
                    self.ship.aliveFlag = False
                    pass
                self.spotAward -= 1
                pass
            pass
        collideList = pygame.sprite.spritecollide(self.ship, self.stages[0].bulletsRemains, True)
        if len(collideList) != 0:
            if self.shipCrashExecute:
                self.ship.aliveFlag = False
                pass
            self.spotAward -= 1
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
    
    def stagesRun(self):
        for stage in self.stages:
            if stage.aliensCreated == False:
                stage.creatAliens()
                pass
            pass
        if len(self.stages) != 0:
            self.stages[0].run()
            if self.stages[0].isDone() == False:
                if self.stages[0].aliensActived == False:
                    self.stages[0].activeAliens()
                    pass
                return self.stages[0].spotAward, False
            else:  
                if self.AITrainMode == False:
                    self.stageSkipCount += 1
                    if self.stageSkipCount > 500:
                        self.stages.remove(self.stages[0])
                        self.stageSkipCount = 0
                        pass
                    pass
                else:
                    self.stages.remove(self.stages[0])
                    pass
                return 0, False
            pass
        return 0, True
    
    def getSurfaceArray3D(self):
        resizeWidth = self.frameWidthReturn
        resizeHeight = self.frameHeightReurn
        window = self.window.copy()
        window = pygame.transform.smoothscale(window, (resizeWidth, resizeHeight)) 
        window = pygame.transform.rotate(window, 90*3)
        window = pygame.transform.flip(window, True, False)
        image = pygame.surfarray.array3d(window)
        return image
    
    def performAction(self, action):
        if self.ship.aliveFlag:
            action = self.actionsDict[str(action)]
            self.ship.movingLeft = action['left']
            self.ship.movingRight = action['right']
            self.ship.movingUp = action['up']
            self.ship.movingDown = action['down']
            self.ship.fireFlag = action['shoot']
            # slow down
            if action['shift']:
                self.ship.speed = self.shipSlowSpeed
                pass
            else:
                self.ship.speed = self.shipNormalSpeed
                pass
            pass
        pass
    
    def runStep(self):
        self.spotAward = 0
        self.background.run()
        self.stars.run()
        stageSpotAward, stagesDone = self.stagesRun()
        self.ship.run()
        self.computeDamage()
        self.eventsProcess()
        self.spotAward += stageSpotAward
        pygame.display.flip()
        image = self.getSurfaceArray3D()
        done = stagesDone
        if self.ship.aliveFlag == False:
            done = True
            if self.AITrainMode == False:
                time.sleep(0.1)
                pass
            pass
        return self.spotAward, image, done
    
    def run(self):
        '''运行游戏'''
        while True:
            reward, stateNext, done = self.runStep()
            pass
        pass
    
    pass
    
        