""" Adjacency Graph Module

.. py:module:: AdjacencyGraph
   :synopsis: Give an object representation of a graph based on an adjacency list
"""

from __future__ import annotations
from typing import Hashable, Tuple
from collections import OrderedDict, deque

class AdjacencyGraph:
	"""AdjacencyGraph class

	The adjacency graph is a weight-less directed graph and can store any
	`Hashable <https://docs.python.org/3.7/glossary.html>`_ value

	Example:

	.. code-block: python
	   :linenos:

	   s = AdjacencyGraph()
	   s.addEdge('1','2')
	   s.addEdge('2','1')

	.. note::
	   Please note of the subtlety with Hashable values. Refer to
	   `Hashing <https://docs.python.org/3/reference/datamodel.html#object.__hash__>`_,
	   particularly on the topic of hashing and equality. Behaviour of this class
	   can only be guaranteed insofar as the values hashing and equality are
	"""

	def __init__(self):
		self.graph = OrderedDict()

	def addVertex(self, vertex: Hashable) -> AdjacencyGraph:
		"""Vertex addition

		Adds vertex to graph. This operation is idempotent

		:param vertex: Vertex to add
		:type vertex: Hashable
		:return: [description]
		:rtype: AdjacencyGraph
		"""
		if vertex not in self.graph:
			self.graph[vertex] = []
		return self

	def addEdge(self, vertexOrigin: Hashable, vertexDestination: Hashable) -> AdjacencyGraph:
		"""Adds an edge to the graph
		Given an origin and a destination, add an edge to the graph from origin to destination

		:param vertexOrigin: Start of edge
		:type vertexOrigin: Hashable
		:param vertexDestination: End of edge
		:type vertexDestination: Hashable
		:returns: self
		:rtype: AdjacencyGraph
		:raises Exception: Raised when either vertex could not be found

		The function is idempotent. Given the same origin and destination on the same AdjacencyGraph object,
		the resulting graph is the same.

		Example:
		.. code-block: python
		   :linenos:

		   s = AdjacencyGraph()
		   s.addVertex('1').addVertex('2')
		   s.addEdge('1','2') # 1 -> 2
		   s.addEdge('1','2') # still 1 -> 2
		"""
		if vertexOrigin not in self.graph:
			raise Exception(f'Origin {vertexOrigin!s} is not yet in the graph')

		if vertexDestination not in self.graph:
			raise Exception(f'Destination {vertexDestination!s} is not yet in the graph')

		if vertexDestination not in self.graph[vertexOrigin]:
			self.graph[vertexOrigin].append(vertexDestination)
		return self

	def __str__(self) -> str:
		"""Readbale string format of adjacency graph

		Returns a string for each vertex and it's neighbours delimited by newline (lf)
		The vertex and neighbours are converted to strings using `__repr__ <https://docs.python.org/3/reference/datamodel.html#object.__repr__>`_
		Additionally the order in which the vertices and neighbours are printed are in the order that they
		were added in using :py:fun:`addVertex` and :py:func:`addEdge`

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
		todoList = deque((vertexOrigin,))
		retracingPath = dict(((vertex, None) for vertex in self.graph.keys()))
		while retracingPath[vertexDestination] is None and todoList:
			vertex = todoList.popleft()
			neighbours = self.graph[vertex]
			for neighbour in neighbours:
				if retracingPath[neighbour] is None:
					retracingPath[neighbour] = vertex
			todoList.extend(neighbours)

		retracingVertex = vertexDestination
		shortestPath = [retracingVertex]
		while retracingVertex != vertexOrigin:
			retracingVertex = retracingPath[retracingVertex]
			shortestPath.append(retracingVertex)

			if retracingVertex is None:
				# short circuit, path cannot be found
				return []

		shortestPath.reverse()
		return shortestPath