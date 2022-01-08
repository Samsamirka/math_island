import pygame
import sys
import os
import random
import sqlite3


FPS = 50
SIZE = WIDTH, HEIGHT = 1500, 937.5
BACKGROUND = pygame.color.Color('black')
TEXT = ''
number = 0

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
    # если файл не существует, то выходим
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
        self.input_answer = TEXT
        self.x = 40  # координата х для появления congratulations
        self.y = 60  # координата y для появления congratulations

    def exercise_1_open(self):
        number = 1
        # появляется условие задачи(получает из Task: text), персонаж, фон и тд
        screen.blit(render_answer(), (self.x, self.y))


def render_answer():  # ответ от системы(верный/неверный ответ)
    if Task.check_answer(TEXT):
        # появление фейерверка на экране
        return 'Всё верно! Получий заслуженные 10 хр :)'
    else:
        return 'Неверно, попробуй ещё разок ;('


def condition_open():  # эта функция повторяется в каждых классах заданий
    pass


def generate_task(id):
    con = sqlite3.connect('text_of_task_and_exercises.db')
    cur = con.cursor()
    text = cur.execute(f"""SELECT text FROM task_exercises 
                    WHERE id = {id}""").fetchall()
    for i in text:
        for g in i:
            text = g

    ends = random.randint(25, 33)  # расстояние между спицами
    h = random.randint(24, 38)  # высота купола
    d = random.randint(90, 120)  # расстояние между концами спиц

    boy = random.choice(NAMES_BOYS)
    girl = random.choice(NAMES_GIRLS)
    boy_edit = NAMES_BOYS_EDIT[NAMES_BOYS.index(boy)]
    girl_edit = NAMES_GIRLS_EDIT[NAMES_GIRLS.index(girl)]

    if id == 1:
        umbrella = random.randint(19, 30)
        handle = round(random.uniform(4, 10), 1)
        answer_1 = 3 * (umbrella - handle)
        return text.format(umbrella=umbrella, handle=handle), answer_1
    elif id == 2:
        h_2 = round(random.uniform(50, 70), 1)
        s = (1 / 2) * ends * h
        answer_2 = round((s * 2))
        return text.format(name=boy, h=h_2), answer_2
    elif id == 3:
        r = random.randint(25, 40)
        answer = (r ** 2 + (r * 2) ** 2) / (r * 2)
        return text.format(name=boy, r=r), answer
    elif id == 4:
        answer = round(2 * 3.14 * h * (d / 2))
        return text.format(girl=girl, girl_edit=girl_edit), answer  # В БАЗЕ ДАННЫХ НУЖНО ДОБАВИТЬ girl_edit
    elif id == 5:
        a = random.randint(30, 51)  # длина
        b = random.randint(70, 151)  # ширина
        num = random.randint(15, 31)  # количество зонтов
        S = random.randint(600, 1301)
        while a % 10 != 0 or b % 10 != 0 or S % 50 != 0:
            a = random.randint(15, 41)
            b = random.randint(60, 101)
            S = random.randint(600, 1301)
        alll = 12 * num  # тк 12 клиньев на одном зонте
        wedges = (alll * S) / 10000  # клинья
        roll = a * b * 0.01  # рулон
        rest = round((roll - wedges), 2)  # обрезки
        answer = round(((rest / roll) * 100), 2)
        return text.format(a=a, b=b, num=num, S=S, girl=girl_edit, boy=boy_edit), answer


class Task:
    def __init__(self, number):
        self.text, self.true_answer = generate_task(number)

    def render_exercise(self, surface):
        pass

    def check_answer(self, answer):  # answer = TEXT, возвращает True/False
        return answer == self.true_answer


def terminate():
    pygame.quit()
    sys.exit()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(TEXT)
                TEXT = ''
            elif event.key == pygame.K_BACKSPACE:
                TEXT = TEXT[:-1]
            else:
                TEXT += event.unicode
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
