import io
import os
import Terrain
import Case
import Characters
import Weapon
import Item
import pygame
from datetime import datetime
import Save


def saveImage(image, number):
    pygame.image.save(image, "Saves/save" + str(number) + ".jpg")
def save(number, type, scene, line, image, characters):

    now = datetime.now().strftime("%d/%m/%Y Ã  %H:%M")

    saveFile = io.open("Saves/save" + str(number) + ".txt", "w", encoding="UTF-8")
    saveFile.write(type + "\n" + scene + "\n" + str(line) + "\n" + now)
    saveFile.close()
    saveImage(image, number)
    if len(characters) > 0:
        saveCharacters(characters, number)
    

def loadImage(number):
    return pygame.image.load("Saves/save" + str(number) + ".jpg")

def load(number):
    try:
        saveFile = io.open("Saves/save" + str(number) + ".txt", "r", encoding="UTF-8")
        lines = saveFile.readlines()
        saveFile.close()

        s = Save.Save(
            loadImage(number),  # image
            lines[0][0:len(lines[0])-1],  # type
            lines[1][0:len(lines[1])-1],  # scene
            int(lines[2][0:len(lines[2])-1]),  # line
            lines[3],  # date de creation
            number
        )
        return s
    except OSError:
        return None

def loadBattle(battle, nbSave):
    file = io.open("Battles/" + battle + ".txt", "r", encoding="UTF-8")
    lines = file.readlines()
    file.close()

    size = (int(lines[0].split("x")[0]), int(lines[0].split("x")[1]))

    cases = []
    for y in range(size[1]):
        for x in range(size[0]):
            cases.append(Case.Case(x, y, int(lines[y + 1][x])))
    terrain = Terrain.Terrain(size[0], size[1])
    terrain.setCases(cases)

    margin = 1 + size[1]

    nbEnemies = int(lines[margin].split(":")[1])
    enemies = []
    for i in range(nbEnemies):
        infos = lines[margin + 1 + i].split(",")
        #infos :
        # 0 - Classe
        # 1 - PosX
        # 2 - PosY
        # 3 - MAX HP
        # 4 - Attaque
        # 5 - Defense
        # 6 - Agilité
        # 7 - Chance
        # 8 - Deplacement
        # 9 - Vitesse
        # 10 - Magie
        # 11 - Resistance
        # 12 - Arme
        # 13 - Lvl
        # 14 - Boss

        characteristics = [
            int(infos[3]),
            int(infos[4]),
            int(infos[5]),
            int(infos[6]),
            int(infos[7]),
            int(infos[8]),
            int(infos[9]),
            int(infos[10]),
            int(infos[11])
        ]
        inventory = [
            Weapon.getWeapon(int(infos[12]))
        ]

        print(infos[14])
        isBoss = "True" in infos[14]

        if infos[0] == "0":  # Barbare
            enemies.append(
                Characters.Barbare(int(infos[1]), int(infos[2]), characteristics, terrain, inventory, int(infos[13]), 0, isBoss)
            )
        elif infos[0] == "1":  # Archer
            enemies.append(
                Characters.Archer(int(infos[1]), int(infos[2]), characteristics, terrain, inventory, int(infos[13]), 0, isBoss)
            )
        elif infos[0] == "2":  # Fredegonde
            enemies.append(
                Characters.Fredegonde(int(infos[1]), int(infos[2]), characteristics, terrain, inventory, int(infos[13]), 0, True, isBoss, False)
            )
    margin += nbEnemies+1


    # On part du principe que le reste sera la position de base des personnages et finalement la suite de l'histoire
    posChars = []
    for line in lines[margin:margin+7]:
        pos = (int(line.split(",")[0]), int(line.split(",")[1]))
        posChars.append(pos)

    nextScene = lines[margin + 7].split(";")  # Type, Nom
    nextScene.append(1)

    return [terrain, enemies, loadCharacters(nbSave, terrain, posChars), nextScene]


