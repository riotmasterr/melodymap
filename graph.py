"""
graph.py
--------
Weighted undirected graph data structure used by MelodyMap.

Internally each vertex maps to a list of edge dictionaries
of the form: {"node": <neighbor>, "weight": <float>}.
"""

from typing import Any, Dict, List


class WeightedGraph:
    """A simple weighted, undirected graph backed by an adjacency list."""

    def __init__(self) -> None:
        self.adjacency_list: Dict[Any, List[Dict[str, Any]]] = {}

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph if it does not already exist."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, v1: Any, v2: Any, weight: float) -> None:
        """
        Add an undirected weighted edge between v1 and v2.

        Both vertices are auto-created if missing. Duplicate edges
        are skipped so calling this twice does not create parallel edges.
        """
        self.add_vertex(v1)
        self.add_vertex(v2)

        # Skip if an edge between v1 and v2 already exists
        if any(edge["node"] == v2 for edge in self.adjacency_list[v1]):
            return

        self.adjacency_list[v1].append({"node": v2, "weight": weight})
        self.adjacency_list[v2].append({"node": v1, "weight": weight})

    def get_neighbors(self, vertex: Any) -> List[Dict[str, Any]]:
        """Return the raw neighbor list for a vertex (empty if missing)."""
        return self.adjacency_list.get(vertex, [])

    def get_weighted_neighbors(self, vertex: Any) -> List[Dict[str, Any]]:
        """Return neighbors sorted by descending edge weight."""
        return sorted(
            self.get_neighbors(vertex),
            key=lambda edge: edge["weight"],
            reverse=True,
        )

    def has_vertex(self, vertex: Any) -> bool:
        return vertex in self.adjacency_list

    def vertex_count(self) -> int:
        return len(self.adjacency_list)

    def edge_count(self) -> int:
        # Each undirected edge appears twice in the adjacency lists
        return sum(len(edges) for edges in self.adjacency_list.values()) // 2
