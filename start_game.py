import pygame
import sqlite3

HEIGHT, WIDTH = 1500, 937
COLOR_ACTIVE = pygame.Color('white')
COLOR_INACTIVE = pygame.Color((30, 30, 30))

input_text = ''
window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
# screen = pygame.Surface((HEIGHT, WIDTH))
# screen.fill(pygame.Color('black'))

screen = pygame.image.load('data/new_fon.png')
all_sprites = pygame.sprite.Group()


class ContinuedGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/continued.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(750, 350))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            con = sqlite3.connect("data/users.db")
            cur = con.cursor()
            users_id = cur.execute("SELECT * FROM users MAX(id)")
            result = cur.execute("""SELECT *
                                    FROM users
                                    WHERE id = ?""", users_id)
            con.close()


class NewGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/new_game.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(500, 600))

    def update(self, *args):
        global input_text
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            con = sqlite3.connect("data/users.db")
            cur = con.cursor()
            delt = """DELETE FROM users"""
            new_profil = cur.execute("""INSERT INTO users(names) VALUES(?) RETURNING id""", (input_text,)).fetchone()[0]
            con.commit()
            print(new_profil)
            con.close()


cont = ContinuedGame()
play = NewGame()


def start(clock: pygame.time.Clock):
    global input_text
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
                    from_player = font.render(input_text, True, (0, 0, 0))
                    pygame.draw.rect(screen, (255, 255, 255), (750, 575, from_player.get_width() + 45,
                                                               from_player.get_height()))
                    screen.blit(from_player, (750, 575))
                elif event.key == pygame.K_RETURN:
                    play.update()
                else:
                    input_text += event.unicode
                    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
                    from_player = font.render(input_text, True, (0, 0, 0))
                    screen.blit(from_player, (750, 575))
            pygame.display.flip()
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        window_surface.blit(screen, (0, 0))
        screen.blit(cont.image, cont.rect)
        screen.blit(play.image, play.rect)
        pygame.display.update()
        clock.tick(30)
    return
