import pygame
import sys
import os
import random
import sqlite3

pygame.init()


FPS = 50
SIZE = WIDTH, HEIGHT = 1000, 625
BACKGROUND = pygame.color.Color('lightskyblue')
input_text = ''
all_condition = ''
number = 0
money = 0
level = 0
tasks = []
next = []
task_start = False
task_made = False
running_island = False
running_condition = False

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

island_sprites = pygame.sprite.Group()
control_sprite = pygame.sprite.Group()
next_sprite = pygame.sprite.Group()
leave_sprite = pygame.sprite.Group()
condition_sprite = pygame.sprite.Group()
back_to_task_sprite = pygame.sprite.Group()


def render_text_task(text, number=None):  # number - номер аздания для его печати в диалоговом окне
    """возвращает text в виде картинки на фоне города с дождем"""
    global backgrnd
    y = 0
    string = ''
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
    if number is not None:
        num_task = font.render(str(number), True, (0, 0, 0))
    else:
        num_task = number
    backgrnd = pygame.transform.scale(load_image('фон_для_задания.jpeg'), SIZE)
    backgrnd.blit(num_task, (WIDTH // 3.57, HEIGHT // 1.72))
    font = pygame.font.Font('data/узкий.ttf', 23)
    text = text[2:-3]
    text = text.split()
    for word in text:
        string += word
        string += ' '
        text_task = font.render(str(string), True, (0, 0, 0))
        if text_task.get_size()[0] > WIDTH // 1.25:
            string = string[:-(len(word) + 1)]
            text_task = font.render(str(string), True, (0, 0, 0))
            backgrnd.blit(text_task, (WIDTH // 15, HEIGHT // 1.43 + y))
            y += 20
            string = word + " "
        elif text_task.get_size()[0] == WIDTH // 1.25:
            backgrnd.blit(text_task, (WIDTH // 15, HEIGHT // 1.43 + y))
            y += 20
            string = ''
        elif text_task.get_size()[0] < WIDTH // 1.25 and text.index(word) == len(text) - 1:
            backgrnd.blit(text_task, (WIDTH // 15, HEIGHT // 1.43 + y))
    next_sprite.draw(backgrnd)
    next_sprite.clear(screen, screen)
    condition_sprite.draw(backgrnd)
    condition_sprite.clear(screen, screen)
    return backgrnd


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


TASKS_IMAGES = {
    1: load_image('1.png'),
    2: load_image('2.png'),
    3: load_image('3.png'),
    4: load_image('4.png'),
    5: load_image('5.png')
}
PLAYER_IMAGES = {
    'money': load_image('Мешок денег.png'),
    'title_island': load_image('Название острова.png')
}
running_island = False


def island_screen():
    global running_island, running, running_start
    global window_surface, screen
    running_island = True
    con = sqlite3.connect("data/users.db")
    cur = con.cursor()
    background = pygame.transform.scale(load_image('Остров.png'), SIZE)
    screen.fill(BACKGROUND)
    screen.blit(background, (WIDTH // 150, HEIGHT // 93.7))
    nick_name = cur.execute("""SELECT name FROM users ORDER BY id DESC LIMIT 1""").fetchone()[0]
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    nickname = font.render(str(nick_name), True, (50, 50, 50))
    screen.blit(nickname, (WIDTH // 150, HEIGHT // 7.8))
    island_title = pygame.transform.scale(PLAYER_IMAGES['title_island'], (WIDTH // 5, HEIGHT // 8.76))
    screen.blit(island_title, (0, 0))
    money_bag = pygame.transform.scale(PLAYER_IMAGES['money'], (WIDTH // 25, HEIGHT // 11.86))
    screen.blit(money_bag, (WIDTH // 1.2, HEIGHT // 11.57))
    lvl = pygame.transform.scale(load_image('LVL.png'), (WIDTH // 25, HEIGHT // 31.23))
    screen.blit(lvl, (WIDTH // 1.2, HEIGHT // 44.6))
    load_island_sprites()
    island_sprites.draw(screen)
    control_sprite.draw(screen)
    leave_sprite.draw(screen)
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    money_player = font.render(str(money), True, (255, 255, 255))
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    experience_player = font.render(str(level), True, (255, 255, 255))
    screen.blit(money_player, (WIDTH // 1.13, HEIGHT // 8.6))
    screen.blit(experience_player, (WIDTH // 1.13, HEIGHT // 62.47))
    con.close()
    global input_text, task_start
    while running_island:
        for event in pygame.event.get():
            island.get_event(event)
            if event.type == pygame.QUIT:
                running_island = running = running_start = False
            if event.type == pygame.KEYDOWN:
                if task_start:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        font = pygame.font.Font('data/узкий.ttf', 23)
                        from_player = font.render(input_text, True, (0, 100, 0))
                        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 15, HEIGHT // 1.1,
                                         from_player.get_width() + 23, from_player.get_height()))
                        screen.blit(from_player, (WIDTH // 15, HEIGHT // 1.1))
                    elif event.key == pygame.K_RETURN:
                        if input_text == '':
                            island.set_answer(0)
                        else:
                            input_text = float(input_text.replace(',', '.'))
                            island.set_answer(input_text)
                        input_text = ''
                    else:
                        try:
                            if event.unicode.isdigit() or event.unicode == '.':
                                input_text += event.unicode
                                font = pygame.font.Font('data/узкий.ttf', 23)
                                from_player = font.render(input_text, True, (0, 100, 0))
                                screen.blit(from_player, (WIDTH // 15, HEIGHT // 1.1))
                        except:
                            raise TypeError('Вводить можно только числа.')
            window_surface.blit(screen, (0, 0))
        pygame.display.flip()

        clock.tick(FPS)


class IslandImage(pygame.sprite.Sprite):
    def __init__(self, task_id, coordinates):
        super().__init__(island_sprites)
        self.task_id = task_id
        self.image = pygame.transform.scale(TASKS_IMAGES[task_id], (WIDTH // 25, HEIGHT // 14.64))
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        global tasks
        tasks.append(self)


ISLAND_COORDINATES = {
    1: (WIDTH // 5.7, HEIGHT // 3.67),
    2: (WIDTH // 2.56, HEIGHT // 2.4),
    3: (WIDTH // 1.875, HEIGHT // 2.64),
    4: (WIDTH // 1.76, HEIGHT // 1.62),
    5: (WIDTH // 2.24, HEIGHT // 1.67)
}


def load_island_sprites():
    for task_id, coordinates in ISLAND_COORDINATES.items():
        IslandImage(task_id, coordinates)
    leave_button = pygame.sprite.Sprite()
    leave_button.image = pygame.transform.scale(load_image('Кнопка выхода.png'), (WIDTH // 7.14, HEIGHT // 17.68))
    leave_button.rect = leave_button.image.get_rect()
    leave_button.rect.x = WIDTH // 1.17
    leave_button.rect.y = HEIGHT // 1.07
    leave_sprite.add(leave_button)


NAMES_BOYS = ['Саша', 'Максим', 'Кирилл', 'Андрей', 'Ваня', 'Петя', 'Коля', 'Боря', 'Серёжа']
NAMES_GIRLS = ['Лиза', 'Оля', 'Самира', 'Катя', 'Маша', 'Юля', 'Аня', 'Лера', 'Вика', 'Настя']
NAMES_BOYS_EDIT = ['Саши', 'Максима', 'Кирилла', 'Андрея', 'Вани', 'Пети', 'Коли', 'Бори', 'Серёжи']
NAMES_GIRLS_EDIT = ['Лизы', 'Оли', 'Самиры', 'Кати', 'Маши', 'Юли', 'Ани', 'Леры', 'Вики', 'Насти']


class Island:
    def __init__(self):
        global next
        global next_sprite, condition_sprite, back_to_task_sprite
        self.input_answer = input_text
        self.task = None
        self.number = 0
        self.won = False  # введеный ответ == правильному
        self.next_button = pygame.sprite.Sprite()
        self.next_button.image = load_image('Стрелка.png')
        self.next_button.image = pygame.transform.scale(self.next_button.image, (WIDTH // 21.4, HEIGHT // 13.39))
        self.next_button.rect = self.next_button.image.get_rect()
        self.next_button.rect.x = WIDTH // 1.23
        self.next_button.rect.y = HEIGHT // 1.13
        next_sprite.add(self.next_button)
        next = [self.next_button]
        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
        self.open_condition_button = pygame.sprite.Sprite()
        self.open_condition_button.image = font.render('+', True, 'royalblue')
        self.open_condition_button.rect = self.open_condition_button.image.get_rect()
        self.open_condition_button.rect.x = WIDTH // 1.3
        self.open_condition_button.rect.y = HEIGHT // 1.14
        condition_sprite.add(self.open_condition_button)
        self.return_button = pygame.sprite.Sprite()
        self.return_button.image = load_image('белая_стрелка.png')
        self.return_button.image = pygame.transform.scale(self.return_button.image, (WIDTH // 21.4, HEIGHT // 13.39))
        self.return_button.rect = self.return_button.image.get_rect()
        self.return_button.rect.x = WIDTH // 1.07
        self.return_button.rect.y = HEIGHT // 23.425
        back_to_task_sprite.add(self.return_button)

    def open_condition(self, text):
        global task_start, for_condition, running_condition
        while running_condition:
            task_start = False
            for_condition = pygame.transform.scale(load_image('Библиотека.jpg'), SIZE)
            background_theory = pygame.transform.scale(load_image("подложка_теория.png"),
                                                       (WIDTH // 1.55, HEIGHT // 1.04))
            num_1 = pygame.transform.scale(load_image('рис_1.png'), (WIDTH // 3, HEIGHT // 3.003))
            num_2 = load_image('рис_2.png', -1)
            num_3 = load_image('рис_3.png', -1)
            for_condition.blit(background_theory, (WIDTH // 31.25, HEIGHT // 37.48))
            for_condition.blit(num_1, (WIDTH // 16.7, HEIGHT // 1.7))
            for_condition.blit(pygame.transform.scale(num_2, (WIDTH // 6, HEIGHT // 3.37)),
                               (WIDTH // 2.2, HEIGHT // 1.6))
            for_condition.blit(pygame.transform.scale(num_3, (WIDTH // 6, HEIGHT // 7.5)),
                               (WIDTH // 3.3, HEIGHT // 1.874))
            *other, characters = os.walk('data/characters')
            character = 'characters/' + str(random.choice(characters[2]))
            for_condition.blit(pygame.transform.scale(load_image(character), (WIDTH // 3, HEIGHT // 1.008)),
                               (WIDTH // 1.5, HEIGHT // 93.7))
            font = pygame.font.Font('data/узкий.ttf', 20)
            text = text[2:-3]
            text = text.split()
            string = ''
            y = 0
            for word in text:
                string += word
                string += ' '
                text_task = font.render(str(string), True, (0, 0, 0))
                if text_task.get_size()[0] > WIDTH // 1.67:
                    string = string[:-(len(word) + 1)]
                    text_task = font.render(str(string), True, (0, 0, 0))
                    for_condition.blit(text_task, (WIDTH // 16.67, HEIGHT // 18.74 + y))
                    y += 25
                    string = word + ' '
                elif text_task.get_size()[0] == WIDTH // 1.67:
                    for_condition.blit(text_task, (WIDTH // 16.67, HEIGHT // 18.74 + y))
                    y += 25
                    string = ''
                elif text_task.get_size()[0] < WIDTH // 1.67 and text.index(word) <= len(text) - 3:
                    for_condition.blit(text_task, (WIDTH // 16.67, HEIGHT // 18.74 + y))
            back_to_task_sprite.draw(for_condition)
            return for_condition

    def set_answer(self, answer):
        self.input_answer = answer
        try:
            self.input_answer = str(float(self.input_answer))
        except ValueError:
            raise ValueError('Вводить нужно числа/вместо запятой ставится точка')
        self.get_result()

    def exercise_open(self, number, text_task):
        self.number = number
        self.task = text_task
        screen.blit(render_text_task(self.task, self.number), (0, 0))

    def get_result(self):
        """ответ от системы(верный/неверный ответ)"""
        global money, level
        global backgrnd
        global task_made
        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 27)
        self.won = self.result.check_answer(self.input_answer)
        if self.won and not task_made:  # task_made - проверка на выполненность задания,
            # чтобы не получать бесконечное количество награды
            # должен переключаться до нажатия энтер
            screen.blit(backgrnd, (0, 0))
            money += 10
            level += 1
            final = 'Всё верно! Получи 10 монет :)'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (WIDTH // 150, HEIGHT // 93.7))
            task_made = True
        elif not self.won and not task_made:
            if money >= 10:
                money -= 10
            screen.blit(backgrnd, (0, 0))
            final = 'К сожалению, неверно. Попробуй ещё разок! Ты теряешь 10 монет ;('
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (WIDTH // 150, HEIGHT // 93.7))
            task_made = True
        elif self.won and task_made:
            screen.blit(backgrnd, (0, 0))
            final = 'Всё верно!'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (WIDTH // 150, HEIGHT // 93.7))
        elif not self.won and task_made:
            screen.blit(backgrnd, (0, 0))
            final = 'К сожалению, неверно. Попробуй ещё разок!'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (WIDTH // 150, HEIGHT // 93.7))

    def get_event(self, *args):
        global task_made, running_island, running, running_start, task_start, condition_sprite
        global money, level, input_text, nick_name, running_condition, back_to_task_sprite, all_condition
        for button in tasks:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(args[0].pos):
                task_start = True
                self.result = Task(button.task_id)  # task_id должен быть записан при создании спрайта
        for arrow in next:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and arrow.rect.collidepoint(args[0].pos):
                task_start = False
                task_made = False
                input_text = ''
                island_screen()
        for leave_btn in leave_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and leave_btn.rect.collidepoint(args[0].pos):
                con = sqlite3.connect("data/users.db")
                cur = con.cursor()
                nick_name = cur.execute("""SELECT name FROM users ORDER BY id DESC LIMIT 1""").fetchone()[0]
                cur.execute("""INSERT INTO users(money, lvl, name) VALUES(?, ?, ?)""", (money, level, nick_name,))
                con.commit()
                con.close()
                running_island = running = running_start = False
        for condition_button in condition_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and condition_button.rect.collidepoint(args[0].pos):
                running_condition = True
                screen.blit(self.open_condition(all_condition), (0, 0))
        for back_button in back_to_task_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and back_button.rect.collidepoint(args[0].pos):
                running_condition = False
                task_start = True
                screen.blit(render_text_task(self.task, self.number), (0, 0))

    def generate_task_1(self, text):
        umbrella = random.randint(19, 30)
        handle = round(random.uniform(4, 10), 1)
        answer_1 = round((3 * (umbrella - handle)), 1)
        return text.format(umbrella=umbrella, handle=handle), answer_1

    def generate_task_2(self, text, ends, boy):
        h_2 = round(random.uniform(50, 70), 1)
        s = (1 / 2) * ends * h_2
        answer_2 = round((s * 2))
        return text.format(name=boy, h=h_2), answer_2

    def generate_task_3(self, text, r, boy):
        answer = (r ** 2 + (r * 2) ** 2) / (r * 2)
        return text.format(name=boy, r=r), answer

    def generate_task_4(self, text, h, d, girl, girl_edit):
        answer = round(2 * 3.14 * h * (d / 2))
        return text.format(girl=girl, girl_edit=girl_edit), answer

    def generate_task_5(self, text, num, a, b, S, girl_edit, boy_edit):
        all_wedges = 12 * num  # тк 12 клиньев на одном зонте
        wedges = (all_wedges * S) / 10000  # клинья
        roll = a * b * 0.01  # рулон
        rest = round((roll - wedges), 2)  # обрезки
        answer = round(((rest / roll) * 100), 2)
        return text.format(a=a, b=b, num=num, S=S, girl=girl_edit, boy=boy_edit), answer

    def generate_task(self, id, **args):
        global answer, number, all_condition
        con = sqlite3.connect('data/text_of_task_and_exercises.db')
        cur = con.cursor()
        text = str(cur.execute("SELECT text FROM task_exercises WHERE id = ?", (id,)).fetchone())
        all_condition = str(cur.execute("SELECT text FROM task_exercises WHERE id = 6").fetchone())

        if 'ends' not in args:
            args['ends'] = random.randint(25, 33)  # расстояние между спицами
        if 'h' not in args:
            args['h'] = random.randint(24, 38)  # высота купола
        if 'd' not in args:
            args['d'] = random.randint(90, 120)  # расстояние между концами спиц
        if 'h_2' not in args:
            args['h_2'] = round(random.uniform(50, 70), 1)
        if 'r' not in args:
            args['r'] = random.randint(25, 40)
        if 'a' not in args:
            args['a'] = random.randint(30, 51)  # длина
            args['b'] = random.randint(70, 151)  # ширина
            args['S'] = random.randint(600, 1301)
            while args['a'] % 10 != 0 or args['b'] % 10 != 0 or args['S'] % 50 != 0:
                args['a'] = random.randint(30, 51)  # длина
                args['b'] = random.randint(70, 151)  # ширина
                args['S'] = random.randint(600, 1301)
        if 'num' not in args:
            args['num'] = random.randint(15, 31)  # количество зонтов

        boy = random.choice(NAMES_BOYS)
        girl = random.choice(NAMES_GIRLS)
        boy_edit = NAMES_BOYS_EDIT[NAMES_BOYS.index(boy)]
        girl_edit = NAMES_GIRLS_EDIT[NAMES_GIRLS.index(girl)]

        all_condition = all_condition.format(girl=girl, boy=boy, d=args['d'], h=args['h'], ends=args['ends'])

        if id == 1:
            text, answer = self.generate_task_1(text)
        elif id == 2:
            text, answer = self.generate_task_2(text, args['ends'], boy)
        elif id == 3:
            text, answer = self.generate_task_3(text, args['r'], boy)
        elif id == 4:
            text, answer = self.generate_task_4(text, args['h'], args['d'], girl, girl_edit)
        elif id == 5:
            text, answer = self.generate_task_5(text, args['num'], args['a'], args['b'], args['S'], girl_edit, boy_edit)
        island.exercise_open(id, text)
        number = id
        return text, answer


class Task:
    def __init__(self, number=None):  # number - номер задания, который получаем из exercise_номер_open()
        self.text, self.true_answer = island.generate_task(number)

    def check_answer(self, answer):  # answer = TEXT, возвращает True/False
        return float(answer) == self.true_answer


backgrnd = pygame.transform.scale(load_image('фон_для_задания.jpeg'), SIZE)
island = Island()

COLOR_ACTIVE = pygame.Color('white')
COLOR_INACTIVE = pygame.Color((30, 30, 30))

input_text = ''
window_surface = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()


class ContinuedGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/continued.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 5.95, HEIGHT // 31.2))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2.7))

    def update(self, *args):
        global nick_name, money, level
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            con = sqlite3.connect("data/users.db")
            cur = con.cursor()
            nick_name, money, level = cur.execute("""SELECT name, money, lvl
                                                        FROM users
                                                        ORDER BY id DESC
                                                        LIMIT 1""").fetchone()
            con.close()
            island_screen()


class NewGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/new_game.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 6.9, HEIGHT // 31.2))
        self.rect = self.image.get_rect(center=(WIDTH // 2.7, HEIGHT // 1.56))

    def update(self, *args):
        global input_text, running_start
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            con = sqlite3.connect("data/users.db")
            cur = con.cursor()
            cur.execute("""INSERT INTO users(name) VALUES(?)""", (input_text,))
            input_text = ''
            con.commit()
            con.close()
            running_start = False
            island_screen()


cont = ContinuedGame()
play = NewGame()
running_start = False


def start(clock: pygame.time.Clock, screen):
    global input_text, running_start
    running_start = True
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 1.63, WIDTH // 5.2, HEIGHT // 18))
    while running_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 27)
                    from_player = font.render(input_text, True, (0, 0, 0))
                    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 1.63, from_player.get_width() + 45,
                                     from_player.get_height()))
                    screen.blit(from_player, (WIDTH // 2, HEIGHT // 1.63))
                if event.key == pygame.K_RETURN:
                    con = sqlite3.connect("data/users.db")
                    cur = con.cursor()
                    cur.execute("""INSERT INTO users(name) VALUES(?)""", (input_text,))
                    input_text = ''
                    con.commit()
                    con.close()
                    running_start = False
                    island_screen()
                else:
                    if len(input_text) < 10 and event.unicode.isprintable():
                        input_text += event.unicode
                        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 27)
                        from_player = font.render(input_text, True, (0, 0, 0))
                        screen.blit(from_player, (WIDTH // 2, HEIGHT // 1.63))
                pygame.display.flip()
            all_sprites.update(event)
        window_surface.blit(screen, (0, 0))
        screen.blit(cont.image, cont.rect)
        screen.blit(play.image, play.rect)
        window_surface.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(30)


pygame.mixer.init()

background_image = pygame.image.load('data/background.png')
background_image = pygame.transform.scale(background_image, SIZE)

to_return = False

pygame.mixer.music.load('data/music.mp3')
music_playing = True
pygame.mixer.music.play(-1)


down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (WIDTH, HEIGHT // 1.87))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (WIDTH // 2.9, HEIGHT // 1.6))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (WIDTH // 2.6, HEIGHT // 2.4))


set_r = pygame.image.load('data/setn_wn.png')
set_r = pygame.transform.scale(set_r, (WIDTH // 2.15, HEIGHT // 1.65))
authors = pygame.image.load('data/authors.png')
authors = pygame.transform.scale(authors, (WIDTH // 9.4, HEIGHT // 14.9))
name1 = pygame.image.load('data/name_s.png')
name1 = pygame.transform.scale(name1, (WIDTH // 5.4, HEIGHT // 26))
name2 = pygame.image.load('data/name_o.png')
name2 = pygame.transform.scale(name2, (WIDTH // 5.9, HEIGHT // 25.3))
sun = pygame.image.load('data/sun.png')
sun = pygame.transform.scale(sun, (WIDTH // 7.7, HEIGHT // 4.7))
sunlight = pygame.image.load('data/sunlights.png')
sunlight = pygame.transform.scale(sunlight, (WIDTH // 4.6, HEIGHT // 3))

set_txt = pygame.image.load('data/settings+txt.png')
set_txt = pygame.transform.scale(set_txt, (WIDTH // 4.9, HEIGHT // 15.24))

mus_txt = pygame.image.load('data/music_txt.png')
mus_txt = pygame.transform.scale(mus_txt, (WIDTH // 9.9, HEIGHT // 26.8))


class PushButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/btn_on.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 13.6, HEIGHT // 13))
        self.rect = self.image.get_rect(center=(WIDTH // 1.6, HEIGHT // 2.88))

    def update(self, *args):
        global music_playing
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            music_playing = not music_playing
            if music_playing:
                pygame.mixer.music.play()
                self.image = pygame.image.load('data/btn_on.png')
            else:
                pygame.mixer.music.stop()
                self.image = pygame.image.load('data/btn_off.png')
            self.image = pygame.transform.scale(self.image, (WIDTH // 13.6, HEIGHT // 13))


class BackButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/белая_стрелка.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 17.2, HEIGHT // 11.2))
        self.rect = self.image.get_rect(center=(WIDTH // 1.034, HEIGHT // 18.74))

    def update(self, *args):
        global running_settings
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            running_settings = False


back = BackButton()
music = PushButton()
running_settings = False


def open_settings(clock: pygame.time.Clock):
    global music_playing, running_settings, running
    running_settings = True
    while running_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings = running = False
            all_sprites.update(event)
        window_surface.blit(background_image, (0, 0))

        window_surface.blit(down_cloud, (WIDTH // -150, HEIGHT // 1.75))
        window_surface.blit(right_cloud, (WIDTH // 1.5, HEIGHT // 9.37))
        window_surface.blit(left_cloud, (0, HEIGHT // 18.74))

        window_surface.blit(set_r, (WIDTH // 3.5, HEIGHT // 7.2))
        window_surface.blit(authors, (WIDTH // 2.14, HEIGHT // 2.46))
        window_surface.blit(name1, (WIDTH // 2.3, HEIGHT // 2))
        window_surface.blit(name2, (WIDTH // 2.3, HEIGHT // 1.874))

        window_surface.blit(set_txt, (WIDTH // 2.35, HEIGHT // 4.69))

        window_surface.blit(mus_txt, (WIDTH // 2.5, HEIGHT // 2.9))

        window_surface.blit(music.image, music.rect)
        window_surface.blit(back.image, back.rect)

        pygame.display.update()
    return music_playing


all_btns = pygame.sprite.Group()


class Sky(pygame.sprite.Group):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('data/cloud1.png')
        self.image2 = pygame.image.load('data/cloud2.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 7.5, HEIGHT // 9.37))
        self.rect = self.image.get_rect(center=(WIDTH // 2.14, HEIGHT // 1.88))
        self.image2 = pygame.transform.scale(self.image2, (WIDTH // 7.5, HEIGHT // 9.37))
        self.rect2 = self.image.get_rect(center=(WIDTH // 2.14, HEIGHT // 1.88))

    def blitRotate(self, surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        surf.blit(rotated_image, rotated_image_rect)


class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_btns)
        self.image = pygame.image.load('data/start_btn.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 4.7, HEIGHT // 5.5))
        self.rect = self.image.get_rect(center=(WIDTH // 2.14, HEIGHT // 1.88))

    def update(self, clock, *args):
        background_start = pygame.transform.scale(pygame.image.load('data/new_fon.png'), SIZE)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            start(clock, background_start)


class SettingsButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_btns)
        self.image = pygame.image.load('data/settings_btn.png')
        self.image = pygame.transform.scale(self.image, (WIDTH // 5.6, HEIGHT // 8))
        self.rect = self.image.get_rect(center=(WIDTH // 2.14, HEIGHT // 1.44))

    def update(self, clock, *args):
        global music_playing
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            open_settings(clock)


text = pygame.image.load('data/mthislnd_text.png')
text = pygame.transform.scale(text, (WIDTH // 4.52, HEIGHT // 5.6))

start_btn = StartButton()
settings_btn = SettingsButton()


clock = pygame.time.Clock()
running = True
angle = 0
done = False
while running:
    window_surface.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_btns.update(clock, event)
    window_surface.blit(background_image, (0, 0))

    window_surface.blit(start_btn.image, start_btn.rect)
    window_surface.blit(settings_btn.image, settings_btn.rect)
    window_surface.blit(sun, (WIDTH // 3.3, HEIGHT // 7.2))

    window_surface.blit(text, (WIDTH // 2.14, HEIGHT // 4.7))

    w, h = sunlight.get_size()
    pos = (WIDTH // 2.7, HEIGHT // 4.1)

    Sky().blitRotate(window_surface, sunlight, pos, (w / 2, h / 2), angle)
    angle += 0.5

    window_surface.blit(down_cloud, (WIDTH // -150, HEIGHT // 1.75))
    window_surface.blit(right_cloud, (WIDTH // 1.5, HEIGHT // 9.4))
    window_surface.blit(left_cloud, (0, HEIGHT // 18.8))

    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()
