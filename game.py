# game.py
import random
import pygame
import copy
import board
import math
from random import randrange
from characters import Pacman, Ghost
from config import BoardPath, spriteRatio, spriteOffset, square, ElementPath, pelletColor, MusicPath, TextPath, DataPath
from utils import pause
from board import Board

class Game:
    def __init__(self, level, score, screen):
        self.paused = True
        self.ghostUpdateDelay = 1
        self.ghostUpdateCount = 0
        self.pacmanUpdateDelay = 1
        self.pacmanUpdateCount = 0
        self.tictakChangeDelay = 10
        self.tictakChangeCount = 0
        self.ghostsAttacked = False
        self.highScore = self.getHighScore()
        self.score = score
        self.level = level
        self.lives = 3
        self.pacman = Pacman(26.0, 13.5, self)  # Center of Second Last Row
        self.screen = screen
        self.board = Board(screen)
        self.total = self.getCount()
        self.ghostScore = 200
        self.levels = [[350, 250], [150, 450], [150, 450], [0, 600]]
        random.shuffle(self.levels)
        # Level index and Level Progress
        self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        self.collected = 0
        self.started = False
        self.gameOver = False
        self.gameOverCounter = 0
        self.points = []
        self.pointsTimer = 10
        # Berry Spawn Time, Berry Death Time, Berry Eaten
        self.berryState = [200, 400, False]
        self.berryLocation = [20.0, 13.5]
        self.berries = ["tile080.png", "tile081.png", "tile082.png", "tile083.png", "tile084.png", "tile085.png", "tile086.png", "tile087.png"]
        self.berriesCollected = []
        self.levelTimer = 0
        self.berryScore = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.extraLifeGiven = False
        self.musicPlaying = 0

    def reset(self):
        from main import reset_game
        reset_game()

    # Driver method: The games primary update method
    def update(self):
        if self.gameOver:
            self.gameOverFunc()
            return
        if self.paused or not self.started:
            self.drawTilesAround(21, 10)
            self.drawTilesAround(21, 11)
            self.drawTilesAround(21, 12)
            self.drawTilesAround(21, 13)
            self.drawTilesAround(21, 14)
            self.drawReady()
            pygame.display.update()
            return

        self.levelTimer += 1
        self.ghostUpdateCount += 1
        self.pacmanUpdateCount += 1
        self.tictakChangeCount += 1
        self.ghostsAttacked = False

        if self.score >= 10000 and not self.extraLifeGiven:
            self.lives += 1
            self.extraLifeGiven = True
            self.forcePlayMusic("pacman_extrapac.wav")

        # Draw tiles around ghosts and pacman
        self.clearBoard()
        for ghost in self.create_ghosts():
            if ghost.attacked:
                self.ghostsAttacked = True

        # Check if the ghost should case pacman
        index = 0
        for state in self.ghostStates:
            state[1] += 1
            if state[1] >= self.levels[index][state[0]]:
                state[1] = 0
                state[0] += 1
                state[0] %= 2
            index += 1

        index = 0
        for ghost in self.create_ghosts():
            if not ghost.attacked and not ghost.dead and self.ghostStates[index][0] == 0:
                ghost.target = [self.pacman.row, self.pacman.col]
            index += 1

        if self.levelTimer == self.lockedInTimer:
            self.lockedIn = False

        self.checkSurroundings()
        if self.ghostUpdateCount == self.ghostUpdateDelay:
            for ghost in self.create_ghosts():
                ghost.setDir()
                ghost.update()
            self.ghostUpdateCount = 0

        if self.tictakChangeCount == self.tictakChangeDelay:
            # Changes the color of special Tic-Taks
            self.flipColor()
            self.tictakChangeCount = 0

        if self.pacmanUpdateCount == self.pacmanUpdateDelay:
            self.pacmanUpdateCount = 0
            self.pacman.update()
            self.pacman.col %= len(self.board.gameBoard[0])
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                if self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                    self.playMusic("munch_1.wav")
                    self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.score += 10
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                elif self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 6:
                    self.forcePlayMusic("power_pellet.wav")
                    self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                    self.score += 50
                    self.ghostScore = 200
                    for ghost in self.create_ghosts():
                        ghost.attackedCount = 0
                        ghost.setAttacked(True)
                        ghost.setTarget()
                        self.ghostsAttacked = True
        self.checkSurroundings()
        self.highScore = max(self.score, self.highScore)

        global running
        if self.collected == self.total:
            print("New Level")
            self.forcePlayMusic("intermission.wav")
            self.level += 1
            self.newLevel()

        if self.level - 1 == 8:  # (self.levels[0][0] + self.levels[0][1]) // 50:
            print("You win", self.level, len(self.levels))
            running = False
        self.softRender()

    # Render method
    def render(self):
        self.screen.fill((0, 0, 0))  # Limpa a tela
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
                    tileImage = pygame.transform.scale(tileImage, (square, square))
                    self.screen.blit(tileImage, (j * square, i * square, square, square))
                elif self.board.gameBoard[i][j] == 2:  # Desenhar Tic-Tak
                    pygame.draw.circle(self.screen, pelletColor, (j * square + square // 2, i * square + square // 2), square // 4)
                elif self.board.gameBoard[i][j] == 5:  # Tic-Tak especial preto
                    pygame.draw.circle(self.screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2), square // 2)
                elif self.board.gameBoard[i][j] == 6:  # Tic-Tak especial branco
                    pygame.draw.circle(self.screen, pelletColor, (j * square + square // 2, i * square + square // 2), square // 2)

                currentTile += 1

        # Desenhar os fantasmas e pacman
        for ghost in self.create_ghosts():
            ghost.draw()
        self.pacman.draw()
        pygame.display.update()

    def softRender(self):
        pointsToDraw = []
        for point in self.points:
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.points.remove(point)
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
        # Updates the screen
        pygame.display.update()

    def playMusic(self, music):
        global musicPlaying
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unload()
            pygame.mixer.music.load(MusicPath + music)
            pygame.mixer.music.queue(MusicPath + music)
            pygame.mixer.music.play()
            if music == "munch_1.wav":
                musicPlaying = 0
            elif music == "siren_1.wav":
                musicPlaying = 2
            else:
                musicPlaying = 1

    def forcePlayMusic(self, music):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(MusicPath + music)
        pygame.mixer.music.play()
        global musicPlaying
        musicPlaying = 1

    def clearBoard(self):
        # Draw tiles around ghosts and pacman
        for ghost in self.create_ghosts():
            self.drawTilesAround(ghost.row, ghost.col)
        self.drawTilesAround(self.pacman.row, self.pacman.col)
        self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])
        # Clears Ready! Label
        self.drawTilesAround(20, 10)
        self.drawTilesAround(20, 11)
        self.drawTilesAround(20, 12)
        self.drawTilesAround(20, 13)
        self.drawTilesAround(20, 14)

    def checkSurroundings(self):
        # Check if pacman got killed
        for ghost in self.create_ghosts():
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                if self.lives == 1:
                    print("You lose")
                    self.forcePlayMusic("death_1.wav")
                    self.gameOver = True
                    # Removes the ghosts from the screen
                    for ghost in self.create_ghosts():
                        self.drawTilesAround(ghost.row, ghost.col)
                    self.drawTilesAround(self.pacman.row, self.pacman.col)
                    self.pacman.draw()
                    pygame.display.update()
                    pause(10000000)
                    return
                self.started = False
                self.forcePlayMusic("pacman_death.wav")
                self.reset()
            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                ghost.setDead(True)
                ghost.setTarget()
                ghost.ghostSpeed = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.ghostScore
                self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                self.ghostScore *= 2
                self.forcePlayMusic("eat_ghost.wav")
        if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and not self.berryState[2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
            self.berryState[2] = True
            self.score += self.berryScore
            self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
            self.berriesCollected.append(self.berries[(self.level - 1) % 8])
            self.forcePlayMusic("eat_fruit.wav")

    # Displays the current score
    def displayScore(self):
        textOneUp = ["tile033.png", "tile021.png", "tile016.png"]
        textHighScore = ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png", "tile002.png", "tile014.png", "tile018.png", "tile004.png"]
        index = 0
        scoreStart = 5
        highScoreStart = 11
        for i in range(scoreStart, scoreStart + len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            self.screen.blit(tileImage, (i * square, 4, square, square))
            index += 1
        score = str(self.score)
        if score == "0":
            score = "00"
        index = 0
        for i in range(0, len(score)):
            digit = int(score[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            self.screen.blit(tileImage, ((scoreStart + 2 + index) * square, square + 4, square, square))
            index += 1

        index = 0
        for i in range(highScoreStart, highScoreStart + len(textHighScore)):
            tileImage = pygame.image.load(TextPath + textHighScore[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            self.screen.blit(tileImage, (i * square, 4, square, square))
            index += 1

        highScore = str(self.highScore)
        if highScore == "0":
            highScore = "00"
        index = 0
        for i in range(0, len(highScore)):
            digit = int(highScore[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            self.screen.blit(tileImage, ((highScoreStart + 6 + index) * square, square + 4, square, square))
            index += 1

    def drawBerry(self):
        if self.levelTimer in range(self.berryState[0], self.berryState[1]) and not self.berryState[2]:
            berryImage = pygame.image.load(ElementPath + self.berries[(self.level - 1) % 8])
            berryImage = pygame.transform.scale(berryImage, (int(square * spriteRatio), int(square * spriteRatio)))
            self.screen.blit(berryImage, (self.berryLocation[1] * square, self.berryLocation[0] * square, square, square))

    def drawPoints(self, points, row, col):
        pointStr = str(points)
        index = 0
        for i in range(len(pointStr)):
            digit = int(pointStr[i])
            tileImage = pygame.image.load(TextPath + "tile" + str(224 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square // 2, square // 2))
            self.screen.blit(tileImage, ((col) * square + (square // 2 * index), row * square - 20, square // 2, square // 2))
            index += 1

    def drawReady(self):
        ready = ["tile274.png", "tile260.png", "tile256.png", "tile259.png", "tile281.png", "tile283.png"]
        for i in range(len(ready)):
            letter = pygame.image.load(TextPath + ready[i])
            letter = pygame.transform.scale(letter, (int(square), int(square)))
            self.screen.blit(letter, ((11 + i) * square, 20 * square, square, square))

    def gameOverFunc(self):
        global running
        if self.gameOverCounter == 12:
            running = False
            self.recordHighScore()
            return

        # Resets the screen around pacman
        self.drawTilesAround(self.pacman.row, self.pacman.col)

        # Draws new image
        pacmanImage = pygame.image.load(ElementPath + "tile" + str(116 + self.gameOverCounter) + ".png")
        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        self.screen.blit(pacmanImage, (self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset, square, square))
        pygame.display.update()
        pause(5000000)
        self.gameOverCounter += 1

    def displayLives(self):
        # 33 rows || 28 cols
        # Lives[[31, 5], [31, 3], [31, 1]]
        livesLoc = [[34, 3], [34, 1]]
        for i in range(self.lives - 1):
            lifeImage = pygame.image.load(ElementPath + "tile054.png")
            lifeImage = pygame.transform.scale(lifeImage, (int(square * spriteRatio), int(square * spriteRatio)))
            self.screen.blit(lifeImage, (livesLoc[i][1] * square, livesLoc[i][0] * square - spriteOffset, square, square))

    def displayBerries(self):
        firstBerrie = [34, 26]
        for i in range(len(self.berriesCollected)):
            berrieImage = pygame.image.load(ElementPath + self.berriesCollected[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(square * spriteRatio), int(square * spriteRatio)))
            self.screen.blit(berrieImage, ((firstBerrie[1] - (2 * i)) * square, firstBerrie[0] * square + 5, square, square))

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
        self.lives += 1
        self.collected = 0
        self.started = False
        self.berryState = [200, 400, False]
        self.levelTimer = 0
        self.lockedIn = True
        for level in self.levels:
            level[0] = min((level[0] + level[1]) - 100, level[0] + 50)
            level[1] = max(100, level[1] - 50)
        random.shuffle(self.levels)
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        self.board.gameBoard = copy.deepcopy(board.gameBoard)
        self.render()

    def drawTilesAround(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row - 2, row + 3):
            for j in range(col - 2, col + 3):
                if i >= 3 and i < len(self.board.gameBoard) - 2 and j >= 0 and j < len(self.board.gameBoard[0]):
                    imageName = str(((i - 3) * len(self.board.gameBoard[0])) + j)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                        imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))
                    # Display image of tile
                    self.screen.blit(tileImage, (j * square, i * square, square, square))

                    if self.board.gameBoard[i][j] == 2:  # Draw Tic-Tak
                        pygame.draw.circle(self.screen, pelletColor, (j * square + square // 2, i * square + square // 2), square // 4)
                    elif self.board.gameBoard[i][j] == 5:  # Black Special Tic-Tak
                        pygame.draw.circle(self.screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2), square // 2)
                    elif self.board.gameBoard[i][j] == 6:  # White Special Tic-Tak
                        pygame.draw.circle(self.screen, pelletColor, (j * square + square // 2, i * square + square // 2), square // 2)

    # Flips Color of Special Tic-Taks
    def flipColor(self):
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] == 5:
                    self.board.gameBoard[i][j] = 6
                    pygame.draw.circle(self.screen, pelletColor, (j * square + square // 2, i * square + square // 2), square // 2)
                elif self.board.gameBoard[i][j] == 6:
                    self.board.gameBoard[i][j] = 5
                    pygame.draw.circle(self.screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2), square // 2)

    def getCount(self):
        total = 0
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] == 2 or self.board.gameBoard[i][j] == 5 or self.board.gameBoard[i][j] == 6:
                    total += 1
        return total

    def getHighScore(self):
        with open(DataPath + "HighScore.txt", "r") as file:
            highScore = int(file.read())
        return highScore

    def recordHighScore(self):
        with open(DataPath + "HighScore.txt", "w") as file:
            file.write(str(self.highScore))


    def create_ghosts(self):
        global ghosts
        if ghosts is None:
            ghosts = [
                Ghost(14.0, 13.5, "red", 0, self),
                Ghost(17.0, 11.5, "blue", 1, self),
                Ghost(17.0, 13.5, "pink", 2, self),
                Ghost(17.0, 15.5, "orange", 3, self)
            ]
        return ghosts

ghosts = None