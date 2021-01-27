import pygame
import copy
import Terrain
import Characters
import Camera
import Weapon
import MenuBattle
import Item
import Classe
from pygame.locals import *


tiles = [pygame.image.load("Assets/Tiles/Plaine.png"), pygame.image.load("Assets/Tiles/Forêt.png"), pygame.image.load("Assets/Tiles/Desert.png")]


def drawBattle(screen, terrain, camera, cursor, characters, enemies):
    screen.fill((0, 0, 0))

    hoverChar = None

    for y in range(15):
        for x in range(15):
            colorB = (110, 110, 110)
            colorC = (230, 235, 242, 0)
            case = terrain.getCases()[(y + camera.getOffsetY()) * terrain.getWidth() + (x + camera.getOffsetX())]
            for char in characters:
                if char.isSelected() and (
                case.getX(), case.getY()) in char.getAttackableCases() and char.canDoSomething():
                    colorB = (210, 25, 25, 200)
                    colorC = (255, 210, 210, 200)
                if char.isSelected() and (case.getX(), case.getY()) in char.getReachableCases() and char.canMove():
                    colorB = (25, 25, 210, 200)
                    colorC = (110, 110, 255, 200)
                if char.isSelected() and (case.getX(), case.getY()) in char.getHealableCases(characters, terrain) and char.canDoSomething():
                    colorB = (5, 150, 60)
                    colorC = (94, 255, 161)
                if char.actualCase.getX() == (cursor[0] + camera.getOffsetX()) and char.actualCase.getY() == (cursor[1] + camera.getOffsetY()):
                    hoverChar = char
                for enemy in enemies:
                    if char.isSelected() and enemy.isOn(case) and char.canAttack(enemy) and char.canDoSomething():
                        colorB = (210, 25, 25)
                        colorC = (255, 210, 210, 200)

            tile = copy.copy(tiles[case.getType()])

            colorFill = pygame.Surface((40, 40), pygame.SRCALPHA)
            colorFill.fill(colorB, (0, 0, 40, 40))
            colorFill.fill(colorC, (2, 2, 36, 36))

            tile.blit(colorFill, (0, 0))
            screen.blit(tile, (x * 40, y * 40))

    for char in characters:
        if char.getActualHP() > 0:
            char.display(screen, camera)
    for enemy in enemies:
        if enemy.getActualHP() > 0:
            if hoverChar is None:
                if enemy.actualCase.getX() == (cursor[0] + camera.getOffsetX()) and enemy.actualCase.getY() == (cursor[1] + camera.getOffsetY()):
                    hoverChar = enemy
            enemy.display(screen, camera)
            if enemy.isBoss():
                screen.fill((255, 250, 40), (enemy.getX() * 40 + 25 - camera.getOffsetX() * 40, enemy.getY() * 40 + 25 - camera.getOffsetY() * 40, 10, 10))
    # Affichage du curseur, un triangle
    pygame.draw.polygon(screen, (0, 0, 0), (
        (cursor[0] * 40 + 5, cursor[1] * 40 + 5),
        (cursor[0] * 40 + 30, cursor[1] * 40 + 5),
        (cursor[0] * 40 + 18, cursor[1] * 40 + 15)
    ))
    if hoverChar is not None:
        MenuBattle.drawStatusChar(hoverChar, screen)


def drawMenu(screen, menu):
    menu.draw(screen)

