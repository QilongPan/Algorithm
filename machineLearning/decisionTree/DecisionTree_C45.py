# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-08-15 07:39:28
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-08-15 07:43:37
from math import log
import operator
class C45(object):
	def __init__(self):
		pass
	def calcShannonEnt(self,dataSet):
		numEntries = len(dataSet)
		labelCounts = {}
		for featVec in dataSet:
			currentLabel = featVec[-1]
			if currentLabel not in labelCounts.keys():
				labelCounts[currentLabel] = 0
			labelCounts[currentLabel] += 1
		shannonEnt = 0.0
		for key in labelCounts:
			prob = float(labelCounts[key])/numEntries
			shannonEnt -= prob * log(prob,2)
		return shannonEnt

	def splitDataSet(self,dataSet,axis,value):
		retDataSet = []
		for featVec in dataSet:
			if featVec[axis] == value:
				#delete axis index element
				reducedFeatVec = featVec[:axis]
				reducedFeatVec.extend(featVec[axis+1:])
				retDataSet.append(reducedFeatVec)
		return retDataSet

	def chooseBestFeatureToSplit(self,dataSet):
		numFeatures = len(dataSet[0]) - 1
		baseEntropy = self.calcShannonEnt(dataSet)
		bestInfoGain = 0.0
		bestFeature = -1
		for i in range(numFeatures):
			featList = [example[i] for example in dataSet]
			#remove duplicate elements
			uniqueVals = set(featList)
			newEntropy = 0.0
			splitInfo = 0.0
			for value in uniqueVals:
				subDataSet = self.splitDataSet(dataSet,i,value)
				prob = len(subDataSet)/float(len(dataSet))
				newEntropy += prob * self.calcShannonEnt(subDataSet)
				splitInfo -= prob * log(prob,2)
			#get information gain rate.this is different id3
			infoGain = (baseEntropy - newEntropy)/splitInfo 
			if infoGain > bestInfoGain:
				bestInfoGain = infoGain
				bestFeature = i
		return bestFeature

	def majorityCnt(self,classList):
		classCount = {}
		for vote in classList:
			if vote not in classCount.keys():
				classCount[vote] = 0
			classCount[vote] += 1
		sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse= True)
		return sortedClassCount[0][0]

	def createTree(self,dataSet,labels):
		classList = [example[-1] for example in dataSet]
		if classList.count(classList[0]) == len(classList):
			return classList[0]
		if len(dataSet[0]) == 1:
			return self.majorityCnt(classList)
		bestFeat = self.chooseBestFeatureToSplit(dataSet)
		bestFeatLabel = labels[bestFeat]
		myTree = {bestFeatLabel:{}}
		del(labels[bestFeat])
		featValues = [example[bestFeat] for example in dataSet]
		uniqueVals = set(featValues)
		for value in uniqueVals:
			subLabels = labels[:]
			myTree[bestFeatLabel][value] = self.createTree(self.splitDataSet(dataSet,bestFeat,value),subLabels)
		return myTree

	def getNumLeafs(self,myTree):
		numLeafs = 0
		firstStr = myTree.keys()[0]
		secondDict = myTree[firstStr]
		for key in secondDict.keys():
			if type(secondDict[key]).__name__ == 'dict':
				numLeafs = 1 + getNumLeafs(secondDict[key])
			else:
				numLeafs += 1
		return numLeafs

	def getTreeDepth(self,myTree):
		maxDepth = 0
		firstStr = myTree.keys()[0]
		secondDict = myTree[firstStr]
		for key in secondDict.keys():
			if type(secondDict[key]).__name__ == 'dict':
				thisDepth = 1 + getTreeDepth(secondDict[key])
			else:
				thisDepth = 1
			if thisDepth > maxDepth:
				maxDepth = thisDepth
		return maxDepth

def creatDataSet():
	dataSet = [[1,1,'yes'],
			[1,1,'yes'],
			[1,0,'no'],
			[0,1,'no'],
			[0,1,'no']]
	labels = ['no surfacing','flippers']
	return dataSet,labels

if __name__ == '__main__':
	myDat,labels = creatDataSet()
	decisionTree = C45()
	print(decisionTree.createTree(myDat,labels))