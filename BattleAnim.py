import pygame
from pygame.locals import *
import MenuBattle


class BattleAnim:
    def __init__(self, screen, character, enemy, enemyStats, charStats):
        self.screen = screen
        self.character = character
        self.enemy = enemy
        self.enemyStats = enemyStats
        self.charStats = charStats

        self.x = 100
        self.y = 150
        self.width = 400
        self.height = 300
        self.animSurface = pygame.Surface((self.width, self.height))

        self.posChar = [300, 50]
        self.posEnemy = [50, 50]

        self.drawStart()

    def drawChar(self, char, x, y):
        toBlit = pygame.transform.scale(char.mapImage, (100, 100))
        if char == self.enemy:
            toBlit = pygame.transform.flip(toBlit, True, False)
        self.animSurface.blit(toBlit, (x, y))
        #self.animSurface.fill((255, 255, 255), (x, y, 40, 40))

    def makeBackground(self):
        self.animSurface.fill((0, 0, 0))

    def displayLife(self, character, x, y):
        xLife = 0
        yLife = 0
        for i in range(character.getMaxHP()):
            self.animSurface.fill((75, 60, 15), (x + xLife, y + yLife, 6, 8))
            if i < character.getActualHP():
                self.animSurface.fill((255, 220, 125), (x + xLife + 1, y + yLife + 1, 4, 6))

            if (i+1) % 27 == 0:
                xLife = 0
                yLife += 10
            else:
                xLife += 7

    def drawUI(self):
        self.makeBackground()
        fontBold = pygame.font.SysFont("Arial", 19, True, False)
        fontItalic = pygame.font.SysFont("Arial", 16, False, True)
        font = pygame.font.SysFont("Arial", 19, False, False)


        stats = [["DMG", self.enemyStats[0], self.charStats[0]],
                 ["PRC", self.enemyStats[1], self.charStats[1]],
                 ["CRT", self.enemyStats[2], self.charStats[2]]]

        # En bas à gauche, nous avons les stats de l'ennemi
        self.animSurface.fill((10, 10, 250), (0, 160, 80, 70))

        # En bas à droite, nous avons nos stats
        self.animSurface.fill((10, 10, 250), (320, 160, 80, 70))

        i = 0
        for stat in stats:
            self.animSurface.blit(fontBold.render(stat[0] + " " + str(stat[1]), False, (255, 255, 255)), (1, 161 + i * 24))
            self.animSurface.blit(fontBold.render(stat[0] + " " + str(stat[2]), False, (255, 255, 255)), (321, 161 + i * 24))
            i += 1

        # Ici, on affiche les armes au dessus des barres de vie
        self.animSurface.fill((10, 100, 250), (80, 210, 100, 20))
        self.animSurface.fill((10, 100, 250), (220, 210, 100, 20))

        self.animSurface.blit(fontItalic.render(self.enemy.getLastWeaponUsed().getName(), False, (255, 255, 255)), (81, 211))
        self.animSurface.blit(fontItalic.render(self.character.getLastWeaponUsed().getName(), False, (255, 255, 255)), (221, 211))

        # Ensuite, nous avons les barres de vie affichées
        self.animSurface.fill((100, 10, 250), (0, 230, 200, 70))
        self.animSurface.fill((10, 100, 250), (200, 230, 200, 70))

        self.displayLife(self.enemy, 5, 235)
        self.displayLife(self.character, 205, 235)


    def drawNormal(self):
        self.drawUI()
        self.drawChar(self.enemy, self.posEnemy[0], self.posEnemy[1])
        self.drawChar(self.character, self.posChar[0], self.posChar[1])


    def drawStart(self):
        self.drawNormal()
        self.displayOnScreen()
        pygame.display.update((self.x, self.y, self.width, self.height))
        pygame.time.delay(1000)

    def drawXP(self, xpObtained):
        self.animSurface.fill((75, 60, 15), (50, 280, 300, 20))
        # XP Déja emmagasinée
        self.animSurface.fill((255, 220, 125), (50, 280, self.character.getXP() * 3, 20))
        self.displayOnScreen()
        pygame.display.update((self.x, self.y, self.width, self.height))

        for i in range(xpObtained):
            self.character.xp += 1
            self.animSurface.fill((255, 220, 125), (50, 280, self.character.getXP() * 3, 20))
            self.displayOnScreen()
            pygame.display.update((self.x, self.y, self.width, self.height))
            if self.character.getXP() == 100:
                lvlUp = self.character.levelUp()
                MenuBattle.LevelUpMenu((200, 100, 200, 200), self.character, lvlUp[1], lvlUp[0], self.screen)
                self.animSurface.fill((75, 60, 15), (50, 280, 300, 20))
            else:
                pygame.time.delay(50)

    def displayOnScreen(self):
        self.screen.blit(self.animSurface, (self.x, self.y))
        pygame.display.update((self.x, self.y, self.width, self.height))

    def drawCrit(self):
        font = pygame.font.SysFont("Arial", 40, True, False)

        self.drawNormal()

        self.animSurface.blit(font.render("!", False, (255, 255, 255)), (self.width // 2, 10))
        self.displayOnScreen()
        pygame.time.delay(500)

    def attack(self, char, isCrit, avoid):
        direction = -30
        if char != self.character:  # Si c'est l'ennemi qui attaque, nous devons inverser le sens d'attaque
            direction = 30

        if isCrit:
            self.drawCrit()

        self.drawUI()
        if direction > 0:
            self.drawChar(self.enemy, self.posEnemy[0] + direction, self.posEnemy[1])
            if avoid:
                self.drawChar(self.character, self.posChar[0] + direction, self.posChar[1])
            else:
                self.drawChar(self.character, self.posChar[0], self.posChar[1])
        else:
            if avoid:
                self.drawChar(self.enemy, self.posEnemy[0] + direction, self.posEnemy[1])
            else:
                self.drawChar(self.enemy, self.posEnemy[0], self.posEnemy[1])
            self.drawChar(self.character, self.posChar[0] + direction, self.posChar[1])

        self.displayOnScreen()
        pygame.time.delay(500)

        self.drawNormal()

        self.displayOnScreen()

    def specialAttack(self, char):
        self.drawNormal()
        fontBig = pygame.font.SysFont("Arial", 40, True, False)
        font = pygame.font.SysFont("Arial", 20, False, False)

        self.animSurface.blit(fontBig.render("!", False, (255, 255, 255)), (self.width // 2 + 60, 10))
        self.animSurface.blit(char.getPortrait(), (self.width // 2 - 50, 10))

        sp = font.render(char.getSpecialAttack(), False, (255, 255, 255))

        pos = (0, 5)
        if char == self.character:
            pos = (395 - sp.get_width(), 5)

        self.animSurface.fill((100, 120, 250), (pos[0], pos[1], sp.get_width() + 5, sp.get_height() + 2))
        self.animSurface.blit(sp, (pos[0] + 2, pos[1] + 1))
        self.displayOnScreen()
        pygame.time.delay(1000)


    def endBattle(self, xpObtained):
        self.drawUI()
        self.drawChar(self.enemy, self.posEnemy[0], self.posEnemy[1])
        self.drawChar(self.character, self.posChar[0], self.posChar[1])

        self.drawXP(xpObtained)

        continuer = True
        while continuer:
            for event in [pygame.event.wait()]:
                if event.type == KEYDOWN:
                    continuer = False

