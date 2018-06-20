#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# cnn
# conv1 -> sigmoid -> fc1 -> sm

import numpy as np
from loadFACE import *
import tensorflow as tf
from getImgLite import getImg

def dataExtractorShuffle(data_all, label_all, num):
	
	num_total = data_all.shape[0]
	shuffle_idx = np.random.choice(num_total, num, replace=False)
	data_batch = data_all[shuffle_idx,:]
	label_batch = label_all[shuffle_idx,:]

	return data_batch, label_batch

def dataExtractorBatch(data_all, label_all, num):

  num_total = data_all.shape[0]
  shuffle_idx = np.random.choice(num_total, num_total, replace=False)
  data_all = data_all[shuffle_idx,:]
  label_all = label_all[shuffle_idx,:]
  batch_num = data_all.shape[0]/num

  data_batch = []
  label_batch= []
  for i in range(batch_num):
  	data_batch.append(data_all[num*i:num*(i+1),:])
  	label_batch.append(label_all[num*i:num*(i+1),:])  

  return data_batch, label_batch, batch_num

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 3, 3, 1], padding='VALID')

# main function goes here

fileDir = "/home/yimeng/Documents/dataset/face/cropped_auto"
inputsize = [80, 80]
trte_thresh = 1000
tr_minibatch = 10
epoch = 50
lr = 1e-4
te_batch = 321
num_class = 17
n_kernel = 8
imgmeta = getImg(fileDir, inputsize)

tr_data = imgmeta.dataset[:trte_thresh]
tr_label = imgmeta.labelset[:trte_thresh]
te_data = imgmeta.dataset[trte_thresh:,:]
te_label = imgmeta.labelset[trte_thresh:,:]

# tr_data_out, tr_label_out = dataExtractor(tr_data, tr_label, tr_batch)

# init
x = tf.placeholder(tf.float32, [None, inputsize[0]*inputsize[1]])
x_image = tf.reshape(x, [-1,inputsize[0],inputsize[1],1])  
y_ = tf.placeholder(tf.float32, [None, num_class])

# conv1
W_conv1 = weight_variable([16, 8, 1, n_kernel])
b_conv1 = bias_variable([n_kernel])
h_conv1 = tf.nn.sigmoid(conv2d(x_image, W_conv1) + b_conv1)

#print h_conv1.shape

# fc1
W_fc1 = weight_variable([22*25*n_kernel, num_class])
b_fc1 = bias_variable([num_class])
h_conv1_flat = tf.reshape(h_conv1, [-1, 22*25*n_kernel])
y_fc = tf.matmul(h_conv1_flat, W_fc1) + b_fc1

# softmax
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_fc))
train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_fc,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# run
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

for i in range(epoch):
  print ">>> epoch %d"%i
  tr_data_out, tr_label_out, batch_num = dataExtractorBatch(tr_data, tr_label, tr_minibatch)
  for batch_idx in range(batch_num):

    batch = (tr_data_out[batch_idx], tr_label_out[batch_idx])
    if batch_idx%10 == 0:
      train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1]})
      print "step %d, training accuracy %g"%(batch_idx, train_accuracy)
    train_step.run(feed_dict={x: batch[0], y_: batch[1]})


te_data_out, te_label_out = dataExtractorShuffle(te_data, te_label, te_batch)
print "test accuracy %g"%accuracy.eval(feed_dict={x: te_data_out, y_: te_label_out})
