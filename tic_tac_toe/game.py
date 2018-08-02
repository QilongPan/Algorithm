# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-20 10:02:47
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-08-02 08:06:37
from __future__ import print_function
import numpy as np 
import random

class Board(object):
	#row:board row, column:board column ,win_chess_num:how many pieces to win
	def __init__(self,**kwargs):
		#if dict exist row value,return row.if not exidt return 3
		self.row = int(kwargs.get('row',3))
		self.column = int(kwargs.get('column',3)) 
		self.win_piece_num = int(kwargs.get('win_piece_num',3))
		#save already play piece .
		#example:states = {0:1,1:2,2:1,3:2} key is location(row*colum),value is palyer
		self.states = {}
		#player1 and player2
		self.players = [1,2]

	def init_board(self,start_player = 0):
		if self.row < self.win_piece_num or self.column < self.win_piece_num:
			raise Exception('board row and colum can not be'
							'less than {}'.format(self.win_piece_num))
		self.current_player = self.players[start_player]
		#empty pieces on board
		self.availables = list(range(self.row * self.column))
		#save already play piece .
		#example:states = {0:1,1:2,2:1,3:2} key is location(row*colum),value is palyer
		self.states = {}
		self.last_move = -1

	def get_current_player(self):
		return self.current_player

	def location_to_move(self,location):
		if len(location) != 2:
			return -1
		i = location[0]
		j = location[1]
		move = i * self.column + j
		if move not in range(self.row * self.column):
			return -1
		return move

	def current_state(self):
		state = np.zeros(self.row * self.column)
		if self.states:
			for key,value in self.states.items():
				state[key] = value
		return state

	def do_move(self,move):
		self.states[move] = self.current_player
	#	print("enter%d" %(move))
		self.availables.remove(move)
		self.current_player = (
			self.players[0] if self.current_player == self.players[1]
			else self.players[1]
			)
		self.last_move = move

	def has_a_winner(self):
		width = self.column
		height = self.row
		states = self.states
		n = self.win_piece_num

		moved = list(set(range(width * height)) - set(self.availables))
		if len(moved) < self.win_piece_num + 2:
		    return False, -1

		for m in moved:
		    #行
			h = m // width
		    #列
			w = m % width
			player = states[m]
			'''
			set具有去重功能，如果连续五个位置的值都是1或者2，那么长度为1
			'''
			if (w in range(width - n + 1) and
			        len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
			    return True, player

			if (h in range(height - n + 1) and
			        len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
			    return True, player

			if (w in range(width - n + 1) and h in range(height - n + 1) and
			        len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
			    return True, player

			if (w in range(n - 1, width) and h in range(height - n + 1) and
			        len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
			    return True, player

		return False, -1

	def game_end(self):
		win,winner = self.has_a_winner()
		if win:
			return True,winner
		elif not len(self.availables):
			return True,-1
		return False,-1




class Game(object):

	def __init__(self,board,**kwargs):
		self.board = board

	def graphic(self,board,player1,player2):
		row = board.row
		column = board.column
		#fill string lenth is 3
		print("Player",player1,"with X".rjust(3))
		print("Player",player2, "with O".rjust(3))
		print()
		for i in range(column):
			#{0:8} make string length is 8
			print("{0:8}".format(i),end='')
		print('\r\n')
		for i in range(row - 1,-1,-1):
			print("{0:4d}".format(i),end='')
			for j in range(column):
				location = i * column + j
				p = board.states.get(location,-1)
				if p == player1:
					print('X'.center(8),end = '')
				elif p == player2:
					print('O'.center(8),end = '')
				else:
					print('_'.center(8),end = '')
			print('\r\n\r\n')



	#start_player is 0 player1 first,is 1 player2 first
	def start_play(self,player1,player2,start_player,is_shown = 1):
		if start_player not in (0,1):
			raise Exception('start_player should be either 0(player1 first)'
							'or 1 (playerr2 first)')
		self.board.init_board(start_player)
		p1,p2 = self.board.players
		player1.set_player_ind(p1)
		player2.set_player_ind(p2)
		players = {p1:player1,p2:player2}
		if is_shown:
			self.graphic(self.board,p1,p2)
		while True:
			current_palyer = self.board.get_current_player()
			player_in_turn = players[current_palyer]
			move = player_in_turn.get_action(self.board)
			self.board.do_move(move)
			if is_shown:
				self.graphic(self.board,player1.player,player2.player)
			end,winner = self.board.game_end()
			if end:
				if is_shown:
					if winner != -1:
						print("Game end. Winner is",players[winner])
					else:
						print("Game end. Tie")
				return winner

	def start_self_play(self,player1,player2,start_player = 0,is_shown = 0):
		start_player = random.randint(0,1)
		self.board.init_board(start_player)
		p1,p2 = self.board.players
		player1.set_player_ind(p1)
		player2.set_player_ind(p2)
		players =  {p1:player1,p2:player2}
		if is_shown:
			self.graphic(self.board,p1,p2)
		states = []
		while True:
			current_player = self.board.get_current_player()
			player_in_turn = players[current_player]
			move = player_in_turn.get_action(self.board)
			states.append(self.board.current_state())
			self.board.do_move(move)
			if is_shown:
				self.graphic(self.board,p1,p2)
			end,winner = self.board.game_end()
			if end:
				states.append(self.board.current_state())
				y = [0,0,0]
				ys = []
				for i in range(len(states)):
					if winner == -1:
						y[0] = -1
					elif winner == 1:
						y[1] = 1
					else:
						y[2] = 2
					ys.append(y)
				return states,ys













