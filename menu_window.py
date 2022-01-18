import pygame
import pygame_gui
import os
import sys

pygame.init()

window_surface = pygame.display.set_mode((1250, 800))

background = pygame.Surface((1250, 800))
mode = 'white'  # вместо цвета надо загрузить изображение
background.fill(pygame.Color(mode))

manager = pygame_gui.UIManager((1250, 800))

new_game_btn = pygame_gui.elements.UIButton(
    # кнопка новой игры
    relative_rect=pygame.Rect((100, 400), (300, 75)),
    text='НАЧАТЬ ИГРУ',
    manager=manager
)

continue_game = pygame_gui.elements.UIButton(
    # кнопка продолжения игры
    relative_rect=pygame.Rect((820, 400), (300, 75)),
    text='ПРОДОЛЖИТЬ',
    manager=manager
)

settings_btn = pygame_gui.elements.UIButton(
    # кнопка настроек(сейчас только переключает фон)
    relative_rect=pygame.Rect((525, 410), (150, 60)),
    text='настройки',
    manager=manager
)


down_cloud = pygame.image.load('data/clouds_down.jpg')
right_cloud = pygame.image.load('data/cloud_right.jpg')
left_cloud = pygame.image.load('data/cloud_left.jpg')


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == settings_btn:
                    if mode == 'black':
                        mode = 'white'
                    else:
                        mode = 'black'
                    background.fill(pygame.Color(mode))
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    window_surface.blit(down_cloud, (0, 360))
    # window_surface.blit(right_cloud, (0, 360))
    # window_surface.blit(left_cloud, (0, 100))

    pygame.display.update()

pygame.quit()
