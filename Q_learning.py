# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-18 14:20:05
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-18 16:02:39
# 
#example url :https://wenku.baidu.com/view/0102fbdd43323968001c92e5.html
import random
#get Reward matrix
def train_data():
	#have six rooms. 0 is room(row index) connected room(column index),-1 is room(row index) not connected room(column index),
	#100 is room(row index) connected last location
	#
	reward = [
		[-1,-1,-1,-1,0,-1],
		[-1,-1,-1,0,-1,100],
		[-1,-1,-1,0,-1,-1],
		[-1,0,0,-1,0,-1],
		[0,-1,-1,0,-1,100],
		[-1,0,-1,-1,0,100]
	]
	return reward

def train(iterator,Q,R,rate,endState):
	for i in range(iterator):
		one_iterator(random.randint(0,len(R)-1),Q,R,rate,endState)

def one_iterator(startState,Q,R,rate,endState):
	while True:
		actions = get_actions(R,startState)
		next_action = actions[random.randint(0,len(actions)-1)]
		max_q = max(Q[next_action])
		Q[startState][next_action] = R[startState][next_action] + rate * max_q
		if next_action == endState :
			break
		else:
			startState = next_action

def get_actions(R,state):
	actions = []
	for i in range(len(R[state])):
		if R[state][i] >= 0:
			actions.append(i)
	return actions

def get_best_action(Q,state):
	max_q = 0
	best_action = 0
	for i in range(len(Q[state])):
		if Q[state][i] > max_q :
			max_q = Q[state][i]
			best_action = i
	return best_action

def get_Q(row,column):
	Q = [[0.0 for _ in range(row)] for _ in range(column)]
	return Q

#main function
if __name__ == "__main__":
	R = train_data()
	Q = get_Q(len(R),len(R[0]))
	endState = len(R) - 1
	train(1000,Q,R,0.8,len(R)-1)
	print(Q)
	while True:
		startState = int(input("Please input start state:"))
		print(startState,end='')
		print("->",end='')
		while True:
			best_action = get_best_action(Q,startState)
			print(best_action,end='')
			print("->",end='')			
			if best_action == endState:
				print("out")
				break
			else:
				startState = best_action
		flag = int(input("continue test,yes input 1,no input other number:"))
		if flag != 1:
			break


	
	