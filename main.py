import sys
import pygame
from random import randint, choice

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Astronaut runner')
clock = pygame.time.Clock()
font = pygame.font.Font('data/Pixeltype.ttf', 50)
game = False
game_time = 0
score = 0
bg_music = pygame.mixer.Sound('data/music.mp3')
bg_music.play(loops=-1)
player = pygame.sprite.GroupSingle()  # картинка игры
barrier_group = pygame.sprite.Group()
sky = pygame.image.load('data/background.webp').convert()
ground = pygame.image.load('data/ground2.jpg').convert()
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1500)
running = True
player_stand = pygame.image.load('data/player_stand.png').convert_alpha()  # начальный экран
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))
game_name = font.render('Astronaut Runner', False, (0, 0, 0))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = font.render('Press space to run', False, (0, 0, 0,))
game_message_rect = game_message.get_rect(center=(400, 370))

def score_display():  # ваш результат
    time_now = int(pygame.time.get_ticks() / 1000) - game_time
    score_surf = font.render(f'Score: {time_now}', False, (0, 0, 0))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return time_now


def collision():  # коллизия препятствий
    if pygame.sprite.spritecollide(player.sprite, barrier_group, False):
        barrier_group.empty()
        return False
    else:
        return True

class Player(pygame.sprite.Sprite):  # 1 class -------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('data/player_walk_1.png').convert_alpha()  # загрузка картинок и звука
        player_walk_2 = pygame.image.load('data//player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_in = 0
        self.player_jump = pygame.image.load('data/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_in]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('data/jump_sound.mp3')
        self.jump_sound.set_volume(0.4)

    def player(self):  # нажатие на пробел
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def gravity_game(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_position(self):  # позиция
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_in += 0.1
            if self.player_in >= len(self.player_walk):
                self.player_in = 0
            self.image = self.player_walk[int(self.player_in)]

    def update(self):
        self.player()
        self.gravity_game()
        self.player_position()
player.add(Player())  # добавляем его

class Barrier_for_player(pygame.sprite.Sprite):  # 2 class -------------------------------------------------------------
    def __init__(self, type):
        super().__init__()  # картинки препятствий
        if type == 'bat':
            bat_1 = pygame.image.load('data/bat3.png').convert_alpha()
            bat_2 = pygame.image.load('data/bat4.png').convert_alpha()
            self.frame = [bat_1, bat_2]
            y_pos = 210
        elif type == 'cactus':
            cactus_1 = pygame.image.load('data/cactus.png').convert_alpha()
            cactus_2 = pygame.image.load('data/cactus.png').convert_alpha()
            self.frame = [cactus_1, cactus_2]
            y_pos = 300
        elif type == 'antlion':
            antlion_1 = pygame.image.load('data/antlion.png').convert_alpha()
            antlion_2 = pygame.image.load('data/antlion2.png').convert_alpha()
            self.frame = [antlion_1, antlion_2]
            y_pos = 300
        else:
            skorpion_1 = pygame.image.load('data/image.png').convert_alpha()
            skorpion_2 = pygame.image.load('data/image2.png').convert_alpha()
            self.frame = [skorpion_1, skorpion_2]
            y_pos = 300
        self.animation = 0
        self.image = self.frame[self.animation]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def barrier_animation(self):
        self.animation += 0.1
        if self.animation >= len(self.frame):
            self.animation = 0
        self.image = self.frame[int(self.animation)]

    def game_end(self):
        if self.rect.x <= -200:
            self.kill()

    def update(self):
        self.barrier_animation()
        self.rect.x -= 5  # speed
        self.game_end()
        if score >= 10:
            self.rect.x -= 1
        if score >= 20:
            self.rect.x -= 2
        if score >= 30:
            self.rect.x -= 3
        if score >= 40:
            self.rect.x -= 4
        if score >= 50:
            self.rect.x -= 5
        if score >= 60:
            self.rect.x -= 6

while running:   # game_cycle ------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game:
            if event.type == timer:    # добавляем картинки препятствий
                barrier_group.add(Barrier_for_player(choice(['antlion', 'cactus', 'bat', 'skorpion', 'skorpion', 'bat',
                                                    'cactus', 'antlion'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # нажатие на пробел
                game = True
                game_time = int(pygame.time.get_ticks() / 1000)
    if game:  # запуск самой игры
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        score = score_display()
        player.draw(screen)
        player.update()
        barrier_group.draw(screen)
        barrier_group.update()
        game = collision()
    else:   # конечный экран
        screen.fill((0, 255, 0))
        screen.blit(player_stand, player_stand_rect)
        score_message = font.render(f'Your score: {score}', False, (0, 0, 0))
        score_message_rect = score_message.get_rect(center=(400, 370))
        screen.blit(game_name, game_name_rect)  # оценка вашего результата
        if 0 < score <= 2:
            score_message2 = font.render(f'Try again:(', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 2 < score <= 10:
            score_message2 = font.render(f'So-so', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 10 < score <= 20:
            score_message2 = font.render(f'Good', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 20 < score <= 30:
            score_message2 = font.render(f'GG', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 30 < score <= 40:
            score_message2 = font.render(f'Well done', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 40 < score <= 50:
            score_message2 = font.render(f'Мaster', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if 40 < score <= 10000:
            score_message2 = font.render(f'o_o', False, (0, 0, 0))
            score_message_rect2 = score_message2.get_rect(center=(400, 340))
            screen.blit(score_message2, score_message_rect2)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)
pygame.quit()