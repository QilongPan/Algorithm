# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-30 19:02:14
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-31 20:53:12

import tensorflow as tf
import numpy as np 
from game import Board,Game
from mcts_alphaZero import MCTSPlayer

class EvaluationValueNet(object):
	def __init__(self,board_height,board_width,model_file = None):
		self.board_width = board_width
		self.board_height = board_height
		self.win_piece_num = 3
		self.board = Board(row = self.board_height,column = self.board_width,win_piece_num = self.win_piece_num)
		self.game = Game(self.board)
		self.x = tf.placeholder("float",[None,self.board_width * self.board_height])
		self.W = tf.Variable(tf.zeros([self.board_height*self.board_width,1]))
		self.b = tf.Variable(tf.zeros([3]))
		self.y = tf.matmul(self.x,self.W) + self.b
	#	self.y = tf.nn.softmax(tf.matmul(self.x,self.W) + self.b)
		self.y_ = tf.placeholder("float",[None,1])
		self.cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y))
		self.train_step = tf.train.GradientDescentOptimizer(0.01).minimize(self.cross_entropy)
		self.session = tf.Session()
		self.init = tf.global_variables_initializer()
		self.session.run(self.init)
		'''
		self.saver = tf.train.Saver()
		if model_file is not None:
			self.restore_model(model_file)
		
		with tf.Session as sess:
			sess = tf.Session()
			sess.run(init)
			self.saver = tf.train.Saver()
			if model_file is not Node:

			for i in range(1000):
				train_x,train_y = self.collect_selfplay_data()
				sess.run(train_step,feed_dict = {x:train_x,y_:train_y})
		'''
	def collect_selfplay_data(self,n_games = 1):
		states = []
		winners = []
		for i in range(n_games):
			player1 = MCTSPlayer()
			player2 = MCTSPlayer()
			returnX,returnY = self.game.start_self_play(player1,player2)
			for m in range(len(returnX)):
				states.append(returnX[m])
				winners.append(returnY[m])
			self.game.board.init_board()
		return states,winners

	def trainStep(self):
			train_x,train_y = self.collect_selfplay_data()
			train_x = np.array(train_x)
			train_y = np.array(train_y).reshape(len(train_x),1)
			self.session.run(self.train_step,feed_dict = {self.x:train_x,self.y_:train_y})
	def save_model(self,model_path):
		self.saver.save(self.session,model_path)

	def restore_model(self,model_path):
		self.saver.restore(self.session,model_path)





