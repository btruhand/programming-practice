import unittest

from python.graphs.adjacency_graph import AdjacencyGraph

class TestAdjacencyGraph(unittest.TestCase):
	def setUp(self):
		self.graph = AdjacencyGraph()

	def test_idempotency(self):
		self.graph.addEdge('1','2').addEdge('1','2')

		self.assertEqual("'1' -> ['2']", str(self.graph))
	def test_edge_ordering(self):
		self.graph.addEdge(5,6).addEdge(7,8).addEdge(5,8).addEdge('str',7)

		self.assertEqual(
			"\n".join(['5 -> [6, 8]', '7 -> [8]', "'str' -> [7]"]),
			str(self.graph)
		)

	def test_hashable_values(self):
		self.graph.addEdge(1,2).addEdge(('tuple', 'test'),2)

		def hashing(self):
			return 10000 + self.value

		def const(self, value):
			self.value = value if value == 1 else 10

		HashableClass = type("HashableClass", (object,), {
			'__init__': const,
			'__hash__': hashing,
			'__repr__': lambda self: 'HashableClass({:d})'.format(self.value)
		})

		self.graph.addEdge(HashableClass(1), 3)
		self.graph.addEdge(HashableClass(2), 4)
		self.assertEqual(
			"\n".join(["1 -> [2]", "('tuple', 'test') -> [2]", "HashableClass(1) -> [3]", "HashableClass(10) -> [4]"]),
			str(self.graph)
		)

	def test_simple_node_values_shortest_path(self):
		self.graph.addEdge(1, 2).addEdge(4,5).addEdge(4,2).addEdge(5,2).addEdge(2,1)

		self.assertEqual([4,2,1], self.graph.shortestPath(4, 1))