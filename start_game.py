import pygame
import pygame_gui

pygame.init()

HEIGHT, WIDTH = 1500, 937

window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
# screen = pygame.Surface((HEIGHT, WIDTH))
# screen.fill(pygame.Color('black'))
screen = pygame.image.load('data/new_fon.png')


manager = pygame_gui.UIManager((HEIGHT, WIDTH))


class Continued_game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/continued.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(515, 350))


class New_game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/new_game.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(500, 600))


cont = Continued_game()
play = New_game()


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

    screen.blit(cont.image, cont.rect)
    screen.blit(play.image, play.rect)

    pygame.display.update()

pygame.quit()
