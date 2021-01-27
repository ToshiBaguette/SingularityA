import pygame, utils
from pygame.locals import *


bgTitle = pygame.image.load("Assets/Title/Background.png")

def drawMenu(screen, cursorPos, texts):
    screen.fill((0, 0, 0))
    # Draw Background
    screen.blit(bgTitle, (0, 0))

    # Texts Nouveau, Charger, Quitter
    font = pygame.font.SysFont("Arial", 21)
    for i in range(len(texts)):
        color = [255, 255, 255]
        if i == cursorPos:
            color = [255, 249, 138]
        text = font.render(texts[i], False, color)
        screen.blit(text, (580 - len(texts[i]) * 10, 400 + i * 19))



def TitleScreen(screen):
    continuer = True
    cursor = 0
    texts = ["Nouvelle Partie", "Charger Sauvegarde", "Options", "Quitter"]
    utils.loadMusic("titleScreen")
    utils.playMusic()

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                return ["Quit"]
            elif event.type == KEYDOWN:
                if event.key == K_UP and cursor > 0:
                    cursor -= 1
                elif event.key == K_DOWN and cursor < len(texts) - 1:
                    cursor += 1
                elif event.key == K_RETURN:
                    # Validation
                    if texts[cursor] == "Nouvelle Partie":
                        if utils.trueEndUnlocked():
                            return ["Dialogue", "TrueScene1", 1]  # Si on a débloqué la True End, on y va
                        return ["Dialogue", "Scene1", 1]  # Sinon, on va sur la scene de base
                    elif texts[cursor] == "Charger Sauvegarde":
                        # Faire menu sauvegardes
                        return ["Load"]
                    elif texts[cursor] == "Options":
                        return ["Options"]
                    elif texts[cursor] == "Quitter":
                        return ["Quit"]

        drawMenu(screen, cursor, texts)
        pygame.display.update()
        # Draw image Background