def handleBattle(event, cursor, camera, terrain, characters, enemies, isSomeoneSelected):
    # Move the Cursor and the Camera
    openMenu = [0]
    if event.key == K_UP:
        if cursor[1] > 0:
            cursor[1] -= 1
        else:
            camera.move(0, -1, terrain)
    elif event.key == K_DOWN:
        if cursor[1] < 14:
            cursor[1] += 1
        else:
            camera.move(0, 1, terrain)
    elif event.key == K_RIGHT:
        if cursor[0] < 14:
            cursor[0] += 1
        else:
            camera.move(1, 0, terrain)
    elif event.key == K_LEFT:
        if cursor[0] > 0:
            cursor[0] -= 1
        else:
            camera.move(-1, 0, terrain)

    # S'occupe de tout ce qui est bouger un personnage et attaquer
    if event.key == K_RETURN:
        if isSomeoneSelected:
            # Si nous avons déjà un personnage selectionné
            selected = None
            for char in characters:
                if char.isSelected():
                    selected = char
                    break
            if cursor[0] == selected.getX() and cursor[1] == selected.getY():
                # On affiche le menu permettant l'ouverture de l'inventaire ou autre.
                openMenu = [4, selected]
            elif (cursor[0] + camera.getOffsetX(),
                cursor[1] + camera.getOffsetY()) in selected.getReachableCases() and selected.canMove():
                isNewSelect = False
                for char in characters:
                    if char.getX() == cursor[0] + camera.getOffsetX() and char.getY() == cursor[1] + camera.getOffsetY():  # Si la case contient déjà un perso, on change de selection
                        if selected.canHeal() and (char.getX(), char.getY()) in selected.getHealableCases(characters,
                                                                                                          terrain):  # Si on peut heal
                            isNewSelect = True
                            isSomeoneSelected = False
                            selected.goHeal(char, terrain, enemies, characters)
                        else:
                            selected.unSelect()
                            char.select(terrain, enemies, characters)
                            isNewSelect = True
                if not isNewSelect:  # Si l'utilisateur clique bien sur une case où le perso peut bouger, sans autre perso dessus
                    openMenu = [selected.move(cursor[0] + camera.getOffsetX(), cursor[1] + camera.getOffsetY(), terrain, enemies, characters), selected]
                    # Une fois qu'un perso a bougé, on le déselectionne
                    selected.unSelect()
                    isSomeoneSelected = False
            else:
                hasHealed = False

                if not selected.canMove():
                    for char in characters:
                        if char.getX() == cursor[0] + camera.getOffsetX() and char.getY() == cursor[1] + camera.getOffsetY():  # Si la case contient déjà un perso, on change de selection
                            if selected.canHeal() and (char.getX(), char.getY()) in selected.getHealableCases(
                                    characters,
                                    terrain):  # Si on peut heal
                                isSomeoneSelected = False
                                hasHealed = True
                                selected.healSomeone(char, enemies)
                                selected.unSelect()
                if not hasHealed:
                    # Nous vérifions que la case ne contient pas un ennemi
                    en = None

                    for enemy in enemies:
                        if enemy.getX() == cursor[0] + camera.getOffsetX() and enemy.getY() == cursor[1] + camera.getOffsetY() and (enemy.getX(), enemy.getY()) in selected.getAttackableCases():
                            # Dans ce cas on combat en plus de se déplacer
                            en = enemy
                            break
                    if en is not None:
                        openMenu = [2, en, selected]

                    selected.unSelect()
                    isSomeoneSelected = False
        else:
            for char in characters:
                if char.getX() == (cursor[0] + camera.getOffsetX()) and char.getY() == (
                        cursor[1] + camera.getOffsetY()) and not char.isTurnEnded():
                    char.select(terrain, enemies, characters)
                    isSomeoneSelected = True
                    break
            if not isSomeoneSelected:
                openMenu = [1]
    return isSomeoneSelected, openMenu

def handleMenu(screen, event, menus):
    action = ["none"]

    if event.type == KEYDOWN:
        if event.key == K_UP:
            menus[-1].moveCursor(-1)  # On ne change la position du curseur que sur le dernier menu ouvert
        elif event.key == K_DOWN:
            menus[-1].moveCursor(1)
        elif event.key == K_LEFT:
            menus[-1].moveCursor(2)
        elif event.key == K_RIGHT:
            menus[-1].moveCursor(3)
        elif event.key == K_RETURN:
            # Quelques valeurs qui seront toujours les mêmes :
            # 1 - Retour, on ferme le menu
            menuValue = menus[-1].select()
            if menuValue[0] == 1:
                menus.remove(menus[-1])
            else:
                action = menuValue
        elif event.key == K_ESCAPE:
            menus.remove(menus[-1])
    for menu in menus:
        drawMenu(screen, menu)

    return action

def finishTurn(characters, enemies, terrain, screen):
    for enemy in enemies:
        if enemy.getActualHP() > 0:
            enemy.startTurn(terrain, characters, enemies)
            enemy.update(terrain, characters, screen, enemies)
    for char in characters:
        char.startTurn(terrain, enemies, characters)

