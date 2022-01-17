import os
import pygame_gui
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 1250, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('myPicture')


manager = pygame_gui.UIManager((800, 600))

switch = pygame_gui.elements.UIButtn(
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
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
