import pygame
import math
import random
from random import seed
from random import randint
import Enemy
import Weapon
import Hero
from pygame import mixer
import time
from multiprocessing import Process

'''TO DO LIST
to install: cd into this folder then do in terminal:
pyinstaller main.py --onefile --windowed
Creates a dist folder, run main from it



add disclaimer page and character select page 

make oryx despawn properly an make it so you cant cheese the laser part by going behind it

add character pick screen

add play again button -- add undertale opening sound for play again

add indication for when oryx is immune

add animations for walking/shooting and find a way to remove background for images (preferably without 
drawing sprites myself lol) (use angle math for shooting animation)

Add items, drops, stat pots, more enemies/diff fights
for items, make a list of possible drops for an enemy, then use randint to see which drop(s) you pull from the list

Add ability to walk offscreen? Like camera follows main character


put all hitboxes in a list
if colliderect with (element in hitbox)
then -->
enemyHit(this)
function takes in an enemy, which has a health and sound attributes whihch the function calls

'''


pygame.init()
mixer.init()

#mainMusic = mixer.music.load("sorc.mp3")

chan0 = pygame.mixer.Channel(0)
#chan0.play(pygame.mixer.Sound("sorc.mp3"), 3000) #loops 3000 times
chan0.play(pygame.mixer.Sound("Music/Calm.mp3"), 3000)
chan0.set_volume(0.2) # takes in value 0-1.0
playerSounds = pygame.mixer.Channel(1)
enemySounds = pygame.mixer.Channel(2)
playerHitSounded = pygame.mixer.Channel(3)
lootDrop = pygame.mixer.Channel(4)
chan5 = pygame.mixer.Channel(5)
chan5.set_volume(0.5)


screen = pygame.display.set_mode((1400, 780))
frame = screen.get_rect()
camera = frame.copy()
space = frame.inflate(frame.width*2, frame.height*2)
clock = pygame.time.Clock() # used for moving at a constant speed regardless of fps


acclaimProjectile = pygame.image.load("Assets/acclaim Projectile.png").convert_alpha()
swordAcclaim = Weapon.Sword("Sword of the Acclaim", 10, 13, 25, acclaimProjectile, "Music/golden_sword.mp3")

greenDagProjectile = pygame.image.load("Assets/greenDagger.png").convert_alpha()
greenDagger = Weapon.Dagger("Emeraldshard Dagger", 5, 25, 20, greenDagProjectile, "Music/poison_fang_dagger.mp3")

player_pos = pygame.Vector2(screen.get_width() / 2 - 50, screen.get_height() - 100)


player = Hero.Knight("Kyle", 1, 100, 50, 10, 15, 10, 10, 10, 10, swordAcclaim, player_pos, "Music/rogue_hit.mp3")
# name, lvl, hp, mana, atk, spd

'''knightRight = pygame.image.load("knightR.png").convert_alpha()
knightRight.set_colorkey((255,255,255))
knightRight = pygame.transform.scale(knightRight, (100, 100))'''


StoneOryx = pygame.image.load("Assets/Statue of Oryx.png").convert_alpha()
StoneOryx = pygame.transform.scale(StoneOryx, (150, 150))
oryxImage = pygame.image.load('Assets/Oryx.png').convert_alpha()
oryxImage = pygame.transform.scale(oryxImage, (200,200))
oryxPos = pygame.Vector2(screen.get_width() / 2 - 100, 100)
# this is where oryx starts, his hitboxes are based off this

oryxWeaponProj = pygame.image.load("Assets/greenLaser.png").convert_alpha()
#oryxWeaponProj = pygame.image.load("lolLaser.png").convert_alpha()
oryxWeaponProj = pygame.transform.scale(oryxWeaponProj, (100, 50))
oryxWeapon = Weapon.Weapon("Oryx's Weapon", 0, 15, 400, oryxWeaponProj, "Music/silentSound.mp3")
redLaserProj = pygame.image.load("Assets/redLaser.jpeg").convert_alpha()
redLaserProj = pygame.transform.scale(redLaserProj, (100, 50))
oryxWeaponTwo = Weapon.Weapon("Oryx's 2nd Weapon", 10, 30, 70, redLaserProj, "Music/laserSound.mp3")
oryx = Enemy.Enemy("Oryx", StoneOryx, 500, 10, 30, 3, oryxPos, "Music/minion_of_oryx_hit.mp3", oryxWeapon)

