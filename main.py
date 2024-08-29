from board import pixel
from config import CaminhoDoTexto, CaminhoDasMusicas
import config
from game import jogo
import pygame

# Variável para verificar se o jogo está na tela de lançamento (tela inicial)
naTelaInicial = True

# Inicializa os módulos de áudio e pygame
pygame.mixer.init()
pygame.init()

# Configurações da tela
tela = pygame.display.set_mode((config.width, config.height))
pygame.display.flip()

# Inicializa o jogo com o nível 1, pontuação inicial e tela
jogo = jogo(1, config.score_inicial, tela)

# Loop principal do jogo
running = True
relogio = pygame.time.Clock()

# Definição das teclas de controle do jogo
PLAYING_KEYS = {
    "up": [pygame.K_w, pygame.K_UP],      # Teclas para mover para cima
    "down": [pygame.K_s, pygame.K_DOWN],  # Teclas para mover para baixo
    "right": [pygame.K_d, pygame.K_RIGHT],  # Teclas para mover para a direita
    "left": [pygame.K_a, pygame.K_LEFT]   # Teclas para mover para a esquerda
}

# Função para exibir a tela de lançamento


def telaInicial():
    # Carrega e exibe o papel de parede
    wallpaper = pygame.image.load("wallpaper.jpg")
    wallpaper = pygame.transform.scale(
        wallpaper, (config.width, config.height))
    tela.blit(wallpaper, (0, 0))

    # Ajusta a escala das letras do título
    escala_letra = 20
    title = ["tituloP.png", "snorlax.png", "tituloK.png", "tituloE.png",
             "espacoTitulo.png", "tituloM.png", "tituloA.png", "tituloN.png"]
    tamanho_titulo = len(title) * escala_letra * 4
    tamanho_tela = config.width
    inicio_x = (tamanho_tela - tamanho_titulo) // 2

    # Desenha o título centralizado na tela
    for i, part in enumerate(title):
        letra = pygame.image.load(CaminhoDoTexto + part)
        letra = pygame.transform.scale(
            letra, (int(escala_letra * 4), int(escala_letra * 4)))
        tela.blit(letra, (inicio_x + (4 * i * escala_letra),
                  2 * escala_letra, escala_letra, escala_letra))

    # Centraliza o texto "Press Space to Play"
    instructions = ["tituloA.png", "tituloP.png", "tituloE.png", "tituloR.png", "tituloT.png", "tituloE.png",
                    "espacoTitulo.png", "tituloE.png", "tituloS.png", "tituloP.png", "tituloA.png", "tituloC.png",
                    "tituloO.png", "espacoTitulo.png", "tituloP.png", "tituloA.png", "tituloR.png", "tituloA.png",
                    "espacoTitulo.png", "tituloJ.png", "tituloO.png", "tituloG.png", "tituloA.png", "tituloR.png"]

    instructions_width = len(instructions) * pixel
    start_x_instructions = (tamanho_tela - instructions_width) // 2
    # Centraliza verticalmente na tela
    inicio_y = (config.height // 2)

    for i in range(len(instructions)):
        letra = pygame.image.load(CaminhoDoTexto + instructions[i])
        letra = pygame.transform.scale(letra, (int(pixel), int(pixel)))
        tela.blit(letra, (start_x_instructions + i * pixel,
                  inicio_y, pixel, pixel))

    pygame.mixer.music.load(
        CaminhoDasMusicas + "oppening.wav")
    pygame.mixer.music.play()
    pygame.display.update()


# Exibe a tela de lançamento inicialmente
running = True
naTelaInicial = True
telaInicial()
relogio = pygame.time.Clock()

# Função para pausar o jogo por um determinado tempo


def pause(time):
    cur = 0
    while not cur == time:
        cur += 1


# Loop principal do jogo
while running:
    relogio.tick(40)  # Controla a taxa de quadros por segundo (FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Se o jogador fechar a janela, salva o high score e encerra o jogo
            running = False
        elif event.type == pygame.KEYDOWN:
            # Detecta se alguma tecla foi pressionada
            jogo.pause = False
            jogo.comecou = True
            if event.key in PLAYING_KEYS["up"]:
                # Move o Pacman para cima se não estiver na tela de lançamento
                if not naTelaInicial:
                    jogo.pacman.novaDirecao = 0
            elif event.key in PLAYING_KEYS["right"]:
                # Move o Pacman para a direita se não estiver na tela de lançamento
                if not naTelaInicial:
                    jogo.pacman.novaDirecao = 1
            elif event.key in PLAYING_KEYS["down"]:
                # Move o Pacman para baixo se não estiver na tela de lançamento
                if not naTelaInicial:
                    jogo.pacman.novaDirecao = 2
            elif event.key in PLAYING_KEYS["left"]:
                # Move o Pacman para a esquerda se não estiver na tela de lançamento
                if not naTelaInicial:
                    jogo.pacman.novaDirecao = 3
            elif event.key == pygame.K_SPACE:
                # Se a tecla espaço for pressionada na tela de lançamento, inicia o jogo
                if naTelaInicial:
                    naTelaInicial = False
                    jogo.pause = True
                    jogo.comecou = False
                    jogo.render()
                    pygame.mixer.music.load(
                        CaminhoDasMusicas + "pacman_beginning.wav")
                    pygame.mixer.music.play()
                    musicaTocando = 1
            elif event.key == pygame.K_q:
                # Se a tecla "Q" for pressionada, encerra o jogo e salva o high score
                running = False

    if not naTelaInicial:
        # Atualiza o estado do jogo se não estiver na tela de lançamento
        jogo.atualiza()
