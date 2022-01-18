import pygame
import pygame_gui
import os
import sys

pygame.init()

HIGHT, WIDTH = 1800, 1000

window_surface = pygame.display.set_mode((HIGHT, WIDTH))
# screen = pygame.Surface((HIGHT, WIDTH))
# screen.fill(pygame.Color('white'))
screen = pygame.image.load('data/background.png')

manager = pygame_gui.UIManager((HIGHT, WIDTH))

new_game_btn = pygame_gui.elements.UIButton(
    # кнопка новой игры
    relative_rect=pygame.Rect((400, 450), (300, 75)),
    text='НАЧАТЬ ИГРУ',
    manager=manager
)

continue_game = pygame_gui.elements.UIButton(
    # кнопка продолжения игры
    relative_rect=pygame.Rect((1100, 450), (300, 75)),
    text='ПРОДОЛЖИТЬ',
    manager=manager
)

settings_btn = pygame_gui.elements.UIButton(
    # кнопка настроек(сейчас только переключает фон)
    relative_rect=pygame.Rect((800, 460), (150, 60)),
    text='настройки',
    manager=manager
)


background = pygame.image.load('data/background.png')

down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (down_cloud.get_width()//1.5, down_cloud.get_height()//1.5))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (right_cloud.get_width()//1.5, right_cloud.get_height()//1.5))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (left_cloud.get_width()//1.5, left_cloud.get_height()//1.5))

sun = pygame.image.load('data/sun.png')
sun = pygame.transform.scale(sun, (sun.get_width()//2, sun.get_height()//2))
sunlight = pygame.image.load('data/sunlights.png')
sunlight = pygame.transform.scale(sunlight, (sunlight.get_width()//2, sunlight.get_height()//2))

text = pygame.image.load('data/mthislnd_text.png')
text = pygame.transform.scale(text, (text.get_width()//2, text.get_height()//2))


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        '''if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == settings_btn:
                    if mode == 'black':
                        mode = 'white'
                    else:
                        mode = 'black'
                    background.fill(pygame.Color(mode))'''
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(screen, (0, 0))
    manager.draw_ui(window_surface)

    # window_surface.blit(background, (0, 600))

    window_surface.blit(down_cloud, (0, 500))
    window_surface.blit(right_cloud, (1280, 10))
    window_surface.blit(left_cloud, (0, 50))

    window_surface.blit(sun, (400, 100))
    window_surface.blit(sunlight, (340, 50))
    window_surface.blit(text, (600, 200))

    pygame.display.update()

pygame.quit()