def loadCharacters(nbSave, terrain, posChars):
    if not os.path.isfile("Saves/chars" + str(nbSave) + ".txt"):  # Si la sauvegarde n'existe pas
        return createCharactersSave(nbSave, terrain, posChars)

    file = io.open("Saves/chars" + str(nbSave) + ".txt", "r", encoding="UTF-8")
    lines = file.readlines()
    file.close()

    if len(lines) == 0:  # Les personnages n'ont pas ete sauvegardes
        return createCharactersSave(nbSave, terrain, posChars)

    characters = []

    for i in range(7):
        infos = lines[i*3 + 0].split(",")
        stats = [
            int(infos[0]),
            int(infos[1]),
            int(infos[2]),
            int(infos[3]),
            int(infos[4]),
            int(infos[5]),
            int(infos[6]),
            int(infos[7]),
            int(infos[8])
        ]

        inventory = []
        infos = lines[i * 3 + 1].split(";")
        for item in infos:
            infosItem = item.split(",")
            if infosItem[0] == "I":  # Dans ce cas on veut un item
                inventory.append(Item.getItem(int(infosItem[1])))
            else:  # On veut une arme
                inventory.append(Weapon.getWeapon(int(infosItem[1])))
        lvl = lines[i * 3 + 2].split(",")
        usable = (lvl[2] == "True" or lvl[2] == "True\n")

        if i == 0:  # Goldy
            characters.append(Characters.Goldy(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 1:  # Inanna
            characters.append(Characters.Inanna(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 2:  # Lulu
            characters.append(Characters.Lugalbanda(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 3:  # UrNungal
            characters.append(Characters.UrNungal(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 4:  # Shura
            characters.append(Characters.Shura(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 5:  # Sagburu
            characters.append(Characters.Sagburu(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), usable))
        elif i == 6:  # Frédégonde
            characters.append(Characters.Fredegonde(posChars[i][0], posChars[i][1], stats, terrain, inventory, int(lvl[0]), int(lvl[1]), False, False, usable))

    return characters

def saveCharacters(characters, nbSave):
    file = io.open("Saves/chars" + str(nbSave) + ".txt", "w", encoding="UTF-8")
    
    for i in range(7):
        stats = str(characters[i].getMaxHP()) + "," + str(characters[i].getAtk()) + "," + str(characters[i].getDef())
        stats += "," + str(characters[i].getAgility()) + "," + str(characters[i].getLuck()) + ","
        stats += str(characters[i].getMaxDeplacement()) + "," + str(characters[i].getSpeed()) + ","
        stats += str(characters[i].getMagie()) + "," + str(characters[i].getResistance())

        inv = ""
        first = True
        for item in characters[i].getInventory():
            if not first:
                inv += ";"
            else:
                first = False

            if item.getTypeItem() == 0:  # Arme
                inv += "W," + str(Weapon.getIdOf(item))
            elif item.getTypeItem() == 1:
                inv += "I,0"
        lvl = str(characters[i].getLevel()) + "," + str(characters[i].getXP()) + "," + str(characters[i].isUsable())
        file.writelines([stats + "\n", inv + "\n", lvl + "\n"])
    file.close()

def createCharactersSave(nbSave, terrain, posChars):
    characters = [
        Characters.Goldy(posChars[0][0], posChars[0][1], [12, 8, 5, 5, 6, 4, 7, 1, 5], terrain, [Weapon.Ea], 1, 0),
        Characters.Inanna(posChars[1][0], posChars[1][1], [10, 5, 3, 1, 4, 4, 3, 5, 1], terrain, [Weapon.Maanna], 1, 0),
        Characters.Lugalbanda(posChars[2][0], posChars[2][1], [18, 5, 6, 4, 3, 5, 4, 1, 3], terrain, [Weapon.Ninsun], 1, 0),
        Characters.UrNungal(posChars[3][0], posChars[3][1], [10, 4, 3, 2, 6, 4, 6, 6, 4], terrain, [Weapon.EaFake], 1, 0),
        Characters.Shura(posChars[4][0], posChars[4][1], [10, 5, 3, 7, 6, 5, 5, 7, 6], terrain, [Weapon.CatSword], 1, 0),
        Characters.Sagburu(posChars[5][0], posChars[5][1], [11, 2, 2, 4, 5, 5, 2, 9, 7], terrain, [Weapon.Baton], 1, 0),
        Characters.Fredegonde(posChars[6][0], posChars[6][1], [30, 6, 2, 10, 7, 5, 6, 1, 1], terrain, [Weapon.QueensMurder], 1, 0, False, False, False)
    ]
    saveCharacters(characters, nbSave)
    return characters


def loadMusic(music):
    pygame.mixer.music.load("Assets/Musiques/" + music + ".mp3")
    s = loadSettings()
    pygame.mixer.music.set_volume(0.03 * (float(s["Volume"]) / 100))

def playMusic(loop=True):
    r = 0
    if loop:
        r = -1
    pygame.mixer.music.play(r)
def stopMusic():
    pygame.mixer.music.stop()


def loadSettings():
    settingsFile = io.open("Assets/Settings.txt", "r", encoding="UTF-8")
    settings = {}
    lines = settingsFile.readlines()
    settingsFile.close()
    for i in range(len(lines)):
        if lines[i] != "\n":
            s = lines[i].split(":")
            settings[s[0]] = s[1][:len(s[1])-1]
    return settings

def changeSetting(setting, value):
    settings = loadSettings()
    settings[setting] = value
    file = io.open("Assets/Settings.txt", "w", encoding="UTF-8")
    for k in settings:
        file.write(k + ":" + str(settings[k]) + "\n")
    file.close()

def saveSettings(settings):
    file = io.open("Assets/Settings.txt", "w", encoding="UTF-8")
    for k in settings:
        file.write(k + ":" + str(settings[k]) + "\n")
    file.close()

def trueEndUnlocked():
    return False

def loadBattleMapImage(character):
    return pygame.image.load("Assets/" + character + "/Battle/map.png")

def loadBattlePortrait(character):
    return pygame.image.load("Assets/" + character + "/Battle/portrait.png")
