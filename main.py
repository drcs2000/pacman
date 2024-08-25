from board import pixel
from config import TextPath, MusicPath
import config
from game import jogo
import pygame
onLaunchScreen = True

pygame.mixer.init()
pygame.init()

# tela settings
tela = pygame.display.set_mode((config.width, config.height))
pygame.display.flip()

# Initialize jogo
jogo = jogo(1, config.initial_score, tela)

# Main jogo loop
running = True
relogio = pygame.time.Clock()

PLAYING_KEYS = {
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "right": [pygame.K_d, pygame.K_RIGHT],
    "left": [pygame.K_a, pygame.K_LEFT]
}


def displayLaunchScreen():
    # Load and display the wallpaper
    wallpaper = pygame.image.load("wallpaper.jpg")
    wallpaper = pygame.transform.scale(
        wallpaper, (config.width, config.height))
    tela.blit(wallpaper, (0, 0))

    # Adjusted scaling for the letters
    letter_scale = 20
    title = ["tituloP.png", "snorlax.png", "tituloK.png", "tituloE.png",
             "espacoTitulo.png", "tituloM.png", "tituloA.png", "tituloN.png"]
    title_width = len(title) * letter_scale * 4
    screen_width = config.width
    start_x = (screen_width - title_width) // 2

    # Draw the title centered on the tela
    for i, part in enumerate(title):
        letter = pygame.image.load(TextPath + part)
        letter = pygame.transform.scale(
            letter, (int(letter_scale * 4), int(letter_scale * 4)))
        tela.blit(letter, (start_x + (4 * i * letter_scale),
                           2 * letter_scale, letter_scale, letter_scale))

    # Centering "Press Space to Play"
    instructions = ["tituloA.png", "tituloP.png", "tituloE.png", "tituloR.png", "tituloT.png", "tituloE.png", "espacoTitulo.png", "tituloE.png", "tituloS.png", "tituloP.png",
                    "tituloA.png", "tituloC.png", "tituloO.png", "espacoTitulo.png", "tituloP.png", "tituloA.png", "tituloR.png", "tituloA.png", "espacoTitulo.png", "tituloJ.png",
                    "tituloO.png", "tituloG.png", "tituloA.png", "tituloR.png"]

    instructions_width = len(instructions) * pixel
    start_x_instructions = (screen_width - instructions_width) // 2
    # Vertically center it in the tela
    start_y_instructions = (config.height // 2)

    for i in range(len(instructions)):
        letter = pygame.image.load(TextPath + instructions[i])
        letter = pygame.transform.scale(letter, (int(pixel), int(pixel)))
        tela.blit(letter, (start_x_instructions + i * pixel,
                           start_y_instructions, pixel, pixel))

    pygame.display.update()


running = True
onLaunchScreen = True
displayLaunchScreen()
relogio = pygame.time.Clock()


def pause(time):
    cur = 0
    while not cur == time:
        cur += 1


while running:
    relogio.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            jogo.recordHighScore()
        elif event.type == pygame.KEYDOWN:
            jogo.pause = False
            jogo.comecou = True
            if event.key in PLAYING_KEYS["up"]:
                if not onLaunchScreen:
                    jogo.pacman.novaDirecao = 0
            elif event.key in PLAYING_KEYS["right"]:
                if not onLaunchScreen:
                    jogo.pacman.novaDirecao = 1
            elif event.key in PLAYING_KEYS["down"]:
                if not onLaunchScreen:
                    jogo.pacman.novaDirecao = 2
            elif event.key in PLAYING_KEYS["left"]:
                if not onLaunchScreen:
                    jogo.pacman.novaDirecao = 3
            elif event.key == pygame.K_SPACE:
                if onLaunchScreen:
                    onLaunchScreen = False
                    jogo.pause = True
                    jogo.comecou = False
                    jogo.render()
                    pygame.mixer.music.load(MusicPath + "apita_o_arbitro.wav")
                    pygame.mixer.music.play()
                    musicaTocando = 1
            elif event.key == pygame.K_q:
                running = False
                jogo.recordHighScore()

    if not onLaunchScreen:
        jogo.update()
