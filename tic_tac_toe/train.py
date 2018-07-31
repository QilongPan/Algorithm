# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-31 19:45:43
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-31 20:21:41

from __future__ import print_function
import numpy as np 
from game import Board,Game 
from evaluation_softmax_net_tensorflow import EvaluationValueNet

class TrainPipeline():
	def __init__(self,init_model = None):
		self.board_row = 3
		self.board_column = 3
		self.win_piece_num = 3
		self.board = Board(row = self.board_row,column = self.board_column,win_piece_num = self.win_piece_num)
		self.game = Game(self.board)
		self.game_batch_num = 50
		self.play_batch_num = 1
		self.epochs = 5

	def run(self):
		policy_value_net = EvaluationValueNet(self.board_row,self.board_column)
		policy_value_net.trainStep()


if __name__ == "__main__":
	training_pipeline = TrainPipeline()
	training_pipeline.run()