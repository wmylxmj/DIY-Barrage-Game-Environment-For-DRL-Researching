# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:38:19 2019

@author: wmy
"""

import numpy as np
import tensorflow as tf
from collections import deque, Counter
from game import AlienGame
from utils import DecayEpsilonGreedy
from model import QNetwork
from utils import StatePreprocessor
import time

# 超参数
frame_height = 200
frame_width = 400
nFrames = 5

weights = 'save/qNetwork-200-400-5.ckpt'

# 输入形状
input_shape = (None, frame_height, frame_width, nFrames)
frame_shape = (frame_height, frame_width)

# 游戏
game = AlienGame()
game.frameHeightReurn = frame_height
game.frameWidthReturn = frame_width

# 行为数
nActions = game.nActions

tf.reset_default_graph()

# 输入
X = tf.placeholder(tf.float32, shape=input_shape)
in_training_mode = tf.placeholder(tf.bool)

# Q网络
mainQ_weights, mainQ_outputs = QNetwork(X, nActions, nameScope='mainQ')
targetQ_weights, targetQ_outputs = QNetwork(X, nActions, nameScope='targetQ')

# 行为Q
X_action = tf.placeholder(tf.int32, shape=(None, ))
Q_action = tf.reduce_sum(targetQ_outputs*tf.one_hot(X_action, nActions), axis=-1, keep_dims=True)

# 权重复制
copy_op = [tf.assign(main_name, targetQ_weights[var_name]) for var_name, main_name in mainQ_weights.items()]
copy_target_to_main = tf.group(*copy_op)

# 输出
y = tf.placeholder(tf.float32, shape=(None, 1))

# 损失
loss = tf.reduce_mean(tf.square(y - Q_action))

# 预处理器
state_preprocessor = StatePreprocessor(nFrames=nFrames, shape=frame_shape)

# tensorflow会话
saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, weights)
    game.reset()
    reward, frame, done = game.runStep()
    state_preprocessor.reset()
    done = False
    episodic_reward = 0
    while not done:
        state = state_preprocessor.generate(frame)
        time_record = time.time()
        actions = mainQ_outputs.eval(feed_dict={X:[state], in_training_mode:False})
        # get the action
        action = np.squeeze(np.argmax(actions, axis=-1))
        # select the action using epsilon greedy policy
        game.performAction(action)
        reward, frame, done = game.runStep()
        next_state = state_preprocessor.generate(frame)
        state = next_state
        episodic_reward += reward
        pass
    print("Reward", episodic_reward)
    pass
        
    

