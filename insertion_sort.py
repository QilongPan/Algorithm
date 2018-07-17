# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-17 19:21:04
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-17 20:16:36

#insert sort
def insertion_sort(temp):
    if len(temp) <= 1:
    	pass
    else:
    	for i in range(1,len(temp)):
			key = temp[i]
			index = i
			for j in range(i-1,-1,-1):
				if key < temp[j]:
					temp[j+1] = temp[j]
					index = j
			temp[index] = key

#main function
if __name__ == "__main__":
	temp = [4,1,3,7,6,2]
	insertion_sort(temp)
	print(temp)
