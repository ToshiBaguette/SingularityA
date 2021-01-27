import Item


class Weapon(Item.Item):
    def __init__(self, name, typeWeapon, might, durability, weight, critRate, accuracy, attackDistance):
        """
        :param name: Nom de l'arme
        :param typeWeapon: Type de l'arme (1-Epee/2-Hache/3-Lance/4-Arc)
        :param might: Puissance de l'arme
        :param durability: Durabilité de l'arme
        :param weight: Poid de l'arme
        :param critRate: Taux de critique de l'arme
        :param accuracy: Précision de l'arme
        :param attackDistance: Distance d'attaque de l'arme
        """
        super().__init__(name, 0, 0)

        self.name = name
        self.type = typeWeapon
        self.might = might
        self.durability = durability
        self.weight = weight
        self.critRate = critRate
        self.accuracy = accuracy
        self.attackDistance = attackDistance

    def getName(self):
        return self.name
    def getType(self):
        return self.type
    def getMight(self):
        return self.might
    def getDurability(self):
        return self.durability
    def getWeight(self):
        return self.weight
    def getCritRate(self):
        return self.critRate
    def getAccuracy(self):
        return self.accuracy
    def getAttackDistance(self):
        return self.attackDistance

    def use(self):
        self.durability -= 1

    def effectiveness(self, weapon):
        """
        :param weapon: Arme à comparer
        :return: 1 si super efficace, -1 si pas efficace du tout, 0 sinon
        """
        # Triangle des armes : Epee > Hache > Lance > Arc > Epee
        if self.type == weapon.type - 1 and weapon.type != 1 or self.type == 4 and weapon.type == 1:
            return 1
        elif self.type == weapon.type + 1 and weapon.type != 4 or self.type == 1 and weapon.type == 4:
            return -1
        return 0


IronSword = Weapon("Épée Fer", 1, 2, 35, 4, 1, 75, 1)  # Épée random
IronBow = Weapon("Arc Fer", 4, 2, 35, 4, 1, 85, 2)  # Arc random

Ea = Weapon("Ea", 1, 5, 99, 3, 1, 100, 1)  # Arme de Goldy
Maanna = Weapon("Maanna", 4, 5, 99, 3, 3, 100, 2)  # Arme d'Inanna
Ninsun = Weapon("Ninsun", 1, 4, 99, 3, 1, 100, 1)  # Arme de Lugalbanda
EaFake = Weapon("Ea (Fausse)", 1, 3, 99, 1, 15, 75, 1)  # Arme de Ur-Nungal
CatSword = Weapon("Épée Chat", 1, 3, 99, 3, 30, 100, 1)  # Arme de Shura
Baton = Weapon("Bâton", 0, 3, 99, 0, 0, 100, 0)  # Arme (provisoire) de Sagburu
QueensMurder = Weapon("Queen's Murder", 1, 7, 99, 2, 15, 100, 1)  # Arme de Frédégonde

weapons = [IronSword, IronBow, Ea, Maanna, Ninsun, EaFake, CatSword, Baton, QueensMurder]
def getWeapon(id):
    return weapons[id]

def getIdOf(weapon):
    for i in range(len(weapons)):
        if weapon.getName() == weapons[i].getName():
            return i
    return -1
