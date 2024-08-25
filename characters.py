import pygame
import math
import board
import random
from utils import podeMover
from config import ElementPath, spriteRatio, pixel, spriteOffset
from random import randrange
from board import gameBoard


class Pacman:
    def __init__(self, row, col, jogo):
        self.row = row
        self.col = col
        self.jogo = jogo  # Adiciona a referência ao objeto jogo
        self.bocaAberta = False
        self.velocidadePacman = 1/4
        self.delayMudarBoca = 5
        self.mudarBoca = 0
        self.direcao = 0  # 0: North, 1: East, 2: South, 3: West
        self.novaDirecao = 0

    def update(self):
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

    # Draws pacman based on his current state

    def draw(self):
        if not self.jogo.comecou:
            pacmanImage = pygame.image.load(ElementPath + "tile112.png")
            pacmanImage = pygame.transform.scale(
                pacmanImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            board.tela.blit(pacmanImage, (self.col * pixel + spriteOffset,
                                          self.row * pixel + spriteOffset, pixel, pixel))
            return

        if self.mudarBoca == self.delayMudarBoca:
            self.mudarBoca = 0
            self.bocaAberta = not self.bocaAberta
        self.mudarBoca += 1
        if self.direcao == 0:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(ElementPath + "tile049.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile051.png")
        elif self.direcao == 1:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(ElementPath + "tile052.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile054.png")
        elif self.direcao == 2:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(ElementPath + "tile053.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile055.png")
        elif self.direcao == 3:
            if self.bocaAberta:
                pacmanImage = pygame.image.load(ElementPath + "tile048.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile050.png")

        pacmanImage = pygame.transform.scale(
            pacmanImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
        board.tela.blit(pacmanImage, (self.col * pixel + spriteOffset,
                                      self.row * pixel + spriteOffset, pixel, pixel))


class Ghost:
    def __init__(self, row, col, nome, changeFeetCount, jogo):
        self.row = row
        self.col = col
        self.atacado = False
        self.nome = nome
        self.direcao = randrange(4)
        self.morto = False
        self.changeFeetCount = changeFeetCount
        self.changeFeetDelay = 5
        self.alvo = [-1, -1]
        self.velocidadeFantasma = 1/4
        self.ultimaLocalizacao = [-1, -1]
        self.timerAposAtaque = 240
        self.contadorAposAtaque = 0
        self.timerMorte = 120
        self.contadorMorte = 0
        self.jogo = jogo

    def update(self):
        if self.alvo == [-1, -1] or (self.row == self.alvo[0] and self.col == self.alvo[1]) or gameBoard[int(self.row)][int(self.col)] == 4 or self.morto:
            self.definirAlvo()
        self.definirDirecao()
        self.movimento()

        if self.atacado:
            self.contadorAposAtaque += 1

        if self.atacado and not self.morto:
            self.velocidadeFantasma = 1/8

        if self.contadorAposAtaque == self.timerAposAtaque and self.atacado:
            if not self.morto:
                self.velocidadeFantasma = 1/4
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)

            self.contadorAposAtaque = 0
            self.atacado = False
            self.definirAlvo()

        if self.morto and gameBoard[self.row][self.col] == 4:
            self.contadorMorte += 1
            self.atacado = False
            if self.contadorMorte == self.timerMorte:
                self.contadorMorte = 0
                self.morto = False
                self.velocidadeFantasma = 1/4

    def draw(self):
        ghostImage = pygame.image.load(ElementPath + "tile152.png")
        currentDir = ((self.direcao + 3) % 4) * 2
        if self.changeFeetCount == self.changeFeetDelay:
            self.changeFeetCount = 0
            currentDir += 1
        self.changeFeetCount += 1
        if self.morto:
            tileNum = 152 + currentDir
            ghostImage = pygame.image.load(
                ElementPath + "tile" + str(tileNum) + ".png")
        elif self.atacado:
            if self.timerAposAtaque - self.contadorAposAtaque < self.timerAposAtaque//3:
                if (self.timerAposAtaque - self.contadorAposAtaque) % 31 < 26:
                    if self.nome == "owl":
                        ghostImage = pygame.image.load(
                            ElementPath + "owl_weak.png")
                    elif self.nome == "pidgeot":
                        ghostImage = pygame.image.load(
                            ElementPath + "pidgeot_weak.png")
                    elif self.nome == "blastoise":
                        ghostImage = pygame.image.load(
                            ElementPath + "blastoise_weak.png")
                    elif self.nome == "charizard":
                        ghostImage = pygame.image.load(
                            ElementPath + "charmander_weak.png")
                else:
                    if self.nome == "owl":
                        ghostImage = pygame.image.load(
                            ElementPath + "owl_weak_2.png")
                    elif self.nome == "pidgeot":
                        ghostImage = pygame.image.load(
                            ElementPath + "pidgeot_weak_2.png")
                    elif self.nome == "blastoise":
                        ghostImage = pygame.image.load(
                            ElementPath + "blastoise_weak_2.png")
                    elif self.nome == "charizard":
                        ghostImage = pygame.image.load(
                            ElementPath + "charmander_weak_2.png")
            else:
                if self.nome == "owl":
                    ghostImage = pygame.image.load(
                        ElementPath + "owl_weak.png")
                elif self.nome == "pidgeot":
                    ghostImage = pygame.image.load(
                        ElementPath + "pidgeot_weak.png")
                elif self.nome == "blastoise":
                    ghostImage = pygame.image.load(
                        ElementPath + "blastoise_weak.png")
                elif self.nome == "charizard":
                    ghostImage = pygame.image.load(
                        ElementPath + "charmander_weak.png")
        else:
            if self.nome == "owl":
                tileNum = 136 + currentDir
                ghostImage = pygame.image.load(
                    ElementPath + "tile" + str(tileNum) + ".png")
            elif self.nome == "pidgeot":
                tileNum = 128 + currentDir
                ghostImage = pygame.image.load(
                    ElementPath + "tile" + str(tileNum) + ".png")
            elif self.nome == "blastoise":
                tileNum = 144 + currentDir
                ghostImage = pygame.image.load(
                    ElementPath + "tile" + str(tileNum) + ".png")
            elif self.nome == "charizard":
                tileNum = 96 + currentDir
                if tileNum < 100:
                    ghostImage = pygame.image.load(
                        ElementPath + "tile0" + str(tileNum) + ".png")
                else:
                    ghostImage = pygame.image.load(
                        ElementPath + "tile" + str(tileNum) + ".png")

        ghostImage = pygame.transform.scale(
            ghostImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
        board.tela.blit(ghostImage, (self.col * pixel + spriteOffset,
                                     self.row * pixel + spriteOffset, pixel, pixel))

    def isValidTwo(self, cRow, cCol, dist, visited):
        if cRow < 3 or cRow >= len(gameBoard) - 5 or cCol < 0 or cCol >= len(gameBoard[0]) or gameBoard[cRow][cCol] == 3:
            return False
        elif visited[cRow][cCol] <= dist:
            return False
        return True

    def isValid(self, cRow, cCol):
        if cCol < 0 or cCol > len(gameBoard[0]) - 1:
            return True
        for ghost in self.jogo.create_ghosts():
            if ghost.nome == self.nome:
                continue
            if ghost.row == cRow and ghost.col == cCol and not self.morto:
                return False
        if not ghostGate.count([cRow, cCol]) == 0:
            if self.morto and self.row < cRow:
                return True
            elif self.row > cRow and not self.morto and not self.atacado and not self.jogo.lockedIn:
                return True
            else:
                return False
        if gameBoard[cRow][cCol] == 3:
            return False
        return True

    def definirDirecao(self):
        dirs = [[0, -self.velocidadeFantasma, 0],
                [1, 0, self.velocidadeFantasma],
                [2, self.velocidadeFantasma, 0],
                [3, 0, -self.velocidadeFantasma]
                ]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for novaDirecao in dirs:
            if self.calcularDistancia(self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]]) < best:
                if not (self.ultimaLocalizacao[0] == self.row + novaDirecao[1] and self.ultimaLocalizacao[1] == self.col + novaDirecao[2]):
                    if novaDirecao[0] == 0 and self.col % 1.0 == 0:
                        if self.isValid(math.floor(self.row + novaDirecao[1]), int(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 1 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + novaDirecao[1]), math.ceil(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 2 and self.col % 1.0 == 0:
                        if self.isValid(math.ceil(self.row + novaDirecao[1]), int(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
                    elif novaDirecao[0] == 3 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + novaDirecao[1]), math.floor(self.col + novaDirecao[2])):
                            bestDir = novaDirecao[0]
                            best = self.calcularDistancia(
                                self.alvo, [self.row + novaDirecao[1], self.col + novaDirecao[2]])
        self.direcao = bestDir

    def calcularDistancia(self, a, b):
        dR = a[0] - b[0]
        dC = a[1] - b[1]
        return math.sqrt((dR * dR) + (dC * dC))

    def definirAlvo(self):
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.morto:
            self.alvo = [ghostGate[0][0] - 1, ghostGate[0][1] + 1]
            return
        elif gameBoard[int(self.row)][int(self.col)] == 4 and self.morto:
            self.alvo = [self.row, self.col]
        elif self.morto:
            self.alvo = [14, 13]
            return

        # Records the quadrants of each ghost's alvo
        quads = [0, 0, 0, 0]
        for ghost in self.jogo.create_ghosts():
            # if ghost.alvo[0] == self.row and ghost.col == self.col:
            #     continue
            if ghost.alvo[0] <= 15 and ghost.alvo[1] >= 13:
                quads[0] += 1
            elif ghost.alvo[0] <= 15 and ghost.alvo[1] < 13:
                quads[1] += 1
            elif ghost.alvo[0] > 15 and ghost.alvo[1] < 13:
                quads[2] += 1
            elif ghost.alvo[0] > 15 and ghost.alvo[1] >= 13:
                quads[3] += 1

        # Finds a alvo that will keep the ghosts dispersed
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

    def movimento(self):
        # print(self.alvo)
        self.ultimaLocalizacao = [self.row, self.col]
        if self.direcao == 0:
            self.row -= self.velocidadeFantasma
        elif self.direcao == 1:
            self.col += self.velocidadeFantasma
        elif self.direcao == 2:
            self.row += self.velocidadeFantasma
        elif self.direcao == 3:
            self.col -= self.velocidadeFantasma

        # Incase they go through the middle tunnel
        self.col = self.col % len(gameBoard[0])
        if self.col < 0:
            self.col = len(gameBoard[0]) - 0.5

    def setAttacked(self, isAttacked):
        self.atacado = isAttacked

    def isAttacked(self):
        return self.atacado

    def setDead(self, isDead):
        self.morto = isDead

    def isDead(self):
        return self.morto


ghostGate = [[15, 13], [15, 14]]
