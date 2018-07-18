# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-18 08:03:25
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-18 10:42:51

'''
use to solve binary classification problems
'''
from functools import reduce

class Sensor(object):
	def __init__(self,features,activator):
		self.activator = activator
		self.weights = [0.0 for _ in range(features)]
		self.bias = 0.0

	def train(self,train_data,labels,iteration,lr):
		for i in range(iteration):
			self.one_iteration(train_data,labels,lr)

	def predict_data(self,data):
		labelValue = self.bias
		for i in range(len(data)):
			labelValue = labelValue + data[i] * list(self.weights)[i]
		return self.activator(labelValue)

	'''
	use Ordinary Least Squares as loss function
	'''
	def update_weights_bias(self,data,predictLabel,label,lr):
		delta = label - predictLabel
		self.weights = list(map(
			lambda x: x[1] + lr * delta * x[0],
			zip(data,self.weights)))
		self.bias += lr * delta

	def one_iteration(self,train_data,labels,lr):
		for i in range(len(train_data)):
			predictLabel = self.predict_data(train_data[i])
			self.update_weights_bias(train_data[i],predictLabel,labels[i],lr)

	'''
	override function
	print object.default transfer
	'''
	def __str__(self):
		return "weights\t:%s\nbias\t:%f\n" %(self.weights,self.bias)


'''
relu activator function
'''
def activator_fn(x):
	return 1 if x > 0 else 0

#return and operation train data
def getDataSet():
	train_data = [
		[0,0],
		[0,1],
		[1,0],
		[1,1]
		]
	labels = [0,0,0,1]
	return train_data,labels

def train_and_operation():
	train_data,labels = getDataSet()
	if len(train_data) < 0 :
		return "no data"
	else:
		sensor = Sensor(len(train_data[0]),activator_fn)
		sensor.train(train_data,labels,10,0.1)
		return sensor

if __name__ == "__main__":
	sensor = train_and_operation()
	print(sensor)
	print('[0,0]-> %d' %(sensor.predict_data([0,0])))
	print('[0,1]-> %d' %(sensor.predict_data([0,1])))
	print('[1,0]-> %d' %(sensor.predict_data([1,0])))
	print('[1,1]-> %d' %(sensor.predict_data([1,1])))