#print(oryxPos.x)

text_font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)  # the int is size of font


def move(surfaceX, surfaceY, goalX, goalY):
    direction = (goalX - surfaceX, goalY - surfaceY)
    length = math.hypot(*direction)
    if length == 0.0:
        direction = (0, -1)
    else:
        direction = direction[0]/length, direction[1]/length
    angle = math.degrees(math.atan2(-direction[1], direction[0]))
    while surfaceX != goalX and surfaceY != goalY:
        surfaceX += direction[0]
        surfaceY += direction[1]


class Bullet:
    def __init__(self, shooterX, shooterY, wpn):
        self.timeAlive = 0
        self.duration = wpn.projDuration
        self.pos = (shooterX, shooterY)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - shooterX, my - shooterY)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        pygame.Surface((50, 50)).convert_alpha()  # this is the actual hitbox of the bullet, the img is irrelevant
        self.bullet = pygame.transform.rotate(wpn.projImage.convert_alpha(), angle).convert_alpha()
        self.speed = wpn.projSpeed

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed,
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        if (testing):
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(bullet_rect))
        surf.blit(self.bullet, bullet_rect)

class EnemyBullet:
    def __init__(self, shooterX, shooterY, wpn, targetX, targetY):
        self.rect = wpn.projImage.get_rect().inflate(0, -5)
        self.timeAlive = 0
        self.duration = wpn.projDuration
        self.pos = (shooterX, shooterY)
        #mx = player_pos.centerx
        #mx, my = player_pos
        #targetX = player_pos.x + randint(0, playerImage.get_width())
        #targetY = player_pos.y + randint(0, playerImage.get_height())
        '''
        The targetX is set to be any random spot on the character so bullets are less consistent
        Therefor they are harder to dodge
        '''
        self.dir = (targetX - shooterX, targetY - shooterY)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        pygame.Surface((50, 50)).convert_alpha()  # this is the actual hitbox of the bullet, the img is irrelevant
        self.bullet = pygame.transform.rotate(wpn.projImage.convert_alpha(), angle).convert_alpha()
        self.speed = wpn.projSpeed

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed,
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        if (testing):
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(bullet_rect))
        surf.blit(self.bullet, bullet_rect)


bullets = []
sounds = []
enemyHitboxes = []
enemyBullets = []

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#x = player.posVector()


def enemyShootProjectile(shooter, startingX, startingY, endingX, endingY):
    chan5.play(pygame.mixer.Sound(shooter.get_wpn().projSound))
    enemyBullets.append(EnemyBullet(startingX, startingY, shooter.get_wpn(), endingX, endingY))


def enemyShootCoords(enemy, targetX, targetY):
    chan5.play(pygame.mixer.Sound(enemy.get_wpn().projSound))
    xOffset = (enemy.get_image().get_width() / 2)
    yOffset = (enemy.get_image().get_height() / 2)
    enemyBullets.append(EnemyBullet(enemy.get_pos().x + xOffset, enemy.get_pos().y + yOffset, enemy.get_wpn(),
    targetX + randint(0, playerImage.get_width()), targetY + randint(0, playerImage.get_width())))

def enemyShoot(enemy):
    xOffset = enemy.get_image().get_width() / 2
    yOffset = enemy.get_image().get_height() / 2
    #xOffset = 100
    #yOffset = 100
    # I tried making it so the bullet would come out of the enemy in the nearest direction of the player
    # eg: if the player is southeast of the enemy, the bullet would fire from the bottom right of the enemy
    # but i think that is both unnecessary and makes the game inconsistent
    '''if (player.get_pos().x > enemy.get_pos().x):
        xOffset = 200
    if (player.get_pos().y > enemy.get_pos().y):
        yOffet = 200
    if (player.get_pos().x < enemy.get_pos().x):
        xOffset = 0
    if (player.get_pos().y < enemy.get_pos().y):
        yOffet = 0
    print(xOffset, yOffset)'''
    enemyBullets.append(EnemyBullet(enemy.get_pos().x + xOffset, enemy.get_pos().y + yOffset, enemy.get_wpn(),
    player_pos.x + randint(0, playerImage.get_width()), player_pos.y + randint(0, playerImage.get_height())))


