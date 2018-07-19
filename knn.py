# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-19 14:19:43
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-19 15:53:18

import matplotlib.pyplot as plt

class KNN(object):
	def __init__(self):
		pass

	def predict_data(self,data,labels,predict_data,k):
		#计算距离
		distances = []
		for i in range(len(data)):
			sum = 0.0
			for j in range(len(data[i])):
				sum += (data[i][j]-predict_data[0]) ** 2
			distances.append(sum ** 0.5)
		print(distances)
		for i in range(len(distances)-1):
			current_index = i
			current_distance = distances[i]
			current_label = labels[i]
			for j in range(i+1,len(distances)):
				if distances[j] < current_distance:
					current_distance = distances[j]
					current_index = j
					current_label = labels[j]
			if current_index != i:
				distances[current_index] = distances[i]
				distances[i] = current_distance
				labels[current_index] = labels[i]
				labels[i] = current_label

		label_count = {}
		for i in range(k):
			label_count[labels[i]] = label_count.get(labels[i],0) + 1
		max_count = 0
		predict_result = 0
		for label,count in label_count.items():
			if count > max_count:
				max_count = count
				predict_result = label
		return predict_result

def create_data():
	data = [
		[1.0,2.0],
		[1.2,0.1],
		[0.1,1.4],
		[0.3,3.5]
	]
	labels = ['A','A','B','B']
	predict_data = [1.1,0.3]
	return data,labels,predict_data

if __name__ == "__main__":
	data,labels,predict_data = create_data()
	knn = KNN()
	print(knn.predict_data(data,labels,predict_data,3))
	data_x = []
	data_y = []
	predict_x = []
	predict_y = []
	for i in range(len(data)):
		data_x.append(data[i][0])
		data_y.append(data[i][1])
	predict_x.append(predict_data[0])
	predict_y.append(predict_data[1])
	plt.scatter(predict_x,predict_y,color='g',s=25,marker='o')
	plt.scatter(data_x,data_y,color='k',s=25,marker='o')
	plt.xlabel("x")
	plt.ylabel("y")
	plt.show()
	

