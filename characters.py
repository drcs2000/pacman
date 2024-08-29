import pygame
import math
import board
import random
from utils import podeMover
from config import CaminhoDosElementos, spriteRatio, pixel, spriteOffset
from random import randrange
from board import gameBoard

# Classe que representa o Pacman no jogo


class Pacman:
    def __init__(self, row, col, jogo):
        self.row = row  # Linha (posição) inicial do Pacman
        self.col = col  # Coluna (posição) inicial do Pacman
        self.jogo = jogo  # Referência ao objeto do jogo principal
        self.bocaAberta = False  # Indica se a boca do Pacman está aberta ou fechada
        self.velocidadePacman = 1/4  # Velocidade de movimento do Pacman
        # Delay para alternar o estado da boca (aberta/fechada)
        self.delayMudarBoca = 5
        self.mudarBoca = 0  # Contador para mudar a boca
        # Direção inicial (0: Norte, 1: Leste, 2: Sul, 3: Oeste)
        self.direcao = 0
        self.novaDirecao = 0  # Direção nova para onde Pacman deve se mover

    # Atualiza a posição do Pacman de acordo com sua direção
    def atualizar(self):
        # Tenta mover na nova direção, se possível
        if self.novaDirecao == 0:
            if podeMover(math.floor(self.row - self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row -= self.velocidadePacman
                self.direcao = self.novaDirecao
                return
        elif self.novaDirecao == 1:
            if podeMover(self.row, math.ceil(self.col + self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col += self.velocidadePacman
                self.direcao = self.novaDirecao
                return
        elif self.novaDirecao == 2:
            if podeMover(math.ceil(self.row + self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row += self.velocidadePacman
                self.direcao = self.novaDirecao
                return
        elif self.novaDirecao == 3:
            if podeMover(self.row, math.floor(self.col - self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col -= self.velocidadePacman
                self.direcao = self.novaDirecao
                return

        # Se a nova direção não for válida, continua na direção atual
        if self.direcao == 0:
            if podeMover(math.floor(self.row - self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row -= self.velocidadePacman
        elif self.direcao == 1:
            if podeMover(self.row, math.ceil(self.col + self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col += self.velocidadePacman
        elif self.direcao == 2:
            if podeMover(math.ceil(self.row + self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row += self.velocidadePacman
        elif self.direcao == 3:
            if podeMover(self.row, math.floor(self.col - self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col -= self.velocidadePacman

    # Desenha o Pacman na tela
    def desenho(self):
        # Se o jogo não começou, desenha Pacman parado
        if not self.jogo.comecou:
            pacmanImage = pygame.image.load(
                CaminhoDosElementos + "tile112.png")
            pacmanImage = pygame.transform.scale(
                pacmanImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            board.tela.blit(pacmanImage, (self.col * pixel + spriteOffset,
                                          self.row * pixel + spriteOffset, pixel, pixel))
            return

        # Alterna a abertura da boca do Pacman
        if self.mudarBoca == self.delayMudarBoca:
            self.mudarBoca = 0
            self.bocaAberta = not self.bocaAberta
        self.mudarBoca += 1

        # Desenha Pacman na direção correta, com a boca aberta ou fechada
        if self.direcao == 0:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_cima_1.png")
            else:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_cima_2.png")
        elif self.direcao == 1:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_direita_1.png")
            else:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_direita_2.png")
        elif self.direcao == 2:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_baixo_1.png")
            else:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_baixo_2.png")
        elif self.direcao == 3:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_esquerda_1.png")
            else:
                pacmanImage = pygame.image.load(
                    CaminhoDosElementos + "pacman_esquerda_2.png")

        # Redimensiona e desenha a imagem do Pacman na tela
        pacmanImage = pygame.transform.scale(
            pacmanImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
        board.tela.blit(pacmanImage, (self.col * pixel + spriteOffset,
                                      self.row * pixel + spriteOffset, pixel, pixel))

# Classe que representa os fantasmas no jogo


class Ghost:
    def __init__(self, row, col, nome, changeFeetCount, jogo):
        self.row = row  # Linha (posição) inicial do fantasma
        self.col = col  # Coluna (posição) inicial do fantasma
        self.atacado = False  # Indica se o fantasma foi atacado
        self.nome = nome  # Nome do fantasma
        self.direcao = randrange(4)  # Direção inicial aleatória
        self.morto = False  # Indica se o fantasma está morto
        self.changeFeetCount = changeFeetCount  # Contador para animação de movimento
        self.changeFeetDelay = 5  # Delay para mudar o estado do movimento
        self.alvo = [-1, -1]  # Alvo atual do fantasma
        self.velocidadeFantasma = 1/4  # Velocidade de movimento do fantasma
        # Última posição conhecida do fantasma
        self.ultimaLocalizacao = [-1, -1]
        self.timerAposAtaque = 240  # Tempo de efeito após ser atacado
        self.contadorAposAtaque = 0  # Contador do tempo após ataque
        self.timerMorte = 120  # Tempo para respawn após morte
        self.contadorMorte = 0  # Contador para respawn
        self.jogo = jogo  # Referência ao objeto do jogo principal

    # Atualiza a posição e o estado do fantasma
    def atualizar(self):
        # Define novo alvo e direção se necessário
        if self.alvo == [-1, -1] or (self.row == self.alvo[0] and self.col == self.alvo[1]) or gameBoard[int(self.row)][int(self.col)] == 4 or self.morto:
            self.definirAlvo()
        self.definirDirecao()
        self.movimento()

        # Aumenta o contador se o fantasma foi atacado
        if self.atacado:
            self.contadorAposAtaque += 1

        # Diminui a velocidade se o fantasma foi atacado
        if self.atacado and not self.morto:
            self.velocidadeFantasma = 1/8

        # Reseta o estado de ataque após o tempo determinado
        if self.contadorAposAtaque == self.timerAposAtaque and self.atacado:
            if not self.morto:
                self.velocidadeFantasma = 1/4
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)

            self.contadorAposAtaque = 0
            self.atacado = False
            self.definirAlvo()

        # Lida com o estado de morte e respawn do fantasma
        if self.morto and gameBoard[self.row][self.col] == 4:
            self.contadorMorte += 1
            self.atacado = False
            if self.contadorMorte == self.timerMorte:
                self.contadorMorte = 0
                self.morto = False
                self.velocidadeFantasma = 1/4

    # Método para desenhar o fantasma na tela
    def desenho(self):
        # Carrega a imagem dos olhos do fantasma (usada quando o fantasma está morto)
        ghostImage = pygame.image.load(CaminhoDosElementos + "olhos0.png")

        # Determina a direção atual do fantasma e ajusta a imagem correspondente
        currentDir = ((self.direcao + 3) % 4) * 2
        if self.changeFeetCount == self.changeFeetDelay:
            self.changeFeetCount = 0
            currentDir += 1
        self.changeFeetCount += 1

        # Se o fantasma está morto, exibe apenas os olhos
        if self.morto:
            posicaoBoard = currentDir
            ghostImage = pygame.image.load(
                CaminhoDosElementos + "olhos" + str(posicaoBoard) + ".png")

        # Se o fantasma foi atacado, exibe a versão fraca do fantasma
        elif self.atacado:
            if self.timerAposAtaque - self.contadorAposAtaque < self.timerAposAtaque // 3:
                # Muda entre duas imagens diferentes para criar uma animação piscante
                if (self.timerAposAtaque - self.contadorAposAtaque) % 31 < 26:
                    if self.nome == "owl":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "owl_weak.png")
                    elif self.nome == "pidgeot":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "pidgeot_weak.png")
                    elif self.nome == "blastoise":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "blastoise_weak.png")
                    elif self.nome == "charizard":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "charmander_weak.png")
                else:
                    if self.nome == "owl":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "owl_weak_2.png")
                    elif self.nome == "pidgeot":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "pidgeot_weak_2.png")
                    elif self.nome == "blastoise":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "blastoise_weak_2.png")
                    elif self.nome == "charizard":
                        ghostImage = pygame.image.load(
                            CaminhoDosElementos + "charmander_weak_2.png")
            else:
                if self.nome == "owl":
                    ghostImage = pygame.image.load(
                        CaminhoDosElementos + "owl_weak.png")
                elif self.nome == "pidgeot":
                    ghostImage = pygame.image.load(
                        CaminhoDosElementos + "pidgeot_weak.png")
                elif self.nome == "blastoise":
                    ghostImage = pygame.image.load(
                        CaminhoDosElementos + "blastoise_weak.png")
                elif self.nome == "charizard":
                    ghostImage = pygame.image.load(
                        CaminhoDosElementos + "charmander_weak.png")

        # Se o fantasma não está morto nem atacado, exibe sua imagem normal
        else:
            if self.nome == "owl":
                posicaoBoard = currentDir
                ghostImage = pygame.image.load(
                    CaminhoDosElementos + self.nome + str(posicaoBoard) + ".png")
            elif self.nome == "pidgeot":
                posicaoBoard = currentDir
                ghostImage = pygame.image.load(
                    CaminhoDosElementos + self.nome + str(posicaoBoard) + ".png")
            elif self.nome == "blastoise":
                posicaoBoard = currentDir
                ghostImage = pygame.image.load(
                    CaminhoDosElementos + self.nome + str(posicaoBoard) + ".png")
            elif self.nome == "charizard":
                posicaoBoard = currentDir
                ghostImage = pygame.image.load(
                    CaminhoDosElementos + self.nome + str(posicaoBoard) + ".png")

        # Redimensiona e desenha a imagem do fantasma na tela
        ghostImage = pygame.transform.scale(
            ghostImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
        board.tela.blit(ghostImage, (self.col * pixel + spriteOffset,
                                     self.row * pixel + spriteOffset, pixel, pixel))

    # Método que verifica se uma posição é válida para o fantasma se mover
    def valido(self, cRow, cCol):
        if cCol < 0 or cCol > len(gameBoard[0]) - 1:
            return True
        for fantasma in self.jogo.criar_fantasma():
            if fantasma.nome == self.nome:
                continue
            if fantasma.row == cRow and fantasma.col == cCol and not self.morto:
                return False
        if not self.ghostGate.count([cRow, cCol]) == 0:
            if self.morto and self.row < cRow:
                return True
            elif self.row > cRow and not self.morto and not self.atacado and not self.jogo.fantasmasPresos:
                return True
            else:
                return False
        if gameBoard[cRow][cCol] == 3:
            return False
        return True

    # Método para definir a direção do movimento do fantasma
    def definirDirecao(self):
        dirs = [[0, -self.velocidadeFantasma, 0],
                [1, 0, self.velocidadeFantasma],
                [2, self.velocidadeFantasma, 0],
                [3, 0, -self.velocidadeFantasma]
                ]
        # Embaralha as direções para evitar padrões previsíveis
        random.shuffle(dirs)
        best = 10000  # Inicializa a melhor distância como um valor grande
        bestDir = -1  # Inicializa a melhor direção como inválida
        for novaDirecao in dirs:
            # Calcula a melhor direção com base na menor distância ao alvo
            if self.calcularDistancia(self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]]) < best:
                if not (self.ultimaLocalizacao[0] == self.row + novaDirecao[1] and self.ultimaLocalizacao[1] == self.col + novaDirecao[2]):
                    if novaDirecao[0] == 0 and self.col % 1.0 == 0:
                        if self.valido(math.floor(self.row + novaDirecao[1]), int(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 1 and self.row % 1.0 == 0:
                        if self.valido(int(self.row + novaDirecao[1]), math.ceil(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 2 and self.col % 1.0 == 0:
                        if self.valido(math.ceil(self.row + novaDirecao[1]), int(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 3 and self.row % 1.0 == 0:
                        if self.valido(int(self.row + novaDirecao[1]), math.floor(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
        self.direcao = bestDir  # Define a direção do fantasma como a melhor direção encontrada

    # Método para calcular a distância entre dois pontos
    def calcularDistancia(self, a, b):
        dR = a[0] - b[0]  # Diferença na linha
        dC = a[1] - b[1]  # Diferença na coluna
        # Retorna a distância euclidiana
        return math.sqrt((dR * dR) + (dC * dC))

    # Método para definir o alvo do fantasma
    def definirAlvo(self):
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.morto:
            # Se o fantasma não está morto e está no portão dos fantasmas, ele tenta sair
            self.alvo = [self.ghostGate[0][0] - 1, self.ghostGate[0][1] + 1]
            return
        elif gameBoard[int(self.row)][int(self.col)] == 4 and self.morto:
            # Se o fantasma está morto, ele permanece no portão até ser revivido
            self.alvo = [self.row, self.col]
        elif self.morto:
            # Se o fantasma está morto, ele se dirige para a posição de respawn
            self.alvo = [14, 13]
            return

        # Registra os quadrantes do alvo de cada fantasma para mantê-los dispersos
        quads = [0, 0, 0, 0]
        for fantasma in self.jogo.criar_fantasma():
            if fantasma.alvo[0] <= 15 and fantasma.alvo[1] >= 13:
                quads[0] += 1
            elif fantasma.alvo[0] <= 15 and fantasma.alvo[1] < 13:
                quads[1] += 1
            elif fantasma.alvo[0] > 15 and fantasma.alvo[1] < 13:
                quads[2] += 1
            elif fantasma.alvo[0] > 15 and fantasma.alvo[1] >= 13:
                quads[3] += 1

        # Encontra um alvo que manterá os fantasmas dispersos
        while True:
            self.alvo = [randrange(31), randrange(28)]
            quad = 0
            if self.alvo[0] <= 15 and self.alvo[1] >= 13:
                quad = 0
            elif self.alvo[0] <= 15 and self.alvo[1] < 13:
                quad = 1
            elif self.alvo[0] > 15 and self.alvo[1] < 13:
                quad = 2
            elif self.alvo[0] > 15 and self.alvo[1] >= 13:
                quad = 3
            if not gameBoard[self.alvo[0]][self.alvo[1]] == 3 and not gameBoard[self.alvo[0]][self.alvo[1]] == 4:
                break
            elif quads[quad] == 0:
                break

    # Método para mover o fantasma de acordo com a direção atual
    def movimento(self):
        self.ultimaLocalizacao = [self.row, self.col]
        if self.direcao == 0:
            self.row -= self.velocidadeFantasma
        elif self.direcao == 1:
            self.col += self.velocidadeFantasma
        elif self.direcao == 2:
            self.row += self.velocidadeFantasma
        elif self.direcao == 3:
            self.col -= self.velocidadeFantasma

        # Caso o fantasma passe pelo túnel central, ele aparece do outro lado
        self.col = self.col % len(gameBoard[0])
        if self.col < 0:
            self.col = len(gameBoard[0]) - 0.5

    # Método para definir se o fantasma foi atacado
    def setAttacked(self, isAttacked):
        self.atacado = isAttacked

    # Método para verificar se o fantasma foi atacado
    def isAttacked(self):
        return self.atacado

    # Método para definir se o fantasma está morto
    def setDead(self, isDead):
        self.morto = isDead

    # Método para verificar se o fantasma está morto
    def isDead(self):
        return self.morto

    # Posições do portão dos fantasmas
    ghostGate = [[15, 13], [15, 14]]