def shoot(shooter):
    bullets.append(Bullet(shooter.get_pos().x + 50, shooter.get_pos().y + 50, shooter.get_wpn()))
    playerSounds.set_volume(0.4)
    playerSounds.play(pygame.mixer.Sound(shooter.wpn.projSound))
    #mixer.music.load(wpn.projSound)
    #mixer.music.set_volume(0.7)
    #mixer.music.play()

def shootWithCoords(shooter, shooterX, shooterY):
    bullets.append(Bullet(shooterX + 50, shooterY + 50, shooter.get_wpn()))
    playerSounds.set_volume(0.4)
    playerSounds.play(pygame.mixer.Sound(shooter.wpn.projSound))
    #mixer.music.load(wpn.projSound)
    #mixer.music.set_volume(0.7)
    #mixer.music.play()

def oryxHit():
    enemySounds.set_volume(1)
    enemySounds.play(pygame.mixer.Sound("Music/minion_of_oryx_hit.mp3"))
    oryx.set_health(oryx.get_health() - 1)
    #mixer.music.load("minion_of_oryx_hit.mp3")
    #mixer.music.set_volume(0.7)
    #mixer.music.play()


def enemyHit(enemy):
    enemySounds.set_volume(1)
    enemySounds.play(pygame.mixer.Sound(enemy.hitSound))
    enemy.set_health(enemy.get_health() - player.calculateDmg())


def playerHit(player, enemy):
    playerHitSounded.set_volume(1)
    playerHitSounded.play(pygame.mixer.Sound(player.hitSound))
    player.set_health(player.get_health() - enemy.calculateDmg())

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)

def redrawWindow():
    screen.fill((255, 255, 255))
    #pygame.draw.rect(screen, (255,0,0), (200,300,200,200),0)
    #pygame.draw.rect(screen, (0,255,0),(500,500,100,200), 0)

run = True
hitTimer = 0
FPS = 60
generalTimer = 0
testing = False
oryxBattle = True
oryxAlive = oryxBattle

oryxImmune = False

rightCounter = 0
neutralCounter = 0
oryxHasBeenHit = 0
regretTimer = 0
fightBegins = False
timeTilFight = 0
movingToCenter = 0
movedToCenter = False
gigaAttack = False
gigaAttackTimer = 0
standardAttack = False
standardAttackTimer = 0

changingPhase = 0
# used for changing assets so I dont have to constantly reload them
leftAttackCounter = 0
rightAttackCounter = 0
doubleAttackCounter = 0

realFightText = 0
phase = 0

if testing:
    player.setAttack(50)

#player.setAttack(50)