def battle(screen, terrain, enemies, chars, next):
    inGame = True
    camera = Camera.Camera(7, 7)

    characters = []
    for char in chars:
        if char.isUsable():
            char.updateReachableCases(terrain, enemies, characters)
            characters.append(char)


    for enemy in enemies:
        enemy.updateReachableCases(terrain, characters, enemies)

    cursor = [7, 7]  # Le curseur est d'abord au milieu de l'écran
    isSomeoneSelected = False
    menuOpened = False
    isBossAlive = True


    menus = []

    drawBattle(screen, terrain, camera, cursor, characters, enemies)
    while inGame:
        for event in [pygame.event.wait()]:
            if event.type == QUIT:
                inGame = False
                return [["Quit"], chars, terrain]
            elif event.type == KEYDOWN:
                if not menuOpened:
                    isSomeoneSelected, openMenu = handleBattle(event, cursor, camera, terrain, characters, enemies, isSomeoneSelected)
                    isTurnFinished = True
                    for char in characters:
                        isTurnFinished = isTurnFinished and char.isTurnEnded()
                    if isTurnFinished:  # Si tous les personnages ont été utilisés
                        menus.clear()
                        menuOpened = False
                        isSomeoneSelected = False
                        finishTurn(characters, enemies, terrain, screen)
                    drawBattle(screen, terrain, camera, cursor, characters, enemies)

                    if openMenu[0] == 1:  # On ouvre le menu normal
                        menus.append(MenuBattle.MenuBattle({"Retour": 1, "Fin.": "endTurn"}, (450, 50, 125, 500)))
                        menuOpened = True
                        event = pygame.event.Event(48545, {"None": 1})  # On supprime l'event actuel pour qu'il ne soit pas compté dans le menu
                    elif openMenu[0] == 2:  # On ouvre le menu inventaire
                        menus.append(MenuBattle.inventoryMenuBattle((50, 50, 100, 100), openMenu[2], openMenu[1]))
                        menuOpened = True
                        event = pygame.event.Event(48545, {"None": 1})  # On supprime l'event actuel pour qu'il ne soit pas compté dans le menu
                    elif openMenu[0] == 3:  # On ouvre le menu de combat
                        menus.append(MenuBattle.MenuBeforeBattle(openMenu[2], openMenu[1], openMenu[2].getInventory()[0]))
                        menuOpened = True
                        event = pygame.event.Event(48545, {"None": 1})  # On supprime l'event actuel pour qu'il ne soit pas compté dans le menu
                    elif openMenu[0] == 4:
                        c = openMenu[1]
                        proche = characters[0]
                        for char in characters:
                            if (c == proche and char != proche) or char.manathanDistance((char.getX(), char.getY()), (c.getX(), c.getY())) < c.manathanDistance((c.getX(), c.getY()), (proche.getX(), proche.getY())) and c != char:
                                proche = char
                        if proche.manathanDistance((c.getX(), c.getY()), (proche.getX(), proche.getY())) == 1:
                            menus.append(MenuBattle.MenuPerso((450, 245, 125, 90), openMenu[1], proche))
                        else:
                            menus.append(MenuBattle.MenuPerso((450, 260, 125, 60), openMenu[1]))
                        menuOpened = True
                        event = pygame.event.Event(48545, {"None": 1})  # On supprime l'event actuel pour qu'il ne soit pas compté dans le menu

                if menuOpened:
                    drawBattle(screen, terrain, camera, cursor, characters, enemies)
                    action = handleMenu(screen, event, menus)
                    if len(menus) == 0:
                        menuOpened = False
                    if action[0] == "endTurn":
                        isSomeoneSelected = False
                        menus.clear()
                        menuOpened = False
                        finishTurn(characters, enemies, terrain, screen)
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)
                    elif action[0] == "battle":
                        menus.clear()
                        menuOpened = False
                        action[1].goAttack(action[2], enemies, action[3], terrain, screen, characters)
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)
                    elif action[0] == 3:
                        menus.clear()
                        menus.append(MenuBattle.MenuBeforeBattle(action[2], action[3], action[1]))
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)
                        for menu in menus:
                            menu.draw(screen)
                    elif action[0] == 5:
                        menus.clear()
                        menus.append(MenuBattle.inventoryMenu((450, 225, 100, 150), action[1]))
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)

                        for menu in menus:
                            menu.draw(screen)
                    elif action[0] == 6:
                        menus.clear()
                        menuOpened = False
                        action[1].endTurn()
                        action[1].unSelect()
                        isSomeoneSelected = False
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)
                    elif action[0] == 7:
                        action[1].useItem(action[2])
                        if action[1].getTypeItem() != 0:
                            action[2].getInventory().remove(action[1])
                            action[2].didSomething()
                        menus.clear()
                        menuOpened = False
                    elif action[0] == 8:
                        # On ouvre le menu d'echanges
                        menus.clear()
                        menus.append(MenuBattle.MenuEchange((195, 225, 205, 150), action[1]))
                        isSomeoneSelected = False
                        drawBattle(screen, terrain, camera, cursor, characters, enemies)
                        for menu in menus:
                            menu.draw(screen)

        for enemy in enemies:
            if enemy.isBoss() and enemy.getActualHP() <= 0:
                isBossAlive = False
                break
            elif enemy.isBoss() and enemy.getActualHP() > 0:
                break
            elif enemy.getActualHP() <= 0:
                enemies.remove(enemy)
        if not isBossAlive:
            return [next, chars, terrain]  # On part du principe que next contient déjà une state, merci utils.

        isSomeoneAlive = False
        for char in characters:
            if char.getActualHP() > 0:
                isSomeoneAlive = True
            else:
                characters.remove(char)
        if not isSomeoneAlive:
            return [["Title"], chars, terrain]

        pygame.display.update()
        pygame.time.wait(50)
