import pygame
import pygame_gui


HEIGHT, WIDTH = 1500, 937
COLOR_ACTIVE = pygame.Color('white')
COLOR_INACTIVE = pygame.Color((30, 30, 30))
FONT = pygame.font.Font(None, 32)

window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
# screen = pygame.Surface((HEIGHT, WIDTH))
# screen.fill(pygame.Color('black'))
screen = pygame.image.load('data/new_fon.png')


manager = pygame_gui.UIManager((HEIGHT, WIDTH))

# text = pygame_gui.

all_sprites = pygame.sprite.Group()


class Continued_game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/continued.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(515, 350))

    def update(self, *args):

        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            import sqlite3

            con = sqlite3.connect("users.db")

            cur = con.cursor()

            users_id = cur.execute("""SELECT * FROM users MAX(id)""")
            result = cur.execute("""SELECT * FROM users WHERE id == """ + str(id) + '"""')

            con.close()


class New_game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.text = None
        self.image = pygame.image.load('data/new_game.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(500, 600))

    def r_text(self, txt):
        self.text = txt

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            import sqlite3

            con = sqlite3.connect("users.db")

            cur = con.cursor()

            delt = """DELETE FROM users"""
            new_profil = cur.execute("""INSERT INTO users.names(""" + self.text + '"""')


cont = Continued_game()
play = New_game()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    New_game.r_text(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def start(clock: pygame.time.Clock):
    running = True

    input_box = InputBox(100, 100, 140, 32)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_box:
                box.handle_event(event)

        for box in input_box:
            box.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        window_surface.blit(screen, (0, 0))
        manager.draw_ui(window_surface)

        screen.blit(cont.image, cont.rect)
        screen.blit(play.image, play.rect)
        for box in input_box:
            box.draw(screen)

        pygame.display.update()
        clock.tick(30)

    return
