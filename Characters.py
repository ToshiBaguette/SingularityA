import Character
import Classe
import utils
import random
import math
import pygame


def BlackWhiteSprit(surface):
    toReturn = surface.copy()
    for i in range(toReturn.get_width()):
        for j in range(toReturn.get_height()):
            color = Character.blackWhitePx(surface.get_at((i, j)))
            toReturn.set_at((i, j), (color, color, color, surface.get_at((i, j))[3]))
    return toReturn


class Goldy(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Gilgamesh, inventory, level, xp, False, False, usable)
        self.name = "Goldy"
        self.specialAttack = "Enuma Elish"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        # Enuma Elish
        enemy.removeHP(damages * 5)
        return True

    def getPortrait(self):
        return self.portrait


class Inanna(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Archer, inventory, level, xp, False, False, usable)
        self.name = "Inanna"
        self.specialAttack = "An Gal Tā Kigal Shē"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        enemy.removeHP(damages * 2)
        return True

    def getPortrait(self):
        return self.portrait

class Lugalbanda(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Saber, inventory, level, xp, False, False, usable)
        self.name = "Lugalbanda"
        self.specialAttack = "Ninsun Strike"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        if weapon.name == "Ninsun":  # Si on utilise Ninsun, alors on déclenche le NP
            enemy.removeHP(damages * 2)
            self.heal(self.getMaxHP() // 2)
        else:  # Si on ne tient pas Ninsun
            enemy.removeHP(damages + self.getAtk() // 2)  # On ajoute la moitié de notre attaque en dégats ignorant la défense
            self.heal((damages + self.getAtk() // 2) / 3)  # On se heal d'un tier des dégats envoyés
        return True

    def getPortrait(self):
        return self.portrait

class Shura(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Caster, inventory, level, xp, False, False, usable)
        self.name = "Shura"
        self.specialAttack = "Ère Glaciaire"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        enemy.removeHP(damages * 1.1)
        return False

    def getPortrait(self):
        return self.portrait


class Sagburu(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Caster, inventory, level, xp, False, False, usable)
        self.name = "Sagburu"
        self.specialAttack = "EKUSUPUROSHION"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        enemy.removeHP(damages + (1.5 * self.getMagie()))
        return True

    def getPortrait(self):
        return self.portrait


class UrNungal(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Faker, inventory, level, xp, False, False, usable)
        self.name = "Ur-Nungal"
        self.specialAttack = "Gate Of Babylon"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        # Gate of Babylon
        nbCoups = 10
        for i in range(nbCoups):
            critInt = random.randint(1, 100)
            if critInt <= critChance:  # On crit
                enemy.removeHP(math.floor(damages / 5) * 3)
            else:
                enemy.removeHP(math.floor(damages / 5))
        return True

    def getPortrait(self):
        return self.portrait


class Fredegonde(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, enemy=False, boss=False, usable=True):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Berserker, inventory, level, xp, enemy, boss, usable)
        self.name = "Frédégonde"
        self.specialAttack = "Pour mon roi"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def attack(self, char, weapon, enemies, screen, counter=True, bonus=1, battleAnim=None):
        super().attack(char, weapon, enemies, screen, counter, 1.1, battleAnim)
        damages = math.floor(((self.getAtk() + weapon.getMight() + weapon.effectiveness(char.getLastWeaponUsed())) - char.getDef()) * 1.1)
        self.removeHP(math.floor(damages // 5))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        # On inflige plus de dégats, et on en reçoit moins
        enemy.removeHP(damages * 1.5)
        self.removeHP(math.floor(damages // 10))
        return True

    def getPortrait(self):
        return self.portrait


class Barbare(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, boss=False):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Barbarian, inventory, level, xp, True, boss, False)
        self.name = "Barbare"
        self.specialAttack = "Attaque"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        # Leur technique spéciale n'est autre qu'une attaque normale
        accInt = random.randint(1, 100)
        critInt = random.randint(1, 100)

        if accInt <= accuracy:
            # Si on touche
            if critInt <= critChance:
                # Et qu'on fait un crit
                enemy.removeHP(damages * 3)
            else:
                enemy.removeHP(damages)
        return True

    def getPortrait(self):
        return self.portrait


class Archer(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, inventory, level=1, xp=0, boss=False):
        super().__init__(posX, posY, characteristics, (0, 0, 0), terrain, Classe.Archer, inventory, level, xp, True, boss, False)
        self.name = "Archer"
        self.specialAttack = "Attaque"
        self.mapImage = utils.loadBattleMapImage(self.name)
        self.portrait = utils.loadBattlePortrait(self.name)

    def display(self, screen, camera):
        toBlit = self.mapImage
        if self.isTurnEnded():
            toBlit = BlackWhiteSprit(self.mapImage)
        screen.blit(toBlit, ((self.x - camera.getOffsetX()) * 40, (self.y - camera.getOffsetY()) * 40))

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        # Leur technique spéciale n'est autre qu'une attaque normale
        accInt = random.randint(1, 100)
        critInt = random.randint(1, 100)

        if accInt <= accuracy:
            # Si on touche
            if critInt <= critChance:
                # Et qu'on fait un crit
                enemy.removeHP(damages * 3)
            else:
                enemy.removeHP(damages)
        return True

    def getPortrait(self):
        return self.portrait
