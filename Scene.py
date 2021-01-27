import pygame, io, utils


def getDialogues(scene):
    fileScene = io.open("Dialogues/" + scene + ".txt", "r", encoding="UTF-8")
    sceneDialogues = fileScene.readlines()
    fileScene.close()
    return sceneDialogues

def getSomething(line):
    l = len(line)
    for i in range(l):
        if line[i] == "~":
            return line[i+1:l-1]  # On retire le saut de ligne

def darkenSprite(sprite):
    dark = pygame.Surface(sprite.get_size()).convert_alpha()
    for y in range(sprite.get_size()[1]):
        for x in range(sprite.get_size()[0]):
            if sprite.get_at((x, y))[3] == 255:
                dark.set_at((x, y), (0, 0, 0, 125))
            else:
                dark.set_at((x, y), (0, 0, 0, 0))
    return dark

def parseDialogue(line):
    """Retourne le personnage qui parle, son état, puis ce qu'il dit, dans un tableau de 3 éléments"""
    r = ["", "", ""]
    l = len(line)
    first = True
    firstChar = 0
    for i in range(l):
        if line[i] == "~":
            if first:
                r[0] = line[0:i]
                firstChar = i
                first = False
            else:
                r[1] = line[firstChar+1:i]
                r[2] = line[i+1:l-1]
                return r[:]
def isOnScreen(char, charactersOnScreen):
    l = len(charactersOnScreen)
    for i in range(l):
        if "Assets/" + char in charactersOnScreen[i]:
            return True
    return False
def getPosOnScreen(char, charactersOnScreen):
    l = len(charactersOnScreen)
    for i in range(l):
        if "Assets/" + char in charactersOnScreen[i]:
            return i


class Scene:
    def __init__(self, numberScene, line):
        self.dialogues = getDialogues(numberScene)
        self.background = getSomething(self.dialogues[0])
        self.imageBg = pygame.image.load("Assets/Background/" + self.background + ".png")
        self.end = getSomething(self.dialogues[-1])
        self.currentLine = line
        self.nbLines = len(self.dialogues)-2  # On retire la ligne du background et de la fin
        self.charactersOnScreen = []
        self.font = pygame.font.SysFont("Arial", 21)
        self.lastSpeak = 0

    def getEnd(self):
        return self.end
    def getCurrentLine(self):
        return self.currentLine

    def nextLine(self):
        self.currentLine += 1
        return self.currentLine == self.nbLines+1  # Si on arrive au bout de la scene, return True

    def draw(self, screen):
        # Affiche le background
        screen.blit(self.imageBg, (0, 0))

        dial = parseDialogue(self.dialogues[self.currentLine])

        if dial[0] == "Music":  # On doit changer de musique
            # Musique notée comme cela : "Music~Musique~Loop"
            utils.loadMusic(str(dial[1]))
            utils.playMusic(bool(dial[2]))
            self.nextLine()
            dial = parseDialogue(self.dialogues[self.currentLine])

        if dial[0] == "Shock":  # On va faire trembler un personnage
            # Notée "Shock~Char~Time~TimeToWait"
            self.shockCharacter(dial[1], int(dial[2].split("~")[0]), int(dial[2].split("~")[1]), screen)
            self.nextLine()
            dial = parseDialogue(self.dialogues[self.currentLine])

        if not isOnScreen(dial[0], self.charactersOnScreen):
            if len(self.charactersOnScreen) == 2:
                toRemove = 0 if self.lastSpeak == 1 else 1
                self.charactersOnScreen[toRemove] = "Assets/" + dial[0] + "/" + dial[1] + ".png"
                self.lastSpeak = toRemove
            else:
                self.charactersOnScreen.append("Assets/" + dial[0] + "/" + dial[1] + ".png")
                self.lastSpeak = getPosOnScreen(dial[0], self.charactersOnScreen)
        else:
            self.charactersOnScreen[getPosOnScreen(dial[0], self.charactersOnScreen)] = "Assets/"+dial[0]+"/"+dial[1]+".png"
            self.lastSpeak = getPosOnScreen(dial[0], self.charactersOnScreen)
        # Affiche les deux derniers personnages à avoir parlé
        for i in range(len(self.charactersOnScreen)):
            toBlit = pygame.image.load(self.charactersOnScreen[i])
            if "Assets/" + dial[0] not in self.charactersOnScreen[i]:  # Assombrit le perso qui ne parle pas
                toBlit.blit(darkenSprite(toBlit), (0, 0))

            screen.blit(toBlit, (i * 400 - 100, 50))

        # Affiche un fond BLEU
        screen.fill((25, 31, 240), (0, 400, 600, 200))

        # Affiche nom du perso en haut à gauche de la boite de dialogue
        persoActuel = self.font.render(dial[0], False, (255, 255, 255))
        screen.blit(persoActuel, (10, 410))

        # Affiche enfin la ligne de dialogue
        self.afficherDialogue(dial[2], screen)

        pygame.display.update()

    def afficherDialogue(self, line, screen):
        l = len(line)
        if l > 63:
            lines = []
            lastSeparation = 0
            for x in range(0, l):
                if x > 0 and x % 62 == 0:
                    if line[x] != " ":
                        # Recherche l'espace le plus proche
                        for y in range(x, lastSeparation, -1):
                            if line[y] == " ":
                                lines.append(line[lastSeparation:y])
                                lastSeparation = y+1
                                break
                    else:
                        lines.append(line[lastSeparation:x])
                        lastSeparation = x+1
            lines.append(line[lastSeparation:l])
            for i in range(len(lines)):
                    render = self.font.render(lines[i], False, (255, 255, 255))
                    screen.blit(render, (10, 450+i*30))
        else:
            render = self.font.render(line, False, (255, 255, 255))
            screen.blit(render, (10, 450))

    def shockCharacter(self, char, nbTimes, wait, screen):
        nbChar = 1
        toBlit = (pygame.image.load(self.charactersOnScreen[0]), pygame.image.load(self.charactersOnScreen[1]))

        if char in self.charactersOnScreen[0]:
            nbChar = 0
            toBlit[1].blit(darkenSprite(toBlit[1]), (0, 0))
        else :
            toBlit[0].blit(darkenSprite(toBlit[0]), (0, 0))

        factor = 10

        for k in range(nbTimes):
            for j in range(2):
                screen.blit(self.imageBg, (0, 0))
                for i in range(2):
                    pos = (i * 400 - 100, 50)
                    if i == nbChar:  # Assombrit le perso qui ne bouge pas
                        pos = (i * 400 - 100 + factor, 50)
                    screen.blit(toBlit[i], pos)

                # Affiche un fond BLEU pour le texte
                screen.fill((25, 31, 240), (0, 400, 600, 200))
                pygame.display.update()
                pygame.time.delay(wait)
                factor = -factor

        screen.blit(self.imageBg, (0, 0))
        for i in range(2):
            screen.blit(toBlit[i], (i * 400 - 100, 50))
        screen.fill((25, 31, 240), (0, 400, 600, 200))
        pygame.display.update()
