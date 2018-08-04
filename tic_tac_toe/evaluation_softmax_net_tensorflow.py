# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-30 19:02:14
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-08-04 11:59:11

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
		self.in_units = self.board_width * self.board_height
		self.h1_units = 5
		self.W1 = tf.Variable(tf.truncated_normal([self.in_units,self.h1_units],stddev = 0.1))
		self.b1 = tf.Variable(tf.zeros([self.h1_units]))
		self.W2 = tf.Variable(tf.zeros([self.h1_units,3]))
		self.b2 = tf.Variable(tf.zeros([3]))
		self.x = tf.placeholder(tf.float32,[None,self.in_units])
		self.keep_prob = tf.placeholder(tf.float32)
		self.hidden1 = tf.nn.relu(tf.matmul(self.x,self.W1) + self.b1)
		self.hidden1_drop = tf.nn.dropout(self.hidden1,self.keep_prob)
		self.y = tf.nn.softmax(tf.matmul(self.hidden1_drop,self.W2) + self.b2)
		self.y_ = tf.placeholder(tf.float32,[None,3])
		self.cross_entropy = tf.reduce_sum(self.y_ * tf.log(self.y))
		self.train_step = tf.train.AdagradOptimizer(0.01).minimize(self.cross_entropy)
		self.session = tf.InteractiveSession()
		tf.global_variables_initializer().run()
		self.saver = tf.train.Saver()

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

	def trainStep(self,game_batch_num):
		for i in range(game_batch_num):
			train_x,train_y = self.collect_selfplay_data()
			train_x = np.array(train_x)
			train_y = np.array(train_y).reshape(len(train_x),3)
			self.train_step.run({self.x:train_x,self.y_:train_y,self.keep_prob:0.75})
		self.save_model('./checkpoint_dir/MyModel')

	def predict(self):
		new_saver = tf.train.import_meta_graph('./checkpoint_dir/MyModel.meta')
		new_saver.restore(self.session,tf.train.latest_checkpoint('./checkpoint_dir'))
		train_x,train_y = self.collect_selfplay_data()
#		train_x = [[2,0,0,2,1,0,1,0,1]]
		train_x = np.array(train_x)
		train_y = np.array(train_y).reshape(len(train_x),3)
		print(train_x)
		print(train_y)
		correct_prediction = tf.equal(tf.argmax(self.y,1),tf.argmax(self.y_,1))
		print(self.session.run(self.y,feed_dict = {self.x:train_x,self.keep_prob:0.75}))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#		print(accuracy.eval({self.x:train_x,self.y_:train_y,keep_prob:1.0}))
#		print(train_x)
#		print(train_y)


	def save_model(self,model_path):
		self.saver.save(self.session,model_path)

	def restore_model(self,model_path):
		self.saver.restore(self.session,model_path)





