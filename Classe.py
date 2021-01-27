class Classe:
    def __init__(self, name, bonusA, bonusB, power, promoted):
        self.name = name
        self.bonusA = bonusA
        self.bonusB = bonusB
        self.power = power
        self.promoted = promoted

    def getName(self):
        return self.name

    def getBonusA(self):
        return self.bonusA

    def getBonusB(self):
        return self.bonusB

    def getPower(self):
        return self.power

    def isPromoted(self):
        return self.promoted


# Classes de base
Saber = Classe("Saber", 0, 0, 3, False)  # Pour Lulu
Archer = Classe("Archer", 0, 0, 3, False)  # Pour Inanna
Caster = Classe("Caster", 0, 0, 2, False)  # Pour Shura et Sagburu
Faker = Classe("Faker", 0, 0, 2, False)  # Pour Ur-Nungal
Gilgamesh = Classe("Gilgamesh", 20, 60, 3, True)  # Classe spéciale pour Goldy

Berserker = Classe("Berserker", 0, 0, 2, False)  # Pour Frédégonde


Barbarian = Classe("Barbare", 0, 0, 3, False)  # La plupart des ennemis

GrandSaber = Classe("Grand Saber", 20, 60, 3, True)  # Classe évoluée pour Lulu
JewelMaster = Classe("Jewel Master", 20, 60, 3, True)  # Classe évoluée pour Inanna
DreamMaker = Classe("DreamMaker", 20, 60, 3, True)  # Classe évoluée pour Shura
Sorcerer = Classe("Sorcerer", 20, 60, 3, True)  # Classe évoluée pour Sagburu
EiyuuHimer = Classe("Eiyuu Hime", 20, 60, 3, True)  # Classe évoluée pour Ur-Nungal



