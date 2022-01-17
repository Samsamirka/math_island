import pygame
import sys
import os
import random
import sqlite3

FPS = 50
SIZE = WIDTH, HEIGHT = 1500, 937.5
BACKGROUND = pygame.color.Color('black')
text = ''
number = 0

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def render_text(text: str, rect: pygame.rect.Rect) -> pygame.surface.Surface:
    """возвращает text в виде картинки, вписанной в rect"""
    pass


def start_screen():
    background = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


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

    def get_result(self) -> pygame.surface.Surface:
        """ответ от системы(верный/неверный ответ)"""
        self.won = self.task.check_answer(self.input_answer)
        if self.won:
            return render_text('Всё верно! Получий заслуженные 10 хр :)')
        else:
            return render_text('Неверно, попробуй ещё разок ;(')

    def render_result(self):
        screen.blit(self.get_result(), (self.x, self.y))
        # что-то вроде clear.self.input_answer
        if self.won:
            # запустить фейерверк
            pass


def condition_open():  # эта функция повторяется в каждых классах
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


def generate_task(id, **args):  # дописать каждый объект по типу ends; args нужны для того, чтобы эта функция работала
    # как для задачек отдельно, так и для самостоятельной, тк в самостоятельной параметры в условиях не меняются
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


running = True
island = Island()
while running:
    for event in pygame.event.get():
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
            island.set_answer(text)  # не забыть обновить текст до пустоты
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()