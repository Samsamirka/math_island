import pygame
import pygame_gui
import os
import sys

HEIGHT, WIDTH = 1500, 937

window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
# screen = pygame.Surface((HEIGHT, WIDTH))
# screen.fill(pygame.Color('black'))
screen = pygame.image.load('data/background.png')
screen = pygame.transform.scale(screen, (screen.get_width()//1.6, screen.get_height()//1.6))

to_return = False
music_playing = True

manager = pygame_gui.UIManager((HEIGHT, WIDTH))

down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (down_cloud.get_width()//1.5, down_cloud.get_height()//1.5))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (right_cloud.get_width()//1.5, right_cloud.get_height()//1.5))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (left_cloud.get_width()//1.5, left_cloud.get_height()//1.5))


set_r = pygame.image.load('data/setn_wn.png')
set_r = pygame.transform.scale(set_r, (set_r.get_width() // 2, set_r.get_height() // 2))
authors = pygame.image.load('data/authors.png')
authors = pygame.transform.scale(authors, (authors.get_width() // 2, authors.get_height() // 2))
name1 = pygame.image.load('data/name_s.png')
name1 = pygame.transform.scale(name1, (name1.get_width() // 2, name1.get_height() // 2))
name2 = pygame.image.load('data/name_l.png')
name2 = pygame.transform.scale(name2, (name2.get_width() // 2, name2.get_height() // 2))
name3 = pygame.image.load('data/name_o.png')
name3 = pygame.transform.scale(name3, (name3.get_width() // 2, name3.get_height() // 2))

set_txt = pygame.image.load('data/settings+txt.png')
set_txt = pygame.transform.scale(set_txt, (set_txt.get_width() // 2, set_txt.get_height() // 2))

mus_txt = pygame.image.load('data/music_txt.png')
mus_txt = pygame.transform.scale(mus_txt, (mus_txt.get_width() // 2, mus_txt.get_height() // 2))

all_sprites = pygame.sprite.Group()


class Push_buttons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/btn_off.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(940, 325))

    def update(self, *args):
        global music_playing
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            music_playing = not music_playing
            if music_playing:
                self.image = pygame.image.load('data/btn_on.png')
            else:
                self.image = pygame.image.load('data/btn_off.png')
            self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))


class Back_buttons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/back_btn.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(1450, 50))

    def update(self, *args):
        global to_return
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            to_return = True


back = Back_buttons()
music = Push_buttons()


def open_settings(clock: pygame.time.Clock, prev_music_playing):
    global music_playing
    music_playing = prev_music_playing
    running = True
    while running:
        for event in pygame.event.get():
            if to_return:
                return music_playing
            all_sprites.update(event)
        window_surface.blit(screen, (0, 0))
        manager.draw_ui(window_surface)

        window_surface.blit(down_cloud, (-10, 500))
        window_surface.blit(right_cloud, (980, 100))
        window_surface.blit(left_cloud, (0, 50))

        window_surface.blit(set_r, (430, 130))
        window_surface.blit(authors, (700, 380))
        window_surface.blit(name1, (650, 460))
        window_surface.blit(name2, (650, 500))
        window_surface.blit(name3, (650, 540))

        window_surface.blit(set_txt, (600, 200))

        window_surface.blit(mus_txt, (600, 320))

        screen.blit(music.image, music.rect)
        screen.blit(back.image, back.rect)

        pygame.display.update()
    return music_playing
