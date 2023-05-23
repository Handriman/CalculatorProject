

'''

        Главный модуль калькулятора
        В нем производится анализ и приведение строки, введенной пользователем,
        К виду пригодному для вычисления функцией eval()

'''


from math import sin, cos, tan, pi, sqrt

import ast

temp_exp = ''
ask_iks = False
iks = 0

# функция вычисление преобразованной строки с помощью eval
def execute(input_str):
    try:
        if input_str == 'x=?':
            return 'x=?'

        return round(eval(input_str),8)
    except ZeroDivisionError:
        return 'Деление на ноль'
    except:
        return 'что-то пошло не так'


# Функция приведения введенной строки к пригодному для вычисления виду
def translator(input_str : str):
    global temp_exp, ask_iks, iks
    try:
        input_str = input_str.lower()
        input_str = input_str.replace(' ', '')
        if 'tg' in input_str: input_str = input_str.replace('tg', 'tan')
        if '^' in input_str: input_str = input_str.replace('^', '**')
        if 'pi' in input_str: input_str = input_str.replace('pi', f'{pi}')
        if 'd/dx' in input_str: input_str = input_str.replace('d/dx', 'diff')
        if '∫' in input_str: input_str = input_str.replace('∫', 'integrate')

        # Если Х используется без операторов интегрирования или дифференцирования, программа "спрашивает" чему он равен
        if 'x' in input_str and 'integrate' not in input_str and 'diff' not in input_str:
            temp_exp = input_str
            ask_iks = True
            return 'x=?'
        input_str = extract_complicated_func(input_str)
        if ask_iks:
            iks = input_str
            input_str = temp_exp.replace('x', iks)
            ask_iks = False
        return input_str

    except:
        return 'Что-то пошло не так'


# Функция вычленения из строки интеграллов и производных для их расчета
def extract_complicated_func(input_str:str):

    subexpressions = []

    # Разбор выражения в виде дерева синтаксического разбора
    tree = ast.parse(input_str)

    # Обход узлов дерева
    for node in ast.walk(tree):
        # Проверка, является ли узел вызовом функции
        if isinstance(node, ast.Call):
            # Преобразование узла обратно в строку
            subexpression = ast.unparse(node)
            subexpression = subexpression.replace(' ', '')
            subexpressions.append(subexpression)

            if 'integrate' in subexpression:
                temp = subexpression[10:-1].split(',')
                print(temp)
                res = integrate(str(temp[0]), str(temp[1]), str(temp[2]))
                input_str = input_str.replace(subexpression, str(res))

            if 'diff' in subexpression:
                temp = subexpression[5:-1].split(',')
                res = diff(str(temp[0]), str(temp[1]))
                input_str = input_str.replace(subexpression, str(res))

    print(subexpressions)

    return input_str


# Функция численного интегрирования методом Симпсона, уточненным методом Рунге
def integrate(input_str, lower, upper):

    f = lambda x: eval(input_str)
    lower = eval(lower)
    upper = eval(upper)

    N = 2
    dx = (upper - lower)/N
    S = 0
    s = 0
    h = (upper-lower)/(4*N)
    h2 = h/2
    print(h2, h)

    for i in range(N):
        s = s + h2 / 3 * (f(lower + i*dx) + 4 * f(lower + i*dx + h2)
                         + 2 * f(lower + i*dx + 2 * h2) + 4 * f(lower + i*dx + 3 * h2)
                         + 2 * f(lower + i*dx + 4*h2) + 4 * f(lower + i*dx + 5 * h2)
                         + 2 * f(lower + i * dx + 6 * h2) + 4 * f(lower + i * dx + 7 * h2)
                         + f(lower + i * dx + 8 * h2))
        S = S + h / 3 * (f(lower + i*dx) + 4 * f(lower + i*dx + h) + 2 * f(lower + i*dx + 2 * h) + 4 * f(lower + i*dx + 3 * h) + f(lower + i*dx + 4*h))
        print(s, S)


    return s + (s-S)/15


# Функция численного дифференецирования методом конечной разности с использованием центральной разности
def diff(func:str, arg):
    f = lambda x: eval(func)
    arg = eval(arg)
    dx = 0.000001
    return round((f(arg + dx)-f(arg - dx))/(2*dx), 7)


is_first = True
previos_answer_button = ['^', '+', '-', '*', '/']
prev_ans = 0



