class Weapon:
    def __init__(self, name, dmg, projSpeed, projDuration, projImage, projSound):
        self.name = name
        self.dmg = dmg
        self.projSpeed = projSpeed
        self.projDuration = projDuration
        self.projImage = projImage
        self.projSound = projSound

    def get_image(self):
        return self.projImage

    def get_sound(self):
        return self.projSound

class Sword(Weapon):
    projSpeed = 13
    projDuration = 30


class Dagger(Weapon):
    projSpeed = 20
    projDuration = 30


