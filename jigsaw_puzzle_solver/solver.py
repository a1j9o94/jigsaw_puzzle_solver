# jigsaw_puzzle_solver/solver.py

import numpy as np
from typing import List, Tuple, Dict, Set
from collections import defaultdict
from shapely.geometry import LineString, Point
from shapely.affinity import rotate

class Edge:
    def __init__(self, points: List[Tuple[float, float]]):
        """
        Initialize an edge with a list of points defining its curve.
        
        :param points: List of (x, y) coordinates defining the edge curve.
        """
        if len(points) < 10:
            raise ValueError("An edge should be defined by at least 10 points for accuracy")
        self.contour = LineString(points)
        self.length = self.contour.length

    def matches(self, other: 'Edge', tolerance: float = 0.01) -> bool:
        # Flip the other edge
        flipped_contour = LineString(other.contour.coords[::-1])
        
        # Check if the contours are similar when aligned
        return self.contour.hausdorff_distance(flipped_contour) < tolerance * self.length

    def rotate(self, angle: float) -> 'Edge':
        rotated_contour = rotate(self.contour, angle, origin='center')
        return Edge(list(rotated_contour.coords))

    @staticmethod
    def create_puzzle_edge(num_points: int = 50) -> 'Edge':
        """
        Create a random puzzle-like edge.
        
        :param num_points: Number of points to use in defining the edge.
        :return: An Edge object representing a puzzle-like curve.
        """
        x = np.linspace(0, 1, num_points)
        y = np.zeros(num_points)
        
        # Create a random curve
        for i in range(2, 5):  # Use 2-4 sine waves of different frequencies
            y += np.sin(i * np.pi * x) * np.random.uniform(0.05, 0.15)
        
        # Ensure the edge starts and ends at y=0
        y -= y[0]
        y -= np.linspace(y[0], y[-1], num_points)
        
        return Edge(list(zip(x, y)))

class PuzzlePiece:
    def __init__(self, edges: List[Edge], piece_id: int):
        if len(edges) != 4:
            raise ValueError("Each puzzle piece must have exactly 4 edges.")
        self.edges = edges
        self.id = piece_id

class PuzzleSolver:
    def __init__(self, pieces: List[PuzzlePiece]):
        self.pieces = pieces
        self.graph = defaultdict(dict)
        self.build_graph()

    def build_graph(self):
        for i, piece in enumerate(self.pieces):
            for j, other_piece in enumerate(self.pieces[i+1:], start=i+1):
                for edge_index, edge in enumerate(piece.edges):
                    for other_edge_index, other_edge in enumerate(other_piece.edges):
                        if edge.matches(other_edge):
                            self.graph[piece.id][other_piece.id] = (edge_index, other_edge_index)
                            self.graph[other_piece.id][piece.id] = (other_edge_index, edge_index)

    def solve(self) -> List[Tuple[int, int, int]]:
        # check for an empty graph
        if len(self.graph) == 0:
            return []
        
        start_piece = self.pieces[0].id
        visited = set()
        solution = []
        self._dfs(start_piece, visited, solution)
        return solution

    def _dfs(self, piece_id: int, visited: Set[int], solution: List[Tuple[int, int, int]]) -> bool:
        visited.add(piece_id)

        if len(visited) == len(self.pieces):
            return True

        for neighbor, (edge, _) in self.graph[piece_id].items():
            if neighbor not in visited:
                solution.append((piece_id, neighbor, edge))
                if self._dfs(neighbor, visited, solution):
                    return True
                solution.pop()

        visited.remove(piece_id)
        return False

def create_sample_puzzle() -> List[PuzzlePiece]:
    edges = [Edge.create_puzzle_edge() for _ in range(4)]
    pieces = [
        PuzzlePiece([edges[0], edges[1].rotate(90), edges[2].rotate(180), edges[3].rotate(270)], 0),
        PuzzlePiece([edges[2], edges[3].rotate(90), edges[0].rotate(180), edges[1].rotate(270)], 1),
        PuzzlePiece([edges[1], edges[0].rotate(90), edges[3].rotate(180), edges[2].rotate(270)], 2),
        PuzzlePiece([edges[3], edges[2].rotate(90), edges[1].rotate(180), edges[0].rotate(270)], 3),
    ]
    return pieces

# main that creates a test puzzle and runs the solver
def main():
    pieces = create_sample_puzzle()
    solver = PuzzleSolver(pieces)
    solution = solver.solve()
    print(solution)

if __name__ == "__main__":
    main()