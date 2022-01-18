'''import os
import pygame
import pygame_gui

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 1250, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('myPicture')
mode = 'fon_start.jpg'
background = pygame.Surface((width, height))
background.fill(pygame.Color('white'))  # set.light_mode)  сделать замену на картинку(не работает)


manager = pygame_gui.UIManager((800, 600))

switch = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 300), (150, 100)),
    text='поменять фон',
    manager=manager
)


def load_image(name, color_key=None):
    full_name = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(full_name):
        raise FileNotFoundError(f"Файл с изображением '{full_name}' не найден")
    image = pygame.image.load(full_name)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((1, 1))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image



class Draw_clouds(pygame.sprite.Sprite):
    image = load_image("fon_start.jpg")
    cloud = load_image("cloud_left.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Draw_clouds.image
        self.rect = self.image.get_rect()


all_sprites = pygame.sprite.Group()


for _ in range(50):
    Draw_clouds(all_sprites)


running = True
owl = load_image('fon_start.jpg')
screen.blit(owl, (0, 0, owl.get_width(), owl.get_height()))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == switch:
                    if mode == 'fon_start.jpg':
                        mode = 'white'
                    else:
                        mode = 'fon_start.jpg'
    # all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
'''

import pygame
import pygame_gui
import os

pygame.init()

window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
mode = 'white'  # вместо цвета надо загрузить изображение
background.fill(pygame.Color(mode))

manager = pygame_gui.UIManager((800, 600))

new_game_btn = pygame_gui.elements.UIButton(
    # кнопка новой игры
    relative_rect=pygame.Rect((100, 400), (200, 50)),
    text='НАЧАТЬ ИГРУ',
    manager=manager
)


continue_game = pygame_gui.elements.UIButton(
    # кнопка продолжения игры
    relative_rect=pygame.Rect((500, 400), (200, 50)),
    text='ПРОДОЛЖИТЬ',
    manager=manager
)

settings_btn = pygame_gui.elements.UIButton(
    # кнопка настроек(сейчас только переключает фон)
    relative_rect=pygame.Rect((100, 500), (100, 40)),
    text='настройки',
    manager=manager
)

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
    # all_sprites.draw(screen)
    pygame.display.update()

# pygame.quit()
