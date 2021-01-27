import pygame
import random
import math
import BattleAnim

def blackWhitePx(pixel):
    bw = (pixel[0] + pixel[1] + pixel[2]) // 3
    return bw

class Character:
    # Characteristics :
    # 0 - MAX HP
    # 1 - Attaque
    # 2 - Defense
    # 3 - Agilité
    # 4 - Chance
    # 5 - Deplacement
    # 6 - Vitesse
    # 7 - Magie
    # 8 - Resistance

    # 9 - Actual HP
    # 10 - Actual Deplacement

    def __init__(self, posX, posY, characteristics, color, terrain, classe, inventory=[], level=1, xp=0, enemy=False, boss=False, usable=True):
        self.x = posX
        self.y = posY
        self.characteristics = characteristics
        self.characteristics.append(self.getMaxHP())
        self.characteristics.append(self.getMaxDeplacement())
        self.reachableCases = []
        self.attackableCases = []
        self.healableCases = []
        self.actualCase = terrain.getCases()[posY * terrain.getWidth() + posX]
        self.level = level
        self.classe = classe
        self.xp = xp
        self.speUnlocked = self.level >= 5

        self.selected = False  # If Character is actually selected by the player
        self.color = color
        self.inventory = inventory  # L'inventaire sera de 5 places, pour tenir des armes ou objets tels que des potions
        self.lastWeaponUsed = inventory[0]
        self.attackDistance = self.lastWeaponUsed.getAttackDistance()
        self.hasDoneThing = False
        self.hasMoved = False
        self.turnEnded = False

        self.usable = usable
        self.enemy = enemy
        self.boss = boss
        self.name = "No Name"
        self.specialAttack = "No Name"

        # Retiré dans le futur
        self.trueColor = color

    # Movement Logic
    def isUsable(self):
        return self.usable
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getReachableCases(self):
        return self.reachableCases
    def getAttackableCases(self):
        return self.attackableCases
    def isOn(self, case):
        return self.x == case.getX() and self.y == case.getY()

    # Characteristics Getters
    def getCharacteristics(self):
        return self.characteristics

    def getMaxHP(self):
        return self.characteristics[0]
    def getActualHP(self):
        return self.characteristics[9]

    def getAtk(self):
        return self.characteristics[1]
    def getDef(self):
        return self.characteristics[2]
    def getAgility(self):
        return self.characteristics[3]
    def getLuck(self):
        return self.characteristics[4]
    def getMagie(self):
        return self.characteristics[7]
    def getResistance(self):
        return self.characteristics[8]

    def getXP(self):
        return self.xp
    def getLevel(self):
        return self.level
    def getClasse(self):
        return self.classe

    def getMaxDeplacement(self):
        return self.characteristics[5]
    def getSpeed(self):
        return self.characteristics[6]
    def getActualDeplacement(self):
        return self.characteristics[10]

    def getInventory(self):
        return self.inventory

    def getActualCase(self):
        return self.actualCase

    def getName(self):
        return self.name
    def getPortrait(self):
        return pygame.Surface((100, 100))
    def getSpecialAttack(self):
        return self.specialAttack

    # Selection Logic
    def isSelected(self):
        return self.selected
    def select(self, terrain, enemies, characters):
        self.selected = True
        self.updateReachableCases(terrain, enemies, characters)
    def unSelect(self):
        self.selected = False

    # For Battle
    def removeHP(self, amount):
        self.characteristics[9] -= amount
    def heal(self, amount):
        print(self.getName() + " se fait heal de " + str(amount) + " PV !")
        self.characteristics[9] += amount
        if self.characteristics[9] > self.getMaxHP():
            self.characteristics[9] = self.getMaxHP()
    def getLastWeaponUsed(self):
        return self.lastWeaponUsed
    def equip(self, weapon):
        self.lastWeaponUsed = weapon
        self.attackDistance = weapon.getAttackDistance()
    def getAttackDistance(self):
        return self.attackDistance

    def isBoss(self):
        return self.boss
    def isEnemy(self):
        return self.enemy

    # Turn Logic
    def startTurn(self, terrain, enemies, characters):
        self.hasDoneThing = False
        self.hasMoved = False
        self.turnEnded = False
        self.characteristics[10] = self.getMaxDeplacement()
        self.color = self.trueColor
        self.updateReachableCases(terrain, enemies, characters)
    def endTurn(self):
        self.turnEnded = True
        self.unSelect()
        bw = blackWhitePx(self.color)
        self.color = (bw, bw, bw)
    def isTurnEnded(self):
        return self.turnEnded
    def canMove(self):
        return not self.hasMoved
    def canDoSomething(self):
        return not self.hasDoneThing
    def didSomething(self):
        self.hasDoneThing = True
    def endingTurn(self, enemies):
        """
        Fonction appelée à chaque action pour vérifier si le tour doit se terminer
        """
        if self.hasDoneThing:
            self.endTurn()
        elif self.hasMoved and not self.hasDoneThing:
            canAttack = False
            for enemy in enemies:
                if enemy.getActualHP() > 0:
                    dist = self.manathanDistance((self.x, self.y), (enemy.getX(), enemy.getY()))
                    if dist == self.getAttackDistance() or self.getAttackDistance() == 3 and dist <= 2:
                        canAttack = True
                        break
            if not canAttack:
                return 4
        return -1

    # Functions
    def manathanDistance(self, pointA, pointB):
        return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])

    def move(self, newX, newY, terrain, enemies, characters):
        self.x = newX
        self.y = newY
        self.characteristics[10] = 0
        self.updateReachableCases(terrain, enemies, characters)
        self.actualCase = terrain.getCases()[newY * terrain.getWidth() + newX]
        self.hasMoved = True

        return self.endingTurn(enemies)

    def display(self, screen, camera):
        pygame.draw.ellipse(screen, self.color, ((self.x - camera.getOffsetX()) * 40 + 4, (self.y - camera.getOffsetY()) * 40 + 4, 32, 32))

    def levelUp(self):
        upStats = []
        self.xp = 0
        if random.randint(1, 100) <= 75:  # Les HP ont 3 chances sur 4 de monter
            self.characteristics[0] += 1
            upStats.append(0)
        for i in range(1, 9):
            if i != 5 and random.randint(1, 100) <= 25:  # 1 chance sur 4 de monter de 1 chaque caractéristique
                self.characteristics[i] += 1
                if i > 5:
                    upStats.append(i - 1)
                else:
                    upStats.append(i)
        self.level += 1
        if self.level == 5:
            self.speUnlocked = True
            return [True, upStats]
        return [False, upStats]


    def healSomeone(self, char, enemies):
        print(self.getName() + " va heal " + char.getName())
        char.heal(10 + self.getMagie())
        self.hasDoneThing = True
        self.endingTurn(enemies)

    def attack(self, char, weapon, enemies, screen, counter=True, bonus=1, battleAnim=None):
        startingHP = char.getActualHP()

        hasAlreadyCounter = False
        self.lastWeaponUsed = weapon
        # Notre attaque
        atk = self.getAtk()
        df = char.getDef()

        uAtk = char.getAtk()
        uDf = self.getDef()

        if self.attackDistance == 3:
            atk = self.getMagie()
            df = char.getResistance()
            uAtk = char.getMagie()
            uDf = self.getResistance()

        damages = math.floor(((atk + weapon.getMight() + weapon.effectiveness(char.getLastWeaponUsed())) - df) * bonus)
        uDamages = ((uAtk + char.getLastWeaponUsed().getMight() + char.getLastWeaponUsed().effectiveness(weapon)) - uDf) * bonus

        if damages < 0:
            damages = 0
        if uDamages < 0:
            uDamages = 0

        if char.getName() == "Frédégonde":  # Frédégonde prend 2x plus de dégats en raison de sa malédiction
            damages *= 2
        if self.getName() == "Frédégonde":
            uDamages *= 2

        atkSpeed = (self.getSpeed() - weapon.getWeight())
        nbAttacks = 1
        if atkSpeed > char.getSpeed() + 2:
            nbAttacks = 2

        hitRate = (weapon.getAccuracy() + self.getAgility() * 2 + self.getLuck())
        defAvoid = ((char.getSpeed() - char.getLastWeaponUsed().getWeight()) * 2 + char.getLuck())

        uHitRate = (char.getLastWeaponUsed().getAccuracy() + char.getAgility() * 2 + char.getLuck())
        uDefAvoid = ((self.getSpeed() - weapon.getWeight()) * 2 + self.getLuck())


        if char.getActualCase().getType() == 1:
            defAvoid += 20
            damages -= 1
        elif char.getActualCase().getType() == 2:
            defAvoid += 5
        if self.getActualCase().getType() == 1:
            uDefAvoid += 20
            uDamages -= 1
        elif self.getActualCase().getType() == 2:
            uDefAvoid += 5

        if hitRate == defAvoid:
            hitRate += 1
        if uHitRate == uDefAvoid:
            uHitRate += 1
        acc = hitRate - defAvoid
        if acc > 100:
            acc = 100
        if acc < 0:
            acc = 0
        uAcc = uHitRate - uDefAvoid
        if uAcc > 100:
            uAcc = 100
        if uAcc < 0:
            uAcc = 0
        critChance = weapon.getCritRate() + self.getLuck() // 2 - char.getLuck()

        if critChance < 0:
            critChance = 0

        uCrit = char.getLastWeaponUsed().getCritRate() + char.getLuck() // 2 - self.getLuck()
        if uCrit < 0:
            uCrit = 0

        if battleAnim is None:
            battleAnim = BattleAnim.BattleAnim(screen, self, char, [uDamages, uAcc, uCrit], [damages, acc, critChance])

        canCounter = (char.getAttackDistance() == self.getAttackDistance() or char.getAttackDistance() == 3)

        for i in range(nbAttacks):
            speInt = random.randint(1, 100)

            if self.speUnlocked and speInt <= self.getAgility() / 2:
                canCounter = canCounter and self.specialTechnique(char, weapon, damages, acc, critChance)
                if canCounter and counter and not hasAlreadyCounter and char.getActualHP() > 0 and (self.manathanDistance((char.getX(), char.getY()), (self.getX(), self.getY())) == char.getAttackDistance() or char.getAttackDistance() == 3):
                    char.attack(self, char.getLastWeaponUsed(), enemies, False)
                    hasAlreadyCounter = True
            else:
                accInt = random.randint(1, 100)
                critInt = random.randint(1, 100)

                battleAnim.attack(self, critInt <= critChance, accInt > acc)
                if accInt <= acc:
                    # Si on touche
                    if critInt <= critChance:
                        # Et qu'on fait un crit
                        char.removeHP(damages * 3)
                    else:
                        char.removeHP(damages)

                battleAnim.drawNormal()
                battleAnim.displayOnScreen()
                pygame.time.delay(200)

                # Contre attaque
                if counter and canCounter and not hasAlreadyCounter and char.getActualHP() > 0:
                    char.attack(self, char.getLastWeaponUsed(), enemies, screen, False, 1, battleAnim)
                    hasAlreadyCounter = True
        if counter:
            self.hasDoneThing = True
            self.endingTurn(enemies)

        # Calcul d'xp !
        if char.getActualHP() != startingHP and not self.isEnemy():
            # Nous avons fait des dégats à l'ennemi, donc nous gagnons de l'xp
            damagesXP = (31 + (char.getLevel() + char.getClasse().getBonusA()) - (self.getLevel() + self.classe.getBonusA())) // self.classe.getPower()
            killXPBase = ((char.getLevel() * char.getClasse().getPower() + char.getClasse().getBonusB()) - (self.level * self.classe.getPower() + self.classe.getBonusB()))
            if killXPBase < 1:
                killXPBase = 1
            if damagesXP < 1:
                damagesXP = 1
            killXP = damagesXP + killXPBase + 20
            if char.isBoss():
                killXP += 40

            if char.getActualHP() > 0:
                battleAnim.endBattle(damagesXP)
            else:
                battleAnim.endBattle(killXP)
        elif not self.isEnemy():
            battleAnim.endBattle(1)

    def goHeal(self, cible, terrain, enemies, characters):
        if self.manathanDistance((self.x, self.y), (cible.getX(), cible.getY())) != 1:
            minDist = 999
            pos = [0, 0]
            toTest = [(cible.getX(), cible.getY() - 1), (cible.getX(), cible.getY() + 1), (cible.getX() - 1, cible.getY()), (cible.getX() + 1, cible.getY())]

            for position in toTest:
                if position in self.reachableCases:
                    dist = self.manathanDistance((self.x, self.y), (cible.getX(), cible.getY()))
                    if minDist > dist:
                        minDist = dist
                        pos = position
            self.move(pos[0], pos[1], terrain, enemies, characters)
        self.healSomeone(cible, enemies)

    def goAttack(self, enemy, enemies, weapon, terrain, screen, characters):
        if self.manathanDistance((self.x, self.y), (enemy.getX(), enemy.getY())) != self.attackDistance or self.attackDistance == 3:
            minDist = 999
            pos = [0, 0]
            toTest = []

            if self.attackDistance == 1 or self.attackDistance == 3:
                toTest = [(enemy.getX(), enemy.getY() - 1), (enemy.getX(), enemy.getY() + 1), (enemy.getX() - 1, enemy.getY()), (enemy.getX() + 1, enemy.getY())]
            elif self.attackDistance == 2:
                toTest = [
                    (enemy.getX() - 2, enemy.getY()), (enemy.getX() + 2, enemy.getY()),
                    (enemy.getX() - 1, enemy.getY() + 1), (enemy.getX() + 1, enemy.getY() + 1),
                    (enemy.getX() - 1, enemy.getY() - 1), (enemy.getX() + 1, enemy.getY() - 1),
                    (enemy.getX(), enemy.getY() + 2), (enemy.getX(), enemy.getY() - 2)
                ]

            for position in toTest:
                if position in self.reachableCases:
                    dist = self.manathanDistance((self.x, self.y), (enemy.getX() + 1, enemy.getY()))
                    if minDist > dist:
                        minDist = dist
                        pos = position
            self.move(pos[0], pos[1], terrain, enemies, characters)
        self.attack(enemy, weapon, enemies, screen)

    def specialTechnique(self, enemy, weapon, damages, accuracy, critChance):
        return

    def update(self, terrain, chars, screen, characters):
        self.updateReachableCases(terrain, chars, characters)
        for player in chars:
            if self.canAttack(player) and player.getActualHP() > 0:
                # dans le cas où nous pouvons bel et bien l'attaquer
                self.goAttack(player, chars, self.inventory[0], terrain, screen, characters)
                break

    def canHealOn(self, terrain, posX, posY, characters):
        toTest = [(posX, posY - 1), (posX, posY + 1), (posX - 1, posY), (posX + 1, posY)]
        for position in toTest:
            if 0 <= position[0] < terrain.getWidth() and 0 <= position[1] < terrain.getHeight() and 0 <= terrain.getCases()[position[1] * terrain.getWidth() + position[0]].getType() <= 2 and position not in self.healableCases and self.isCharacterOnCase(characters, position[0], position[1]):  # Si la case peut être heal et n'est pas déjà enregistrée
                self.healableCases.append(position)

    def canAttackOn(self, terrain, posX, posY):
        toTest = []  # Toutes les positions attaquables qu'on doit vérifier

        if self.attackDistance == 1:  # Si on attaque au corps à corps
            toTest = [(posX, posY - 1), (posX, posY + 1), (posX - 1, posY), (posX + 1, posY)]
        elif self.attackDistance == 2:  # Si on attaque de loin
            toTest = [
                (posX - 2, posY), (posX + 2, posY),
                (posX - 1, posY + 1), (posX + 1, posY + 1),
                (posX - 1, posY - 1), (posX + 1, posY - 1),
                (posX, posY + 2), (posX, posY - 2)
            ]
        elif self.attackDistance == 3:  # Si on attaque autant de loin que de proche
            toTest = [
                (posX, posY - 1), (posX, posY + 1), (posX - 1, posY), (posX + 1, posY),
                (posX - 2, posY), (posX + 2, posY),
                (posX - 1, posY + 1), (posX + 1, posY + 1),
                (posX - 1, posY - 1), (posX + 1, posY - 1),
                (posX, posY + 2), (posX, posY - 2)
            ]

        for position in toTest:
            if 0 <= position[0] < terrain.getWidth() and 0 <= position[1] < terrain.getHeight() and 0 <= terrain.getCases()[position[1] * terrain.getWidth() + position[0]].getType() <= 2 and position not in self.attackableCases:  # Si la case peut être attaquée et n'est pas déjà enregistrée
                self.attackableCases.append(position)

    def isEnemyOnCase(self, enemies, posX, posY):
        for enemy in enemies:
            if enemy.getActualHP() > 0 and enemy.getX() == posX and enemy.getY() == posY:
                return True
        return False

    def getHealableCases(self, characters, terrain):
        return self.healableCases

    def canHeal(self):
        for item in self.inventory:
            if item.getType() == 0:  # Si c'est une arme
                if item.getType() == 0:  # Si c'est un bâton
                    return True
        return False

    def isCharacterOnCase(self, characters, posX, posY):
        for character in characters:
            if character.getActualHP() > 0 and character.getX() == posX and character.getY() == posY and character != self:
                return True
        return False


    def canGoOn(self, terrain, posX, posY, movement, enemies, characters, isCharBefore=False):
        if movement < 0 or not 0 <= terrain.getCases()[posY * terrain.getHeight() + posX].getType() <= 2:
            return False
        else:
            charHere = self.isCharacterOnCase(characters, posX, posY)
            if not (posX, posY) in self.reachableCases:
                self.reachableCases.append((posX, posY))
                if not charHere:
                    self.canAttackOn(terrain, posX, posY)
                    if self.canHeal():
                        self.canHealOn(terrain, posX, posY, characters)

            toTest = [
                (posX + 1, posY),
                (posX - 1, posY),
                (posX, posY + 1),
                (posX, posY - 1)
            ]

            for position in toTest:
                if 0 <= position[0] < terrain.getWidth() and 0 <= position[1] < terrain.getHeight() and not self.isEnemyOnCase(enemies, position[0], position[1]):
                    if 1 <= terrain.getCases()[position[1] * terrain.getWidth() + position[0]].getType() <= 2:
                        self.canGoOn(terrain, position[0], position[1], movement - 2, enemies, characters, charHere)
                    else:
                        self.canGoOn(terrain, position[0], position[1], movement - 1, enemies, characters, charHere)

    def canAttack(self, char):
        return (char.getX(), char.getY()) in self.attackableCases

    def updateReachableCases(self, terrain, enemies, characters):
        self.reachableCases.clear()
        self.attackableCases.clear()
        self.healableCases.clear()

        self.canGoOn(terrain, self.x,  self.y, self.getActualDeplacement(), enemies, characters)
