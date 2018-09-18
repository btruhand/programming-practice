import unittest
from python.heaps.binary_heap import BinaryHeap

class TestBinaryHeap(unittest.TestCase):
	def assertMaxHeapProperty(self, heap, parent):
		heap_size = len(heap)
		left_child = 2 * parent + 1
		right_child = 2 * parent + 2
		if left_child < heap_size:
			self.assertGreaterEqual(
				heap[parent],
				heap[left_child],
				f"Max heap property not satisfied at index {parent} and left child {left_child}"
			)
			self.assertMaxHeapProperty(heap, left_child)
		if right_child < heap_size:
			self.assertGreaterEqual(
				heap[parent],
				heap[right_child],
				f"Max heap property not satisfied at index {parent} and right child {right_child}"
			)
			self.assertMaxHeapProperty(heap, right_child)
	
	def assertMinHeapProperty(self, heap, parent):
		heap_size = len(heap)
		left_child = 2 * parent + 1
		right_child = 2 * parent + 2
		if left_child < heap_size:
			self.assertLessEqual(
				heap[parent],
				heap[left_child],
				f"Min heap property not satisfied at index {parent} and left child {left_child}"
			)
			self.assertMinHeapProperty(heap, left_child)
		if right_child < heap_size:
			self.assertLessEqual(
				heap[parent],
				heap[right_child],
				f"Min heap property not satisfied at index {parent} and right child {right_child}"
			)
			self.assertMinHeapProperty(heap, right_child)

	def setUp(self):
		self.max_bin_heap = BinaryHeap(BinaryHeap.MAX_HEAP)
		self.min_bin_heap = BinaryHeap(BinaryHeap.MIN_HEAP)
	
	def test_empty_array(self):
		self.max_bin_heap.heapify([])
		self.min_bin_heap.heapify([])

		self.assertEqual([], self.max_bin_heap.heap)
		self.assertEqual([], self.min_bin_heap.heap)
	
	def test_insert_one_element(self):
		self.max_bin_heap.insert(1)
		self.min_bin_heap.insert(1)

		self.assertEqual([1], self.max_bin_heap.heap)
		self.assertEqual([1], self.min_bin_heap.heap)
	
	def test_heapify_three_elements(self):
		self.max_bin_heap.insert(1).insert(2).insert(3)
		self.min_bin_heap.insert(3).insert(2).insert(1)

		self.assertMaxHeapProperty(self.max_bin_heap.heap, 0)
		self.assertMinHeapProperty(self.min_bin_heap.heap, 0)
	
	def test_max_heapify_many_unique_elements(self):
		self.max_bin_heap.insert(10)\
			.insert(120)\
			.insert(70)\
			.insert(15)\
			.insert(8)\
			.insert(14)\
			.insert(-10)\
			.insert(13)\
			.insert(33)\
		
		self.assertMaxHeapProperty(self.max_bin_heap.heap, 0)
	
	def test_min_heapify_many_unique_elements(self):
		self.min_bin_heap.insert(65)\
			.insert(88)\
			.insert(90)\
			.insert(10)\
			.insert(12)\
			.insert(89)\
			.insert(-1)\
			.insert(0)\
			.insert(15)\
		
		self.assertMinHeapProperty(self.min_bin_heap.heap, 0)
	
	def test_max_heapify_unique_and_duplicate_elements(self):
		self.max_bin_heap.insert(100)\
			.insert(53)\
			.insert(65)\
			.insert(13)\
			.insert(53)\
			.insert(100)\
		
		self.assertMaxHeapProperty(self.max_bin_heap.heap, 0)
	
	def test_min_heapify_unique_and_duplicate_elements(self):
		self.max_bin_heap.insert(43)\
			.insert(53)\
			.insert(55)\
			.insert(55)\
			.insert(20)\
			.insert(131)\
			.insert(56)\
			.insert(43)\
			.insert(32)\
		
		self.assertMinHeapProperty(self.min_bin_heap.heap, 0)
	
	def test_max_heapify_from_array(self):
		test_data = [100, 53, 65, 13, 53, 100, 16, 17, 8, 101]
		self.max_bin_heap.heapify(test_data)
		self.assertMaxHeapProperty(self.max_bin_heap.heap, 0)

	def test_min_heapify_from_array(self):
		test_data = [43, 53, 55, 55, 20, 131, 56, 43, 32]
		self.min_bin_heap.heapify(test_data)
		self.assertMinHeapProperty(self.min_bin_heap.heap, 0)