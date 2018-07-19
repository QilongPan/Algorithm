# -*- coding: utf-8 -*-
# @Author: Qilong Pan
# @Date:   2018-07-19 18:06:14
# @Last Modified by:   Qilong Pan
# @Last Modified time: 2018-07-19 20:36:55
# Find the largest subarray

def find_max_corrsing_subarray(arr,low,mid,high):
	left_sum = -1000000
	sum = 0
	max_left = mid
	for i in range(mid,low-1,-1):
		sum = sum + arr[i]
		if sum > left_sum:
			left_sum = sum
			max_left = i
	right_sum = -1000000
	max_right = mid
	sum = 0
	for i in range(mid+1,high+1):
		sum = sum + arr[i]
		if sum > right_sum:
			right_sum = sum
			max_right = mid
	return max_left,max_right,left_sum+right_sum

def find_maximum_subarray(arr,low,high):
	if high == low:
		return low,high,arr[low]
	else:
		mid = int((low+high)/2)
		left_low,left_high,left_sum = find_maximum_subarray(arr,low,mid)
		right_low,right_high,right_sum = find_maximum_subarray(arr,mid+1,high)
		cross_low,cross_high,cross_sum = find_max_corrsing_subarray(arr,low,mid,high)
		if left_sum >= right_sum and left_sum >= cross_sum:
			return left_low,left_high,left_sum
		elif right_sum >= left_sum and right_sum >= cross_sum:
			return right_low,right_high,right_sum
		else:
			return cross_low,cross_high,cross_sum

if __name__ == "__main__":
	arr = [13,-3,-25,20,-3,-16,-23,-12,24,-23,24,18,-50,20,-7,12,-5,-22,15,-4,7]
	start_index,end_index,max_sum = find_maximum_subarray(arr,0,len(arr)-1)
	print("start index:%d\t\tmax sum is %d" %(start_index,max_sum))


