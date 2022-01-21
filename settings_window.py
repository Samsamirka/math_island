import pygame
import pygame_gui
import os
import sys

pygame.init()

HEIGHT, WIDTH = 1500, 937

window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
# screen = pygame.Surface((HEIGHT, WIDTH))
# screen.fill(pygame.Color('black'))
screen = pygame.image.load('data/background.png')
screen = pygame.transform.scale(screen, (screen.get_width()//1.6, screen.get_height()//1.6))


manager = pygame_gui.UIManager((HEIGHT, WIDTH))

down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (down_cloud.get_width()//1.5, down_cloud.get_height()//1.5))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (right_cloud.get_width()//1.5, right_cloud.get_height()//1.5))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (left_cloud.get_width()//1.5, left_cloud.get_height()//1.5))


set_r = pygame.image.load('data/set_wn.png')
set_r = pygame.transform.scale(set_r, (set_r.get_width() // 2, set_r.get_height() // 2))
authors = pygame.image.load('data/autors.png')
authors = pygame.transform.scale(authors, (authors.get_width() // 2, authors.get_height() // 2))
name1 = pygame.image.load('data/name_s.png')
name1 = pygame.transform.scale(name1, (name1.get_width() // 2, name1.get_height() // 2))
name2 = pygame.image.load('data/name_l.png')
name2 = pygame.transform.scale(name2, (name2.get_width() // 2, name2.get_height() // 2))
name3 = pygame.image.load('data/name_o.png')
name3 = pygame.transform.scale(name3, (name3.get_width() // 2, name3.get_height() // 2))

set_txt = pygame.image.load('data/set_txt.png')
set_txt = pygame.transform.scale(set_txt, (set_txt.get_width() // 2, set_txt.get_height() // 2))
mus_txt = pygame.image.load('data/mus_txt.png')
mus_txt = pygame.transform.scale(mus_txt, (mus_txt.get_width() // 2, mus_txt.get_height() // 2))

off_m = pygame.image.load('data/mus_off.png')
off_m = pygame.transform.scale(off_m, (off_m.get_width() // 2, off_m.get_height() // 2))
on_m = pygame.image.load('data/mus_on.png')
on_m = pygame.transform.scale(on_m, (on_m.get_width() // 2, on_m.get_height() // 2))


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)
    manager.update(time_delta)
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

    window_surface.blit(off_m, (770, 305))
    window_surface.blit(on_m, (890, 305))

    pygame.display.update()

pygame.quit()
