import pygame


class Hero:
    def __init__(self, classImage, walkingRight, lvl, hp, mana, atk, spd, dex, defense, vit, wis, wpn, posVector, hitSound):
        self.classImage = classImage
        self.walkingRight = walkingRight
        self.lvl = lvl
        self.hp = hp
        self.mana = mana
        self.atk = atk
        self.spd = spd
        self.dex = dex
        self.defense = defense
        self.vit = vit
        self.wis = wis
        self.wpn = wpn
        self.posVector = posVector
        self.hitSound = hitSound


    def setAttack(self, att):
        self.atk = att

    def calculateDmg(self):
        return self.wpn.dmg + self.atk

    def get_wpn(self):
        return self.wpn

    def get_health(self):
        return self.hp

    def set_health(self, health):
        self.hp = health

    def get_image(self):
        return self.classImage

    def set_image(self, img):
        self.classImage = img

    def get_pos(self):
        return self.posVector

    def set_pos(self, pos):
        self.posVector = pos

    def get_hitSound(self):
        return self.hitSound


class Knight(Hero):
    def __init__(self, name, lvl, hp, mana, atk, spd, dex, defense, vit, wis, wpn, posVector, hitSound):
        super().__init__("Assets/Knight.png", "Assets/knightWalkingRight.png", lvl, hp, mana, atk, spd, dex, defense, vit, wis, wpn, posVector, hitSound)
        # add lvl scaling here
        self.maxDef = 40
        self.name = name

    def get_name(self):
        return self.name + " the Knight."

    def get_image(self):
        return self.classImage

    def get_pos(self):
        return self.posVector

    def set_image(self, img):
        self.classImage = img