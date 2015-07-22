#!/usr/bin/python
#### A Minium heap structure in python supporting insertion, deletion, looking for the Min
#### and replace the Min with a given number.
#### Author: Ni Shuai Version: 1.0

#### it is hard to deal with indexing with the first value in the heap[0], so the first value
#### in the heap is considered to be of index 1, otherwise the computing will take a bit longer.
class Min_heap:
	def __init__(self, array=[]):
		self.array=[0]
		self.length=1
		for i in array:
			self.insert(i)

	def insert(self, number):
		self.length+=1			
		self.array=self.array+[number]
		self.check_up(self.length-1)

	def check_up(self, index):
		if self.array[index//2]>self.array[index]:
			self.array[index//2],self.array[index]=self.array[index],self.array[index//2]
			self.check_up((index-1)//2)

	def replace_min(self, number):
		self.array[1]=number
		self.check_down(1)

	def check_down(self, index):
		child1=2*index; child2=2*index+1
		if child1>self.length-1:
			return	
		if child1==self.length-1:
			if self.array[index]>self.array[child1]:
				self.array[index],self.array[child1]=self.array[child1],self.array[index]
				return	
		if self.array[index]>self.array[child1]:
			if self.array[index]>self.array[child2]:
				if self.array[child1]>self.array[child2]:
					self.array[index],self.array[child2]=self.array[child2],self.array[index]
					self.check_down(child2)
				else:
					self.array[index],self.array[child1]=self.array[child1],self.array[index]
					self.check_down(child1)
			else:
					self.array[index],self.array[child1]=self.array[child1],self.array[index]
					self.check_down(child1)
		else:
			if self.array[index]>self.array[child2]:
				self.array[index],self.array[child2]=self.array[child2],self.array[index]
				self.check_down(child2)
			else:
				pass
#### just some sanity test				
aa=Min_heap([3,4,1,1,2,0,8,5,46,2,33,2,33,44,5,4,1,8,0,5])
aa.insert(0)
aa.replace_min(88)
aa.replace_min(10000)
print aa.length
print aa.array
