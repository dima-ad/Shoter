import os

import pygame

pygame.init()

SCREEN_WIDTH = 1025
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS1.6")

clock = pygame.time.Clock()

moving_left = False
moving_right = False

background = (50, 168, 60)

def draw_bg():
    screen.fill(background)

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y,  scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.flip = False
        self.speed = speed
        img = pygame.image.load(f'{char_type}/Idle/0.png')

        self.image = pygame.transform.scale(img,
                                            (
                                                int(img.get_width() * scale),
                                                int(img.get_height() * scale)
                                            ))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        animation_type = ['Idle', 'Run', 'Jump']
        for animation in animation_type:
            temp_list = []
            num_of_frames = len(os.listdir(f'{self.char_type}/{animation}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (
                    int(img.get_width() * scale), int(img.get_height() * scale)
                ))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]

    def update(self):
        ANIMATION_COOLDOWN = 100

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_indec >= len(self.animation_list[self.action]):
            self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = - self.speed
            self.flip = True
        if moving_right:
            dx = self.speed
            self.flip = False

        self.rect.x = self.rect.x + dx
        self.rect.y += dy

player = Soldier('player', 200, 200, 3, 7)
enemy = Soldier('player', 400, 200, 3, 5)

run = True

while run:
    draw_bg()
    clock.tick(120)
    player.update_animation()
    enemy.update_animation()
    player.draw()
    enemy.draw()

    if player.alive():
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player.move(moving_left, moving_right)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

pygame.quit()



