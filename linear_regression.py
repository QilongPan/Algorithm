# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-18 11:20:40
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-18 13:33:34
'''
linear regression
'''

class LinearRegression(object):
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
			labelValue = labelValue + data[i] * self.weights[i]
		return self.activator(labelValue)
	'''
	use Ordinary Least Squares as loss function
	'''
	def update_weights_bias(self,data,predictLabel,label,lr):
		delta = label - predictLabel
		for i in range(len(self.weights)):
			self.weights[i] = self.weights[i] + lr * delta * data[i]
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
step function as activator function
'''
def activator_fn(x):
	return x

'''
init data
'''
def get_dataset():
	train_datas = [
		[1],
		[2],
		[3],
		[4],
		[5]
	]
	labels = [210,410,610,810,1010]
	return train_datas,labels

def train_and_operation():
	train_data,labels = get_dataset()
	if len(train_data) < 0 :
		return "no data"
	else:
		linearRegression = LinearRegression(len(train_data[0]),activator_fn)
		linearRegression.train(train_data,labels,100000,0.01)
		return linearRegression

def train_data():
	train_datas, labels = get_dataset()

if __name__ == "__main__":
	linearRegression = train_and_operation()
	print(linearRegression)
	print('Work 3.4 years,monthly salary = %.2f' %(linearRegression.predict_data([6])))