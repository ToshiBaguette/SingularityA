import utils, pygame
from pygame.locals import *

def drawSettings(screen, settings, font):
    screen.fill((3, 113, 171), (0, 0, 600, 600))  # Fond bleu
    
    # Volume
    actualVolume = float(settings["Volume"])
    screen.fill((74, 192, 255), (10, 120, 580, 100))  # Fond plus clair
    textVolume = font.render("Volume : " + str(actualVolume), False, (255, 255, 255))
    screen.blit(textVolume, (20, 130))
    screen.fill((255, 255, 255), (15, 180, 570, 5))
    # Attention gros calcul de ses morts
    volumeCursorX = actualVolume * 585 / 100 - 10
    pygame.draw.ellipse(screen, (255, 255, 255), (volumeCursorX, 171, 20, 20))

    # Back Button
    pygame.draw.ellipse(screen, (74, 192, 255), (5, 5, 50, 50))
    pygame.draw.polygon(screen, (255, 255, 255),
                        ((40, 15), (40, 45), (10, 30))
                        )


def Options(screen):
    settings = utils.loadSettings()
    continuer = True
    font = pygame.font.SysFont("Arial", 21)

    drawSettings(screen, settings, font)
    pygame.display.update()

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
                return ["Quit", "Scene1", 1]
            elif event.type == MOUSEMOTION and event.buttons[0] == 1:
                if event.pos[0] < 570 and event.pos[0] > 14 and event.pos[1] < 201 and event.pos[1] > 179:
                    settings["Volume"] = round(event.pos[0] * 100 / 570, 1)
                    drawSettings(screen, settings, font)
                    pygame.display.update()
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[0] <= 55 and event.pos[0] >= 5 and event.pos[1] <= 55 and event.pos[1] >= 5:
                    utils.saveSettings(settings)
                    return ["Title", "Scene1", 1]


