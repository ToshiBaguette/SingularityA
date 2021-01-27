class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def getOffsetX(self):
        return self.x - 7
    def getOffsetY(self):
        return self.y - 7

    def move(self, dirX, dirY, terrain):
        if (dirX > 0 and (self.getOffsetX() + 15) < terrain.getWidth()) or (dirX < 0 and self.getOffsetX() > 0):
            self.x += dirX

        elif (dirY > 0 and (self.getOffsetY() + 15) < terrain.getHeight()) or (dirY < 0 and self.getOffsetY() > 0):
            self.y += dirY
