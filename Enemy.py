#import main as m

counter = 0

class Enemy:
    def __init__(self, name, image, health, dmg, speed, defense, posVector, hitSound, wpn):
        self.name = name
        self.image = image
        self.health = health
        self.dmg = dmg
        self.speed = speed
        self.defense = defense
        self.posVector = posVector
        self.hitSound = hitSound
        self.wpn = wpn
        self.maxHealth = health

    def move_to_center(self):
        if not (610 <= self.posVector.x <= 620):
            if self.posVector.x < 610:
                self.posVector.x += 5
            else:
                self.posVector.x -= 5
        if not (260 <= self.posVector.y <= 270):
            if self.posVector.y < 260:
                self.posVector.y += 5
            else:
                self.posVector.y -= 5

    def move_to_left(self):
        if self.posVector.x > 60:
            self.posVector.x -= 30
        if not (260 <= self.posVector.y <= 270):
            if self.posVector.y < 260:
                self.posVector.y += 30
            else:
                self.posVector.y -= 30

    def move_to_top(self):
        if self.posVector.y > 40:
            self.posVector.y -= 30
        if self.posVector.x > 640:
            self.posVector.x -= 30
        if self.posVector.x < 580:
            self.posVector.x += 30

    def move_to_right(self):
        if self.posVector.x < 1200:
            self.posVector.x += 30
        if not (260 <= self.posVector.y <= 270):
            if self.posVector.y < 260:
                self.posVector.y += 10
            else:
                self.posVector.y -= 10

    def get_wpn(self):
        return self.wpn

    def set_wpn(self, wep):
        self.wpn = wep

    def calculateDmg(self):
        return self.wpn.dmg + self.dmg

    def get_wpn(self):
        return self.wpn

    def get_health(self):
        return self.health

    def set_health(self, hp):
        self.health = hp

    def get_image(self):
        return self.image

    def set_image(self, img):
        self.image = img

    def get_pos(self):
        return self.posVector





class Oryx(Enemy):
    def __init__(self, name, image, health, dmg, speed, defense):
        super().__init__("Oryx", "Oryx.png", 100, 10, 30, 3, (400, 100))
        self.maxHealth = health

    #def get_health(self):
        #return self.health

