from __future__ import annotations
from typing import Any, List
from operator import lt, gt

class BinaryHeap:
	"""Binary heap
	
	The BinaryHeap is an implementation of the binary heap data structure
	as outlined in `<https://en.wikipedia.org/wiki/Binary_heap>`_

	It may hold any data structure which supports `comparison operators`_

	.. _comparison operators: https://docs.python.org/3/reference/datamodel.html#object.__lt__
	"""

	MAX_HEAP = 0
	MIN_HEAP = 1

	def __init__(self, type):
		self.heap = []
		self.current_size = 0
		self.comparator = gt if type == BinaryHeap.MAX_HEAP else lt
	
	def heapify(self, to_heap: List[Any]) -> None:
		"""Build a heap from list
		
		Given an list use that list to build the inner state of the heap

		:param to_heap: [description]
		:type to_heap: List[Any]
		:rtype: None
		"""
		self.heap = to_heap
		self.current_size = len(to_heap)
		idx = (self.current_size - 1) // 2 
		for idx in range((self.current_size - 1) // 2, -1, -1):
			self.__bubble_down(idx)
	
	def __bubble_down(self, start_idx):
		idx = start_idx
		while idx < self.current_size:
			left_child = 2 * idx + 1
			right_child = 2 * idx + 2
			swap_with = -1 # sentinel value

			if left_child < self.current_size\
				and self.comparator(self.heap[left_child], self.heap[idx]):
				swap_with = left_child
			if right_child < self.current_size\
				and self.comparator(self.heap[right_child], self.heap[idx]):
				swap_with = right_child

			if swap_with != -1:
				self.heap[swap_with], self.heap[idx] = self.heap[idx], self.heap[swap_with]
				idx = swap_with
			else:
				break

	
	def insert(self, value: Any) -> self:
		"""Inserts a value according to the comparator heuristic
		
		Given a value use comparator to put the value in the heap
		so that it still respects the heap property
		
		:param value: The value to heapify
		:type value: Any 
		:return: [description]
		:rtype: self
		"""
		self.heap.append(value)
		self.current_size = self.current_size + 1
		idx = self.current_size - 1
		stop = False

		while not stop and idx != 0:
			parent = (idx - 1) // 2
			if self.comparator(self.heap[parent], self.heap[idx]):
				stop = True
			else:
				self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
				idx = parent
		
		return self