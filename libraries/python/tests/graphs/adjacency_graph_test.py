import unittest

from python.graphs.adjacency_graph import AdjacencyGraph

class TestAdjacencyGraph(unittest.TestCase):
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

	def test_hashable_values(self):
		tupleVertex = ('tuple', 'test')
		self.graph.addVertex(1).addVertex(2).addVertex(tupleVertex)
		self.graph.addEdge(1,2).addEdge(tupleVertex, 2)

		def hashing(self):
			return 10000 + self.value

		def const(self, value):
			self.value = value if value == 1 else 10

		HashableClass = type("HashableClass", (object,), {
			'__init__': const,
			'__hash__': hashing,
			'__repr__': lambda self: 'HashableClass({:d})'.format(self.value),
			'__str__': lambda self: repr(self),
			'__eq__': lambda self, other: self.value == other.value
		})

		self.graph.addVertex(HashableClass(1)).addVertex(3)\
			.addVertex(HashableClass(2)).addVertex(4)
		self.graph.addEdge(HashableClass(1), 3)
		self.graph.addEdge(HashableClass(2), 4)
		self.assertEqual(
			"\n".join([
				"1 -> [2]", '2 -> []', "('tuple', 'test') -> [2]",
				"HashableClass(1) -> [3]", "3 -> []", "HashableClass(10) -> [4]", "4 -> []"
			]),
			str(self.graph)
		)

	def test_simple_node_values_shortest_path(self):
		self.graph.addVertex(4).addVertex(5).addVertex(2).addVertex(1)
		self.graph.addEdge(4,5).addEdge(4,2).addEdge(5,2).addEdge(2,1)

		self.assertEqual([5,2,1], self.graph.shortestPath(4, 1))