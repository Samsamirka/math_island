import pygame
import sys
import os
import random
import sqlite3

FPS = 50
SIZE = WIDTH, HEIGHT = 1500, 937.5
BACKGROUND = pygame.color.Color('lightskyblue')
text = ''
number = 0
experience = 0

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

island_sprites = pygame.sprite.Group()
control_sprite = pygame.sprite.Group()  # создать спрайт самостоятельной и добавить сюда; не забыть scale


def render_text(text: str, rect: pygame.rect.Rect) -> pygame.surface.Surface:
    """возвращает text в виде картинки, вписанной в rect"""
    pass


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
    'first': load_image('1.png'),
    'second': load_image('2.png'),
    'third': load_image('3.png'),
    'fourth': load_image('4.png'),
    'fifth': load_image('5.png'),
    'control': load_image('Самостоятельные.png')
}
PLAYER_IMAGES = {
    'money': load_image('Мешок денег.png'),
    'title_island': load_image('Название острова.png')
}


def island_screen():
    background = pygame.transform.scale(load_image('Остров.png'), (WIDTH, HEIGHT))
    screen.fill(BACKGROUND)
    screen.blit(background, (10, 10))
    island_title = pygame.transform.scale(PLAYER_IMAGES['title_island'], (300, 107))
    screen.blit(island_title, (0, 0))
    money_bag = pygame.transform.scale(PLAYER_IMAGES['money'], (60, 79))
    screen.blit(money_bag, (1260, 81.5))
    load_tasks_sprites()
    island_sprites.draw(screen)
    control_sprite.draw(screen)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()
        clock.tick(FPS)


def load_tasks_sprites():
    image_task_1 = pygame.sprite.Sprite()
    image_task_1.image = pygame.transform.scale(TASKS_IMAGES['first'], (60, 64))
    image_task_1.rect = image_task_1.image.get_rect()
    image_task_1.rect.x = 263
    image_task_1.rect.y = 255
    island_sprites.add(image_task_1)
    image_task_2 = pygame.sprite.Sprite()
    image_task_2.image = pygame.transform.scale(TASKS_IMAGES['second'], (60, 64))
    image_task_2.rect = image_task_2.image.get_rect()
    image_task_2.rect.x = 587
    image_task_2.rect.y = 390
    island_sprites.add(image_task_2)
    image_task_3 = pygame.sprite.Sprite()
    image_task_3.image = pygame.transform.scale(TASKS_IMAGES['third'], (60, 64))
    image_task_3.rect = image_task_3.image.get_rect()
    image_task_3.rect.x = 799.7
    image_task_3.rect.y = 354.6
    island_sprites.add(image_task_3)
    image_task_4 = pygame.sprite.Sprite()
    image_task_4.image = pygame.transform.scale(TASKS_IMAGES['fourth'], (60, 64))
    image_task_4.rect = image_task_4.image.get_rect()
    image_task_4.rect.x = 850.5
    image_task_4.rect.y = 580
    island_sprites.add(image_task_4)
    image_task_5 = pygame.sprite.Sprite()
    image_task_5.image = pygame.transform.scale(TASKS_IMAGES['fifth'], (60, 64))
    image_task_5.rect = image_task_5.image.get_rect()
    image_task_5.rect.x = 668.9
    image_task_5.rect.y = 560.3
    island_sprites.add(image_task_5)
    control_image = pygame.sprite.Sprite()
    control_image.image = pygame.transform.scale(TASKS_IMAGES['control'], (60, 64))
    control_image.rect = control_image.image.get_rect()
    control_image.rect.x = 1110
    control_image.rect.y = 244.9
    control_sprite.add(control_image)


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


def update(*args):
    count = 0
    for button in island_sprites:
        count += 1
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(args[0].pos):
            generate_task(count)
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
            generate_task(count, ends=ends, h=h, d=d, h_2=h_2, r=r, a=a, b=b, S=S, num=num)
    count = 0