while run:
    screen.fill("light blue")
    clock.tick(FPS)   # BEGINS a timer, next call will return the differnece in time between this call and current call
    hitTimer = hitTimer + 1
    generalTimer += 1
    #print(generalTimer)
    #print(phase)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    '''if gameOver == True:
        while True:
            draw_text("Level: ", text_font, ("white"), 200, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break'''

    playerImage = pygame.image.load(player.classImage)  # loads knight image from files
    playerImage = pygame.transform.scale(playerImage, (80, 80))
    #playerImage.convert_alpha()
    #if player.classImage != "Knight.png":
        #playerImage.set_colorkey("white")
    #playerImage.set_colorkey("white")
    #playerImage = pygame.Surface(playerImage, pygame.SRCALPHA)

    if player.get_health() <= 0:
        pygame.mixer.stop()
        chan0.play(pygame.mixer.Sound("Music/death_screen.mp3"))
        fade(screen.get_width(), screen.get_height())
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            draw_text("You died ", text_font, ("white"), screen.get_width()/2 - 100, 100)
            draw_text("Level: ", text_font, ("white"), screen.get_width()/2 - 100, 300)
            draw_text(str(player.lvl), text_font, ("white"), screen.get_width()/2 + 60, 300)
            pygame.display.flip()
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hitTimer >= 20:
            # add "and player has weapon" once implement equipment,
            # so you can only shoot while having a weapon
            bullets.append(Bullet(*player_pos, player.wpn))
            hitTimer = 0'''
    if run == False:
        break

    if oryxBattle:
        if oryxAlive:
            if oryxAlive:
                screen.blit(oryx.image, oryxPos)  # puts image of oryx at his hitbox location
                oryxRect = oryx.get_image().get_rect().inflate(30, -60).move(oryxPos.x, oryxPos.y + 25)
                # manually resizing hitbox for oryx image
                # oryx rect is the actual hitbox and location of oryx, img is irrelevant
            if not fightBegins:
                oryxImmune = True
                if oryxHasBeenHit < 1:
                    draw_text("Zzzzz...", text_font, ("black"), (oryxPos.x + 130), oryxPos.y - 10)
                elif oryxHasBeenHit >= 1000:
                    timeTilFight += 1
                    string = "You will regret that."
                    if regretTimer < len(string):
                        if generalTimer % 4 == 0:
                            regretTimer += 1
                            chan0.set_volume(0.1)
                            chan0.play(pygame.mixer.Sound("Music/asriel.mp3"))
                    draw_text(string[0:regretTimer], text_font, ("black"), oryxPos.x - 150, oryxPos.y - 50)
                    # slowly prints out the message
                    if timeTilFight >= 150:
                        # i used timeTilFight as a timer, same with a lot of other variables.
                        # should clean this up later
                        chan0.set_volume(0.3)
                        chan0.play(pygame.mixer.Sound("Music/ METALOVANIA.mp3"), 3000)
                        fightBegins = True
            if fightBegins:
                if oryx.health <= 0:
                    chan0.play(pygame.mixer.Sound("Music/victoryTheme.mp3"))
                    whiteBag = pygame.image.load("Assets/whiteBag.png").convert_alpha()
                    whiteBag = pygame.transform.scale(whiteBag, (100, 50))
                    oryxCoords = oryxPos
                    #oryxPos = pygame.Vector2(5000, 5000)
                    lootDrop.set_volume(1)
                    lootDrop.play(pygame.mixer.Sound("Music/loot_appears.mp3"))
                    oryxAlive = False

                '''if movingToCenter == 0:
                    oryxImmune = False
                else:
                    oryxImmune = True'''

                if oryx.health >= 150 and phase == 0:
                    phase = 1
                if oryx.health < 150 and phase == 1:
                    changingPhase = 1
                    phase = 2

                if phase == 1:
                    oryxImmune = False
                    if oryxPos.x < player_pos.x:
                        oryxPos.x += randint(0, 5)
                    else:
                        oryxPos.x += randint(-5, 0)
                    if oryxPos.y < player_pos.y:
                        oryxPos.y += randint(0, 5)
                    else:
                        oryxPos.y += randint(-5, 0)
                    if generalTimer % 60 == 0 and oryx.get_health() > 150:
                        enemyShootCoords(oryx, player_pos.x + 200, player_pos.y + 200)
                        enemyShootCoords(oryx, player_pos.x - 200, player_pos.y - 200)
                        enemyShoot(oryx)

                if phase == 2:
                    oryxImmune = True
                    realFightText += 1
                    if realFightText < 130:
                        generalTimer = 0
                        draw_text("Ha! Now the real fight begins!", pygame.font.SysFont("Arial", 30, bold=True), "black", oryxPos.x - 100, oryxPos.y + 30)
                    if changingPhase == 1:
                        oryx.set_image(oryxImage)
                        oryx.set_wpn(oryxWeaponTwo)
                        changingPhase = 0
                        generalTimer = 0
                    if not (610 <= oryxPos.x <= 620 and 260 <= oryxPos.y <= 270):
                        generalTimer = 0
                        oryx.move_to_center()
                        movingToCenter += 1
                    if 610 <= oryxPos.x <= 620 and 260 <= oryxPos.y <= 270 and realFightText > 150:   # these are the values from moveToCenter
                        movedToCenter = True
                        movingToCenter = 0
                        #gigaAttack = 1
                        if generalTimer <= 200:
                            '''the general timer here is how long the attack lasts, make sure you reset
                            gen timer to 0 before the attack begins, and keep this consistent
                            change gen time to change this attack's duration'''
                            if generalTimer % 2 == 0:
                                enemyShootCoords(oryx, randint(0, screen.get_width() - 1), randint(0, screen.get_height() - 1))
                        if generalTimer > 200:
                            phase = 3
                            generalTimer = 0
                if phase == 3 or phase == 4:
                    oryxImmune = True
                    if not (oryxPos.x <= 60 and 250 <= oryxPos.y <= 280) and phase == 3:
                        oryx.move_to_left()
                        generalTimer = 0
                    if generalTimer <= 200:
                        if 10 < generalTimer < 50:
                            if (generalTimer == 11):
                                missingInt = randint(0, 5)
                                chan5.play(pygame.mixer.Sound("Music/laserLoading.mp3"))
                            if missingInt != 0:
                                screen.blit(redLaserProj, (000, 0))
                            if missingInt != 0 and missingInt != 1:
                                screen.blit(redLaserProj, (000, 100))
                            if missingInt != 1 and missingInt != 2:
                                screen.blit(redLaserProj, (000, 200))
                            if missingInt != 2 and missingInt != 3:
                                screen.blit(redLaserProj, (000, 300))
                            if missingInt != 3 and missingInt != 4:
                                screen.blit(redLaserProj, (000, 400))
                            if missingInt != 4 and missingInt != 5:
                                screen.blit(redLaserProj, (000, 500))
                            if missingInt != 6 and missingInt != 7:
                                screen.blit(redLaserProj, (000, 600))
                            if missingInt != 7:
                                screen.blit(redLaserProj, (000, 700))
                        if generalTimer == 50:
                            chan5.stop()
                            '''enemyShootProjectile is for spawning a bullet at a certain spot, and then
                            having it go to a specified spot
                            enemyShootCoords spawns at the enemys location and goes to a specified spot
                            enemyShoot spawns at enemy and shoots at the player'''
                            for i in range(8):
                                if i != missingInt and i != missingInt + 1:
                                    enemyShootProjectile(oryx, 120, (100 * i) + 22, screen.get_width(), (100 * i) + 22)
                        if generalTimer == 70 and leftAttackCounter < 3:
                            leftAttackCounter += 1
                            generalTimer = 10
                            '''enemyShootProjectile(oryx, 100, 0, screen.get_width(), 0)
                            enemyShootProjectile(oryx, 100, 100, screen.get_width(), 100)
                            enemyShootProjectile(oryx, 100, 200, screen.get_width(), 200)
                            enemyShootProjectile(oryx, 100, 300, screen.get_width(), 300)
                            enemyShootProjectile(oryx, 100, 400, screen.get_width(), 400)
                            enemyShootProjectile(oryx, 100, 500, screen.get_width(), 500)
                            enemyShootProjectile(oryx, 100, 600, screen.get_width(), 600)
                            enemyShootProjectile(oryx, 100, 700, screen.get_width(), 700)'''
                        if generalTimer >= 100:
                            phase = 4
                            if not (oryxPos.x >= 1200 and 250 <= oryxPos.y <= 280):
                                '''these functions are reliant on an Enemy function ,make sure the bounds are
                                consistent in each method, or else funky stuff happens'''
                                oryx.move_to_right()
                                generalTimer = 101
                            if oryxPos.x >= 1200 and 250 <= oryxPos.y <= 280:
                                if generalTimer == 101:
                                    missingInt = randint(0, 5)
                                    #chan5.play(pygame.mixer.Sound("laserLoading.mp3"))
                                if 101 <= generalTimer <= 150:
                                    if missingInt != 0:
                                        screen.blit(redLaserProj, (1300, 0))
                                    if missingInt != 0 and missingInt != 1:
                                        screen.blit(redLaserProj, (1300, 100))
                                    if missingInt != 1 and missingInt != 2:
                                        screen.blit(redLaserProj, (1300, 200))
                                    if missingInt != 2 and missingInt != 3:
                                        screen.blit(redLaserProj, (1300, 300))
                                    if missingInt != 3 and missingInt != 4:
                                        screen.blit(redLaserProj, (1300, 400))
                                    if missingInt != 4 and missingInt != 5:
                                        screen.blit(redLaserProj, (1300, 500))
                                    if missingInt != 6 and missingInt != 7:
                                        screen.blit(redLaserProj, (1300, 600))
                                    if missingInt != 7:
                                        screen.blit(redLaserProj, (1300, 700))
                                if generalTimer == 150:
                                    chan5.stop()
                                    for i in range(8):
                                        if i != missingInt and i != missingInt + 1:
                                            enemyShootProjectile(oryx, 1320, (100 * i) + 22, 0, (100 * i) + 22)
                                if generalTimer == 170 and rightAttackCounter < 3:
                                    generalTimer = 100
                                    rightAttackCounter += 1
                                if rightAttackCounter > 3 and generalTimer >= 199:
                                    phase = 5
                                    rightAttackCounter = 0
                                    leftAttackCounter = 0
                                    generalTimer = 0
                if phase == 5 or (phase == 4 and generalTimer > 200):
                    phase = 5
                    if not (580 <= oryxPos.x <= 640 and 0 <= oryxPos.y <= 40):
                        generalTimer = 0
                        oryx.move_to_top()
                    if 580 <= oryxPos.x <= 640 and 0 <= oryxPos.y <= 150:
                        #print("reached here")
                        if 10 < generalTimer < 50:
                            if generalTimer == 11:
                                missingInt = randint(0, 5)
                                missingInt2 = randint(0, 5)
                                #chan5.play(pygame.mixer.Sound("laserLoading.mp3"))
                            if missingInt != 0:
                                screen.blit(redLaserProj, (1300, 0))
                            if missingInt != 0 and missingInt != 1:
                                screen.blit(redLaserProj, (1300, 100))
                            if missingInt != 1 and missingInt != 2:
                                screen.blit(redLaserProj, (1300, 200))
                            if missingInt != 2 and missingInt != 3:
                                screen.blit(redLaserProj, (1300, 300))
                            if missingInt != 3 and missingInt != 4:
                                screen.blit(redLaserProj, (1300, 400))
                            if missingInt != 4 and missingInt != 5:
                                screen.blit(redLaserProj, (1300, 500))
                            if missingInt != 6 and missingInt != 7:
                                screen.blit(redLaserProj, (1300, 600))
                            if missingInt != 7:
                                screen.blit(redLaserProj, (1300, 700))

                            if missingInt2 != 0:
                                screen.blit(redLaserProj, (0, 0))
                            if missingInt2 != 0 and missingInt2 != 1:
                                screen.blit(redLaserProj, (0, 100))
                            if missingInt2 != 1 and missingInt2 != 2:
                                screen.blit(redLaserProj, (0, 200))
                            if missingInt2 != 2 and missingInt2 != 3:
                                screen.blit(redLaserProj, (0, 300))
                            if missingInt2 != 3 and missingInt2 != 4:
                                screen.blit(redLaserProj, (0, 400))
                            if missingInt2 != 4 and missingInt2 != 5:
                                screen.blit(redLaserProj, (0, 500))
                            if missingInt2 != 6 and missingInt2 != 7:
                                screen.blit(redLaserProj, (0, 600))
                            if missingInt2 != 7:
                                screen.blit(redLaserProj, (0, 700))

                        if generalTimer == 49:
                            chan5.stop()
                            doubleAttackCounter += 1
                            for i in range(8):
                                if i != missingInt and i != missingInt + 1:
                                    enemyShootProjectile(oryx, 1320, (100 * i) + 22, 0, (100 * i) + 22)
                            for i in range(8):
                                if i != missingInt2 and i != missingInt2 + 1:
                                    enemyShootProjectile(oryx, 20, (100 * i) + 22, screen.get_width(), (100 * i) + 22)
                        if generalTimer == 70 and doubleAttackCounter < 3:
                            generalTimer = 0
                        if generalTimer >= 100:
                            phase = 6
                            doubleAttackCounter = 0
                            generalTimer = 0

                if phase == 6:
                    oryxImmune = False
                    if not (610 <= oryxPos.x <= 620 and 260 <= oryxPos.y <= 270):
                        generalTimer = 0
                        draw_text("Huff... puff...", text_font, "black", oryxPos.x + 50, oryxPos.y - 10)
                        oryx.move_to_center()
                    draw_text("Huff... puff...", text_font, "black", oryxPos.x + 50, oryxPos.y - 10)
                    if generalTimer > 60:
                        phase = 2
                        generalTimer = 0















                    '''if movingToCenter == 0:
                        oryxPos.x += randint(-10, 10)
                        oryxPos.y += randint(-10, 10)
                    if generalTimer % 15 == 0 and 0 < oryx.get_health() <= 150:
                    #enemyShoot automatically aims at player,
                    #enemyShootCoords aims anywhere you want
                    #enemyShoot(oryx)
                    enemyShootCoords(oryx, player_pos.x, player_pos.y)'''
        if oryxAlive == False:
            screen.blit(whiteBag, oryxCoords)

    if testing:
        if oryxBattle:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(oryxRect))  # this is the hitbox representation

    draw_text("Health: ", text_font, ("black"), 0, 0)  # text font is defined above, 0,0 is coords
    draw_text(str(player.get_health()), text_font, (0, 0, 0), 180, 0)
    if oryxAlive:
        draw_text("Oryx Health: ", text_font, ("black"), (screen.get_width() - 400), 0)
        # text font is defined above, 0,0 is coords
        if oryxImmune == True:
            draw_text("IMMUNE", text_font, (0, 0, 0), (screen.get_width() - 100), 0)
        else:
            draw_text(str(oryx.get_health()), text_font, (0, 0, 0), (screen.get_width() - 100), 0)

    for bullet in bullets[:]:
        # this code checks each bullet to see if they're colliding with anything, or off-screen, and
        # performs actions accordingly
        bullet.update()     #updates pos of bullets
        bullet.timeAlive = bullet.timeAlive + 1
        bullet.draw(screen)
        #if pygame.Rect.colliderect(deezrect, bullet):
            #playerHit(player, player)
        if bullet.timeAlive > bullet.duration:
            bullets.remove(bullet)
            continue    # have to continue because you can't remove the bullet again after it's been removed
        if oryxBattle:
            if oryxRect.collidepoint(bullet.pos):   #replace this with if bullet collides with anything, subtract its health
                # and play a sound, maybe make a function for when things get hit
                if oryx.health == oryx.maxHealth:
                    oryxHasBeenHit += 1
                if oryxHasBeenHit == 1:
                    chan0.stop()
                bullets.remove(bullet)
                if oryxImmune:
                    enemySounds.set_volume(1)
                    enemySounds.play(pygame.mixer.Sound("Music/shieldSound.mp3"))
                if not oryxImmune:
                    enemyHit(oryx)
                #mixer.music.load("minion_of_oryx_hit.mp3")
                #mixer.music.set_volume(0.7)
                #sounds.append(Process(target = oryxHit))
                #mixer.music.play()
                continue
        if not screen.get_rect().inflate(500, 500).collidepoint(bullet.pos):
            bullets.remove(bullet)

    if 0 < oryxHasBeenHit < 1000:
        oryxHasBeenHit += 1
        if oryxPos.y <= screen.get_height()/2 - oryx.get_image().get_height() + 40:
            oryxPos.y += 5
        else:
            oryxHasBeenHit = 1000



    #deez = pygame.display.set_mode((400,300))
    #pygame.draw.rect(screen, ("black"), (400, 300, 400, 300))
    #if player_pos.collidepoint(screen):
        #print('hi')
    #deezrect = pygame.draw.rect(screen, ("black"), (200, 250, 100, 300), 0)
    #screen.blit(deezrect, (200,250,100,300))



    for bullet in enemyBullets[:]:
        # this code checks each bullet to see if they're colliding with anything, or off-screen, and
        # performs actions accordingly
        bullet.update()     #updates pos of bullets
        bullet.timeAlive = bullet.timeAlive + 1
        bullet.draw(screen)
        if bullet.timeAlive > bullet.duration:
            enemyBullets.remove(bullet)
            continue    # have to continue because you can't remove the bullet again after it's been removed
        #if pygame.Rect.colliderect(bullet.rect.move(bullet.pos), playerRect):
        if playerRect.collidepoint(bullet.pos):
            # playerRect.collidepoint(bullet.pos):
            # replace this with if bullet collides with anything, subtract its health
            # and play a sound, maybe make a function for when things get hit
            enemyBullets.remove(bullet)
            playerHit(player, oryx)  #find a way to determine who hit the player,
            #maybe put a self.owner attribute in the enemyBullet class to check who fired the bullet that hit the player
            continue
        if not screen.get_rect().inflate(500, 500).collidepoint(bullet.pos):
            enemyBullets.remove(bullet)    #makes sure bullets will eventually delete, if duration is infinite

    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0] and hitTimer >= 10:
        try:
            shoot(player)
            #shoot(playerRect.centerx, playerRect.centery, player.wpn)
            #bullets.append(Bullet(*player_pos, player.wpn))
            hitTimer = 0
        except AttributeError:
            pass
    '''if (keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.MOUSEBUTTONUP] or keys[pygame.K_o]) and hitTimer >= 10:
        print("This is happening")
        bullets.append(Bullet(*player_pos, player.wpn))
        hitTimer = 0'''
    #player moves indepedent of framerate because of dt
    dt = clock.tick(60)  # this is the time in seconds that it took to do all above calculations
    #rightCounter += 1
    #neutralCounter += 1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= 0.05 * dt * player.spd
        if player_pos.y <= 0:
            player_pos.y = 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += 0.05 * dt * player.spd
        if player_pos.y + playerImage.get_height() >= screen.get_height():
            player_pos.y = screen.get_height() - 1 - playerImage.get_height()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= 0.05 * dt * player.spd
        if player_pos.x <= 0:
            player_pos.x = 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += 0.05 * dt * player.spd
        if player_pos.x + playerImage.get_width() >= screen.get_width():
            player_pos.x = screen.get_width() - 1 - playerImage.get_width()
        '''if (player.get_image() == "KnightDrawing.png"):
            rightCounter += 1
        if (player.get_image() == "Knight.png"):
            neutralCounter += 1
        if (neutralCounter >= 7):
            player.set_image("KnightDrawing.png")
            neutralCounter = 0
        if rightCounter >= 7:
            player.set_image("Knight.png")

            rightCounter = 0
    if not (keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_a]
            or keys[pygame.K_LEFT] or keys[pygame.K_s] or keys[pygame.K_DOWN]
            or keys[pygame.K_w] or keys[pygame.K_UP]):
        player.set_image("Knight.png")
        # if the player is standing still doing nothing, use default image
    #camera.center = player_pos.x'''
         # the above code is for animation, switching between 2 frames to make it look like you're walking
    '''for bullet in bullets:
        bullet.draw(screen)

    for bullet in enemyBullets:
        bullet.draw(screen)'''

    # playerRect = playerImage.get_rect(center = (player_pos))
    # playerRect = playerImage.get_rect().move(player_pos.x, player_pos.y).inflate(-25, -5)
    playerRect = playerImage.get_rect().inflate(playerImage.get_width() / 2, playerImage.get_height() / 2).move(
        player_pos)     # makes the hitbox more representative of the image, maybe change this
    if testing:
        pygame.draw.rect(screen, (0, 255, 0), playerRect)
    screen.blit(playerImage, player_pos)

    #if pygame.Rect.colliderect(deezrect, playerRect):
        #playerHit(player, oryx)
        #The player hitbox is accurate, bullet is not

    pygame.display.flip()



