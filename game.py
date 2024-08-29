import random
import pygame
import copy
import board
import math
from random import randrange
from characters import Pacman, Ghost
from config import CaminhoDoBoard, spriteRatio, spriteOffset, pixel, CaminhoDosElementos, corTickTack, CaminhoDasMusicas, CaminhoDoTexto, CaminhoDaPontuacao
from board import Board
import os

# Classe principal que gerencia o jogo


class jogo:
    def __init__(self, nivel, score, tela):
        # Inicializa os atributos do jogo
        self.pause = True  # Inicia o jogo em modo pausado
        self.atualizarDelayFantasma = 1  # Define o atraso na atualização dos fantasmas
        self.atualizarFantasma = 0  # Contador de atualização dos fantasmas
        self.atualizarDelayPacman = 1  # Define o atraso na atualização do Pacman
        self.atualizacaoContadorPacman = 0  # Contador de atualização do Pacman
        # Define o atraso para mudar a cor dos Tic-Taks especiais
        self.mudarDelayTickTack = 10
        self.contagemTickTack = 0  # Contador para a mudança de cor dos Tic-Taks
        self.fantasmaAtacado = False  # Indica se algum fantasma foi atacado
        self.highScore = self.getHighScore()  # Obtém a pontuação mais alta
        self.score = score  # Define a pontuação inicial do jogador
        self.nivel = nivel  # Define o nível inicial do jogo
        self.vidas = 3  # Define o número de vidas iniciais do Pacman
        # Inicializa o Pacman na posição especificada
        self.pacman = Pacman(26.0, 13.5, self)
        self.tela = tela  # Define a superfície da tela onde o jogo será renderizado
        self.board = Board(tela)  # Inicializa o tabuleiro do jogo
        self.total = self.getCount()  # Conta o número total de Tic-Taks no tabuleiro
        self.pontuacaoFantasma = 200  # Pontuação inicial para fantasmas
        self.niveis = [[350, 250], [150, 450], [150, 450],
                       [0, 600]]  # Configura os níveis de dificuldade
        random.shuffle(self.niveis)  # Embaralha a ordem dos tempos dos níveis
        self.fantasmasStates = [[1, 0], [0, 0], [1, 0],
                                [0, 0]]  # Estados iniciais dos fantasmas
        index = 0
        for state in self.fantasmasStates:
            # Define se o fantasma está caçando ou fugindo
            state[0] = randrange(2)
            # Define o tempo inicial no estado atual
            state[1] = randrange(self.niveis[index][state[0]] + 1)
            index += 1
        self.coletado = 0  # Contador de Tic-Taks coletados
        self.comecou = False  # Indica se o jogo começou
        self.gameOver = False  # Indica se o jogo terminou
        self.contadorGameOver = 0  # Contador do estado de game over
        self.pontos = []  # Lista para armazenar os pontos que aparecem temporariamente na tela
        self.timerPontos = 10  # Define o tempo de exibição dos pontos temporários
        # Estado das frutas (tempo para aparecer, tempo para desaparecer, se foi coletada)
        self.frutasState = [200, 400, False]
        # Posição onde as frutas aparecem
        self.localizacaoFrutas = [20.0, 13.5]
        self.frutas = ["berrie1.png", "berrie2.png", "berrie3.png", "berrie4.png",
                       # Lista de frutas disponíveis
                       "berrie5.png", "berrie6.png", "berrie7.png", "berrie8.png"]
        self.frutasColetadas = []  # Lista de frutas coletadas pelo jogador
        self.timerNivel = 0  # Contador de tempo para o nível atual
        self.pontuacaoFrutas = 100  # Pontuação obtida ao coletar uma fruta
        # Tempo em que os fantasmas ficam presos no início do nível
        self.timerFantasmasPresos = 100
        self.fantasmasPresos = True  # Indica se os fantasmas ainda estão presos
        # Indica se o jogador já ganhou uma vida extra ao alcançar 10.000 pontos
        self.novaVidaExtra = False
        self.musicaTocando = 0  # Controla qual música está tocando
        self.morreu = False  # Indica se o Pacman morreu
        self.gameOverAjustado = False  # Indica se o estado de game over foi tratado

    def reset(self):
        self.morreu = True
        [fantasma.definirAlvo() for fantasma in self.criar_fantasma()]
        self.pacman = Pacman(26.0, 13.5, self)
        self.pause = True
        self.render()

    def atualiza(self):
        # Se o jogo terminou, executa as ações de Game Over
        if self.gameOver:
            if not self.gameOverAjustado:
                self.guardarHighScore()  # Salva a pontuação mais alta
                self.funcaoDeGameOver()  # Executa a função de Game Over
                self.gameOverAjustado = True
            return

        # Se o jogo está pausado ou ainda não começou, exibe a mensagem "READY!" e desenha ao redor
        if self.pause or not self.comecou:
            self.desenharAoRedor(21, 10)
            self.desenharAoRedor(21, 11)
            self.desenharAoRedor(21, 12)
            self.desenharAoRedor(21, 13)
            self.desenharAoRedor(21, 14)
            self.desenhaReady()
            pygame.display.update()
            return

        # Incrementa os temporizadores para controle do nível e atualização dos personagens
        self.timerNivel += 1
        self.atualizarFantasma += 1
        self.atualizacaoContadorPacman += 1
        self.contagemTickTack += 1
        self.fantasmaAtacado = False  # Reseta o estado de fantasma atacado

        # Verifica se o jogador alcançou 10.000 pontos e ganha uma vida extra se ainda não ganhou
        if self.score >= 10000 and not self.novaVidaExtra:
            self.vidas += 1
            self.novaVidaExtra = True
            self.forcarTocarMusica("pacman_extrapac.wav")

        # Limpa o tabuleiro ao redor dos personagens para atualizações
        self.limparBoard()

        # Marca se algum fantasma foi atacado
        for fantasma in self.criar_fantasma():
            if fantasma.atacado:
                self.fantasmaAtacado = True

        # Atualiza os estados dos fantasmas entre caçar e fugir
        for index, state in enumerate(self.fantasmasStates):
            state[1] += 1
            if state[1] >= self.niveis[index][state[0]]:
                state[0] = (state[0] + 1) % 2  # Alterna entre caçar e fugir
                state[1] = 0

        # Define o alvo dos fantasmas como o Pacman se estiverem em modo de caça
        for index, fantasma in enumerate(self.criar_fantasma()):
            if not fantasma.atacado and not fantasma.morto and self.fantasmasStates[index][0] == 0:
                fantasma.alvo = [self.pacman.row, self.pacman.col]

        # Libera os fantasmas presos após o tempo inicial do nível
        if self.timerNivel == self.timerFantasmasPresos:
            self.fantasmasPresos = False

        # Verifica se há interações entre Pacman e fantasmas ou frutas
        self.checarArredores()

        # Atualiza os fantasmas a cada ciclo determinado por `atualizarDelayFantasma`
        if self.atualizarFantasma == self.atualizarDelayFantasma:
            for fantasma in self.criar_fantasma():
                fantasma.definirDirecao()  # Define a direção do fantasma
                fantasma.atualizar()  # Atualiza o estado do fantasma
            self.atualizarFantasma = 0

        # Muda a cor dos Tic-Taks especiais a cada ciclo determinado por `mudarDelayTickTack`
        if self.contagemTickTack == self.mudarDelayTickTack:
            self.piscarCor()
            self.contagemTickTack = 0

        # Atualiza o Pacman a cada ciclo determinado por `atualizarDelayPacman`
        if self.atualizacaoContadorPacman == self.atualizarDelayPacman:
            self.atualizacaoContadorPacman = 0
            self.pacman.atualizar()
            self.pacman.col %= len(self.board.gameBoard[0])  # Mantém o Pacman dentro dos limites do tabuleiro

            # Verifica se o Pacman comeu um Tic-Tak normal ou especial
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                cell_value = self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)]
                if cell_value == 2:  # Tic-Tak normal
                    self.tocarMusica("munch_1.wav")
                    self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1  # Marca como comido
                    self.score += 10  # Aumenta a pontuação
                    self.coletado += 1  # Incrementa o contador de Tic-Taks coletados
                    pygame.draw.rect(self.tela, (57, 140, 16), (self.pacman.col * pixel, self.pacman.row * pixel, pixel, pixel))
                elif cell_value in [5, 6]:  # Tic-Tak especial
                    self.forcarTocarMusica("power_pellet.wav")
                    self.board.gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1  # Marca como comido
                    self.coletado += 1  # Incrementa o contador de Tic-Taks coletados
                    pygame.draw.rect(self.tela, (57, 140, 16), (self.pacman.col * pixel, self.pacman.row * pixel, pixel, pixel))
                    self.score += 50  # Aumenta a pontuação
                    self.pontuacaoFantasma = 200  # Define a pontuação base para fantasmas
                    for fantasma in self.criar_fantasma():
                        fantasma.contadorAposAtaque = 0  # Reseta o contador de ataque
                        fantasma.setAttacked(True)  # Coloca o fantasma em estado de ataque
                        fantasma.definirAlvo()  # Redefine o alvo do fantasma
                        self.fantasmaAtacado = True  # Marca que um fantasma foi atacado

            # Verifica novamente as interações após a atualização do Pacman
            self.checarArredores()

            # Verifica se todos os Tic-Taks foram coletados
            if self.coletado == self.total:
                self.forcarTocarMusica("intermission.wav")
                self.nivel += 1  # Avança para o próximo nível
                self.newLevel()  # Configura o novo nível

            # Verifica se o jogador completou todos os níveis
            if self.nivel - 1 == 8:
                global running
                running = False  # Termina o jogo

            # Renderiza o estado atual do jogo
            self.softRender()

    def render(self):
        self.tela.fill((57, 140, 16))  # Limpa a tela com a cor verde
        lugarNoBoardAtual = 0
        self.mostrarVidas()  # Exibe as vidas restantes do Pacman
        self.mostrarScore()  # Exibe a pontuação atual e o high score
        
        # Itera pelas linhas do tabuleiro para desenhar os elementos
        for i in range(3, len(self.board.gameBoard) - 2):
            # Itera pelas colunas do tabuleiro
            for j in range(len(self.board.gameBoard[0])):
                # Se a célula contém uma parede
                if self.board.gameBoard[i][j] == 3:
                    # Gera o nome da imagem da parede com base na posição
                    imageName = str(lugarNoBoardAtual).zfill(3)
                    imageName = "board" + imageName + ".png"
                    # Carrega e redimensiona a imagem da parede
                    tileImage = pygame.image.load(CaminhoDoBoard + imageName)
                    tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
                    # Desenha a parede na tela
                    self.tela.blit(tileImage, (j * pixel, i * pixel, pixel, pixel))
                elif self.board.gameBoard[i][j] == 2:  # Se a célula contém um Tic-Tak
                    pygame.draw.circle(self.tela, corTickTack, 
                                    (j * pixel + pixel // 2, i * pixel + pixel // 2), 
                                    pixel // 4)  # Desenha o Tic-Tak
                elif self.board.gameBoard[i][j] == 5:  # Se a célula contém um Tic-Tak especial preto
                    pygame.draw.circle(self.tela, (57, 140, 16), 
                                    (j * pixel + pixel // 2, i * pixel + pixel // 2), 
                                    pixel // 2)  # Desenha o Tic-Tak especial
                elif self.board.gameBoard[i][j] == 6:  # Se a célula contém um Tic-Tak especial branco
                    pygame.draw.circle(self.tela, corTickTack, 
                                    (j * pixel + pixel // 2, i * pixel + pixel // 2), 
                                    pixel // 2)  # Desenha o Tic-Tak especial
                lugarNoBoardAtual += 1  # Incrementa o contador de posição no tabuleiro
        
        # Desenha os fantasmas e o Pacman na tela
        for fantasma in self.criar_fantasma():
            fantasma.desenho()  # Desenha o fantasma na posição atual
        self.pacman.desenho()  # Desenha o Pacman na posição atual
        pygame.display.update()  # Atualiza a tela com as novas imagens

    def softRender(self):
        pontosParaDesenhar = []  # Lista para armazenar os pontos que precisam ser desenhados
        
        # Verifica os pontos temporários que precisam ser exibidos
        for point in self.pontos:
            if point[3] < self.timerPontos:
                pontosParaDesenhar.append([point[2], point[0], point[1]])
                point[3] += 1  # Incrementa o contador de exibição do ponto
            else:
                self.pontos.remove(point)  # Remove o ponto se o tempo de exibição expirou
                self.desenharAoRedor(point[0], point[1])  # Redesenha o bloco onde o ponto estava

        for point in pontosParaDesenhar:
            self.drawPoints(point[0], point[1], point[2])  # Desenha os pontos que ainda estão sendo exibidos

        # Desenha os fantasmas e o Pacman na tela
        for fantasma in self.criar_fantasma():
            fantasma.desenho()  # Desenha o fantasma na posição atual
        self.pacman.desenho()  # Desenha o Pacman na posição atual
        
        self.mostrarScore()  # Exibe a pontuação atual
        self.mostrarFrutas()  # Exibe as frutas coletadas
        self.mostrarVidas()  # Exibe as vidas restantes
        self.desenharFrutas()  # Desenha a fruta se estiver disponível
        pygame.display.update()  # Atualiza a tela com as novas imagens

    def tocarMusica(self, music):
        global musicaTocando
        if not pygame.mixer.music.get_busy():  # Se nenhuma música está tocando, toca a nova música
            pygame.mixer.music.unload()  # Para a música atual
            pygame.mixer.music.load(CaminhoDasMusicas + music)  # Carrega a nova música
            pygame.mixer.music.queue(CaminhoDasMusicas + music)  # Adiciona a música à fila
            pygame.mixer.music.play()  # Toca a música
            
            # Define qual música está tocando com base no arquivo
            if music == "munch_1.wav":
                musicaTocando = 0
            elif music == "siren_1.wav":
                musicaTocando = 2
            else:
                musicaTocando = 1

    def forcarTocarMusica(self, music):
        # Força a interrupção da música atual para tocar uma nova imediatamente
        pygame.mixer.music.unload()  # Para a música atual
        pygame.mixer.music.load(CaminhoDasMusicas + music)  # Carrega a nova música
        pygame.mixer.music.play()  # Toca a nova música
        
        global musicaTocando
        musicaTocando = 1  # Marca que uma nova música está tocando

    def limparBoard(self):
        # Limpa as áreas ao redor dos fantasmas, Pacman e frutas
        for fantasma in self.criar_fantasma():
            self.desenharAoRedor(fantasma.row, fantasma.col)  # Redesenha o bloco ao redor do fantasma
        self.desenharAoRedor(self.pacman.row, self.pacman.col)  # Redesenha o bloco ao redor do Pacman
        self.desenharAoRedor(self.localizacaoFrutas[0], self.localizacaoFrutas[1])  # Redesenha o bloco ao redor da fruta
        
        # Limpa a área onde o texto "READY!" é exibido
        for i in range(10, 15):
            self.desenharAoRedor(20, i)


    def checarArredores(self):
        # Verifica as interações entre o Pacman e os fantasmas ou frutas
        for fantasma in self.criar_fantasma():
            if self.touchingPacman(fantasma.row, fantasma.col) and not fantasma.atacado:
                self.vidas -= 1  # Se um fantasma não atacado toca o Pacman, o Pacman perde uma vida
                
                if self.vidas == 0:
                    self.forcarTocarMusica("death_1.wav")  # Toca a música de fim de jogo
                    self.gameOver = True  # Marca o jogo como terminado
                else:
                    self.forcarTocarMusica("pacman_death.wav")  # Toca a música de morte do Pacman
                    self.reset()  # Reinicia o jogo com uma vida a menos
                
                return  # Sai da função após lidar com o toque de um fantasma

            elif self.touchingPacman(fantasma.row, fantasma.col) and fantasma.isAttacked() and not fantasma.isDead():
                # Se o Pacman toca um fantasma atacado e o fantasma não está morto
                fantasma.setDead(True)  # Marca o fantasma como morto
                fantasma.definirAlvo()  # Redefine o alvo do fantasma
                fantasma.velocidadeFantasma = 1  # Define a velocidade do fantasma
                fantasma.row = math.floor(fantasma.row)
                fantasma.col = math.floor(fantasma.col)
                self.score += self.pontuacaoFantasma  # Aumenta a pontuação do jogador
                
                # Adiciona os pontos temporários na tela
                self.pontos.append([fantasma.row, fantasma.col, self.pontuacaoFantasma, 0])
                self.pontuacaoFantasma *= 2  # Dobra a pontuação para o próximo fantasma
                self.forcarTocarMusica("eat_ghost.wav")  # Toca uma música especial

        # Verifica se o Pacman toca uma fruta e coleta ela
        if self.touchingPacman(self.localizacaoFrutas[0], self.localizacaoFrutas[1]) and not self.frutasState[2] and self.timerNivel in range(self.frutasState[0], self.frutasState[1]):
            self.frutasState[2] = True  # Marca a fruta como coletada
            self.score += self.pontuacaoFrutas  # Adiciona a pontuação da fruta ao jogador
            
            # Exibe os pontos temporários na tela
            self.pontos.append([self.localizacaoFrutas[0], self.localizacaoFrutas[1], self.pontuacaoFrutas, 0])
            self.frutasColetadas.append(self.frutas[(self.nivel - 1) % 8])  # Adiciona a fruta à lista de frutas coletadas
            self.forcarTocarMusica("eat_fruit.wav")  # Toca a música de sucesso ao coletar a fruta

    def mostrarScore(self):
        textOneUp = ["score1.png", "verdeU.png", "verdeP.png"]
        textHighScore = ["verdeH.png", "verdeI.png", "verdeG.png", "verdeH.png",
                        "tile015.png", "verdeS.png", "verdeC.png", "verdeO.png", "verdeR.png", "verdeE.png"]
        index = 0
        scoreStart = 5  # Início da exibição da pontuação
        highScoreStart = 11  # Início da exibição do High Score

        # Exibe o texto "1UP"
        for i in range(scoreStart, scoreStart + len(textOneUp)):
            tileImage = pygame.image.load(CaminhoDoTexto + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, (i * pixel, 4, pixel, pixel))
            index += 1

        # Exibe a pontuação atual do jogador
        score = str(self.score).zfill(2)  # Garante que a pontuação tenha pelo menos 2 dígitos
        for i, digit in enumerate(score):
            tileImage = pygame.image.load(CaminhoDoTexto + "score" + digit + ".png")
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, ((scoreStart + 2 + i) * pixel, pixel + 4, pixel, pixel))

        # Exibe o texto "HIGH SCORE"
        for i in range(highScoreStart, highScoreStart + len(textHighScore)):
            tileImage = pygame.image.load(CaminhoDoTexto + textHighScore[i - highScoreStart])
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, (i * pixel, 4, pixel, pixel))

        # Exibe o High Score registrado
        highScore = str(self.highScore[0]).zfill(2)  # Garante que o High Score tenha pelo menos 2 dígitos
        for i, digit in enumerate(highScore):
            tileImage = pygame.image.load(CaminhoDoTexto + "score" + digit + ".png")
            tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
            self.tela.blit(tileImage, ((highScoreStart + 6 + i) * pixel, pixel + 4, pixel, pixel))

    # Desenha a fruta bônus no tabuleiro quando disponível
    def desenharFrutas(self):
        # Verifica se a fruta bônus deve ser exibida no tabuleiro
        if self.timerNivel in range(self.frutasState[0], self.frutasState[1]) and not self.frutasState[2]:
            berryImage = pygame.image.load(CaminhoDosElementos + self.frutas[(self.nivel - 1) % 8])
            berryImage = pygame.transform.scale(berryImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(berryImage, (self.localizacaoFrutas[1] * pixel, self.localizacaoFrutas[0] * pixel, pixel, pixel))


    # Desenha a pontuação temporária na tela após o Pacman coletar uma fruta ou derrotar um fantasma
    def drawPoints(self, pontos, row, col):
        pointStr = str(pontos)  # Converte os pontos em string
        index = 0
        
        # Desenha cada dígito da pontuação temporária na tela
        for i in range(len(pointStr)):
            digit = pointStr[i]
            tileImage = pygame.image.load(CaminhoDoTexto + "score" + digit + ".png")
            tileImage = pygame.transform.scale(tileImage, (pixel // 2, pixel // 2))
            self.tela.blit(tileImage, ((col) * pixel + (pixel // 2 * index), row * pixel - 20, pixel // 2, pixel // 2))
            index += 1

    # Exibe o texto "READY!" na tela antes do início do jogo ou após uma vida ser perdida
    def desenhaReady(self):
        ready = ["verdeR.png", "verdeE.png", "verdeA.png", "verdeD.png", "verdeY.png", "verdeExclamacao.png"]
        
        # Desenha o texto "READY!" na tela antes do início do jogo ou após uma vida ser perdida
        for i in range(len(ready)):
            letra = pygame.image.load(CaminhoDoTexto + ready[i])
            letra = pygame.transform.scale(letra, (int(pixel), int(pixel)))
            self.tela.blit(letra, ((11 + i) * pixel, 20 * pixel, pixel, pixel))


    # Função executada quando o jogo termina
    def funcaoDeGameOver(self):
        if self.gameOverAjustado:
            return  # Previne que a função seja executada várias vezes

        # Reseta a tela
        self.tela.fill((0, 0, 0))  # Preenche a tela com preto

        # Exibe a mensagem de "GAME OVER"
        mensagemDeGameOver = ["pretoF.png", "pretoI.png", "pretoM.png", "espaco.png", "pretoD.png", "pretoE.png", "espaco.png", "pretoJ.png", "pretoO.png", "pretoG.png", "pretoO.png"]
        for i in range(len(mensagemDeGameOver)):
            letra = pygame.image.load(CaminhoDoTexto + mensagemDeGameOver[i])
            letra = pygame.transform.scale(letra, (int(pixel), int(pixel)))
            self.tela.blit(letra, ((8 + i) * pixel, 4 * pixel, pixel, pixel))

        # Exibe o título "SCORES"
        tituloDoScore = ["pretoP.png", "pretoO.png", "pretoN.png", "pretoT.png", "pretoO.png", "pretoS.png"]
        for i in range(len(tituloDoScore)):
            letra = pygame.image.load(CaminhoDoTexto + tituloDoScore[i])
            letra = pygame.transform.scale(letra, (int(pixel), int(pixel)))
            self.tela.blit(letra, ((10 + i) * pixel, 8 * pixel, pixel, pixel))

        # Exibe as 10 maiores pontuações
        scores = self.getHighScore()  # Obtém as pontuações altas
        for idx, score in enumerate(scores):
            score_str = str(score).zfill(5)  # Garante que as pontuações tenham pelo menos 4 dígitos
            for j, char in enumerate(score_str):
                tileImage = pygame.image.load(CaminhoDoTexto + "pontuacao" + char + ".png")
                tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
                self.tela.blit(tileImage, ((11 + j) * pixel, (10 + idx) * pixel, pixel, pixel))

        pygame.display.update()
        self.contadorGameOver += 1  # Incrementa o contador de Game Over

    # Exibe as vidas restantes do jogador na tela
    def mostrarVidas(self):
        localizacaoVidas = [[34, 3], [34, 1]]  # Posições para exibir as vidas
        
        # Exibe uma vida a menos que o total (Pacman já em jogo não conta)
        for i in range(self.vidas - 1):
            imagemVidas = pygame.image.load(CaminhoDosElementos + "pacman_direita_2.png")
            imagemVidas = pygame.transform.scale(imagemVidas, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(imagemVidas, (localizacaoVidas[i][1] * pixel, localizacaoVidas[i][0] * pixel - spriteOffset, pixel, pixel))

    # Exibe as frutas coletadas na parte inferior da tela
    def mostrarFrutas(self):
        firstBerrie = [34, 26]  # Posição inicial para desenhar as frutas
        
        # Exibe as frutas coletadas na parte inferior da tela
        for i in range(len(self.frutasColetadas)):
            berrieImage = pygame.image.load(CaminhoDosElementos + self.frutasColetadas[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(pixel * spriteRatio), int(pixel * spriteRatio)))
            self.tela.blit(berrieImage, ((firstBerrie[1] - (2 * i)) * pixel, firstBerrie[0] * pixel + 5, pixel, pixel))


    # Verifica se Pacman está na mesma posição que a dada pelo `row` e `col`
    def touchingPacman(self, row, col):
        # Verifica se Pacman está na mesma posição que a dada pelo `row` e `col`
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

    # Prepara o jogo para um novo nível após completar o nível atual
    def newLevel(self):
        self.reset()  # Reinicia o jogo (ex: reseta a posição do Pacman e dos fantasmas)
        self.coletado = 0  # Reseta o contador de itens coletados para o novo nível
        self.comecou = False  # Indica que o novo nível ainda não começou
        
        # Redefine o estado da fruta bônus (quando e se aparece)
        self.frutasState = [200, 400, False]
        self.timerNivel = 0  # Reseta o temporizador do nível
        self.fantasmasPresos = True  # Define o estado inicial dos fantasmas como "presos" na base

        # Ajusta os tempos dos ciclos de perseguição/espalhamento dos fantasmas para o novo nível
        for nivel in self.niveis:
            nivel[0] = min((nivel[0] + nivel[1]) - 100, nivel[0] + 50)  # Reduz o tempo de perseguição dos fantasmas
            nivel[1] = max(100, nivel[1] - 50)  # Reduz o tempo de espalhamento dos fantasmas

        random.shuffle(self.niveis)  # Embaralha os níveis dos fantasmas para variar o comportamento

        index = 0
        for state in self.fantasmasStates:
            state[0] = randrange(2)  # Aleatoriamente define se o fantasma começa perseguindo ou espalhado
            state[1] = randrange(self.niveis[index][state[0]] + 1)  # Define o tempo inicial no estado
            index += 1

        self.board.gameBoard = copy.deepcopy(board.gameBoard)  # Reinicializa o tabuleiro para o novo nível
        self.render()  # Renderiza o novo estado do jogo


    # Redesenha os tiles ao redor de uma posição específica (row, col) para garantir que o movimento do Pacman e dos fantasmas seja fluido
    def desenharAoRedor(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        
        # Redesenha os tiles ao redor de uma posição específica (row, col)
        for i in range(row - 2, row + 3):
            for j in range(col - 2, col + 3):
                if i >= 3 and i < len(self.board.gameBoard) - 2 and j >= 0 and j < len(self.board.gameBoard[0]):
                    imageName = str(((i - 3) * len(self.board.gameBoard[0])) + j).zfill(3)
                    imageName = "board" + imageName + ".png"
                    
                    # Carrega e redimensiona a imagem do tile
                    tileImage = pygame.image.load(CaminhoDoBoard + imageName)
                    tileImage = pygame.transform.scale(tileImage, (pixel, pixel))
                    self.tela.blit(tileImage, (j * pixel, i * pixel, pixel, pixel))

                    # Verifica e desenha Tic-Taks normais ou especiais
                    if self.board.gameBoard[i][j] == 2:
                        pygame.draw.circle(self.tela, corTickTack, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 4)
                    elif self.board.gameBoard[i][j] == 5:  # Tic-Tak especial preto
                        pygame.draw.circle(self.tela, (57, 140, 16), (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)
                    elif self.board.gameBoard[i][j] == 6:  # Tic-Tak especial branco
                        pygame.draw.circle(self.tela, corTickTack, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)

    # Alterna a cor dos Tic-Taks especiais para criar um efeito visual de "piscar" no tabuleiro
    def piscarCor(self):
        # Alterna a cor dos Tic-Taks especiais para criar um efeito visual de "piscar" no tabuleiro
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] == 5:
                    self.board.gameBoard[i][j] = 6  # Alterna o Tic-Tak preto para branco
                    pygame.draw.circle(self.tela, corTickTack, (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)
                elif self.board.gameBoard[i][j] == 6:
                    self.board.gameBoard[i][j] = 5  # Alterna o Tic-Tak branco para preto
                    pygame.draw.circle(self.tela, (57, 140, 16), (j * pixel + pixel // 2, i * pixel + pixel // 2), pixel // 2)

    # Conta o número total de Tic-Taks no tabuleiro para determinar o progresso do Pacman no nível
    def getCount(self):
        total = 0
        
        # Conta o número total de Tic-Taks no tabuleiro para determinar o progresso do Pacman no nível
        for i in range(3, len(self.board.gameBoard) - 2):
            for j in range(len(self.board.gameBoard[0])):
                if self.board.gameBoard[i][j] in [2, 5, 6]:
                    total += 1  # Conta os Tic-Taks normais e especiais
        
        return total

    # Obtém as pontuações mais altas registradas a partir de um arquivo de texto
    def getHighScore(self):
        if not os.path.exists(CaminhoDaPontuacao + "HighScore.txt"):
            # Cria o arquivo se não existir e inicializa com zeros
            with open(CaminhoDaPontuacao + "HighScore.txt", "w") as file:
                file.write("0\n" * 10)

        with open(CaminhoDaPontuacao + "HighScore.txt", "r") as file:
            scores = file.readlines()
            scores = [int(score.strip()) for score in scores]

        return scores

    # Registra a pontuação do jogador se for uma das 10 mais altas
    def guardarHighScore(self):
        # Garante que essa função seja chamada apenas uma vez após o jogo terminar
        if not hasattr(self, 'highScoreList'):
            self.highScoreList = self.getHighScore()  # Obtém as pontuações altas apenas uma vez

        # Verifica se a pontuação atual é maior que a menor pontuação no top 10
        if self.score > self.highScoreList[-1]:
            self.highScoreList.append(self.score)  # Adiciona a nova pontuação
            self.highScoreList.sort(reverse=True)  # Ordena as pontuações em ordem decrescente
            self.highScoreList = self.highScoreList[:10]  # Mantém apenas as 10 melhores pontuações

            # Escreve as pontuações atualizadas de volta no arquivo
            with open(CaminhoDaPontuacao + "HighScore.txt", "w") as file:
                for score in self.highScoreList:
                    file.write(str(score) + "\n")

    # Cria os fantasmas do jogo ou redefine-os se o jogador perder uma vida
    def criar_fantasma(self):
        global ghosts
        if ghosts is None or self.morreu:
            ghosts = [
                Ghost(14.0, 13.5, "charizard", 0, self),  # Cria o fantasma Charizard
                Ghost(17.0, 11.5, "owl", 1, self),  # Cria o fantasma Owl
                Ghost(17.0, 13.5, "pidgeot", 2, self),  # Cria o fantasma Pidgeot
                Ghost(17.0, 15.5, "blastoise", 3, self)  # Cria o fantasma Blastoise
            ]
            self.morreu = False  # Indica que o Pacman não está morto
    
        return ghosts



ghosts = None
