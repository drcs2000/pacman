import pygame
import copy

# Classe responsável por configurar o tabuleiro do jogo
class Board:
    def __init__(self, tela):
        # Matriz que representa o layout do tabuleiro do jogo.
        # Os números nesta matriz correspondem a diferentes tipos de blocos:
        # 1 - Caminho livre
        # 2 - Comida normal (Tic-Tak)
        # 3 - Parede
        # 4 - Porta do esconderijo dos fantasmas
        # 5 - Tic-Tak especial verde
        # 6 - Tic-Tak especial branco
        self.gameBoard = [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 6, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 6, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3,
                3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3,
                3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3,
                2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3,
                1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3,
                1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3,
                3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4,
                4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 4, 4, 4,
                4, 4, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4,
                4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3,
                3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3,
                3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3,
                3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
            [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
            [3, 6, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1,
                2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 6, 3],
            [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3,
                3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
            [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3,
                3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
            [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3,
                2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
            [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
            [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3,
                2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
            [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ]
        self.tela = tela  # Armazena a superfície da tela do jogo

# Configurações para o tamanho dos sprites e o deslocamento dos mesmos
spriteRatio = 3/2  # Proporção de escala dos sprites em relação ao tamanho do pixel
pixel = 25  # Tamanho de cada unidade quadrada no tabuleiro (em pixels)
spriteOffset = pixel * (1 - spriteRatio) * (1/2)  # Deslocamento dos sprites para centralização

# Inicialização da tela do jogo (usando a matriz de gameBoard para definir o tamanho)
# Aqui, criamos uma tela temporária apenas para acessar as dimensões do tabuleiro
dummy_board = Board(None)
tela = pygame.display.set_mode((len(dummy_board.gameBoard[0]) * pixel, len(
    dummy_board.gameBoard) * pixel))  # Define as dimensões da tela com base no tamanho do gameBoard
pygame.display.flip()  # Atualiza a tela para refletir essas configurações

# Criação do tabuleiro do jogo real, agora passando a tela correta
board = Board(tela)
gameBoard = copy.deepcopy(board.gameBoard)  # Faz uma cópia do tabuleiro do jogo para uso posterior

musicaTocando = 0  # Indica o estado atual da música no jogo: 0 - Chomp, 1 - Música importante, 2 - Sirene