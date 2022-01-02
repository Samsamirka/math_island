import pygame
import sys
import os
import random
import sqlite3


NAMES_BOYS = ['Саша', 'Максим', 'Кирилл', 'Андрей', 'Ваня', 'Петя', 'Коля', 'Боря', 'Серёжа']
NAMES_GIRLS = ['Лиза', 'Оля', 'Самира', 'Катя', 'Маша', 'Юля', 'Аня', 'Лера', 'Вика', 'Настя']
NAMES_BOYS_EDIT = ['Саши', 'Максима', 'Кирилла', 'Андрея', 'Вани', 'Пети', 'Коли', 'Бори', 'Серёжи']
NAMES_GIRLS_EDIT = ['Лизы', 'Оли', 'Самиры', 'Кати', 'Маши', 'Юли', 'Ани', 'Леры', 'Вики', 'Насти']

BOY = random.choice(NAMES_BOYS)
GIRL = random.choice(NAMES_GIRLS)
BOY_EDIT = NAMES_BOYS_EDIT[NAMES_BOYS.index(BOY)]
GIRL_EDIT = NAMES_GIRLS_EDIT[NAMES_GIRLS.index(GIRL)]


class StartWindow:
    def __init__(self):
        pass

    def start_open(self):
        pass

    def settings_open(self):
        pass


class Island:
    def __init__(self):
        pass

    def theory_open(self):  # теория везде одинаковая
        pass

    def control_work_open(self):
        pass

    def exercise_1_open(self):
        pass

    def exercise_2_open(self):
        pass

    def exercise_3_open(self):
        pass

    def exercise_4_open(self):
        pass

    def exercise_5_open(self):
        pass


def condition_open(self):  # эта функция повторяется в каждых классах заданий
    pass


def render_answer(self):  # ответ от системы(верный/неверный ответ)
    pass


def generate_task(number):
    con = sqlite3.connect('text_of_task_and_exercises.db')
    cur = con.cursor()
    text = cur.execute(f"""SELECT text FROM task_exercises 
                    WHERE id = {number}""").fetchall()
    for i in text:
        for g in i:
            text = g

    ends = random.randint(25, 33)  # расстояние между спицами
    h = random.randint(24, 38)  # высота купола
    d = random.randint(90, 120)  # расстояние между концами спиц

    if number == 1:
        umbrella = random.randint(19, 30)
        handle = round(random.uniform(4, 10), 1)
        answer_1 = 3 * (umbrella - handle)
        return text.format(umbrella=umbrella, handle=handle), answer_1
    elif number == 2:
        h_2 = round(random.uniform(50, 70), 1)
        l = ends  # сменяем название переменной, чтобы было проще ориентироваться в условие
        s = (1 / 2) * l * h
        answer_2 = round((s * 2))
        return text.format(name=BOY, h=h_2), answer_2
    elif number == 3:
        r = random.randint(25, 40)
        answer = (r ** 2 + (r * 2) ** 2) / (r * 2)
        return text.format(name=BOY, r=r), answer



class Task:
    def __init__(self, number):
        self.text, self.true_answer = generate_task(number)

    def render_exercise(self, surface):
        pass

    def check_answer(self, answer):
        return answer == self.true_answer
