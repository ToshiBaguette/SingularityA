import Character


class Enemy(Character.Character):
    def __init__(self, posX, posY, characteristics, terrain, classe, weapon, level=1, boss=False):
        super().__init__(posX, posY, characteristics, (250, 25, 145), terrain, classe, [weapon], level)
        self.boss = boss

    def update(self, terrain, chars, screen):
        for player in chars:
            if self.canAttack(player):
                # dans le cas où nous pouvons bel et bien l'attaquer
                self.goAttack(player, chars, self.inventory[0], terrain, screen)
                break

    def isBoss(self):
        return self.boss
