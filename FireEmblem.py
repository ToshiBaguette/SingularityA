import pygame
import Battle
import DialogueScene
import TitleScreen
import LoadMenu
import SaveMenu
import Options
import utils
from pygame.locals import *


def init():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    return screen

def FireEmblem(screen):
    inGame = True
    nbSave = 0
    state = ["Title", "Scene1", 1]
    characters = []
    while inGame:
        if state[0] == "Dialogue":
            state = DialogueScene.Dialogue(screen, state[1], state[2])
        elif state[0] == "Battle":
            infosBattle = utils.loadBattle(state[1], nbSave)
            endBattle = Battle.battle(screen, infosBattle[0], infosBattle[1], infosBattle[2], infosBattle[3])
            state = endBattle[0]
            characters = endBattle[1]
            if state[0] not in ["Quit", "Title"]:
                utils.save("auto", state[0], state[1], state[2], pygame.Surface((600, 600)), characters)
        elif state[0] == "Title":
            state = TitleScreen.TitleScreen(screen)
        elif state[0] == "Load":
            state = LoadMenu.loadMenu(screen)
        elif state[0] == "Save":
            state = SaveMenu.SaveMenu(screen, state[1], state[2], state[3], state[4], characters)
        elif state[0] == "Options":
            state = Options.Options(screen)
        elif state[0] == "Quit":
            inGame = False


if __name__ == '__main__':
    FireEmblem(init())
    pygame.quit()
