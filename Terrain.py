import Case

class Terrain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cases = []

    def setCases(self, cases):
        self.cases = cases
    def createCases(self, type):
        for i in range(self.height):
            for j in range(self.width):
                self.cases.append(Case.Case(j, i, type))


    def getCases(self):
        return self.cases
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
