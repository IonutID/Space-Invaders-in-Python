import pygame
import os
import random
print(pygame.font.get_fonts())

pygame.init()

FPS = 60
clock = pygame.time.Clock()


WIDTH = 1366
HEIGHT = 768

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

#Assets este preluat de pe internet

#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

#Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
RED_Laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_Laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_Laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_Laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png.")), (WIDTH, HEIGHT))

#Font
MAIN_FONT = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 25, True)
LOST_FONT = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 50, True)
TITLE_FONT = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 70, True)



#Player Variables
level= 1
lives = 3
speed = 10
slow = 0.5
enemies = []
ships_per_level = 5
enemies_speed = 1
lost = False
lost_c = 0
laser_speed = 20


class Ship:
    COOLDOWN = FPS/(level * 2)
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_las(self, spd, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.visibile(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -=10
                self.lasers.remove(laser)


    def get_width(self):
        return self.ship_image.get_width()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif  self.cool_down_counter > 0:
            self.cool_down_counter +=1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_height(self):
        return self.ship_image.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_Laser
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def move_las(self, spd, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(spd)
            if laser.visibile(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red" : (RED_SPACE_SHIP, RED_Laser),
        "green": (GREEN_SPACE_SHIP, GREEN_Laser),
        "blue" : (BLUE_SPACE_SHIP, BLUE_Laser)
    }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_image)
    def move(self, spd):
        self.y += spd
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, spd):
        self.y +=spd

    def visibile(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return  collide(self, obj)

#Objects
player = Player(300, 300)

def collide(a, b):
    offset_x = a.x - b.x
    offset_y = a.y - b.y
    return a.mask.overlap(b.mask, (offset_x, offset_y)) != None

def redraw_window():
    global lost
    global lives
    global level

    WINDOW.blit(BACKGROUND,(0, 0))

    lives_label = MAIN_FONT.render(f"Lives: {lives}", True, pygame.color.Color("white"))
    level_label = MAIN_FONT.render(f"Level: {level}", True, pygame.color.Color("white"))

    WINDOW.blit(level_label, (10, 10))
    WINDOW.blit(lives_label, (WIDTH - level_label.get_width() - 10, 10))

    for enemy in enemies:
        enemy.draw(WINDOW)

    player.draw(WINDOW)

    print(lost)
    if lost:
        lost_label = LOST_FONT.render("Nooob!!!", True, pygame.color.Color("red"))
        WINDOW.blit(lost_label,(WIDTH/2- lost_label.get_width()/2, 400 ))

    pygame.display.update()

def main():
    run = True
    global level
    global lives
    global speed
    global slow
    global enemies
    global ships_per_level
    global enemies_speed
    global lost
    global lost_c

    while run:
        clock.tick(FPS)

        if lives <= 0 or player.health <=0:
            lost = True
            lost_c +=1

        if lost:
            if lost_c > FPS * 2:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level = level + 1
            ships_per_level = ships_per_level + 5
            for i in range(ships_per_level):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w] and player.y > 0:
            if keys_pressed[pygame.K_LSHIFT]:
                player.y-=int(speed * slow)
            else:
                player.y-=speed
            pass
        if keys_pressed[pygame.K_s] and player.y < HEIGHT-player.get_height():
            if keys_pressed[pygame.K_LSHIFT]:
                player.y+=int(speed * slow)
            else:
                player.y+=speed
            pass
        if keys_pressed[pygame.K_a] and player.x > 0:
            if keys_pressed[pygame.K_LSHIFT]:
                player.x-=int(speed * slow)
            else:
                player.x-=speed
            pass
        if keys_pressed[pygame.K_d] and player.x < WIDTH - player.get_width():
            if keys_pressed[pygame.K_LSHIFT]:
                player.x+=int(speed * slow)
            else:
                player.x+=speed
            pass
        if keys_pressed[pygame.K_SPACE]:
            player.shoot()
            pass

        for enemy in enemies[:]:
            enemy.move_las(laser_speed, player)
            enemy.move(enemies_speed)

            if random.randrange(0, 10/level *FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_las(-laser_speed, enemies)
        redraw_window()

def main_menu():
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0,0))
        title_label = TITLE_FONT.render("Press any KEY to begin...", 1, (255,255,255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


main_menu()
