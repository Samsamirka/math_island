import pygame
import sys
import os
import random
import sqlite3

pygame.init()


FPS = 50
SIZE = WIDTH, HEIGHT = 1500, 937
BACKGROUND = pygame.color.Color('lightskyblue')
input_text = ''
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
back_to_task_sprite = pygame.sprite.Group()


def render_text_task(text, number=None):  # number - номер аздания для его печати в диалоговом окне
    """возвращает text в виде картинки на фоне города с дождем"""
    global backgrnd
    count = 0
    y = 0
    string = ''
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 70)
    if number is not None:
        num_task = font.render(str(number), True, (0, 0, 0))
    else:
        num_task = number
    backgrnd = pygame.transform.scale(load_image('фон_для_задания.jpeg'), (1500, 937))
    backgrnd.blit(num_task, (420, 545))
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 37)
    text = text[2:-3]
    text = text.split()
    for word in text:
        count += 1
        string += word
        string += ' '
        text_task = font.render(str(string), True, (0, 0, 0))
        if text_task.get_size()[0] > 1200:
            string = string[:-(len(word) + 1)]
            text_task = font.render(str(string), True, (0, 0, 0))
            backgrnd.blit(text_task, (100, 650 + y))
            y += 35
            count = 0
            string = ''
        elif text_task.get_size()[0] == 1200:
            backgrnd.blit(text_task, (100, 650 + y))
            y += 35
            count = 0
            string = ''
        elif text_task.get_size()[0] < 1200 and text.index(word) == len(text) - 1:
            backgrnd.blit(text_task, (100, 650 + y))
    next_sprite.draw(backgrnd)
    next_sprite.clear(screen, screen)
    back_to_task_sprite.draw(backgrnd)
    back_to_task_sprite.clear(screen, screen)
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
    # 6: load_image('Самостоятельные.png')
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
    background = pygame.transform.scale(load_image('Остров.png'), (WIDTH, HEIGHT))
    screen.fill(BACKGROUND)
    screen.blit(background, (10, 10))
    nick_name = cur.execute("""SELECT name FROM users ORDER BY id DESC LIMIT 1""").fetchone()[0]
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    nickname = font.render(str(nick_name), True, (50, 50, 50))
    screen.blit(nickname, (10, 120))
    island_title = pygame.transform.scale(PLAYER_IMAGES['title_island'], (300, 107))
    screen.blit(island_title, (0, 0))
    money_bag = pygame.transform.scale(PLAYER_IMAGES['money'], (60, 79))
    screen.blit(money_bag, (1260, 81))
    lvl = pygame.transform.scale(load_image('LVL.png'), (60, 30))
    screen.blit(lvl, (1240, 21))
    load_island_sprites()
    island_sprites.draw(screen)
    control_sprite.draw(screen)
    leave_sprite.draw(screen)
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    money_player = font.render(str(money), True, (255, 255, 255))
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
    experience_player = font.render(str(level), True, (255, 255, 255))
    screen.blit(money_player, (1330, 120))
    screen.blit(experience_player, (1330, 15))
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
                        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
                        from_player = font.render(input_text, True, (0, 100, 0))
                        pygame.draw.rect(screen, (255, 255, 255), (100, 860, from_player.get_width() + 35,
                                                                   from_player.get_height()))
                        screen.blit(from_player, (100, 860))
                    elif event.key == pygame.K_RETURN:
                        if input_text == '':
                            island.set_answer(0)
                        else:
                            input_text = float(input_text.replace(',', '.'))
                            island.set_answer(input_text)
                        input_text = ''
                    else:
                        input_text += event.unicode
                        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
                        from_player = font.render(input_text, True, (0, 100, 0))
                        screen.blit(from_player, (100, 860))
            window_surface.blit(screen, (0, 0))
        pygame.display.flip()

        clock.tick(FPS)

class IslandImage(pygame.sprite.Sprite):
    def __init__(self, task_id, coordinates):
        super().__init__(island_sprites)
        self.task_id = task_id
        self.image = pygame.transform.scale(TASKS_IMAGES[task_id], (60, 64))
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        global tasks
        tasks.append(self)


ISLAND_COORDINATES = {
    1: (263, 255),
    2: (587, 390),
    3: (800, 355),
    4: (851, 580),
    5: (669, 560)
    # 6: (1110, 245)
}


