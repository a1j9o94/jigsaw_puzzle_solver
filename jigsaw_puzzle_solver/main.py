import numpy as np
from typing import List, Tuple, Dict, Set
from collections import defaultdict

class Edge:
    def __init__(self, vector: np.ndarray):
        self.vector = vector
        self.length = np.linalg.norm(vector)

    def matches(self, other: 'Edge', tolerance: float = 0.01) -> bool:
        return np.allclose(self.vector, -other.vector, atol=tolerance)

class PuzzlePiece:
    def __init__(self, edges: List[Edge], piece_id: int):
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
        start_piece = self.pieces[0].id
        visited = set()
        solution = []
        self._dfs(start_piece, visited, solution)
        return solution

    def _dfs(self, piece_id: int, visited: Set[int], solution: List[Tuple[int, int, int]]) -> bool:
        visited.add(piece_id)

        if len(visited) == len(self.pieces):
            return True

        for neighbor, (edge, neighbor_edge) in self.graph[piece_id].items():
            if neighbor not in visited:
                solution.append((piece_id, neighbor, edge))
                if self._dfs(neighbor, visited, solution):
                    return True
                solution.pop()

        visited.remove(piece_id)
        return False

# Example usage
def create_sample_puzzle() -> List[PuzzlePiece]:
    # This is a simplified example. In a real scenario, you'd process images to get these vectors.
    pieces = [
        PuzzlePiece([Edge(np.array([1, 0])), Edge(np.array([0, 1])), Edge(np.array([-1, 0])), Edge(np.array([0, -1]))], 0),
        PuzzlePiece([Edge(np.array([-1, 0])), Edge(np.array([0, 1])), Edge(np.array([1, 0])), Edge(np.array([0, -1]))], 1),
        PuzzlePiece([Edge(np.array([0, -1])), Edge(np.array([1, 0])), Edge(np.array([0, 1])), Edge(np.array([-1, 0]))], 2),
        PuzzlePiece([Edge(np.array([0, -1])), Edge(np.array([-1, 0])), Edge(np.array([0, 1])), Edge(np.array([1, 0]))], 3),
    ]
    return pieces

def main():
    puzzle_pieces = create_sample_puzzle()
    solver = PuzzleSolver(puzzle_pieces)
    solution = solver.solve()
    
    print("Puzzle solution:")
    for piece_id, neighbor_id, edge in solution:
        print(f"Piece {piece_id} connects to Piece {neighbor_id} via edge {edge}")

if __name__ == "__main__":
    main()