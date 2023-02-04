# Cross-Zero game
# Practical work on SkillFactory course
# Oleg Vasilcov, flow FPW-1011, Feb-2023

from random import choice
from copy import deepcopy

field = {' ': ['1', '2', '3'],
         'a': ['-', '-', '-'],
         'b': ['-', '-', '-'],
         'c': ['-', '-', '-']}  # поле игры

field_new = deepcopy(field)

data_var = ['a1', 'a2', 'a3',
            'b1', 'b2', 'b3',
            'c1', 'c2', 'c3']

data_var_new = data_var.copy()  # скопированный список ходов

data_win = [{'a1', 'a2', 'a3'},
            {'b1', 'b2', 'b3'},
            {'c1', 'c2', 'c3'},
            {'a1', 'b1', 'c1'},
            {'a2', 'b2', 'c2'},
            {'a3', 'b3', 'c3'},
            {'a1', 'b2', 'c3'},
            {'a3', 'b2', 'c1'}]  # выигрышные комбинации

x_list = ('X', 'x', 'Х', 'х')  # на всякий случай добавил буквы с русской раскладки
o_list = ('O', 'o', 'О', 'о')
n_list = ('N', 'n')
q_list = ('Q', 'q')

x_win_list = set()  # будем добавлять в сет координаты для проверки на выигрышную комбинацию
o_win_list = set()

fm = None


def field_show(board):  # Печать поля игры
    for i, j in board.items():
        print(i + '  ' + j[0] + '  ' + j[1] + '  ' + j[2])
    print()


def field_refresh(our_dict):  # функция очистки поля от Х-ов и О-ов, для новой игры
    for i, j in our_dict.items():
        for k in range(len(j)):
            if i == ' ':
                continue
            else:
                j[k] = '-'


def data_var_refresh():  # функция очистки координат хода
    global data_var_new
    data_var_new.clear()
    data_var_new = data_var.copy()


def win_situation(win_list):  # если выигрышная комбинация образовалась более 3-х ходов
    s = [win_list.intersection(i) for i in data_win]
    for i in s:
        if len(i) == 3:
            return i


def start_question():
    while True:
        s = input('\nВыйти - "Q", Начать заново - "N": ')
        if s in n_list:
            return start()
        elif s in q_list:
            return print('До свиданья!!!')
        else:
            print('Введите Q - (выход) или N - (новая игра)!!!')


def first_move_change(any_list, win_list):  # Если будет первый ход программы
    global fm
    fm = choice(data_var_new)
    field_new[fm[0]][int(fm[1]) - 1] = choice(any_list).upper()
    data_var_new.remove(fm)
    win_list.add(fm)


# Функция изменения клетки поля на Х или О, по координатам, плюс рандомный ход программы
def field_change(move, win_list_own, win_list_game, list_own, list_game):
    # move - это координаты (а1, а2 и т.д.)
    data_var_new.remove(move)  # удаление координаты своего хода, чтобы не выпало программе
    if not data_var_new:
        field_new[move[0]][int(move[1]) - 1] = choice(list_own).upper()
        win_list_own.add(move)
        print()
        return print('Ходы закончились!\n')
    else:
        a = choice(data_var_new)  # рандомный координаты выбор для хода программы
        field_new[move[0]][int(move[1]) - 1] = choice(list_own).upper()  # Может можно и проще, но я пока не придумал
        field_new[a[0]][int(a[1]) - 1] = choice(list_game).upper()
        win_list_own.add(move)
        win_list_game.add(a)
        data_var_new.remove(a)  # Удаление координат хода программы, чтобы на след интерации не было повтора
    print(f'Отлично, мой ход: {a}\n')


def game(win_list_own, win_list_game, list_own, list_game):  # цикл игры
    print(f'Отлично, мой первый ход: {fm} \n')
    field_show(field_new)
    while win_situation(win_list_own) not in data_win:  # выполнять цикл пока не будет выигрышной комбинации игрока
        if win_situation(win_list_game) in data_win:  # проверка выигрышной комбинации у программы
            print('Все плохо, вы Проиграли!!!')
            return start_question()
        else:
            if data_var_new:
                move = input('Введите координаты своего хода в формате ("a1, b2, c3"... и т.д.): ')
                if move in data_var_new:
                    field_change(move, win_list_own, win_list_game, list_own, list_game)
                    field_show(field_new)
                elif move in set(data_var).symmetric_difference(set(data_var_new)):
                    print('\nЭто поле занято, попробуйте еще раз...\n')
                    field_show(field_new)
                    continue
                elif move in q_list:
                    return print('До свиданья!!!')
                elif move in n_list:
                    return start()
                else:
                    print('\nТаких координат на поле нету, попробуйте еще раз...\n')
                    field_show(field_new)
                    continue
            elif win_situation(win_list_game) not in data_win:
                print('Ничья!')
                return start_question()

    print('Поздравляю вы выиграли!')
    return start_question()


def start():
    print()
    global fm  # переменная для первого хода программы
    fm = '-'  # значение переменной если будет новая игра, и игрок ходит первый
    field_show(field)
    field_refresh(field_new)  # очистка поля для новой игры
    x_win_list.clear()  # очистка ходов за Х для новой игры
    o_win_list.clear()  # очистка ходов за О для новой игры
    data_var_refresh()  # очистка координат для новой игры
    select = input('Выберите каким символом будете играть, введите "X"-крестик или "O"-нолик: ')
    print()
    if select in q_list:
        return print('До свиданья!!!')  # выход из игры
    elif select in n_list:
        start()  # новая игра
    elif select in x_list:  # проверка Х на Ru или En раскладке.
        choose = input('Теперь выберите кто ходит первый Я - 1, или Ты - 2: ')
        if choose == '2':
            game(x_win_list, o_win_list, x_list, o_list)
        elif choose == '1':
            first_move_change(o_list, o_win_list)
            game(x_win_list, o_win_list, x_list, o_list)
        else:
            print('Нужно выбрать кто ходит первый! цифра "1" - мой ход первый, цифра - "2" твой!')
            start_question()
    elif select in o_list:  # проверка О на Ru или En-раскладке.
        choose = input('Теперь выберите кто ходит первый Я - 1, или Ты - 2: ')
        if choose == '2':
            game(o_win_list, x_win_list, o_list, x_list)
        elif choose == '1':
            first_move_change(x_list, x_win_list)
            game(o_win_list, x_win_list, o_list, x_list)
        else:
            print('Нужно выбрать кто ходит первый! цифра "1" - мой ход первый, цифра - "2" твой!')
            start_question()
    else:
        print('Мы играем в крестики нолики, так что, начните заново и введите либо Х(крестик), либо О(нолик)!!!')
        start_question()


print('\nВас приветствует игра крестики-нолики!\n')
print('(P.S. Для выхода из игры введите: "Q", начать заново: "N")')
start()
