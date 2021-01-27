class Item:
    def __init__(self, name, type, effect):
        """
        :param name: Nom de l'item
        :param type: Type d'item
        :param effect: Effet, par exemple le nombre de pv rendus avec une potion
        """
        self.name = name
        self.typeItem = type
        self.effect = effect

    def useItem(self, user):
        if self.typeItem == 0:  # Weapon
            user.equip(self)
        if self.typeItem == 1:  # Si potion
            user.heal(self.effect)

    def getTypeItem(self):
        return self.typeItem

    def getName(self):
        return self.name


potion = Item("Potion", 1, 10)
items = [potion]
def getItem(id):
    return items[id]

