# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:37:02 2019

@author: wmy
"""

import numpy as np
from collections import deque, Counter
from PIL import Image

class DecayEpsilonGreedy(object):
    
    def __init__(self, epsInit=0.5, epsMin=0.05, epsMax=0.95, epsDecaySteps=10000):
        self.epsilon = epsInit
        self.epsMin = epsMin
        self.epsMax = epsMax
        self.epsDecaySteps = epsDecaySteps
        self.step = 0
        pass
    
    def policyDecision(self, action, nActions):
        self.epsilon = max(self.epsMin, self.epsMax-(self.epsMax-self.epsMin)* \
                           self.step/self.epsDecaySteps)
        self.step += 1
        if np.random.rand() < self.epsilon:
            return np.random.randint(nActions)
        else:
            return np.squeeze(action)
        pass
    
    pass


class StatePreprocessor(object):
    
    def __init__(self, nFrames, shape):
        self.nFrames = nFrames
        self.shape = shape
        self.stateList = []
        self.height = shape[0]
        self.width = shape[1]
        for i in range(nFrames):
            self.stateList.append(np.zeros((self.height, self.width, 1)))
            pass
        pass
    
    def generate(self, frame):
        # resize
        if frame.shape[0] != self.shape[0] and frame.shape[1] != self.shape[1]:
            frame = Image.fromarray(frame)
            frame = frame.resize((self.width, self.height))
            frame = np.array(frame)
            pass
        # gray
        frame = frame.mean(axis=2)
        frame = frame.reshape((self.height, self.width, 1))
        self.stateList.remove(self.stateList[0])
        self.stateList.append(frame)
        output = self.stateList[0]
        for i in range(1, self.nFrames):
            output = np.concatenate([output, self.stateList[i]], axis=2)
            pass
        output = output / 127.5 - 1.0
        return np.array(output)
    
    def reset(self):
        self.stateList = []
        for i in range(self.nFrames):
            self.stateList.append(np.zeros((self.height, self.width, 1)))
            pass
        pass
    
    pass
        


