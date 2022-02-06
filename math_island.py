import pygame
import sys
import os
import random
import sqlite3

FPS = 50
SIZE = WIDTH, HEIGHT = 1500, 937
BACKGROUND = pygame.color.Color('lightskyblue')
input_text = ''
number = 0
experience = 0
tasks = []
next = []
task_made = False

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

island_sprites = pygame.sprite.Group()
control_sprite = pygame.sprite.Group()
next_sprite = pygame.sprite.Group()


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
    5: load_image('5.png'),
    6: load_image('Самостоятельные.png')
}
PLAYER_IMAGES = {
    'money': load_image('Мешок денег.png'),
    'title_island': load_image('Название острова.png')
}


def island_screen():
    global experience
    background = pygame.transform.scale(load_image('Остров.png'), (WIDTH, HEIGHT))
    screen.fill(BACKGROUND)
    screen.blit(background, (10, 10))
    island_title = pygame.transform.scale(PLAYER_IMAGES['title_island'], (300, 107))
    screen.blit(island_title, (0, 0))
    money_bag = pygame.transform.scale(PLAYER_IMAGES['money'], (60, 79))
    screen.blit(money_bag, (1260, 81))
    load_tasks_sprites()
    island_sprites.draw(screen)
    control_sprite.draw(screen)
    font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 25)
    money = font.render(str(experience), True, (255, 255, 255))
    screen.blit(money, (1330, 120))

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
    5: (669, 560),
    6: (1110, 245)
}


def load_tasks_sprites():
    for task_id, coordinates in ISLAND_COORDINATES.items():
        IslandImage(task_id, coordinates)


NAMES_BOYS = ['Саша', 'Максим', 'Кирилл', 'Андрей', 'Ваня', 'Петя', 'Коля', 'Боря', 'Серёжа']
NAMES_GIRLS = ['Лиза', 'Оля', 'Самира', 'Катя', 'Маша', 'Юля', 'Аня', 'Лера', 'Вика', 'Настя']
NAMES_BOYS_EDIT = ['Саши', 'Максима', 'Кирилла', 'Андрея', 'Вани', 'Пети', 'Коли', 'Бори', 'Серёжи']
NAMES_GIRLS_EDIT = ['Лизы', 'Оли', 'Самиры', 'Кати', 'Маши', 'Юли', 'Ани', 'Леры', 'Вики', 'Насти']


class StartWindow:
    def __init__(self):
        pass

    def start_open(self):
        pass

    def settings_open(self):
        pass


class Island:
    def __init__(self):
        global next
        global next_sprite
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
        global experience
        global backgrnd
        global task_made
        font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
        self.won = self.task.check_answer(self.input_answer)
        if self.won and not task_made:  # task_made - проверка на выполненность задания,
            # чтобы не получать бесконечное количество награды
            # должен переключаться до нажатия энтер
            screen.blit(backgrnd, (0, 0))
            experience += 10
            final = 'Всё верно! Получи 10 xp :)'
            result = font.render(final, True, (255, 255, 255))
            screen.blit(result, (10, 10))
            task_made = True
        elif not self.won and not task_made:
            if experience >= 10:
                experience -= 10
            screen.blit(backgrnd, (0, 0))
            final = 'К сожалению, неверно. Попробуй ещё разок! Ты теряешь 10 xp ;('
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
        global task_made
        for button in tasks:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(args[0].pos):
                self.task = Task(button.task_id)  # task_id должен быть записан при создании спрайта
        for arrow in next:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and arrow.rect.collidepoint(args[0].pos):
                task_made = False
                island_screen()
        for btn in control_sprite:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(args[0].pos):
                ends = random.randint(25, 33)  # расстояние между спицами
                h = random.randint(24, 38)  # высота купола
                d = random.randint(90, 120)  # расстояние между концами спиц
                h_2 = round(random.uniform(50, 70), 1)
                r = random.randint(25, 40)
                a = random.randint(30, 51)  # длина
                b = random.randint(70, 151)  # ширина
                S = random.randint(600, 1301)
                while a % 10 != 0 or b % 10 != 0 or S % 50 != 0:
                    a = random.randint(30, 51)  # длина
                    b = random.randint(70, 151)  # ширина
                    S = random.randint(600, 1301)
                num = random.randint(15, 31)
                generate_task(ends=ends, h=h, d=d, h_2=h_2, r=r, a=a, b=b, S=S, num=num, id=6)


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
    con = sqlite3.connect('text_of_task_and_exercises.db')
    cur = con.cursor()
    text = str(cur.execute("SELECT text FROM task_exercises WHERE id = ?", (id,)).fetchone())

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

    if id == 1:
        text, answer = generate_task_1(text)  # и так нужно написать еще 4 функции
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


def terminate():
    pygame.quit()
    sys.exit()

backgrnd = pygame.transform.scale(load_image('фон_для_задания.jpeg'), (1500, 937))
island_screen()
running = True
island = Island()

while running:
    for event in pygame.event.get():
        island.get_event(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
                from_player = font.render(input_text, True, (0, 100, 0))
                pygame.draw.rect(screen, (255, 255, 255), (100, 860, from_player.get_width() + 35,
                                                               from_player.get_height()))
                screen.blit(from_player, (100, 860))
            elif event.key == pygame.K_RETURN:
                print(input_text)
                island.set_answer(input_text)
                input_text = ''
            else:
                input_text += event.unicode
                font = pygame.font.Font('data/ofont.ru_AsylbekM29.kz.ttf', 35)
                from_player = font.render(input_text, True, (0, 100, 0))
                screen.blit(from_player, (100, 860))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
