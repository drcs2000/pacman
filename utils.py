from typing import List


def podeMover(row: int, col: int, gameBoard: List[List[int]]) -> bool:
    """Verifica se Pac-Man ou os fantasmas podem se mover para a posição especificada."""
    if col == -1 or col == len(gameBoard[0]):
        return True
    return gameBoard[int(row)][int(col)] != 3