def load_island_sprites():
    for task_id, coordinates in ISLAND_COORDINATES.items():
        IslandImage(task_id, coordinates)
    leave_button = pygame.sprite.Sprite()
    leave_button.image = pygame.transform.scale(load_image('Кнопка выхода.png'), (210, 53))
    leave_button.rect = leave_button.image.get_rect()
    leave_button.rect.x = 1280
    leave_button.rect.y = 874
    leave_sprite.add(leave_button)



NAMES_BOYS = ['Саша', 'Максим', 'Кирилл', 'Андрей', 'Ваня', 'Петя', 'Коля', 'Боря', 'Серёжа']
NAMES_GIRLS = ['Лиза', 'Оля', 'Самира', 'Катя', 'Маша', 'Юля', 'Аня', 'Лера', 'Вика', 'Настя']
NAMES_BOYS_EDIT = ['Саши', 'Максима', 'Кирилла', 'Андрея', 'Вани', 'Пети', 'Коли', 'Бори', 'Серёжи']
NAMES_GIRLS_EDIT = ['Лизы', 'Оли', 'Самиры', 'Кати', 'Маши', 'Юли', 'Ани', 'Леры', 'Вики', 'Насти']


class Island:
    def __init__(self):
        global next
        global next_sprite, back_to_task_sprite
        self.input_answer = input_text
        self.task = None
        self.number = 0
        self.won = False  # введеный ответ == правильному
        self.next_button = pygame.sprite.Sprite()
        self.next_button.image = load_image('Стрелка.png')
        self.next_button.image = pygame.transform.scale(self.next_button.image, (70, 70))
        self.next_button.rect = self.next_button.image.get_rect()
        self.next_button.rect.x = 1220
        self.next_button.rect.y = 830
        next_sprite.add(self.next_button)
        next = [self.next_button]
        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 70)
        self.open_condition_button = pygame.sprite.Sprite()
        self.open_condition_button.image = font.render('+', True, 'royalblue')
        self.open_condition_button.rect = self.open_condition_button.image.get_rect()
        self.open_condition_button.rect.x = 1150
        self.open_condition_button.rect.y = 825
        back_to_task_sprite.add(self.open_condition_button)

    def open_condition(self, running_condition):
        global task_start, for_condition
        if running_condition:
            task_start = False
            for_condition = pygame.transform.scale(load_image("полное_условие.jpeg"), (1500, 937))

            return for_condition

    def set_answer(self, answer):
        self.input_answer = answer
        try:
            self.input_answer = str(float(self.input_answer))
        except ValueError:
            print('Вводить нужно числа/вместо запятой ставится точка')
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
        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
        self.won = self.task.check_answer(self.input_answer)
        if self.won and not task_made:  # task_made - проверка на выполненность задания,
            # чтобы не получать бесконечное количество награды
            # должен переключаться до нажатия энтер
            screen.blit(backgrnd, (0, 0))
            money += 10
            level += 1
            final = 'Всё верно! Получи 10 монет :)'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (10, 10))
            task_made = True
        elif not self.won and not task_made:
            if money >= 10:
                money -= 10
            screen.blit(backgrnd, (0, 0))
            final = 'К сожалению, неверно. Попробуй ещё разок! Ты теряешь 10 монет ;('
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (10, 10))
            task_made = True
        elif self.won and task_made:
            screen.blit(backgrnd, (0, 0))
            final = 'Всё верно!'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (10, 10))
        elif not self.won and task_made:
            screen.blit(backgrnd, (0, 0))
            final = 'К сожалению, неверно. Попробуй ещё разок!'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (10, 10))

    def get_event(self, *args):
        global task_made, running_island, running, running_start, task_start, back_to_task_sprite
        global money, level, input_text, nick_name, running_condition
        for button in tasks:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(args[0].pos):
                task_start = True
                self.task = Task(button.task_id)  # task_id должен быть записан при создании спрайта
        for arrow in next:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and arrow.rect.collidepoint(args[0].pos):
                task_start = False
                task_made = False
                input_text = ''
                island_screen()
        # for btn in control_sprite:
            # if args and args[0].type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(args[0].pos):
                # ends = random.randint(25, 33)  # расстояние между спицами
                # h = random.randint(24, 38)  # высота купола
                # d = random.randint(90, 120)  # расстояние между концами спиц
                # h_2 = round(random.uniform(50, 70), 1)
                # r = random.randint(25, 40)
                # a = random.randint(30, 51)  # длина
                # b = random.randint(70, 151)  # ширина
                # S = random.randint(600, 1301)
                # while a % 10 != 0 or b % 10 != 0 or S % 50 != 0:
                    # a = random.randint(30, 51)  # длина
                    # b = random.randint(70, 151)  # ширина
                    # S = random.randint(600, 1301)
                # num = random.randint(15, 31)
                # generate_task(ends=ends, h=h, d=d, h_2=h_2, r=r, a=a, b=b, S=S, num=num, id=6)
        for leave_btn in leave_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and leave_btn.rect.collidepoint(args[0].pos):
                con = sqlite3.connect("data/users.db")
                cur = con.cursor()
                nick_name = cur.execute("""SELECT name FROM users ORDER BY id DESC LIMIT 1""").fetchone()[0]
                cur.execute("""INSERT INTO users(money, lvl, name) VALUES(?, ?, ?)""", (money, level, nick_name,))
                con.commit()
                con.close()
                running_island = running = running_start = False
        for condition_button in back_to_task_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and condition_button.rect.collidepoint(args[0].pos):
                running_condition = True
                screen.blit(self.open_condition(running_condition), (0, 0))


