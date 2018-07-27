# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-27 09:03:44
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-27 18:11:03

import numpy as np 
import tensorflow as tf 
import math

class EvaluationValueNet(object):
	def __init__(self,board_width,board_height,model_file = None):
		self.board_width = board_width
		self.board_height = board_height
		self.input_board = tf.placeholder([None,self.board_height,self.board_width,1])
		#第1,2个参数代表卷积核参数大小，第3个参数是图像通道数，第4个参数代表卷积核的数目
		self.W_conv1 = self.weight_varible([5,5,1,32])
		#每1个卷积核都有其对应的偏执量
		self.b_conv1 = self.bias_variable([32])
		self.h_conv1 = tf.nn.relu(self.conv2d(self.input_board,self.W_conv1)+self.b_conv1)
		self.h_pool1 = self.max_pool_2x2(self.h_conv1)
		#第二层
		self.W_conv2 = self.weight_varible([5,5,32,64])
		self.b_conv2 = self.bias_variable([64])
		self.h_conv2 = tf.nn.relu(self.conv2d(self.h_pool1,self.W_conv2) + self.b_conv2)
		self.h_pool2 = self.max_pool_2x2(self.h_conv2)

		#全连接层
		self.W_fc1 = self.weight_varible([math.ceil(math.ceil(self.board_height/2)/2) * math.ceil(math.ceil(self.board_height/2)/2) *64,1024 ])
		self.b_fc1 = self.bias_variable([1024])
		self.h_pool2_flat = tf.reshape(self.h_pool2,[-1,math.ceil(math.ceil(self.board_height/2)/2) * math.ceil(math.ceil(self.board_height/2)/2) *64])
		self.h_fc1 = tf.nn.relu(tf.matmul(self.h_pool2_flat,self.W_fc1) + self.b_fc1)

		self.keep_prob = tf.placeholder(tf.float32)
		self.h_fc1_drop = tf.nn.dropout(self.h_fc1,self.keep_prob)

		self.W_fc2 = self.weight_varible([1024,self.board_height*self.board_width])
		self.b_fc2 = self.bias_variable(self.board_height * self.board_width)

		self.y_conv = tf.nn.softmax(tf.matmul(self.h_fc1_drop,self.W_fc2) + self.b_fc2)

		self.cross_entropy = -tf.reduce_sum(self.y * tf.log(self.y_conv))
		self.train_step = tf.train.AdamOptimizer(1e-3).minimize(self.cross_entropy)
		self.correct_prediction = tf.equal(tf.argmax(self.y_conv,1),tf.argmax(self.y,1))
		self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction,tf.float32))
		
		self.saver = tf.train.Saver()
		init = tf.global_variables_initializer()
		self.sess.run(init)
		if model_file is not None:
			self.restore_model(model_file)


	def conv2d(self,x,W):
		#strides=[b,h,w,c]  
		#b表示在样本上的步长默认为1，也就是每一个样本都会进行运算
		#h表示在高度上的默认移动步长为1，这个可以自己设定，根据网络的结构合理调节。
		#w表示在宽度上的默认移动步长为1，这个同上可以自己设定。
		#c表示在通道上的默认移动步长为1，这个表示每一个通道都会进行运算。
		return tf.nn.conv2d(x,W,strides = [1,1,1,1],padding = 'SAME')

	def max_pool_2x2(self,x):
		# 池化卷积结果（conv2d）池化层采用kernel大小为2*2，步数也为2，周围补0，取最大值。数据量缩小了4倍
		return tf.nn.max_pool(x,ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')

	#偏执变量
	def bias_variable(self,shape):
		initial = tf.constant(0.1,shape = shape)
		return tf.Variable(initial)

	def weight_varible(self,shape):
		initial = tf.truncated_normal(shape,stddev = 0.1)
		return tf.Variable(initial)

	def save_model(self,model_path):
		self.saver.save(self.session,model_path)

	def restore_model(self,model_path):
		self.saver.restore(self.session,model_path)




