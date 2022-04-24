from libraries import exit, randint
from directory import *
pygame.init()

width, heigth = 1260, 720
enemys = 1


screen = pygame.display.set_mode((width, heigth), pygame.FULLSCREEN)
pygame.display.set_caption("COLECT POINTS SUPER")


class Star:
    def __init__(self):
        self.mult_vel = 1
        self.var = randint(0, 10)
        self.cont = 0
        self.depth = randint(10, 24)
        self.x = randint(-10, 1260)
        self.y = randint(-10, 764)
        self.var_tp = 10
        self.tp = (self.depth * int(self.var_tp))

    def update(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.mult_vel += 0.05

        else:
            if self.mult_vel > 1:
                self.mult_vel -= 0.01
            else:
                pass

        self.y += ((self.depth / 2) * self.mult_vel)

        if self.y > heigth:
            self.y = randint(-50, -5)
            self.x = randint(-10, 1260)

        if self.cont <= 5:
            self.var_tp -= (self.var / 10)

        if self.cont > 5:
            self.var_tp += (self.var / 10)

        if self.cont == 10:
            self.cont = 0

        self.cont += 1

        self.tp = (self.depth * int(self.var_tp))
        pygame.draw.rect(screen, (self.tp, self.tp, self.tp), ((self.x, self.y), (2, 2)))


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_idle = []
        self.size = 5 * 32
        self.x = player.x
        self.y = player.y

        self.cont = 0

        for i in range(3):
            img = pygame.image.load(sprite_bullet)
            img = img.subsurface((i * 32, 0), (32, 32))
            '''img = pygame.transform.scale(img, (self.size, self.size))'''
            self.bullet_idle.append(img)

        self.image = self.bullet_idle[self.cont]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.center = self.x, self.y

    def update(self):
        self.cont += 0.25
        self.image = self.bullet_idle[int(self.cont % len(self.bullet_idle))]
        self.y -= 50

        self.rect.center = self.x, self.y

        if self.y <= -10:
            all_sprites_bullet.remove(self)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_idle = []
        self.explosion = []
        self.x = randint(0, width)
        self.y = randint(-100, 0)
        self.size = 3 * 32
        self.cont = 0
        self.velocity = randint(1, 3)
        self.distroied = False

        for i in range(8):
            if i < 4:
                img = pygame.image.load(sprite_enemy).convert_alpha()
                img = img.subsurface((i * 32, 0), (32, 32))
                img = pygame.transform.scale(img, (self.size, self.size))
                self.enemy_idle.append(img)

            img = pygame.image.load(sprite_explosion).convert_alpha()
            img = img.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (self.size, self.size))
            self.explosion.append(img)

        self.image = self.enemy_idle[self.cont]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.x, self.y

    def distroy(self):
        self.distroied = True

    def update(self):
        if not self.distroied:
            self.y += self.velocity
            self.rect.center = self.x, self.y

            if self.x > player.x:
                self.x -= self.velocity
                self.rect.center = self.x, self.y

            if self.x < player.x:
                self.x += self.velocity
                self.rect.center = self.x, self.y

            self.cont += 0.25

            self.image = self.enemy_idle[int(self.cont % len(self.enemy_idle))]

        else:
            self.cont += 0.25
            self.image = self.explosion[int(self.cont % len(self.explosion))]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_idle = []
        self.player_moving = []
        self.x = 500
        self.y = 500
        self.size = 5 * 32
        self.cont = 0
        self.set_volume = 0.2
        self.sound_nav = pygame.mixer.Sound(sound_nav_directory)
        self.sound_nav.set_volume(self.set_volume)
        self.sound_nav.play(-1)
        self.velocity = 10

        for i in range(4):
            img = pygame.image.load(sprite_player).convert_alpha()
            img = img.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (self.size, self.size))
            self.player_idle.append(img)

        for i in range(4, 6):
            img = pygame.image.load(sprite_player).convert_alpha()
            img = img.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (self.size, self.size))
            self.player_moving.append(img)

        self.image = self.player_idle[int(self.cont)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.x, self.y

        self.right = self.up = self.down = self.left = False
        self.idle = self.gravity = True

    def walk_left(self):
        self.left = True
        self.right = self.up = self.down = self.idle = False

    def walk_right(self):
        self.right = True
        self.up = self.down = self.left = self.idle = False

    def walk_up(self):
        self.up = True
        self.right = self.down = self.left = self.idle = False

    def walk_down(self):
        self.down = True
        self.right = self.up = self.left = self.idle = False

    def stopped(self):
        self.idle = True
        self.right = self.up = self.down = self.left = False

    def update(self):
        if self.x <= 64:
            self.x += 8

        if self.x >= (width-64):
            self.x -= 8

        if self.y >= (heigth-80):
            self.y = (heigth-80)

        if self.y <= 64:
            self.y += 8

        if self.gravity:
            self.y += 3
            self.rect.center = self.x, self.y

        if self.idle:
            self.cont += 0.25
            self.image = self.player_idle[int(self.cont % len(self.player_idle))]
            self.set_volume = 0.2
            self.sound_nav.set_volume(self.set_volume)

        if self.left:
            self.cont += 0.20
            self.image = self.player_moving[int(self.cont % len(self.player_moving))]

            self.x -= self.velocity

            self.rect.center = self.x, self.y

            self.idle, self.left = True, False

            self.set_volume = 0.5
            self.sound_nav.set_volume(self.set_volume)

        if self.right:
            self.cont += 0.20
            self.image = self.player_moving[int(self.cont % len(self.player_moving))]
            self.image = pygame.transform.flip(self.image, True, False)

            self.x += self.velocity

            self.rect.center = self.x, self.y

            self.idle, self.right = True, False

            self.set_volume = 0.5
            self.sound_nav.set_volume(self.set_volume)

        if self.up:
            self.cont += 0.20
            self.image = self.player_idle[int(self.cont % len(self.player_idle))]

            self.y -= self.velocity

            self.rect.center = self.x, self.y

            self.idle, self.up = True, False

            self.set_volume = 0.7
            self.sound_nav.set_volume(self.set_volume)

        if self.down:
            self.cont += 0.20
            self.image = self.player_idle[int(self.cont % len(self.player_idle))]

            self.y += self.velocity

            self.rect.center = self.x, self.y

            self.idle, self.down = True, False

            self.set_volume = 0.1
            self.sound_nav.set_volume(self.set_volume)


player = Player()
all_sprites_player = pygame.sprite.Group()

all_sprites_player.add(player)
all_sprites_bullet = pygame.sprite.Group()
all_sprites_enemys = pygame.sprite.Group()

all_sky = []
for i in range(300):
    all_sky.append(Star())

frame = pygame.time.Clock()


class Mission1:
    while True:
        frame.tick(30)
        screen.fill(black)
        font_render = font.render(f"pontos: {points}", False, white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet()
                    all_sprites_bullet.add(bullet)
                    shot.play()

        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            player.left = True
        else:
            player.left = False

        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.right = True
        else:
            player.right = False

        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            player.up = True
        else:
            player.down = False

        if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            player.down = True
        else:
            player.down = False

        for i in range(int(enemys)):
            if len(all_sprites_enemys) < int(enemys):
                enemy = Enemy()
                all_sprites_enemys.add(enemy)

        if pygame.sprite.groupcollide(all_sprites_bullet, all_sprites_enemys, True, True):
            points += 10

            enemys += 0.2
            explosion.play()

        if pygame.sprite.groupcollide(all_sprites_enemys, all_sprites_player, True, False):
            pass

        all_sprites_bullet.draw(screen)
        all_sprites_player.draw(screen)
        all_sprites_enemys.draw(screen)

        for i in all_sky:
            i.update()

        all_sprites_player.update()
        all_sprites_bullet.update()
        all_sprites_enemys.update()

        screen.blit(font_render, (width - 300, 10))

        pygame.display.flip()



