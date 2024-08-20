import pygame
from typing import List
from config import DataPath

def canMove(row: int, col: int, gameBoard: List[List[int]]) -> bool:
    """Verifica se Pac-Man ou os fantasmas podem se mover para a posição especificada."""
    if col == -1 or col == len(gameBoard[0]):
        return True
    return gameBoard[int(row)][int(col)] != 3

def pause(time: int) -> None:
    """Pausa o jogo por uma quantidade específica de tempo (em milissegundos)."""
    pygame.time.wait(time)

def getHighScore() -> int:
    """Obtém a pontuação mais alta registrada."""
    try:
        with open(DataPath + "HighScore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Retorna 0 se o arquivo não for encontrado
    except ValueError:
        return 0  # Retorna 0 se o conteúdo do arquivo não puder ser convertido para inteiro

def recordHighScore(highScore: int) -> None:
    """Grava a pontuação mais alta no arquivo."""
    with open(DataPath + "HighScore.txt", "w") as file:
        file.write(str(highScore))
