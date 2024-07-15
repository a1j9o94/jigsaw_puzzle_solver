# tests/test_solver.py

import pytest
from collections import defaultdict
from jigsaw_puzzle_solver.solver import PuzzleSolver, create_sample_puzzle

def test_puzzle_solution():
    puzzle_pieces = create_sample_puzzle()
    solver = PuzzleSolver(puzzle_pieces)
    solution = solver.solve()
    
    assert is_valid_solution(puzzle_pieces, solution), "The solution is not valid"

def is_valid_solution(pieces, solution):
    used_pieces = set()
    connections = defaultdict(set)

    for piece_id, neighbor_id, edge in solution:
        used_pieces.add(piece_id)
        used_pieces.add(neighbor_id)
        connections[piece_id].add(neighbor_id)
        connections[neighbor_id].add(piece_id)

    # Check if all pieces are used
    if len(used_pieces) != len(pieces):
        print(f"Error: Not all pieces were used. Used {len(used_pieces)} out of {len(pieces)}")
        return False

    # Check if the number of connections is correct
    total_connections = sum(len(conn) for conn in connections.values())
    expected_connections = 2 * (len(pieces) - 1)  # Each connection is counted twice, once for each piece
    if total_connections != expected_connections:
        print(f"Error: Incorrect number of connections. Found {total_connections // 2}, expected {expected_connections // 2}")
        return False

    # Check if the graph is connected
    visited = set()
    stack = [next(iter(used_pieces))]
    while stack:
        piece = stack.pop()
        if piece not in visited:
            visited.add(piece)
            stack.extend(connections[piece] - visited)

    if len(visited) != len(pieces):
        print("Error: The solution is not a single connected component")
        return False

    return True

def test_edge_matching():
    puzzle_pieces = create_sample_puzzle()
    solver = PuzzleSolver(puzzle_pieces)
    
    # Check if the graph is built correctly
    assert len(solver.graph) == len(puzzle_pieces), "Graph should have an entry for each puzzle piece"
    
    # Check if each piece has the correct number of connections
    for piece_id, connections in solver.graph.items():
        assert 1 <= len(connections) <= 3, f"Each piece should have 1 to 3 connections, piece {piece_id} has {len(connections)}"

def test_solve_empty_puzzle():
    solver = PuzzleSolver([])
    solution = solver.solve()
    assert len(solution) == 0, "Empty puzzle should have empty solution"

# Add more tests as needed