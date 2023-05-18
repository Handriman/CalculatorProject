

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
def execute(input_str):
    try:
        if input_str == 'x=?':
            return 'x=?'

        return round(eval(input_str), 5)
    except ZeroDivisionError:
        return 'Деление на ноль'
    except:
        return 'что-то пошло не так'



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


    print(subexpressions)
    for subexpression in subexpressions:
        if 'integrate' in subexpression:
            temp = subexpression[10:-1].split(',')
            print(temp)
            res = integrate(str(temp[0]), str(temp[1]), str(temp[2]))
            input_str = input_str.replace(subexpression, str(res))

        if 'diff' in subexpression:
            temp = subexpression[5:-1].split(',')
            res = diff(str(temp[0]), str(temp[1]))
            input_str = input_str.replace(subexpression, str(res))
    return input_str



def integrate(input_str, lower, upper):

    f = lambda x: eval(str(input_str))
    lower = eval(lower)
    upper = eval(upper)
    S = 0
    dx = (upper - lower)/500

    for i in range(500):
        S += dx * (f(lower + dx * i)+f(lower + dx * (i+1)))/2

    return round(S, 5)

def diff(func:str, arg):
    f = lambda x: eval(func)
    arg = eval(arg)
    dx = 0.000001
    return round((f(arg + dx)-f(arg))/dx, 5)


is_first = True
previos_answer_button = ['^', '+', '-', '*', '/']
prev_ans = 0



def main():
    while True:
        a = input()
        eval(translator(a))
        res = round(eval(translator(a)), 9)
        print(res)


if __name__ == '__main__':
    main()