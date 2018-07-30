# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-30 19:02:14
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-30 20:22:57

import tensorflow as tf 

class EvaluationValueNet(object):
	def __init__(self,board_height,board_width,model_file = Node):
		self.board_width = board_width
		self.board_height = board_height
		self.win_piece_num = 3
		self.board = Board(row = self.board_height,column = self.board_width,win_piece_num = self.win_piece_num)
		self.game = Game(self.board)
		x = tf.placeholder("float",[None,self.board_width * self.board_height])
		W = tf.Variable(tf.zeros([self.board_height*self.board_width,3]))
		b = tf.Variable(tf.zeros([3]))
		y = tf.nn.softmax(tf.matmul(x,W) + b)
		y_ = tf.placeholder("float",[None,3])
		cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
		train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
		init = tf.initialize_all_variables()
		sess = tf.Session()
		sess.run(init)
		for i in range(1000):
			train_x,train_y = self.collect_selfplay_data()
			sess.run(train_step,feed_dict = {x:train_x,y_:train_y})

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
			self.game.init_board()
		return states,winners
			



