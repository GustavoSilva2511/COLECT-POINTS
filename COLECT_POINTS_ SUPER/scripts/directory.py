from libraries import os, pygame
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

main_directory = os.path.dirname(__file__)
sprite_player = os.path.join(main_directory, "../Sprites/player.png")
sprite_enemy = os.path.join(main_directory, "../Sprites/enemy.png")
sprite_enemy2 = os.path.join(main_directory, "../Sprites/enemy2.png")
sprite_bullet = os.path.join(main_directory, "../sprites/bullet.png")
sprite_explosion = os.path.join(main_directory, "../sprites/explosion.png")

music = os.path.join(main_directory, "../sounds/music_game.mp3")
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

sound_nav_directory = os.path.join(main_directory, "../sounds/sound_nav.wav")
sound_explosion_directory = os.path.join(main_directory, "../sounds/explosion.wav")
explosion = pygame.mixer.Sound(sound_explosion_directory)

sound_shot_directory = os.path.join(main_directory, "../sounds/shot.wav")
shot = pygame.mixer.Sound(sound_shot_directory)
shot.set_volume(0.5)

points = 0

font = pygame.font.SysFont("arial", 50)
font_render = font.render(f"pontos: {points}", False, white)
