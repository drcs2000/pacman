import pygame
from board import gameBoard

# File Paths
BoardPath = "Assets/BoardImages/"
ElementPath = "Assets/ElementImages/"
TextPath = "Assets/TextImages/"
DataPath = "Assets/Data/"
MusicPath = "Assets/Music/"

# jogo Settings
spriteRatio = 3/2
pixel = 25
spriteOffset = pixel * (1 - spriteRatio) * (1/2)
pelletColor = (222, 161, 133)

# jogo Keys
PLAYING_KEYS = {
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "right": [pygame.K_d, pygame.K_RIGHT],
    "left": [pygame.K_a, pygame.K_LEFT]
}

# Other Constants
vidas_iniciais = 3
initial_score = 0
(width, height) = (len(gameBoard[0]) * pixel,
                   len(gameBoard) * pixel)  # jogo tela
