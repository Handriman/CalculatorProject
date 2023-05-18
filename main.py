
'''

    Модуль пользовательского интерфейса калькулятора
    В нем создается рабочий интерфейс, в нем происходит
    Ввод выражения и отображение результата


'''


import tkinter as tk
from tkinter import font

from calculator import *

# создаем окно
window = tk.Tk()


# функция обновления строки ввода, которая вызывает функцию-обработчик кнопок
def entry_update(a):
    global is_first
    # если производится новое вычисление, то в строку добавляются символы
    if  is_first:
        btn_handler(a)
    # иначе из строки удаляется прошлое выражение и вписывается новое
    else:
        btn_ac()
        if a in previos_answer_button:
            btn_handler('ans')
        btn_handler(a)


# функция-обработчик нажатия экранных кнопок
def btn_handler(a):
    # если нажатая кнопка это кнопка действия, то вызывается соответвующая функция
    if a == 'del':
        btn_del()
        return
    if a == 'AC':
        btn_ac()
        return
    if a == '=':
        btn_exe()
        return
    # если нажатая кнопка это выражение, требующее открывающей скобки, то она добавляется к символу кнокпи
    if a == 'sin' or a == 'cos' or a == 'tg' or a == 'd/dx' or a == '∫':
        enter.insert(tk.INSERT, a + '(')
        return
    if a == '\"x\"':
        enter.insert(tk.INSERT, 'x')
        return
    # если нажата кнопка прошлого ответа, то вставляется прошлый ответ
    if a == 'ans':
        enter.insert(tk.INSERT, str(prev_ans))
        return
    enter.insert(tk.INSERT, a)

# функция кнопки стирания одного символа
def btn_del():
    temp = enter.get()
    enter.delete(0, tk.END)
    enter.insert(0, temp[:-1])

# функция кнопки удаления всего выражения
def btn_ac():
    global is_first
    is_first = True
    enter.delete(0, tk.END)

# функция кнопки выполнения вычислений
def btn_exe():
    global is_first, prev_ans
    is_first = False
    stroka = enter.get()
    stroka = translator(stroka)
    print(stroka)
    try:
        res = execute(stroka)
        lbl['text'] = str(res)
        prev_ans = res
    except ZeroDivisionError:
        lbl['text'] = 'Деление на ноль'
    except NameError:
        lbl['text'] = 'X только в ∫ и d/dx'

# задание параметров окна
window.title('Калькулятор')
window.geometry('425x625')

# рамка для полей ввода и вывода
frm_io = tk.Frame(master=window)
# рамка для кнопок если создать дополнительные рамки с кнопками, то можно реализовать смену слоев кнопок
# тем самым на уже занятое место, дабавить кнопку с новой функцией
frm_btn_1 = tk.Frame(master=window)

# списки-шаблоны, они отображают расположение кнопок на экране, изменение списков, приведет к изменению UI

# список с "именами" кнопок
button_list = [

    ['sin', 'cos', 'tg', '∫', 'd/dx'],
    ['(', ')', ',', '\"x\"','^'],
    ['7', '8', '9', 'del', 'AC'],
    ['4', '5', '6', '+', '-'],
    ['1', '2', '3', '*', '/'],
    ['.', '0', 'pi','ans', '=' ]

]
# список с цветами фона кнопок
btn_bg_color = [
    ['gray', 'gray', 'gray', 'gray', 'gray'],
    ['gray', 'gray', 'gray', 'gray', 'gray'],
    ['white', 'white', 'white', 'tomato', 'tomato'],
    ['white', 'white', 'white', 'white', 'white'],
    ['white', 'white', 'white', 'white', 'white'],
    ['white', 'white', 'white','white', 'royal blue', ],
]
# список с цветами шрифта кнопок
btn_fg_color = [
    ['white', 'white', 'white', 'white', 'white'],
    ['white', 'white', 'white', 'white', 'white'],
    ['black', 'black', 'black', 'black', 'black'],
    ['black', 'black', 'black', 'black', 'black'],
    ['black', 'black', 'black', 'black', 'black'],
    ['black', 'black', 'black','black', 'white' ],
]

# шрифты с разными размерами
bold_font = font.Font(size=17)
bold_font_text = font.Font(size=25)

# создание объекта класса Label для вывода результатов вычислений
lbl = tk.Label(master=frm_io, text='', background='white', width=20, height=2, font=bold_font_text)

# создание объекта класса Entry для ввода выражений
enter = tk.Entry(master=frm_io, width=22, font=bold_font_text, relief=tk.FLAT)

# Компановка этих элементов
enter.grid(column=0, row=0)
lbl.grid(column=0, row=1)

# for i in range(3):
#     window.columnconfigure(i, weight=1, minsize=75)
#     window.rowconfigure(i, weight=1, minsize=50)

# Циклы создания кнопок
for i in range(len(button_list)):
    for j in range(len(button_list[i])):
        btn = tk.Button(master=frm_btn_1,
                        text=button_list[i][j],
                        width=5,
                        height=2,
                        font=bold_font,
                        command=lambda a=button_list[i][j]: entry_update(a),
                        bg=btn_bg_color[i][j],
                        fg=btn_fg_color[i][j]
                        )

        btn.grid(column=j, row=i, padx=5, pady=5)


# упаковка рамки с полями ввода и вывода и рамки с кнопками
frm_io.pack()
frm_btn_1.pack()

# запуск окна
window.mainloop()
