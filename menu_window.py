import pygame
import start_game
import settings_window

pygame.init()
pygame.mixer.init()

HEIGHT, WIDTH = 1500, 937

window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
screen = pygame.image.load('data/background.png')
screen = pygame.transform.scale(screen, (screen.get_width() // 1.6, screen.get_height() // 1.6))


pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1, 0.0)
music_playing = True

all_btns = pygame.sprite.Group()


class Clouds(pygame.sprite.Group):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('data/cloud1.png')
        self.image2 = pygame.image.load('data/cloud2.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(700, 500))
        self.image2 = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect2 = self.image.get_rect(center=(700, 500))


class StartButtons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_btns)
        self.image = pygame.image.load('data/start_btn.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(700, 500))

    def update(self, clock, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            start_game.start(clock)


class SettingsButtons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_btns)
        self.image = pygame.image.load('data/settings_btn.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(700, 650))

    def update(self, clock, *args):
        global music_playing
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            music_playing = settings_window.open_settings(clock, music_playing)


down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (down_cloud.get_width() // 1.5, down_cloud.get_height() // 1.5))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (right_cloud.get_width() // 1.5, right_cloud.get_height() // 1.5))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (left_cloud.get_width() // 1.5, left_cloud.get_height() // 1.5))

sun = pygame.image.load('data/sun.png')
sun = pygame.transform.scale(sun, (sun.get_width() // 2, sun.get_height() // 2))
sunlight = pygame.image.load('data/sunlights.png')
sunlight = pygame.transform.scale(sunlight, (sunlight.get_width() // 2, sunlight.get_height() // 2))

text = pygame.image.load('data/mthislnd_text.png')
text = pygame.transform.scale(text, (text.get_width() // 2, text.get_height() // 2))

start_btn = StartButtons()
settings_btn = SettingsButtons()


def menu_w(clock: pygame.time.Clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_btns.update(clock, event)
        window_surface.blit(screen, (0, 0))

        window_surface.blit(start_btn.image, start_btn.rect)
        window_surface.blit(settings_btn.image, settings_btn.rect)

        window_surface.blit(sun, (450, 130))
        window_surface.blit(sunlight, (390, 80))
        window_surface.blit(text, (700, 200))

        window_surface.blit(down_cloud, (-10, 500))
        window_surface.blit(right_cloud, (980, 100))
        window_surface.blit(left_cloud, (0, 50))

        pygame.display.update()
