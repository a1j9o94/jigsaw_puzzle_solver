# jigsaw_puzzle_solver/visualizer.py

import matplotlib.pyplot as plt
from jigsaw_puzzle_solver.solver import Edge, PuzzlePiece
from typing import List

def visualize_piece(piece: PuzzlePiece):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for i, edge in enumerate(piece.edges):
        x, y = zip(*edge.contour.coords)
        if i == 0:
            ax.plot(x, y, 'b-')
        elif i == 1:
            ax.plot(y, [-xi for xi in x], 'r-')
        elif i == 2:
            ax.plot([-xi for xi in x], [-yi for yi in y], 'g-')
        else:
            ax.plot([-yi for yi in y], x, 'm-')
    
    ax.set_aspect('equal', 'box')
    ax.set_title(f'Puzzle Piece {piece.id}')
    plt.show()

def visualize_puzzle(pieces: List[PuzzlePiece]):
    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    for i, piece in enumerate(pieces):
        ax = axs[i // 2, i % 2]
        for j, edge in enumerate(piece.edges):
            x, y = zip(*edge.contour.coords)
            if j == 0:
                ax.plot(x, y, 'b-')
            elif j == 1:
                ax.plot(y, [-xi for xi in x], 'r-')
            elif j == 2:
                ax.plot([-xi for xi in x], [-yi for yi in y], 'g-')
            else:
                ax.plot([-yi for yi in y], x, 'm-')
        ax.set_aspect('equal', 'box')
        ax.set_title(f'Puzzle Piece {piece.id}')
    plt.tight_layout()
    plt.show()

# Usage:
# from jigsaw_puzzle_solver.solver import create_sample_puzzle
# pieces = create_sample_puzzle()
# visualize_puzzle(pieces)

def main():
    from jigsaw_puzzle_solver.solver import create_sample_puzzle
    pieces = create_sample_puzzle()
    visualize_puzzle(pieces)

if __name__ == "__main__":
    main()