# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:35:24 2019

@author: wmy
"""

import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers import flatten, conv2d, fully_connected
from tensorflow.layers import batch_normalization

def QNetwork(X, nActions, nameScope='QNetwork'):
    initializer = tf.contrib.layers.variance_scaling_initializer()
    with tf.variable_scope(nameScope) as scope:
        X = conv2d(X, num_outputs=64, kernel_size=(3, 3), \
                   stride=(2, 2), padding='valid', weights_initializer=initializer)
        X = batch_normalization(X, axis=-1)
        tf.summary.histogram('layer1', X)
        X = conv2d(X, num_outputs=128, kernel_size=(3, 3), \
                   stride=(2, 2), padding='valid', weights_initializer=initializer)
        X = batch_normalization(X, axis=-1)
        tf.summary.histogram('layer2', X)
        X = conv2d(X, num_outputs=256, kernel_size=(3, 3), \
                   stride=(2, 2), padding='valid', weights_initializer=initializer)
        X = batch_normalization(X, axis=-1)
        tf.summary.histogram('layer3', X)
        flat = flatten(X)
        fc = fully_connected(flat, num_outputs=128, weights_initializer=initializer)
        tf.summary.histogram('fc', fc)
        output = fully_connected(fc, num_outputs=nActions, \
                                 activation_fn=None, weights_initializer=initializer)
        tf.summary.histogram('output', output)
        parameters = {v.name[len(scope.name):]: v for v in \
                             tf.get_collection(key=tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope.name)}
        return parameters, output
    