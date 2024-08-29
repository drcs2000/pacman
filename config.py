import pygame
from board import gameBoard

# Caminhos para os arquivos usados no jogo
CaminhoDoBoard = "Assets/board/"  # Caminho para as imagens do tabuleiro
# Caminho para as imagens dos elementos (Pacman, fantasmas, etc.)
CaminhoDosElementos = "Assets/elementos/"
# Caminho para as imagens de texto (pontuações, etc.)
CaminhoDoTexto = "Assets/texto/"
# Caminho para os dados do jogo (pontuações altas, etc.)
CaminhoDaPontuacao = "Assets/score/"
# Caminho para os arquivos de música
CaminhoDasMusicas = "Assets/musicas/"

# Configurações do jogo
spriteRatio = 3/2  # Proporção de escala dos sprites em relação ao tamanho do pixel
pixel = 25  # Tamanho de cada unidade quadrada no tabuleiro (em pixels)
# Deslocamento dos sprites para centralização
spriteOffset = pixel * (1 - spriteRatio) * (1/2)
corTickTack = (222, 161, 133)  # Cor das "pílulas" (Tic-Taks) no jogo

# Mapeamento das teclas usadas para controlar o Pacman
PLAYING_KEYS = {
    # Teclas para mover para cima (W ou Seta para cima)
    "up": [pygame.K_w, pygame.K_UP],
    # Teclas para mover para baixo (S ou Seta para baixo)
    "down": [pygame.K_s, pygame.K_DOWN],
    # Teclas para mover para a direita (D ou Seta para a direita)
    "right": [pygame.K_d, pygame.K_RIGHT],
    # Teclas para mover para a esquerda (A ou Seta para a esquerda)
    "left": [pygame.K_a, pygame.K_LEFT]
}

# Outras constantes
vidas_iniciais = 3  # Número inicial de vidas para o Pacman
score_inicial = 0  # Pontuação inicial do jogador
(width, height) = (len(gameBoard[0]) * pixel,
                   # Dimensões da tela do jogo, baseadas no tamanho do tabuleiro
                   len(gameBoard) * pixel)
