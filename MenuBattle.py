import pygame
from pygame.locals import *

def drawFond(screen, pos):
    screen.fill((150, 150, 150), (pos[0] - 1, pos[1] - 1, pos[2] + 2, pos[3] + 2))
    screen.fill((10, 10, 250), (pos[0], pos[1], pos[2], pos[3]))  # Affiche le fond

class MenuBattle:
    def __init__(self, choices, pos):
        """
        :param choices: Dictionnaire contenant le nom de chaque champ ainsi qu'un état vers lequel il renvoie, pour ouvrir un autre menu par exemple
        :param pos: Tuple représentant la position du menu à l'écran, ainsi que la taille
        """
        self.cursor = 0  # Position du curseur dans la liste des choix
        self.choices = choices
        self.nbChoices = len(choices)
        self.pos = pos

    def moveCursor(self, direction):
        """
        :param direction: 1 ou -1, afin de changer la position du curseur
        """
        if 0 > self.cursor + direction:
            self.cursor = self.nbChoices - 1
        elif self.cursor + direction >= self.nbChoices:
            self.cursor = 0
        else:
            self.cursor += direction

    def draw(self, screen):
        drawFond(screen, self.pos)

        # Now the fun BEGIIIIIN
        font = pygame.font.SysFont("Arial", 20, False, False)
        iteration = 0
        # Some super ultra funny stuff pour calculer la position du texte et son espacement
        espace = self.pos[3] // self.nbChoices

        for key in self.choices:
            if iteration == self.cursor:
                screen.fill((150, 150, 250), (self.pos[0], self.pos[1] + iteration * espace, self.pos[2], espace))
            text = font.render(key, False, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.pos[2] // 2 - text.get_width() // 2), self.pos[1] + iteration * espace + (espace // 2 - text.get_height() // 2)))
            iteration += 1

    def select(self):
        """
        :return: Retourne la valeur associée au dictionnaire de choix
        """
        return [list(self.choices.values())[self.cursor]]


class MenuBeforeBattle(MenuBattle):
    def __init__(self, user, enemy, weapon):
        self.choices = {"Combattre": "battle", "Retour": 1}
        self.nbChoices = 2
        self.pos = (10, 10, 300, 400)
        self.cursor = 0
        self.user = user
        self.enemy = enemy
        self.weapon = weapon

    def draw(self, screen):
        drawFond(screen, self.pos)
        font = pygame.font.SysFont("Arial", 20, False, False)

        # Actual HP
        HPText = font.render("PV", False, (255, 255, 255))
        UHP = font.render(str(self.user.getActualHP()), False, (255, 255, 255))
        EHP = font.render(str(self.enemy.getActualHP()), False, (255, 255, 255))

        screen.blit(HPText, (self.pos[0] + 10, self.pos[1] + 100))
        screen.blit(UHP, (self.pos[0] + 90, self.pos[1] + 100))
        screen.blit(EHP, (self.pos[0] + 250, self.pos[1] + 100))

        # Damages
        atk = self.user.getAtk()
        df = self.enemy.getDef()
        if self.user.getAttackDistance() == 3:
            atk = self.user.getMagie()
            df = self.enemy.getResistance()
        uDamage = (atk + self.weapon.getMight() + self.weapon.effectiveness(self.enemy.getLastWeaponUsed())) - df
        atk = self.enemy.getAtk()
        df = self.user.getDef()
        if self.enemy.getAttackDistance() == 3:
            atk = self.enemy.getMagie()
            df = self.user.getResistance()
        eDamage = (atk + self.enemy.getLastWeaponUsed().getMight() + self.enemy.getLastWeaponUsed().effectiveness(self.weapon)) - df

        if uDamage < 0:
            uDamage = 0
        if eDamage < 0:
            eDamage = 0

        DamageText = font.render("Dégats", False, (255, 255, 255))
        uDamageText = font.render(str(uDamage), False, (255, 255, 255))
        eDamageText = font.render(str(eDamage), False, (255, 255, 255))

        screen.blit(DamageText, (self.pos[0] + 10, self.pos[1] + 130))
        screen.blit(uDamageText, (self.pos[0] + 90, self.pos[1] + 130))
        screen.blit(eDamageText, (self.pos[0] + 250, self.pos[1] + 130))

        # Precision
        uPrec = (self.weapon.getAccuracy() + self.user.getAgility() * 2 + self.user.getLuck()) - ((self.enemy.getSpeed() - self.enemy.getLastWeaponUsed().getWeight()) * 2 + self.enemy.getLuck())
        if uPrec > 100:
            uPrec = 100
        if uPrec < 0:
            uPrec = 0
        ePrec = (self.enemy.getLastWeaponUsed().getAccuracy() + self.enemy.getAgility() * 2 + self.enemy.getLuck()) - ((self.user.getSpeed() - self.weapon.getWeight()) * 2 + self.user.getLuck())
        if ePrec > 100:
            ePrec = 100
        if ePrec < 0:
            ePrec = 0

        precisionText = font.render("Precision", False, (255, 255, 255))
        uPrecText = font.render(str(uPrec), False, (255, 255, 255))
        ePrecText = font.render(str(ePrec), False, (255, 255, 255))

        screen.blit(precisionText, (self.pos[0] + 10, self.pos[1] + 160))
        screen.blit(uPrecText, (self.pos[0] + 90, self.pos[1] + 160))
        screen.blit(ePrecText, (self.pos[0] + 250, self.pos[1] + 160))

        # Crit
        uCrit = self.weapon.getCritRate() + self.user.getLuck() // 2 - self.enemy.getLuck()
        if uCrit > 100:
            uCrit = 100
        if uCrit < 0:
            uCrit = 0
        eCrit = self.enemy.getLastWeaponUsed().getCritRate() + self.enemy.getLuck() // 2 - self.user.getLuck()
        if eCrit > 100:
            eCrit = 100
        if eCrit < 0:
            eCrit = 0

        critText = font.render("Critique", False, (255, 255, 255))
        uCritText = font.render(str(uCrit), False, (255, 255, 255))
        eCritText = font.render(str(eCrit), False, (255, 255, 255))

        screen.blit(critText, (self.pos[0] + 10, self.pos[1] + 190))
        screen.blit(uCritText, (self.pos[0] + 90, self.pos[1] + 190))
        screen.blit(eCritText, (self.pos[0] + 250, self.pos[1] + 190))

        i = 0
        for key in self.choices:
            if i == self.cursor:
                screen.fill((150, 150, 250), (self.pos[0], self.pos[1] + 260 + i * 30, self.pos[2], 30))
            text = font.render(key, False, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.pos[2] // 2 - text.get_width() // 2), self.pos[1] + 260 + i * 30 + (15 - text.get_height() // 2)))
            i += 1

        screen.blit(self.user.getPortrait(), (self.pos[0] + 55, 10))
        screen.blit(self.enemy.getPortrait(), (self.pos[0] + 190, 10))

    def select(self):
        toReturn = list(self.choices.values())[self.cursor]
        if toReturn != 1:
            # Si on décide de combattre
            return ["battle", self.user, self.enemy, self.weapon]
        return [toReturn]


class inventoryMenuBattle(MenuBattle):
    def __init__(self, pos, user, enemy):
        self.cursor = 0
        self.choices = {}
        for item in user.getInventory():
            self.choices[item.getName()] = item
        self.nbChoices = len(user.getInventory())
        self.pos = pos
        self.enemy = enemy
        self.user = user

    def draw(self, screen):
        drawFond(screen, self.pos)
        font = pygame.font.SysFont("Arial", 20, False, False)

        iteration = 0
        for key in self.choices:
            if iteration == self.cursor:
                screen.fill((150, 150, 250), (self.pos[0], self.pos[1] + iteration * 30, self.pos[2], 30))
            text = font.render(key, False, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.pos[2] // 2 - text.get_width() // 2), self.pos[1] + iteration * 30 + (15 - text.get_height() // 2)))
            iteration += 1

    def select(self):
        return [3, list(self.choices.values())[self.cursor], self.user, self.enemy]


class MenuPerso(MenuBattle):
    def __init__(self, pos, user, proche=None):
        self.pos = pos
        self.user = user

        self.choices = {"Inventaire": 5, "Attendre": 6}
        self.nbChoices = 2

        if proche is not None:
            self.choices["Echanger"] = 8
            self.nbChoices += 1

        self.proche = proche
        self.cursor = 0

    def draw(self, screen):
        drawFond(screen, self.pos)
        font = pygame.font.SysFont("Arial", 20, False, False)

        iteration = 0
        for key in self.choices:
            if iteration == self.cursor:
                screen.fill((150, 150, 150), (self.pos[0], self.pos[1] + iteration * 30, self.pos[2], 30))
            text = font.render(key, False, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.pos[2] // 2 - text.get_width() // 2), self.pos[1] + iteration * 30 + (15 - text.get_height() // 2)))
            iteration += 1

    def select(self):
        if self.proche is not None and self.cursor == 2:
            return [list(self.choices.values())[self.cursor], [self.user, self.proche]]

        return [list(self.choices.values())[self.cursor], self.user]

class inventoryMenu(MenuBattle):
    def __init__(self, pos, user):
        self.pos = pos
        self.user = user
        self.choices = {}
        self.nbChoices = len(user.getInventory())
        self.cursor = 0

        for item in user.getInventory():
            self.choices[item.getName()] = item

    def draw(self, screen):
        drawFond(screen, self.pos)
        font = pygame.font.SysFont("Arial", 20, False, False)

        iteration = 0
        for key in self.choices:
            if iteration == self.cursor:
                screen.fill((150, 150, 150), (self.pos[0], self.pos[1] + iteration * 30, self.pos[2], 30))
            text = font.render(key, False, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.pos[2] // 2 - text.get_width() // 2),
                               self.pos[1] + iteration * 30 + (15 - text.get_height() // 2)))
            iteration += 1

    def select(self):
        return [7,  list(self.choices.values())[self.cursor], self.user]


class MenuEchange:
    def __init__(self, pos, users):
        self.pos = pos
        self.users = users
        self.cursor = [0, 0]

        self.fInventory = {}
        self.sInventory = {}
        for item in users[0].getInventory():
            self.fInventory[item.getName()] = item
        for item in users[1].getInventory():
            self.sInventory[item.getName()] = item
        self.selected = [-1, -1]

    def moveCursor(self, direction):
        """
        :param direction: 1 ou -1, afin de changer la position du curseur
        """
        nbChoices = 5
        # if self.cursor[1] == 0:
        #     nbChoices = len(self.users[0].getInventory())
        # else:
        #     nbChoices = len(self.users[1].getInventory())

        if -1 <= direction <= 1:
            if 0 > self.cursor[0] + direction:
                self.cursor[0] = nbChoices - 1
            elif self.cursor[0] + direction >= nbChoices:
                self.cursor[0] = 0
            else:
                self.cursor[0] += direction
        else:
            if direction == 2 and self.cursor[1] == 0:
                self.cursor[1] = 1
            elif direction == 3 and self.cursor[1] == 1:
                self.cursor[1] = 0
            else:
                if direction == 2:
                    self.cursor[1] -= 1
                else:
                    self.cursor[1] += 1

    def select(self):
        if self.selected[0] == -1:
            self.selected[0] = self.cursor[0]
            self.selected[1] = self.cursor[1]
            return ["none"]
        elif self.selected[1] == self.cursor[1]:
            if self.selected[0] == self.cursor[0]:
                self.selected = [-1, -1]
            else:
                self.selected[0] = self.cursor[0]
            return ["none"]

        else:
            if self.selected[0] >= len(self.users[self.selected[1]].getInventory()):
                # Dans ce cas nous voulons prendre une arme
                if not self.cursor[0] >= len(self.users[self.cursor[1]].getInventory()):
                    # Dans le cas où le curseur est sur quelque chose
                    self.users[self.selected[1]].getInventory().append(self.users[self.cursor[1]].getInventory()[self.cursor[0]])
                    self.users[self.cursor[1]].getInventory().remove(self.users[self.cursor[1]].getInventory()[self.cursor[0]])
                    return [1]
            else:
                # On part du principe que le truc selectionné est dans l'inventaire de quelqu'un
                if self.cursor[0] >= len(self.users[self.cursor[1]].getInventory()):
                    # Dans ce cas, nous voulons donner une arme
                    self.users[self.cursor[1]].getInventory().append(self.users[self.selected[1]].getInventory()[self.selected[0]])
                    self.users[self.selected[1]].getInventory().remove(self.users[self.selected[1]].getInventory()[self.selected[0]])
                    return [1]
                else:
                    # Dans ce cas, nous faisons un échange
                    obj = self.users[self.selected[1]].getInventory()[self.selected[0]]
                    objj = self.users[self.cursor[1]].getInventory()[self.cursor[0]]

                    self.users[self.cursor[1]].getInventory().append(obj)
                    self.users[self.selected[1]].getInventory().append(objj)

                    self.users[self.cursor[1]].getInventory().remove(objj)
                    self.users[self.selected[1]].getInventory().remove(obj)
                    return [1]

    def draw(self, screen):
        drawFond(screen, self.pos)
        font = pygame.font.SysFont("Arial", 20, False, False)

        # Inventory Joueur 1
        for i in range(5):
            if i == self.cursor[0]:
                if self.cursor[1] == 0:
                    screen.fill((150, 150, 150), (self.pos[0], self.pos[1] + i * 30, self.pos[2] // 2, 30))
                else:
                    screen.fill((150, 150, 150), (self.pos[0] + (self.pos[2] // 4 * 2), self.pos[1] + i * 30, self.pos[2] // 2 + 1, 30))
            if i < len(self.users[0].getInventory()):
                text = font.render(list(self.fInventory.keys())[i], False, (255, 255, 255))
                screen.blit(text, (self.pos[0] + ((self.pos[2] // 4 - 5) - text.get_width() // 2),
                                   self.pos[1] + i * 30 + (15 - text.get_height() // 2)))
            if i < len(self.users[1].getInventory()):
                text = font.render(list(self.sInventory.keys())[i], False, (255, 255, 255))
                screen.blit(text, (self.pos[0] + ((self.pos[2] // 4 + self.pos[2] // 4 * 2) - text.get_width() // 2),
                                   self.pos[1] + i * 30 + (15 - text.get_height() // 2)))

        screen.fill((255, 255, 255), (self.pos[0] + 100, self.pos[1], 5, self.pos[3]))


class LevelUpMenu(MenuBattle):
    def __init__(self, pos, character, upStats, speUnlocked, screen):
        self.pos = pos
        self.character = character
        self.upStats = upStats
        self.speUnlocked = speUnlocked
        self.draw(screen)

    def draw(self, screen):
        menu = pygame.Surface((self.pos[2], self.pos[3]))
        menu.fill((10, 10, 250))

        characteristics = {
            "PV": self.character.getMaxHP(),
            "Atk": self.character.getAtk(),
            "Def": self.character.getDef(),
            "Skill": self.character.getAgility(),
            "Chance": self.character.getLuck(),
            "Vitesse": self.character.getSpeed(),
            "Magie": self.character.getMagie(),
            "Res": self.character.getResistance()
        }

        font = pygame.font.SysFont("Arial", 20, False, False)
        x = 0
        y = 0
        i = 0
        for char in characteristics:
            text = char + " " + str(characteristics.get(char))
            if i in self.upStats:
                text += " +"
            menu.blit(font.render(text, False, (255, 255, 255)), (x, y))
            y += 21
            if y == 84:
                y = 0
                x += 100
            i += 1
        if self.speUnlocked:
            menu.blit(font.render("Attaque spéciale débloquée :", False, (255, 255, 255)), (10, 110))
            menu.blit(font.render(self.character.getSpecialAttack(), False, (255, 255, 255)), (10, 131))

        menu.blit(font.render("Appuyez sur une touche.", False, (255, 255, 255)), (10, 152))
        screen.blit(menu, (self.pos[0], self.pos[1]))
        pygame.display.update(self.pos)
        continuer = True
        while continuer:
            for event in [pygame.event.wait()]:
                if event.type == KEYDOWN:
                    continuer = False
                    break


# Menu status char
def drawStatusChar(character, screen):
    drawFond(screen, (10, 10, 210, 120))
    font = pygame.font.SysFont("Arial", 20, False, False)
    name = font.render(character.getName(), False, (255, 255, 255))
    pvText = font.render("PV", False, (255, 255, 255))
    pvDisplay = font.render(str(character.getActualHP()) + "/" + str(character.getMaxHP()), False, (255, 255, 255))

    screen.blit(character.getPortrait(), (20, 20))
    screen.blit(name, (130, 20))
    screen.blit(pvText, (130, 50))
    screen.blit(pvDisplay, (130, 80))
