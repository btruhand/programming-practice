""" Adjacency Graph Module

.. py:module:: AdjacencyGraph
   :synopsis: Give an object representation of a graph based on an adjacency list
"""

from typing import Hashable, Tuple
from collections import OrderedDict, deque

class AdjacencyGraph:
	"""AdjacencyGraph class

	The adjacency graph is a weight-less directed graph and can store any `Hashable <https://docs.python.org/3.7/glossary.html>`_ value

	Example:

	.. code-block: python
	   :linenos:

	   s = AdjacencyGraph()
	   s.addEdge('1','2')
	   s.addEdge('2','1')
	"""

	def __init__(self):
		self.graph = OrderedDict()

	def addEdge(self, vertexOrigin: Hashable, vertexDestination: Hashable) -> self:
		"""Adds an edge to the graph
		Given an origin and a destination, add an edge to the graph from origin to destination

		:param vertexOrigin: Start of edge
		:type vertexOrigin: Hashable
		:param vertexDestination: End of edge
		:type vertexDestination: Hashable
		:returns: self
		:rtype: AdjacencyGraph

		The function is idempotent. Given the same origin and destination on the same AdjacencyGraph object,
		the resulting graph is the same.

		Example:
		.. code-block: python
		   :linenos:

		   s = AdjacencyGraph()
		   s.addEdge('1','2') # 1 -> 2
		   s.addEdge('1','2') # still 1 -> 2
		"""
		if vertexOrigin not in self.graph:
			self.graph[vertexOrigin] = []

		if vertexDestination not in self.graph[vertexOrigin]:
			self.graph[vertexOrigin].append(vertexDestination)

	def __str__(self) -> str:
		"""Readbale string format of adjacency graph

		Returns a string for each vertex and it's neighbours delimited by newline (lf)
		The vertex and neighbours are converted to strings using `__repr__ <https://docs.python.org/3/reference/datamodel.html#object.__repr__>`_
		Additionally the order in which the vertices and neighbours are printed are in the order that they
		were added in using :py:func:`addEdge`

		:return: The string representation
		:rtype: str
		"""

		buildUp = []
		for vertex, neighbours in self.graph.items():
			buildUp.append('{!r} -> {!r}'.format(vertex, neighbours))
		return "\n".join(buildUp)

	def shortestPath(self, vertexOrigin: Hashable, vertexDestination: Hashable) -> Tuple[Hashable]:
		"""Shortest path finder

		Finds the shortest path from a given vertex origin to a vertex destination
		Vertex equality is based on the `__eq__ <https://docs.python.org/3/reference/datamodel.html#object.__eq__>`_ function

		:param vertexOrigin: Vertex origin
		:type vertexOrigin: Hashable
		:param vertexDestination: Vertex destination
		:type vertexDestination: Hashable
		:return: A tuple of the indices
		:rtype: Tuple[Hashable]
		"""
		todoList = deque((vertexOrigin))
		retracingPath = dict(((vertex, None) for vertex in self.graph.keys()))
		while retracingPath[vertexDestination] is None:
			vertex = todoList.popleft()
			neighbours = self.graph[vertex]
			todoList.append(neighbours)

		retracingVertex = vertexDestination
		shortestPath = []
		while retracingVertex != vertexOrigin:
			shortestPath.append(retracingVertex)
			retracingVertex = retracingPath[retracingVertex]

		return shortestPath.reverse()