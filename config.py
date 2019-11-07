# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:09:07 2019

@author: wmy
"""

class GameConfigure(object):
    
    def __init__(self):
        '''设置'''
        self.windowWidth = 1400
        self.windowHeight = 700
        self.shipNormalSpeed = 3
        self.shipSlowSpeed = 1.2
        self.shipBulletSpeed = 8
        self.shipFireInterval = 12
        self.numStars = 100
        self.numBGMs = 4
        self.starMoveSpeed = 3
        self.musicPlayFlag = False
        self.AIMode = False
        pass
    
    pass