import random
import pygame
import copy
import board
import math
from random import randrange
from characters import Pacman, Ghost
from config import BoardPath, spriteRatio, spriteOffset, pixel, ElementPath, pelletColor, MusicPath, TextPath, DataPath
from board import Board
import os


class jogo:
    def __init__(self, nivel, score, tela):
        self.pause = True
        self.atualizarDelayFantasma = 1
        self.atualizarFantasma = 0
        self.atualizarDelayPacman = 1
        self.atualizacaoContadorPacman = 0
        self.mudarDelayTickTack = 10
        self.contagemTickTack = 0
        self.fantasmaAtacado = False
        self.highScore = self.getHighScore()
        self.score = score
        self.nivel = nivel
        self.vidas = 3
        self.pacman = Pacman(26.0, 13.5, self)  # Center of Second Last Row
        self.tela = tela
        self.board = Board(tela)
        self.total = self.getCount()
        self.pontuacaoFantasma = 200
        self.niveis = [[350, 250], [150, 450], [150, 450], [0, 600]]
        random.shuffle(self.niveis)
        self.fantasmasStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.fantasmasStates:
            state[0] = randrange(2)
            state[1] = randrange(self.niveis[index][state[0]] + 1)
            index += 1
        self.coletado = 0
        self.comecou = False
        self.gameOver = False
        self.contadorGameOver = 0
        self.pontos = []
        self.pointsTimer = 10
        self.frutasState = [200, 400, False]
        self.localizacaoFrutas = [20.0, 13.5]
        self.frutas = ["berrie1.png", "berrie2.png", "berrie3.png", "berrie4.png",
                       "berrie5.png", "berrie6.png", "berrie7.png", "berrie8.png"]
        self.frutasColetadas = []
        self.timerNivel = 0
        self.pontuacaoFrutas = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.novaVidaExtra = False
        self.musicaTocando = 0
        self.morreu = False
        self.gameOverHandled = False

    def reset(self):
        self.morreu = True

        for ghost in self.create_ghosts():
            ghost.definirAlvo()

        # Reposiciona o Pacman no ponto inicial
        self.pacman = Pacman(26.0, 13.5, self)

        self.pause = True  # Pausa o jogo para aguardar o início pelo jogador
        self.render()  # Renderiza o estado inicial do jogo

    # Driver method: The games primary update method
    def update(self):
        if self.gameOver:
            if not self.gameOverHandled:
                self.recordHighScore()
                self.gameOverFunc()
                self.gameOverHandled = True
            return
        if self.pause or not self.comecou:
            self.drawTilesAround(21, 10)
            self.drawTilesAround(21, 11)
            self.drawTilesAround(21, 12)
            self.drawTilesAround(21, 13)
            self.drawTilesAround(21, 14)
            self.drawReady()
            pygame.display.update()
            return

        self.timerNivel += 1
        self.atualizarFantasma += 1
        self.atualizacaoContadorPacman += 1
        self.contagemTickTack += 1
        self.fantasmaAtacado = False

        if self.score >= 10000 and not self.novaVidaExtra:
            self.vidas = self.vidas + 1
            self.novaVidaExtra = True
            self.forcePlayMusic("pacman_extrapac.wav")

        # Draw tiles around ghosts and pacman
        self.clearBoard()
        for ghost in self.create_ghosts():
            if ghost.atacado:
                self.fantasmaAtacado = True

        # Check if the ghost should chase Pacman
        index = 0
        for state in self.fantasmasStates:
            state[1] += 1
            if state[1] >= self.niveis[index][state[0]]:
                state[1] = 0
                state[0] += 1
                state[0] %= 2
            index += 1

        index = 0
        for ghost in self.create_ghosts():
            if not ghost.atacado and not ghost.morto and self.fantasmasStates[index][0] == 0:
                ghost.alvo = [self.pacman.row, self.pacman.col]
            index += 1

        if self.timerNivel == self.lockedInTimer:
            self.lockedIn = False

        self.checkSurroundings()
        if self.atualizarFantasma == self.atualizarDelayFantasma:
            for ghost in self.create_ghosts():
                ghost.definirDirecao()
                ghost.update()
            self.atualizarFantasma = 0

        if self.contagemTickTack == self.mudarDelayTickTack:
            # Changes the color of special Tic-Taks
            self.flipColor()
            self.contagemTickTack = 0

        if self.atualizacaoContadorPacman == self.atualizarDelayPacman:
            self.atualizacaoContadorPacman = 0
            self.pacman.update()
            self.pacman.col %= len(self.board.gameBoard[0])
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                if self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                    self.playMusic("munch_1.wav")
                    self.board.gameBoard[int(
                        self.pacman.row)][int(self.pacman.col)] = 1
                    self.score += 10
                    self.coletado += 1
                    # Fill tile with black
                    pygame.draw.rect(self.tela, (57, 140, 16), (self.pacman.col *
                                                                pixel, self.pacman.row * pixel, pixel, pixel))
                elif self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 6:
                    self.forcePlayMusic("golaco.wav")
                    self.board.gameBoard[int(
                        self.pacman.row)][int(self.pacman.col)] = 1
                    self.coletado += 1
                    # Fill tile with black
                    pygame.draw.rect(self.tela, (57, 140, 16), (self.pacman.col *
                                                                pixel, self.pacman.row * pixel, pixel, pixel))
                    self.score += 50
                    self.pontuacaoFantasma = 200
                    for ghost in self.create_ghosts():
                        ghost.contadorAposAtaque = 0
                        ghost.setAttacked(True)
                        ghost.definirAlvo()
                        self.fantasmaAtacado = True
        self.checkSurroundings()

        global running
        if self.coletado == self.total:
            print("New Level")
            self.forcePlayMusic("brasil.wav")
            self.nivel += 1
            self.newLevel()

        if self.nivel - 1 == 8:
            print("You win", self.nivel, len(self.niveis))
            running = False
        self.softRender()

    # Render method
    def render(self):
        self.tela.fill((57, 140, 16))  # Limpa a tela
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(self.board.gameBoard) - 2):  # Correção aqui
            for j in range(len(self.board.gameBoard[0])):  # Correção aqui
                if self.board.gameBoard[i][j] == 3:  # Desenhar parede
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                        imageName = "0" + imageName
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(
                        tileImage, (pixel, pixel))
                    self.tela.blit(
                        tileImage, (j * pixel, i * pixel, pixel, pixel))
                elif self.board.gameBoard[i][j] == 2:  # Desenhar Tic-Tak
                    pygame.draw.circle(
                        self.tela, pelletColor, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 4)
                elif self.board.gameBoard[i][j] == 5:  # Tic-Tak especial preto
                    pygame.draw.circle(
                        self.tela, (0, 0, 0), (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)
                elif self.board.gameBoard[i][j] == 6:  # Tic-Tak especial branco
                    pygame.draw.circle(
                        self.tela, pelletColor, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)

                currentTile += 1

        # Desenhar os fantasmas e pacman
        for ghost in self.create_ghosts():
            ghost.draw()
        self.pacman.draw()
        pygame.display.update()

    def softRender(self):
        pointsToDraw = []
        for point in self.pontos:
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.pontos.remove(point)
                self.drawTilesAround(point[0], point[1])

        for point in pointsToDraw:
            self.drawPoints(point[0], point[1], point[2])

        # Draw Sprites
        for ghost in self.create_ghosts():
            ghost.draw()
        self.pacman.draw()
        self.displayScore()
        self.displayBerries()
        self.displayLives()
        self.drawBerry()
        # Updates the tela
        pygame.display.update()

    def playMusic(self, music):
        global musicaTocando
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unload()
            pygame.mixer.music.load(MusicPath + music)
            pygame.mixer.music.queue(MusicPath + music)
            pygame.mixer.music.play()
            if music == "munch_1.wav":
                musicaTocando = 0
            elif music == "siren_1.wav":
                musicaTocando = 2
            else:
                musicaTocando = 1

    def forcePlayMusic(self, music):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(MusicPath + music)
        pygame.mixer.music.play()
        global musicaTocando
        musicaTocando = 1

    def clearBoard(self):
        # Draw tiles around ghosts and pacman
        for ghost in self.create_ghosts():
            self.drawTilesAround(ghost.row, ghost.col)
        self.drawTilesAround(self.pacman.row, self.pacman.col)
        self.drawTilesAround(
            self.localizacaoFrutas[0], self.localizacaoFrutas[1])
        # Clears Ready! Label
        self.drawTilesAround(20, 10)
        self.drawTilesAround(20, 11)
        self.drawTilesAround(20, 12)
        self.drawTilesAround(20, 13)
        self.drawTilesAround(20, 14)

    def checkSurroundings(self):
        # Verifica se o Pacman foi morto
        for ghost in self.create_ghosts():
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.atacado:
                self.vidas = self.vidas - 1
                if self.vidas == 0:
                    print("You lose")
                    self.forcePlayMusic("fim.wav")
                    self.gameOver = True
                    return
                else:
                    print("Pacman perdeu uma vida")
                    self.forcePlayMusic("pacman_death.wav")
                    self.reset()  # Reinicia o nível com uma vida a menos
                    return

            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                ghost.setDead(True)
                ghost.definirAlvo()
                ghost.velocidadeFantasma = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.pontuacaoFantasma
                self.pontos.append(
                    [ghost.row, ghost.col, self.pontuacaoFantasma, 0])
                self.pontuacaoFantasma *= 2
                self.forcePlayMusic("toca_a_musica.wav")
        if self.touchingPacman(self.localizacaoFrutas[0], self.localizacaoFrutas[1]) and not self.frutasState[2] and self.timerNivel in range(self.frutasState[0], self.frutasState[1]):
            self.frutasState[2] = True
            self.score += self.pontuacaoFrutas
            self.pontos.append(
                [self.localizacaoFrutas[0], self.localizacaoFrutas[1], self.pontuacaoFrutas, 0])
            self.frutasColetadas.append(self.frutas[(self.nivel - 1) % 8])
            self.forcePlayMusic("campeao.wav")

    # Displays the current score
    def displayScore(self):
        textOneUp = ["score1.png", "verdeU.png", "verdeP.png"]
        textHighScore = ["verdeH.png", "verdeI.png", "verdeG.png", "verdeH.png",
                         "tile015.png", "verdeS.png", "verdeC.png", "verdeO.png", "verdeR.png", "verdeE.png"]
        index = 0
        scoreStart = 5
        highScoreStart = 11

        # Display '1UP' text
        for i in range(scoreStart, scoreStart + len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, (i * pixel, 4, pixel, pixel))
            index += 1

        # Display the current score
        # Ensure score is at least 2 digits long
        score = str(self.score).zfill(2)
        for i, digit in enumerate(score):
            tileImage = pygame.image.load(
                TextPath + "score" + digit + ".png")
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, ((scoreStart + 2 + i)
                                       * pixel, pixel + 4, pixel, pixel))

        # Display 'HIGH SCORE' text
        for i in range(highScoreStart, highScoreStart + len(textHighScore)):
            tileImage = pygame.image.load(
                TextPath + textHighScore[i - highScoreStart])
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, (i * pixel, 4, pixel, pixel))

        # Ensure high score is a list of digits (from the score at index 0)
        # Always take the first score as the high score
        highScore = str(self.highScore[0]).zfill(2)
        for i, digit in enumerate(highScore):
            tileImage = pygame.image.load(
                TextPath + "score" + digit + ".png")
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(
                tileImage, ((highScoreStart + 6 + i) * pixel, pixel + 4, pixel, pixel))

    def drawBerry(self):
        if self.timerNivel in range(self.frutasState[0], self.frutasState[1]) and not self.frutasState[2]:
            berryImage = pygame.image.load(
                ElementPath + self.frutas[(self.nivel - 1) % 8])
            berryImage = pygame.transform.scale(
                berryImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(
                berryImage, (self.localizacaoFrutas[1] * pixel, self.localizacaoFrutas[0] * pixel, pixel, pixel))

    def drawPoints(self, pontos, row, col):
        pointStr = str(pontos)
        index = 0
        for i in range(len(pointStr)):
            digit = pointStr[i]
            tileImage = pygame.image.load(
                TextPath + "score" + digit + ".png")
            tileImage = pygame.transform.scale(
                tileImage, (pixel // 2, pixel // 2))
            self.tela.blit(tileImage, ((col) * pixel + (pixel //
                                                        2 * index), row * pixel - 20, pixel // 2, pixel // 2))
            index += 1

    def drawReady(self):
        ready = ["verdeR.png", "verdeE.png", "verdeA.png",
                 "verdeD.png", "verdeY.png", "verdeExclamacao.png"]
        for i in range(len(ready)):
            letter = pygame.image.load(TextPath + ready[i])
            letter = pygame.transform.scale(letter, (int(pixel), int(pixel)))
            self.tela.blit(letter, ((11 + i) * pixel,
                                    20 * pixel, pixel, pixel))

    def gameOverFunc(self):
        if self.gameOverHandled:
            return  # Prevent the function from running multiple times

        # Resets the tela
        self.tela.fill((0, 0, 0))  # Fill the tela with black

        # Display jogo Over message
        gameOverMessage = ["pretoF.png", "pretoI.png", "pretoM.png", "espaco.png",
                           "pretoD.png", "pretoE.png", "espaco.png",
                           "pretoJ.png", "pretoO.png", "pretoG.png", "pretoO.png"]
        for i in range(len(gameOverMessage)):
            letter = pygame.image.load(TextPath + gameOverMessage[i])
            letter = pygame.transform.scale(letter, (int(pixel), int(pixel)))
            self.tela.blit(
                letter, ((8 + i) * pixel, 4 * pixel, pixel, pixel))

        # Display Scores title
        scoresTitle = ["pretoP.png", "pretoO.png", "pretoN.png",
                       "pretoT.png", "pretoO.png", "pretoS.png"]
        for i in range(len(scoresTitle)):
            letter = pygame.image.load(TextPath + scoresTitle[i])
            letter = pygame.transform.scale(letter, (int(pixel), int(pixel)))
            self.tela.blit(letter, ((10 + i) * pixel,
                                    8 * pixel, pixel, pixel))

        # Display the top 10 scores
        scores = self.getHighScore()  # This should only be called once now
        for idx, score in enumerate(scores):
            # Ensure scores are at least 5 digits long
            score_str = str(score).zfill(4)
            for j, char in enumerate(score_str):
                tileImage = pygame.image.load(
                    TextPath + "pontuacao" + char + ".png")
                tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
                self.tela.blit(tileImage, ((11 + j) * pixel,
                                           (10 + idx) * pixel, pixel, pixel))

        pygame.display.update()
        self.contadorGameOver += 1

    def displayLives(self):
        livesLoc = [[34, 3], [34, 1]]
        for i in range(self.vidas - 1):
            lifeImage = pygame.image.load(ElementPath + "tile054.png")
            lifeImage = pygame.transform.scale(
                lifeImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(
                lifeImage, (livesLoc[i][1] * pixel, livesLoc[i][0] * pixel - spriteOffset, pixel, pixel))

    def displayBerries(self):
        firstBerrie = [34, 26]
        for i in range(len(self.frutasColetadas)):
            berrieImage = pygame.image.load(
                ElementPath + self.frutasColetadas[i])
            berrieImage = pygame.transform.scale(
                berrieImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(berrieImage, ((
                firstBerrie[1] - (2 * i)) * pixel, firstBerrie[0] * pixel + 5, pixel, pixel))

    def touchingPacman(self, row, col):
        if row - 0.5 <= self.pacman.row and row >= self.pacman.row and col == self.pacman.col:
            return True
        elif row + 0.5 >= self.pacman.row and row <= self.pacman.row and col == self.pacman.col:
            return True
        elif row == self.pacman.row and col - 0.5 <= self.pacman.col and col >= self.pacman.col:
            return True
        elif row == self.pacman.row and col + 0.5 >= self.pacman.col and col <= self.pacman.col:
            return True
        elif row == self.pacman.row and col == self.pacman.col:
            return True
        return False

    def newLevel(self):
        self.reset()
        self.coletado = 0
        self.comecou = False
        self.frutasState = [200, 400, False]
        self.timerNivel = 0
        self.lockedIn = True
        for nivel in self.niveis:
            nivel[0] = min((nivel[0] + nivel[1]) - 100, nivel[0] + 50)
            nivel[1] = max(100, nivel[1] - 50)
        random.shuffle(self.niveis)
        index = 0
        for state in self.fantasmasStates:
            state[0] = randrange(2)
            state[1] = randrange(self.niveis[index][state[0]] + 1)
            index += 1
        self.board.gameBoard = copy.deepcopy(board.gameBoard)
        self.render()

    def drawTilesAround(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row - 2, row + 3):
            for j in range(col - 2, col + 3):
                if i >= 3 and i < len(self.board.gameBoard) - 2 and j >= 0 and j < len(self.board.gameBoard[0]):
                    imageName = str(
                        ((i - 3) * len(self.board.gameBoard[0])) + j)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                        imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(
                        tileImage, (pixel, pixel))
                    # Display image of tile
                    self.tela.blit(
                        tileImage, (j * pixel, i * pixel, pixel, pixel))

                    if self.board.gameBoard[i][j] == 2:  # Draw Tic-Tak
                        pygame.draw.circle(
                            self.tela, pelletColor, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 4)
                    # Black Special Tic-Tak
                    elif self.board.gameBoard[i][j] == 5:
                        pygame.draw.circle(
                            self.tela, (0, 0, 0), (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)
                    # White Special Tic-Tak
                    elif self.board.gameBoard[i][j] == 6:
                        pygame.draw.circle(
                            self.tela, pelletColor, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)

    # Flips Color of Special Tic-Taks
    def flipColor(self):
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] == 5:
                    self.board.gameBoard[i][j] = 6
                    pygame.draw.circle(
                        self.tela, pelletColor, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)
                elif self.board.gameBoard[i][j] == 6:
                    self.board.gameBoard[i][j] = 5
                    pygame.draw.circle(
                        self.tela, (0, 0, 0), (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)

    def getCount(self):
        total = 0
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] == 2 or self.board.gameBoard[i][j] == 5 or self.board.gameBoard[i][j] == 6:
                    total += 1
        return total

    def getHighScore(self):
        print('passou aqui')
        if not os.path.exists(DataPath + "HighScore.txt"):
            # Create a file if it doesn't exist and initialize with zeros
            with open(DataPath + "HighScore.txt", "w") as file:
                file.write("0\n" * 10)

        with open(DataPath + "HighScore.txt", "r") as file:
            scores = file.readlines()
            scores = [int(score.strip()) for score in scores]

        return scores

    def recordHighScore(self):
        # Ensure this function is called only once after the jogo ends
        if not hasattr(self, 'highScoreList'):
            # Get the current high scores only once
            self.highScoreList = self.getHighScore()

        # Check if the current score is greater than the lowest score in the top 10
        if self.score > self.highScoreList[-1]:
            self.highScoreList.append(self.score)  # Add the new score
            # Sort the scores in descending order
            self.highScoreList.sort(reverse=True)
            # Keep only the top 10 scores
            self.highScoreList = self.highScoreList[:10]

            # Write the updated scores back to the file
            with open(DataPath + "HighScore.txt", "w") as file:
                for score in self.highScoreList:
                    file.write(str(score) + "\n")

    def create_ghosts(self):
        global ghosts
        if ghosts is None or self.morreu:
            ghosts = [
                Ghost(14.0, 13.5, "charizard", 0, self),
                Ghost(17.0, 11.5, "owl", 1, self),
                Ghost(17.0, 13.5, "pidgeot", 2, self),
                Ghost(17.0, 15.5, "blastoise", 3, self)
            ]
            self.morreu = False
        return ghosts


ghosts = None
