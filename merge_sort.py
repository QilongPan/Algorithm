# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-18 18:08:51
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-18 20:14:32

def merge_sort(temp,start,end):
	if start < end:
		mid = int((start+end)/2)
		merge_sort(temp,start,mid)
		merge_sort(temp,mid+1,end)
		merge(temp,start,mid,end)

def merge(temp,start,mid,end):
	left_array = []
	right_array = []
	for i in range(mid-start+1):
		left_array.append(temp[i+start])
	for i in range(mid+1,end+1):
		right_array.append(temp[i])
	current_left_index = 0
	current_right_index = 0
	current_temp_index = start
	while current_left_index < len(left_array) and current_right_index < len(right_array):
		if left_array[current_left_index] <= right_array[current_right_index]:
			temp[current_temp_index] = left_array[current_left_index]
			current_left_index = current_left_index + 1
		else:
			temp[current_temp_index] = right_array[current_right_index]
			current_right_index = current_right_index + 1
		current_temp_index = current_temp_index + 1
	while current_left_index < len(left_array):
		temp[current_temp_index] = left_array[current_left_index]
		current_temp_index = current_temp_index + 1
		current_left_index = current_left_index + 1
	while current_right_index < len(right_array):
		temp[current_temp_index] = right_array[current_right_index]
		current_temp_index = current_temp_index + 1
		current_right_index = current_right_index + 1

#main function
if __name__ == "__main__":
	temp = [2,1,0,5,4,-1,-8,20,19]
	merge_sort(temp,0,len(temp)-1)
	print(temp)