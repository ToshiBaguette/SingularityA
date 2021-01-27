class Save:

    def __init__(self, image, t, scene, line, creation, number):
        self.createdAt = creation
        self.image = image
        self.scene = scene
        self.type = t
        self.line = line
        self.number = number

    def getImage(self):
        return self.image

    def getCreationDate(self):
        return self.createdAt

    def getScene(self):
        return self.scene

    def getType(self):
        return self.type

    def getLine(self):
        return self.line

    def getNumber(self):
        return self.number

    def toState(self):
        return [self.type, self.scene, self.line]
