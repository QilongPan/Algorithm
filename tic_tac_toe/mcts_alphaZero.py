# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-20 10:31:13
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-23 20:07:50

class TreeNode(object):

	def __init__(self,parent,prior_p):
		self.parent = parent
		self._children = {}
		self.n_visits = 0
		self._Q = 0
		self._u = 0
		self._P = prior_p

	def expand(self,action_priors):
		pass
class MCTS(object):
	def __init__(self):
		pass
		
class MCTSPlayer(object):
	def __init__(self):
		pass

	def set_player_ind(self,p):
		self.player = p

	def get_action(self,board):
		pass
