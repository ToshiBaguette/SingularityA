import pygame, utils
from pygame.locals import *

def getSaves(page):
    # 5 saves par page
    start = (page - 1) * 5 - 1
    end = page * 5 - 1

    saves = []

    for i in range(start, end):
        if i == -1:
            saves.append(utils.load("auto"))  # On charge la sauvegarde auto
        else:
            saves.append(utils.load(i))
    return saves

def drawSaves(screen, saves, cursor, page):
    font = pygame.font.SysFont("Arial", 21)

    p = font.render("Page " + str(page), False, (0, 0, 0))
    screen.blit(p, (5, 5))

    for i in range(5):
        x, y = (100, i * 110 + 25)
        color = [17, 104, 150]
        if cursor == i:
            color = [17, 41, 150]
        screen.fill(color, (x, y, 400, 100))
        if saves[i] is not None:
            # On calcul le tout
            img = pygame.transform.scale(saves[i].getImage(), (100, 100))
            txt = "Savegarde "
            if saves[i].getNumber() == "auto":
                txt += "auto"
            else:
                txt += ": " + str(saves[i].getNumber() + 1)
            title = font.render(txt, False, (0, 0, 0))
            createdAt = font.render("Créé : " + str(saves[i].getCreationDate()), False, (0, 0, 0))

            # On affiche le tout
            screen.blit(img, (x, y))
            screen.blit(title, (x + 105, y + 5))
            screen.blit(createdAt, (x + 105, y + 30))
        else:
            text = font.render("Pas de sauvegarde", False, (0, 0, 0))
            screen.blit(text, (x + 85, y + 30))

def loadMenu(screen):
    continuer = True
    saves = getSaves(1)
    page = 1
    cursor = 0

    screen.fill((74, 192, 255), (0, 0, 600, 600))

    screen.fill((17, 104, 150), (560, 280, 20, 20))  # Indicateur page à droite

    drawSaves(screen, saves, cursor, 1)
    pygame.display.update()

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                return ["Quit"]
            if event.type == KEYDOWN:
                if event.key == K_DOWN and cursor < 4:
                    cursor += 1
                elif event.key == K_UP and cursor > 0:
                    cursor -= 1
                elif event.key == K_RIGHT:
                    page += 1
                    saves = getSaves(page)
                    cursor = 0
                elif event.key == K_LEFT and page > 1:
                    page -= 1
                    saves = getSaves(page)
                    cursor = 0
                elif event.key == K_RETURN and saves[cursor] is not None:
                    # On prend cette save
                    return saves[cursor].toState()
                elif event.key == K_ESCAPE or event.key == K_DELETE:
                    return ["Title"]

                screen.fill((74, 192, 255), (0, 0, 600, 600))
                if page > 1:
                    screen.fill((17, 104, 150), (20, 280, 20, 20))  # Indicateur page à gauche
                screen.fill((17, 104, 150), (560, 280, 20, 20))  # Indicateur page à droite

                drawSaves(screen, saves, cursor, page)
                pygame.display.update()

