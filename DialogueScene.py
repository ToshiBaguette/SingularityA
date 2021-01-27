import pygame, Scene, utils
from pygame.locals import *

def Dialogue(screen, sceneN, line):
    scene = Scene.Scene(sceneN, line)

    inGame = True
    scene.draw(screen)
    while inGame:
        for event in pygame.event.get():
            if event.type == QUIT:
                return ["Quit", ""]
            if event.type == KEYDOWN:
                if event.key in [K_RETURN, K_SPACE]:
                    finish = scene.nextLine()
                    if finish:
                        next = scene.getEnd()
                        toReturn = []
                        if "Choice" in next:
                            toReturn = ["Choice", next, 0]
                        elif "Scene" in next:
                            toReturn = ["Dialogue", next, 1]
                        elif "End" in next:
                            toReturn = ["End", next, 0]
                        elif "battle" in next or "Battle" in next:
                            toReturn = ["Battle", next, 0]
                        elif "title" in next or "Title" in next:
                            toReturn = ["Title"]
                        return toReturn
                    scene.draw(screen)
                if event.key == K_s:
                    return ["Save", "Dialogue", sceneN, scene.getCurrentLine(), screen.copy()]
        pygame.time.wait(50)