class Island:
    def __init__(self):
        self.input_answer = text
        self.x = 40  # координата х для появления congratulations
        self.y = 60  # координата y для появления congratulations
        self.task = None
        self.number = 0
        self.won = False  # введеный ответ == правильному

    def set_answer(self, answer):
        self.input_answer = answer

    def exercise_1_open(self):
        self.number = 1
        self.task = Task(self.number)
        render_text(self.task.text)
        # появляется условие задачи(получает из self.task.text), персонаж, фон и тд

    def exercise_2_open(self):
        self.number = 2
        self.task = Task(self.number)
        render_text(self.task.text)
        # появляется условие задачи(получает из self.task.text), персонаж, фон и тд

    def exercise_3_open(self):
        self.number = 3
        self.task = Task(self.number)
        render_text(self.task.text)
        # появляется условие задачи(получает из self.task.text), персонаж, фон и тд

    def exercise_4_open(self):
        self.number = 4
        self.task = Task(self.number)
        render_text(self.task.text)
        # появляется условие задачи(получает из self.task.text), персонаж, фон и тд

    def exercise_5_open(self):
        self.number = 5
        self.task = Task(self.number)
        render_text(self.task.text)
        # появляется условие задачи(получает из self.task.text), персонаж, фон и тд

    def get_result(self) -> pygame.surface.Surface:
        """ответ от системы(верный/неверный ответ)"""
        self.won = self.task.check_answer(self.input_answer)
        if self.won:
            return render_text('Всё верно! Получий заслуженные 10 хр :)')
        else:
            return render_text('Неверно, попробуй ещё разок ;(')

    def render_result(self):
        screen.blit(self.get_result(), (self.x, self.y))
        self.input_answer.clear()
        if self.won:
            # запустить фейерверк
            pass


def generate_task_1(text):
    umbrella = random.randint(19, 30)
    handle = round(random.uniform(4, 10), 1)
    answer_1 = 3 * (umbrella - handle)
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
    return text.format(girl=girl, girl_edit=girl_edit), answer  # В БАЗЕ ДАННЫХ НУЖНО ДОБАВИТЬ girl_edit


def generate_task_5(text, num, a, b, S, girl_edit, boy_edit):
    all_wedges = 12 * num  # тк 12 клиньев на одном зонте
    wedges = (all_wedges * S) / 10000  # клинья
    roll = a * b * 0.01  # рулон
    rest = round((roll - wedges), 2)  # обрезки
    answer = round(((rest / roll) * 100), 2)
    return text.format(a=a, b=b, num=num, S=S, girl=girl_edit, boy=boy_edit), answer


def generate_task(id, **args):
    con = sqlite3.connect('text_of_task_and_exercises.db')
    cur = con.cursor()
    text = cur.execute("SELECT text FROM task_exercises WHERE id = ?", id).fetchone()

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
        return generate_task_1(text)  # и так нужно написать еще 4 функции
    elif id == 2:
        generate_task_2(text, args['ends'], boy)
    elif id == 3:
        generate_task_3(text, args['r'], boy)
    elif id == 4:
        generate_task_4(text, args['h'], args['d'], girl, girl_edit)
    elif id == 5:
        generate_task_5(text, args['num'], args['a'], args['b'], args['S'], girl_edit, boy_edit)


class Task:
    def __init__(self, number):  # number - номер задания, который получаем из exercise_номер_open()
        self.text, self.true_answer = generate_task(number)

    def render_exercise(self, surface):
        pass

    def check_answer(self, answer):  # answer = TEXT, возвращает True/False
        return answer == self.true_answer


def terminate():
    pygame.quit()
    sys.exit()


island_screen()
running = True
island = Island()

while running:
    for event in pygame.event.get():
        island_sprites.update(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                text = ''
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
            island.set_answer(text)  # использовали clear
    island_sprites.draw(screen)
    island_sprites.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()