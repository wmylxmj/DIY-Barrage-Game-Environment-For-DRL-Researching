# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:01:03 2019

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
batch_size = 32
learning_rate = 0.001
num_episodes = 800
discount_factor = 0.97

pretrained_weights = "save/qNetwork-200-400-5.ckpt"

global_step = 0
copy_steps = 100
steps_train = 8
start_steps = 1000

logdir = 'logs'

# 输入形状
input_shape = (None, frame_height, frame_width, nFrames)
frame_shape = (frame_height, frame_width)

# 游戏
game = AlienGame()
game.frameHeightReurn = frame_height
game.frameWidthReturn = frame_width
game.shipCrashExecute = False

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

# 优化器
optimizer = tf.train.AdamOptimizer(learning_rate)
training_op = optimizer.minimize(loss)

# 日志
loss_summary = tf.summary.scalar('loss', loss)
merge_summary = tf.summary.merge_all()
file_writer = tf.summary.FileWriter(logdir, tf.get_default_graph())

# 全局参数初始化
init = tf.global_variables_initializer()

# 预处理器
state_preprocessor = StatePreprocessor(nFrames=nFrames, shape=frame_shape)

# epsilon 贪婪策略
epsilon_greedy = DecayEpsilonGreedy()

# 经验回放缓存
buffer_len = 1000
exp_buffer = deque(maxlen=buffer_len)

def sample_memories(batch_size):
    perm_batch = np.random.permutation(len(exp_buffer))[:batch_size]
    mem = np.array(exp_buffer)[perm_batch]
    return mem[:,0], mem[:,1], mem[:,2], mem[:,3], mem[:,4]

# tensorflow会话
saver = tf.train.Saver()
with tf.Session() as sess:
    if pretrained_weights != None:
        saver.restore(sess, pretrained_weights)
        print("[OK] Weights Loaded.")
        pass
    else:
        init.run()
        pass
    for i in range(num_episodes):
        game.reset()
        reward, frame, done = game.runStep()
        state_preprocessor.reset()
        actions_counter = Counter() 
        episodic_loss = []
        epoch = 0
        episodic_reward = 0
        done = False
        while not done:
            state = state_preprocessor.generate(frame)
            time_record = time.time()
            actions = mainQ_outputs.eval(feed_dict={X:[state], in_training_mode:False})
            print('Global Step', global_step, 'Decision Time', time.time()-time_record)
            # get the action
            action = np.argmax(actions, axis=-1)
            actions_counter[str(action)] += 1 
            # select the action using epsilon greedy policy
            action = epsilon_greedy.policyDecision(action, nActions)
            game.performAction(action)
            reward, frame, done = game.runStep()
            next_state = state_preprocessor.generate(frame)
            exp_buffer.append([state, action, next_state, reward, done])
            if global_step % steps_train == 0 and global_step > start_steps:
                # sample experience
                o_obs, o_act, o_next_obs, o_rew, o_done = sample_memories(batch_size)
                # states
                o_obs = [x for x in o_obs]
                # next states
                o_next_obs = [x for x in o_next_obs]
                # next actions
                next_act = mainQ_outputs.eval(feed_dict={X:o_next_obs, in_training_mode:False})
                # reward
                y_batch = o_rew + discount_factor * np.max(next_act, axis=-1) * (1-o_done) 
                # merge all summaries and write to the file
                mrg_summary = merge_summary.eval(feed_dict={X:o_obs, y:np.expand_dims(y_batch, axis=-1), X_action:o_act, in_training_mode:False})
                file_writer.add_summary(mrg_summary, global_step)
                # train
                train_loss, _ = sess.run([loss, training_op], feed_dict={X:o_obs, y:np.expand_dims(y_batch, axis=-1), X_action:o_act, in_training_mode:True})
                episodic_loss.append(train_loss)
                saver.save(sess, "save/qNetwork-" + str(frame_height) + "-" + \
                           str(frame_width) + "-" + str(nFrames) + ".ckpt")
                print('Loss', train_loss)
                pass
            # after some interval we copy our main Q network weights to target Q network
            if (global_step+1) % copy_steps == 0 and global_step > start_steps:
                copy_target_to_main.run()
                pass
            state = next_state
            epoch += 1
            global_step += 1
            episodic_reward += reward
            pass
        print('Epoch', epoch, 'Reward', episodic_reward)
        pass
    pass
        
    

