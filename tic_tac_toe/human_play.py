# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-20 10:10:57
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-26 07:42:31
#
from __future__ import print_function
from game import Board,Game
from mcts_alphaZero import MCTSPlayer

class Human(object):
	#player is human tag
	def __init__(self):
		self.player = None

	def set_player_ind(self,p):
		self.player = p

	def get_action(self,board):
		try:
			location = input("Your move: ")
			if isinstance(location, str):  # for python3
			    location = [int(n, 10) for n in location.split(",")]
			move = board.location_to_move(location)
		except Exception as e:
			move = -1
		if move == -1 or move not in board.availables:
			print("invalid move")
			move = self.get_action(board)
		return move

def run(row,column,win_piece_num,start_player):
	board = Board(row = row,column = column,win_piece_num = win_piece_num)
	game = Game(board)
	human = Human()
	mcts_player = MCTSPlayer()
#	human2 = Human()
	game.start_play(human,mcts_player,start_player,is_shown = 1)


if __name__ == '__main__':
	win_piece_num = 3
	row = 3
	column = 3
	start_player = int(input("please choose first player(input 0 is human first,1 is computer first):"))
	run(row,column,win_piece_num,start_player)