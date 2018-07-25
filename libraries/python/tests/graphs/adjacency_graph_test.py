import unittest
from python.graphs.adjacency_graph import AdjacencyGraph

class TestAdjacencyGraph(unittest.TestCase):
	def hashable_hashing(self):
		return 10000 + hash(self.value)

	def hashable_init(self, value):
		self.value = value

	def hashable_equality(self, other):
		return type(self) == type(other) and self.value == other.value

	HashableClass = type("HashableClass", (object,), {
		'__init__': hashable_init,
		'__hash__': hashable_hashing,
		'__repr__': lambda self: 'HashableClass({:d})'.format(self.value),
		'__str__': lambda self: repr(self),
		'__eq__': hashable_equality
	})

	def setUp(self):
		self.graph = AdjacencyGraph()

	def test_vertex_idempotency(self):
		self.graph.addVertex(1).addVertex(1)

		self.assertEqual('1 -> []', str(self.graph))

	def test_edge_idempotency(self):
		self.graph.addVertex('1').addVertex('2')
		self.graph.addEdge('1','2').addEdge('1','2')

		self.assertEqual("\n".join(["'1' -> ['2']", "'2' -> []"]), str(self.graph))

	def test_edge_no_origin(self):
		self.graph.addVertex('dest')
		with self.assertRaises(Exception, msg="Origin 'origin' is not yet a vertex"):
			self.graph.addEdge('origin', 'dest')

	def test_edge_no_destination(self):
		self.graph.addVertex('origin')
		with self.assertRaises(Exception, msg="Destination 'dest' is not yet a vertex"):
			self.graph.addEdge('origin', 'dest')

	def test_edge_ordering(self):
		self.graph.addVertex(5).addVertex(7).addVertex(6).addVertex(8).addVertex('str')
		self.graph.addEdge(5,6).addEdge(7,8).addEdge(5,8).addEdge('str',7)

		self.assertEqual(
			"\n".join(['5 -> [6, 8]', '7 -> [8]', '6 -> []', '8 -> []', "'str' -> [7]"]),
			str(self.graph)
		)

	def test_edges_with_hashable_vertices(self):
		tupleVertex = ('tuple', 'test')
		self.graph.addVertex(1).addVertex(2).addVertex(tupleVertex)
		self.graph.addEdge(1,2).addEdge(tupleVertex, 2)

		self.graph.addVertex(self.HashableClass(1)).addVertex(3)\
			.addVertex(self.HashableClass(2)).addVertex(4)
		self.graph.addEdge(self.HashableClass(1), 3)
		self.graph.addEdge(self.HashableClass(2), 4)
		self.assertEqual(
			"\n".join([
				"1 -> [2]", '2 -> []', "('tuple', 'test') -> [2]",
				"HashableClass(1) -> [3]", "3 -> []", "HashableClass(2) -> [4]", "4 -> []"
			]),
			str(self.graph)
		)

	def test_shortest_path_to_self(self):
		self.graph.addVertex(1)
		self.graph.addEdge(1, 1)
		self.assertEqual([1], self.graph.shortestPath(1, 1))

	def test_simple_node_values_shortest_path(self):
		self.graph.addVertex(4).addVertex(5).addVertex(2).addVertex(1)
		self.graph.addEdge(4,5).addEdge(4,2).addEdge(5,2).addEdge(2,1)
		self.assertEqual([4,2,1], self.graph.shortestPath(4, 1))

	def test_shortest_path_that_does_not_exist(self):
		self.graph.addVertex(1).addVertex(2).addVertex(3)
		self.graph.addEdge(1, 2).addEdge(2, 3)
		self.assertEqual([], self.graph.shortestPath(3, 1))

	def test_shortest_path_with_loop(self):
		self.graph.addVertex(1).addVertex(2).addVertex(3)
		self.graph.addEdge(1, 2).addEdge(2, 1).addEdge(2, 3).addEdge(3, 3)
		self.assertEqual([1, 2, 3], self.graph.shortestPath(1, 3))

	def test_path_to_self_even_if_no_self_loop_edge(self):
		self.graph.addVertex(1)
		self.assertEqual([1], self.graph.shortestPath(1, 1))

	def test_arbitrary_number_of_edges(self):
		self.graph.addVertex(1).addVertex(5).addVertex(6).addVertex(3).addVertex(4).addVertex(7)
		self.graph.addEdge(1, 5).addEdge(1, 6).addEdge(1, 7).addEdge(5, 4).addEdge(6, 1)\
			.addEdge(5, 5).addEdge(6, 7).addEdge(6, 4).addEdge(7, 4).addEdge(4, 3).addEdge(4, 1)

		self.assertEqual([1,5,4,3], self.graph.shortestPath(1, 3))

	def test_shortest_path_with_complex_hashable_vertices(self):
		tupleVertex = ('1', '2')
		self.graph.addVertex(1).addVertex(self.HashableClass(1)).addVertex(self.HashableClass(2))\
			.addVertex(2).addVertex('2').addVertex(tupleVertex)

		self.graph.addEdge(1, self.HashableClass(1)).addEdge(1, 2).addEdge(2, tupleVertex)\
			.addEdge(tupleVertex, self.HashableClass(2)).addEdge(self.HashableClass(2), '2')

		self.assertEqual([1, 2, tupleVertex, self.HashableClass(2), '2'], self.graph.shortestPath(1, '2'))