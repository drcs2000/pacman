import pygame
import math
import board
import random
from config import CaminhoDosElementos, spriteRatio, pixel, spriteOffset
from random import randrange
from board import gameBoard
from typing import List

class Pacman:
    def __init__(self, row, col, jogo):
        # Inicializa o Pacman com a linha e coluna iniciais, referência ao jogo, 
        # e define os estados iniciais do Pacman, como a velocidade e direção
        self.row = row  # Linha (posição) inicial do Pacman
        self.col = col  # Coluna (posição) inicial do Pacman
        self.jogo = jogo  # Referência ao objeto do jogo principal
        self.bocaAberta = False  # Estado da boca do Pacman (aberta/fechada)
        self.velocidadePacman = 1/4  # Velocidade de movimento do Pacman
        self.delayMudarBoca = 5  # Delay para alternar o estado da boca
        self.mudarBoca = 0  # Contador para mudar a boca
        self.direcao = 0  # Direção atual do Pacman (0: Norte, 1: Leste, 2: Sul, 3: Oeste)
        self.novaDirecao = 0  # Nova direção para onde Pacman deve se mover

    def atualizar(self):
        # Tenta mover Pacman na nova direção, se possível
        if self.novaDirecao == 0 and podeMover(math.floor(self.row - self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
            self.row -= self.velocidadePacman  # Move Pacman para cima
            self.direcao = self.novaDirecao  # Atualiza a direção para a nova direção
        elif self.novaDirecao == 1 and podeMover(self.row, math.ceil(self.col + self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
            self.col += self.velocidadePacman  # Move Pacman para a direita
            self.direcao = self.novaDirecao  # Atualiza a direção para a nova direção
        elif self.novaDirecao == 2 and podeMover(math.ceil(self.row + self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
            self.row += self.velocidadePacman  # Move Pacman para baixo
            self.direcao = self.novaDirecao  # Atualiza a direção para a nova direção
        elif self.novaDirecao == 3 and podeMover(self.row, math.floor(self.col - self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
            self.col -= self.velocidadePacman  # Move Pacman para a esquerda
            self.direcao = self.novaDirecao  # Atualiza a direção para a nova direção
        else:
            # Se a nova direção não for válida, continua na direção atual
            if self.direcao == 0 and podeMover(math.floor(self.row - self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row -= self.velocidadePacman  # Continua movendo Pacman para cima
            elif self.direcao == 1 and podeMover(self.row, math.ceil(self.col + self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col += self.velocidadePacman  # Continua movendo Pacman para a direita
            elif self.direcao == 2 and podeMover(math.ceil(self.row + self.velocidadePacman), self.col, gameBoard) and self.col % 1.0 == 0:
                self.row += self.velocidadePacman  # Continua movendo Pacman para baixo
            elif self.direcao == 3 and podeMover(self.row, math.floor(self.col - self.velocidadePacman), gameBoard) and self.row % 1.0 == 0:
                self.col -= self.velocidadePacman  # Continua movendo Pacman para a esquerda

    def desenho(self):
        # Se o jogo ainda não começou, desenha o Pacman parado
        if not self.jogo.comecou:
            pacmanImage = pygame.image.load(CaminhoDosElementos + "tile112.png")
        else:
            # Alterna a abertura da boca do Pacman
            if self.mudarBoca == self.delayMudarBoca:
                self.mudarBoca = 0  # Reseta o contador de mudança da boca
                self.bocaAberta = not self.bocaAberta  # Alterna entre aberta/fechada
            self.mudarBoca += 1  # Incrementa o contador de mudança da boca

            # Seleciona a imagem correta do Pacman com base na direção e no estado da boca
            if self.direcao == 0:
                pacmanImage = pygame.image.load(CaminhoDosElementos + ("pacman_cima_1.png" if self.bocaAberta else "pacman_cima_2.png"))
            elif self.direcao == 1:
                pacmanImage = pygame.image.load(CaminhoDosElementos + ("pacman_direita_1.png" if self.bocaAberta else "pacman_direita_2.png"))
            elif self.direcao == 2:
                pacmanImage = pygame.image.load(CaminhoDosElementos + ("pacman_baixo_1.png" if self.bocaAberta else "pacman_baixo_2.png"))
            elif self.direcao == 3:
                pacmanImage = pygame.image.load(CaminhoDosElementos + ("pacman_esquerda_1.png" if self.bocaAberta else "pacman_esquerda_2.png"))

        # Redimensiona e desenha a imagem do Pacman na tela
        pacmanImage = pygame.transform.scale(pacmanImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
        board.tela.blit(pacmanImage, (self.col * pixel + spriteOffset, self.row * pixel + spriteOffset, pixel, pixel))

class Ghost:
    def __init__(self, row, col, nome, contadorDeMudançaDePes, jogo):
        self.row = row  # Linha (posição) inicial do fantasma
        self.col = col  # Coluna (posição) inicial do fantasma
        self.atacado = False  # Indica se o fantasma foi atacado (modo vulnerável)
        self.nome = nome  # Nome do fantasma
        self.direcao = randrange(4)  # Direção inicial aleatória (0=Norte, 1=Leste, 2=Sul, 3=Oeste)
        self.morto = False  # Indica se o fantasma está morto
        self.contadorDeMudançaDePes = contadorDeMudançaDePes  # Contador para alternância de animação de movimento
        self.atrasoDeMudançaDePes = 5  # Delay para mudar a animação de movimento
        self.alvo = [-1, -1]  # Alvo atual para onde o fantasma deve se mover
        self.velocidadeFantasma = 1/4  # Velocidade de movimento do fantasma
        self.ultimaLocalizacao = [-1, -1]  # Última posição registrada do fantasma
        self.timerAposAtaque = 240  # Tempo durante o qual o fantasma permanece vulnerável após ser atacado
        self.contadorAposAtaque = 0  # Contador para o tempo vulnerável após ataque
        self.timerMorte = 120  # Tempo para respawn após morte
        self.contadorMorte = 0  # Contador de tempo para respawn
        self.jogo = jogo  # Referência ao objeto principal do jogo

    def atualizar(self):
        # Verifica se o fantasma está morto
        if self.morto:
            if gameBoard[int(self.row)][int(self.col)] == 4:  # Verifica se o fantasma está no ghostGate
                self.contadorMorte += 1
                if self.contadorMorte < self.timerMorte:
                    # Fantasma faz movimentos aleatórios rápidos enquanto está no ghostGate
                    self.definirDirecao()
                    self.movimento()
                else:
                    # Quando o tempo de respawn acabar, o fantasma revive
                    self.contadorMorte = 0
                    self.morto = False
                    self.atacado = False  # Remove o estado de ataque
                    self.velocidadeFantasma = 1/4  # Restaura a velocidade normal
            else:
                # Se o fantasma está morto e fora do ghostGate, ele se move rápido para lá
                self.velocidadeFantasma = 1  # Aumenta a velocidade para retorno ao ghostGate
                self.alvo = [14, 13]  # Define o ghostGate como alvo
                self.definirDirecao()
                self.movimento()
            return  # Saia cedo se o fantasma estiver morto

        # Define um novo alvo para o fantasma se necessário
        if self.alvo == [-1, -1] or (int(self.row) == self.alvo[0] and int(self.col) == self.alvo[1]) or gameBoard[int(self.row)][int(self.col)] == 4:
            self.definirAlvo()

        self.definirDirecao()  # Define a direção baseada no alvo
        self.movimento()  # Movimenta o fantasma na direção definida

        # Se o fantasma foi atacado, ele se move mais devagar
        if self.atacado:
            self.contadorAposAtaque += 1
            self.velocidadeFantasma = 1/8  # Reduz a velocidade durante o estado vulnerável
            if self.contadorAposAtaque == self.timerAposAtaque:
                # Reseta o estado de ataque após o tempo definido
                self.atacado = False
                self.velocidadeFantasma = 1/4
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)
            elif self.contadorAposAtaque < self.timerAposAtaque:
                # O fantasma pisca durante o tempo vulnerável
                if (self.timerAposAtaque - self.contadorAposAtaque) % 31 < 16:
                    self.direcao = 4  # Usa direção inexistente para controlar o pisca-pisca
                else:
                    self.direcao = 5  # Alterna para a outra imagem "weak"

    def desenho(self):
        ghostImage = None
        if self.morto:
            # Mostra apenas os olhos quando o fantasma está morto
            ghostImage = pygame.image.load(CaminhoDosElementos + "olhos0.png")
        elif self.atacado and self.contadorAposAtaque < self.timerAposAtaque:
            # Controla a exibição das imagens "weak" e "weak_2" durante o estado vulnerável
            if self.timerAposAtaque - self.contadorAposAtaque > self.timerAposAtaque // 3:
                # Exibe a imagem "weak" enquanto o fantasma ainda tem tempo suficiente no estado vulnerável
                ghostImage = pygame.image.load(CaminhoDosElementos + f"{self.nome}_weak.png")
            else:
                # Alterna entre "weak" e "weak_2" quando está prestes a sair do estado vulnerável
                if self.direcao == 4:
                    ghostImage = pygame.image.load(CaminhoDosElementos + f"{self.nome}_weak.png")
                elif self.direcao == 5:
                    ghostImage = pygame.image.load(CaminhoDosElementos + f"{self.nome}_weak_2.png")
        else:
            # Exibe a animação normal do fantasma, dependendo da direção
            currentDir = ((self.direcao + 3) % 4) * 2
            if self.contadorDeMudançaDePes == self.atrasoDeMudançaDePes:
                self.contadorDeMudançaDePes = 0
                currentDir += 1
            self.contadorDeMudançaDePes += 1
            ghostImage = pygame.image.load(CaminhoDosElementos + self.nome + str(currentDir) + ".png")

        # Redimensiona e desenha a imagem do fantasma na tela
        if ghostImage:
            ghostImage = pygame.transform.scale(ghostImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            board.tela.blit(ghostImage, (self.col * pixel + spriteOffset, self.row * pixel + spriteOffset, pixel, pixel))

    def movimento(self):
        # Movimenta o fantasma baseado na direção atual
        self.ultimaLocalizacao = [self.row, self.col]  # Armazena a última posição antes de mover
        if self.direcao == 0:
            self.row -= self.velocidadeFantasma  # Move para cima
        elif self.direcao == 1:
            self.col += self.velocidadeFantasma  # Move para a direita
        elif self.direcao == 2:
            self.row += self.velocidadeFantasma  # Move para baixo
        elif self.direcao == 3:
            self.col -= self.velocidadeFantasma  # Move para a esquerda

        # Controla o teletransporte do fantasma através do túnel
        self.col = self.col % len(gameBoard[0])
        if self.col < 0:
            self.col = len(gameBoard[0]) - 0.5

    def definirDirecao(self):
        # Define a melhor direção para o fantasma se mover
        dirs = [[0, -self.velocidadeFantasma, 0],  # Norte
                [1, 0, self.velocidadeFantasma],  # Leste
                [2, self.velocidadeFantasma, 0],  # Sul
                [3, 0, -self.velocidadeFantasma]  # Oeste
                ]
        random.shuffle(dirs)  # Embaralha as direções para evitar previsibilidade
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

    def calcularDistancia(self, a, b):
        # Calcula a distância euclidiana entre dois pontos (a e b)
        dR = a[0] - b[0]  # Diferença na linha
        dC = a[1] - b[1]  # Diferença na coluna
        return math.sqrt((dR * dR) + (dC * dC))  # Retorna a distância euclidiana

    def definirAlvo(self):
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.morto:
            self.alvo = [self.ghostGate[0][0] - 1, self.ghostGate[0][1] + 1]
            return
        elif gameBoard[int(self.row)][int(self.col)] == 4 and self.morto:
            self.alvo = [self.row, self.col]
        elif self.morto:
            self.alvo = [14, 13]
            return

        # Lógica especial para Charizard
        if self.nome == "charizard":
            pacman_row, pacman_col = self.jogo.pacman.row, self.jogo.pacman.col

            # Calcular a diferença de posição entre Charizard e Pacman
            diff_row = pacman_row - self.row
            diff_col = pacman_col - self.col

            # Escolher a direção com a maior distância
            if diff_row > diff_col:
                if diff_row > 0:
                    self.alvo = [pacman_row - 1, pacman_col]  # Move para cima
                else:
                    self.alvo = [pacman_row + 1, pacman_col]  # Move para baixo
            else:
                if diff_col > 0:
                    self.alvo = [pacman_row, pacman_col - 1]  # Move para a esquerda
                else:
                    self.alvo = [pacman_row, pacman_col + 1]  # Move para a direita

            return

        # Lógica padrão para os outros fantasmas
        quadrantes = [0, 0, 0, 0]
        for fantasma in self.jogo.criar_fantasma():
            if fantasma.alvo[0] <= 15 and fantasma.alvo[1] >= 13:
                quadrantes[0] += 1
            elif fantasma.alvo[0] <= 15 and fantasma.alvo[1] < 13:
                quadrantes[1] += 1
            elif fantasma.alvo[0] > 15 and fantasma.alvo[1] < 13:
                quadrantes[2] += 1
            elif fantasma.alvo[0] > 15 and fantasma.alvo[1] >= 13:
                quadrantes[3] += 1

        while True:
            self.alvo = [randrange(31), randrange(28)]
            quadrante = 0
            if self.alvo[0] <= 15 and self.alvo[1] >= 13:
                quadrante = 0
            elif self.alvo[0] <= 15 and self.alvo[1] < 13:
                quadrante = 1
            elif self.alvo[0] > 15 and self.alvo[1] < 13:
                quadrante = 2
            elif self.alvo[0] > 15 and self.alvo[1] >= 13:
                quadrante = 3
            if not gameBoard[self.alvo[0]][self.alvo[1]] == 3 and not gameBoard[self.alvo[0]][self.alvo[1]] == 4:
                break
            elif quadrantes[quadrante] == 0:
                break

    def valido(self, cRow, cCol):
        # Verifica se o fantasma pode se mover para a nova posição
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

    def setAttacked(self, isAttacked):
        # Define o estado de ataque do fantasma
        self.atacado = isAttacked

    def isAttacked(self):
        # Retorna o estado de ataque do fantasma
        return self.atacado

    def setDead(self, isDead):
        # Define o estado de morte do fantasma
        self.morto = isDead

    def isDead(self):
        # Retorna o estado de morte do fantasma
        return self.morto

    # Coordenadas do ghostGate (portão do esconderijo dos fantasmas)
    ghostGate = [[15, 13], [15, 14]]

def podeMover(row: int, col: int, gameBoard: List[List[int]]) -> bool:
    # Verifica se Pac-Man ou os fantasmas podem se mover para a posição especificada.
    if col == -1 or col == len(gameBoard[0]):
        return True
    return gameBoard[int(row)][int(col)] != 3
