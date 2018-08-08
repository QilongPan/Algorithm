# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-20 10:31:13
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-08-08 18:06:21

import random
import math

class TreeNode(object):

	def __init__(self,move):
		self.child = []
		self.visits = 0
		self.win = 0
		self.draw = 0
		self.move = move
		self.best_move = -1


class MCTS(object):
	def __init__(self,board,player_id,n_simulations):
		self.all_simulation_number = n_simulations
		self.current_simulation_number = 0
		self.board = board
		self.player_id = player_id
		self.root = TreeNode(-1)
		self.simulation_result = None

	def search(self):
		while self.current_simulation_number < self.all_simulation_number:
			self.one_simulation(self.root)
			self.current_simulation_number += 1
		'''
		for i in range(len(self.root.child)):
			if self.root.child[i].visits > 0:
				print("move",end='')
				print(self.root.child[i].move,end='')
				print("win:",end='')
				print(self.root.child[i].win,end = '')
				print("visits:",end='')
				print(self.root.child[i].visits,end = '')
				print("winrate:",end='')
				print(self.root.child[i].win/self.root.child[i].visits)
		print(self.root.best_move)
		'''
		return self.root.best_move
	def one_simulation(self,root):
		win,winner = self.board.game_end()
		if not win:
			if root.visits == 0:
				self.simulation_result = self.random_play_game()
			else:
				if len(root.child) == 0:
					self.create_child(root)
				next_child = self.select(root)
				if next_child == -1:
					print("one_simulation error no child")
				else:
					last_move = self.board.last_move
					self.make_move(next_child.move)
					self.one_simulation(next_child)
					self.unmake_move(next_child.move,last_move)
		else:
			self.simulation_result = winner
		root.visits += 1
		self.update_win(root,self.simulation_result)
		if len(root.child) != 0:
			self.set_best_child(root)

	def create_child(self,root):
		for i in range(len(self.board.availables)):
			root.child.append(TreeNode(self.board.availables[i]))

	#random play game 
	def random_play_game(self):
		moves = []
		current_player = self.board.current_player
		last_move = self.board.last_move
		win,winner = None,None
		while True:
			win,winner = self.board.game_end()
			if win:
				break
			else:
				move = self.board.availables[random.randint(0,len(self.board.availables) - 1)]
				moves.append(move)
				self.board.do_move(move)
		#reduction
		for i in range(len(moves)):
			self.board.availables.append(moves[i])
			self.board.states.pop(moves[i])
		self.board.current_player = current_player
		self.board.last_move = last_move
		self.board.availables.sort()
		return winner


	def select(self,root):
		uct_value = 0
		best_value = -1
		best_child = -1
		if len(root.child) == 0:
			print("select no child")
		for i in range(len(root.child)):
			
			if root.child[i].visits > 0:
				win_rate = root.child[i].win / root.child[i].visits
				draw_rate = root.child[i].draw / root.child[i].visits
				expose_value = 1 * math.sqrt(2 * math.log(root.visits)/root.child[i].visits)
				if self.board.current_player == self.player_id:
					uct_value = draw_rate + win_rate + expose_value
				else:
					uct_value = 1 - win_rate + expose_value
			else:
				uct_value = 100 + random.random()
				
		#	uct_value = 100 + random.random()
			if uct_value > best_value:
				best_value = uct_value
				best_child = root.child[i]
		return best_child


	def make_move(self,move):
		self.board.do_move(move)

	def unmake_move(self,move,last_move):
		self.board.availables.append(move)
		self.board.current_player = (
			self.board.players[0] if self.board.current_player == self.board.players[1]
			else self.board.players[1]
			)
		self.board.last_move = last_move
		self.board.states.pop(move)
		self.board.availables.sort()

	def update_win(self,root,simulation_result):
		if simulation_result == self.player_id:
			root.win += 1
		elif simulation_result == -1:
			root.draw += 1

	def set_best_child(self,root):
		best_value = -1
		best_draw_rate = -1
		for i in range(len(root.child)):
			if root.child[i].visits > 0 :
				win_rate = root.child[i].win / root.child[i].visits
				draw_rate = root.child[i].draw / root.child[i].visits
				if win_rate + draw_rate > best_value:
					best_value = win_rate + draw_rate
					root.best_move = root.child[i].move


class MCTSPlayer(object):
	def __init__(self,n_simulations = 2000):
		self.n_simulations = n_simulations
		self.player = None

	def set_player_ind(self,p):
		self.player = p

	def get_player_ind(self):
		return self.player

	def get_action(self,board):
		mcts = MCTS(board,self.player,self.n_simulations)
		move = mcts.search()
		return move
