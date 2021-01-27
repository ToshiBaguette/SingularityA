class Case:
    def __init__(self, posX, posY, type):
        """
        posX = Position en X dans la grille
        posY = Position en Y dans la grille
        type = Type de case : 0 - Plaine / 1 - Forêt / 2 - Désert
        """
        self.x = posX
        self.y = posY
        self.type = type

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getType(self):
        return self.type