def generate_task_1(text):
    umbrella = random.randint(19, 30)
    handle = round(random.uniform(4, 10), 1)
    answer_1 = round((3 * (umbrella - handle)), 1)
    print(answer_1)
    return text.format(umbrella=umbrella, handle=handle), answer_1


def generate_task_2(text, ends, boy):
    h_2 = round(random.uniform(50, 70), 1)
    s = (1 / 2) * ends * h_2
    answer_2 = round((s * 2))
    return text.format(name=boy, h=h_2), answer_2


def generate_task_3(text, r, boy):
    answer = (r ** 2 + (r * 2) ** 2) / (r * 2)
    return text.format(name=boy, r=r), answer


def generate_task_4(text, h, d, girl, girl_edit):
    answer = round(2 * 3.14 * h * (d / 2))
    return text.format(girl=girl, girl_edit=girl_edit), answer


def generate_task_5(text, num, a, b, S, girl_edit, boy_edit):
    all_wedges = 12 * num  # тк 12 клиньев на одном зонте
    wedges = (all_wedges * S) / 10000  # клинья
    roll = a * b * 0.01  # рулон
    rest = round((roll - wedges), 2)  # обрезки
    answer = round(((rest / roll) * 100), 2)
    return text.format(a=a, b=b, num=num, S=S, girl=girl_edit, boy=boy_edit), answer


def generate_task(id, **args):
    global answer
    global number
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
        text, answer = generate_task_1(text)
    elif id == 2:
        text, answer = generate_task_2(text, args['ends'], boy)
    elif id == 3:
        text, answer = generate_task_3(text, args['r'], boy)
    elif id == 4:
        text, answer = generate_task_4(text, args['h'], args['d'], girl, girl_edit)
    elif id == 5:
        text, answer = generate_task_5(text, args['num'], args['a'], args['b'], args['S'], girl_edit, boy_edit)
    island.exercise_open(id, text)
    number = id
    return text, answer


class Task:
    def __init__(self, number=None):  # number - номер задания, который получаем из exercise_номер_open()
        self.text, self.true_answer = generate_task(number)

    def check_answer(self, answer):  # answer = TEXT, возвращает True/False
        return float(answer) == self.true_answer


backgrnd = pygame.transform.scale(load_image('фон_для_задания.jpeg'), (1500, 937))
island = Island()


WIDTH, HEIGHT = 1500, 937
COLOR_ACTIVE = pygame.Color('white')
COLOR_INACTIVE = pygame.Color((30, 30, 30))

input_text = ''
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()


class ContinuedGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/continued.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(750, 350))

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
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(550, 600))

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
    pygame.draw.rect(screen, (255, 255, 255), (750, 575, 288, 52))
    while running_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
                    from_player = font.render(input_text, True, (0, 0, 0))
                    print(from_player.get_width() + 45)
                    pygame.draw.rect(screen, (255, 255, 255), (750, 575, from_player.get_width() + 45,
                                                                         from_player.get_height()))
                    screen.blit(from_player, (750, 575))
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode
                        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 45)
                        from_player = font.render(input_text, True, (0, 0, 0))
                        screen.blit(from_player, (750, 575))
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
background_image = pygame.transform.scale(background_image, (background_image.get_width() / 1.6, background_image.get_height() // 1.6))

to_return = False

pygame.mixer.music.load('data/music.mp3')
music_playing = True
pygame.mixer.music.play()


down_cloud = pygame.image.load('data/down_cloud.png')
down_cloud = pygame.transform.scale(down_cloud, (down_cloud.get_width() // 1.5, down_cloud.get_height() // 1.5))
right_cloud = pygame.image.load('data/right_cloud.png')
right_cloud = pygame.transform.scale(right_cloud, (right_cloud.get_width() // 1.5, right_cloud.get_height() // 1.5))
left_cloud = pygame.image.load('data/left_cloud.png')
left_cloud = pygame.transform.scale(left_cloud, (left_cloud.get_width() // 1.5, left_cloud.get_height() // 1.5))


set_r = pygame.image.load('data/setn_wn.png')
set_r = pygame.transform.scale(set_r, (set_r.get_width() // 2, set_r.get_height() // 2))
authors = pygame.image.load('data/authors.png')
authors = pygame.transform.scale(authors, (authors.get_width() // 2, authors.get_height() // 2))
name1 = pygame.image.load('data/name_s.png')
name1 = pygame.transform.scale(name1, (name1.get_width() // 2, name1.get_height() // 2))
name2 = pygame.image.load('data/name_l.png')
name2 = pygame.transform.scale(name2, (name2.get_width() // 2, name2.get_height() // 2))
name3 = pygame.image.load('data/name_o.png')
name3 = pygame.transform.scale(name3, (name3.get_width() // 2, name3.get_height() // 2))

set_txt = pygame.image.load('data/settings+txt.png')
set_txt = pygame.transform.scale(set_txt, (set_txt.get_width() // 2, set_txt.get_height() // 2))

mus_txt = pygame.image.load('data/music_txt.png')
mus_txt = pygame.transform.scale(mus_txt, (mus_txt.get_width() // 2, mus_txt.get_height() // 2))


class PushButtons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/btn_on.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(940, 325))

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
            self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))


class BackButtons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/back_btn.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(1450, 50))

    def update(self, *args):
        global running_settings
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            running_settings = False


back = BackButtons()
music = PushButtons()
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

        window_surface.blit(music.image, music.rect)
        window_surface.blit(back.image, back.rect)

        pygame.display.update()
    return music_playing


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
        background_start = pygame.image.load('data/new_fon.png')
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            start(clock, background_start)


class SettingsButtons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_btns)
        self.image = pygame.image.load('data/settings_btn.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(center=(700, 650))

    def update(self, clock, *args):
        global music_playing
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            open_settings(clock)


sun = pygame.image.load('data/sun.png')
sun = pygame.transform.scale(sun, (sun.get_width() // 2, sun.get_height() // 2))
sunlight = pygame.image.load('data/sunlights.png')
sunlight = pygame.transform.scale(sunlight, (sunlight.get_width() // 2, sunlight.get_height() // 2))

text = pygame.image.load('data/mthislnd_text.png')
text = pygame.transform.scale(text, (text.get_width() // 2, text.get_height() // 2))

start_btn = StartButtons()
settings_btn = SettingsButtons()


clock = pygame.time.Clock()
running = True
while running:
    window_surface.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_btns.update(clock, event)
    window_surface.blit(background_image, (0, 0))

    window_surface.blit(start_btn.image, start_btn.rect)
    window_surface.blit(settings_btn.image, settings_btn.rect)

    window_surface.blit(sun, (450, 130))
    window_surface.blit(sunlight, (390, 80))
    window_surface.blit(text, (700, 200))

    window_surface.blit(down_cloud, (-10, 500))
    window_surface.blit(right_cloud, (980, 100))
    window_surface.blit(left_cloud, (0, 50))

    pygame.display.update()

pygame.quit()
sys.exit()
