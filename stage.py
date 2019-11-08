# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:53:07 2019

@author: wmy
"""

from aliens import Alien, AlienBullet
import pygame
from config import GameConfigure
from pygame.sprite import Sprite
import random
import math
from effect import BoomEffect
from pygame.sprite import Group

class Stage(GameConfigure):
    
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
        # 残余爆炸效果
        self.boomEffectsRemains = Group()
        pass
    
    def creatAliens(self):
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
                    # 被击杀 爆炸效果录入
                    self.boomEffectsRemains.add(alien.boomEffect)
                    # 残余子弹录入
                    for bullet in alien.bullets.sprites():
                        self.bulletsRemains.add(bullet)
                        pass
                    # 删除
                    self.aliens.remove(alien)
                    pass
                pass
            self.done = done
            pass
        # 移除完成的爆炸效果
        for bommEffect in self.boomEffectsRemains:
            if bommEffect.endFlag == True:
                self.boomEffectsRemains.remove(bommEffect)
                pass
            pass
        # 更新
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
        