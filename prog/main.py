import time
import math
from tkinter import *  # библиотека для графического интерфейса
from tkinter import messagebox

root = Tk()  # переменная для окна

# функция которая реагирует на передвижение и масштабирование окна
def config(event):
    if event.widget == root:
        global dx, dy, cx, cy, w, h

        f_top.place(width=event.width,
                    height=event.height)  # меняем размер рамки, в которой находится полотно для графика
        canvas.config(width=event.width, height=event.height)  # меняем размер полотна для графика
        w = f_top.winfo_width() + 250     # меняем переменную для ширины окна и увеличиваем ее
        h = f_top.winfo_height()          # меняем переменную для высоты окна

        # вычисляем стоимость одного пикселя холста
        dx = w / (x_right - x_left)
        dy = h / (y_top - y_bottom)

        # вычисляем центр координат
        cx = -x_left * dx
        cy = y_top * dy

        #time.sleep(0.03)       # задержка изменений
        if Coord == 2:         # в зависимости от системы координат заново рисуем график и оси
            DrawDecard(w, h)
        if Coord == 1:
            DrawPolar(w, h)


def frange(begin, end, step):  # функция  расчета нецелого х
    x = begin
    t = []
    while x <= end:
        t.append(x)
        x += step
    return t


def Try(a, b, c, d, coordinates):  # функция выполнить расчёт
    global A, B, C, D, Coord, x_tmp, y_tmp  # переменные для хранения вводимых значений
    true = 0
    try:  # преобразование данных в числа для программы
        A = float(a)
        B = float(b)
        C = float(c)
        D = float(d)
        Coord = int(coordinates)
        x_tmp, y_tmp = calcCissoid(A, B, C, D)  # получаем массивы точек х и у
        true = 1
    except ValueError:  # если числа не преобразованы или не сделан выбор, сообщение об ошибке
        messagebox.showinfo("Ошибка", "Сообщение ошибки: введено неверное значение или не выбрана система координат!")

    if true:
        if abs(A) <= 10 and abs(B) <= 10 and abs(C) <= 10 and abs(D) <= 10:  # проверка на корректность введённых данных
            Draw()                                                           # отрисовка
        else:
            messagebox.showinfo("Ошибка", "Сообщение ошибки: данные должны быть в диапазоне: [0, 10]")


def calcCissoid(A, B, C, D):  # функция расчета у для х
    a1 = 0
    b1 = 0
    y_tmp = []
    i = 0
    x_tmp = frange(x_left, x_right, 0.5)                   # х считается в функции frange
    a1 = -math.pow(A * A, -1) - math.pow(C, -1)            # pow - возведение в степень
    b1 = -math.pow(B * B, -1) + math.pow(D, -1)
    for x in x_tmp:                                        # y = разница общих уравнений эллипса и прямой
        y = math.sqrt(math.fabs(1 - (x * x * a1) + b1))    # fabs - для работы с float
        y_tmp.append(y)                                    # значения Y на каждый X
    return x_tmp, y_tmp


def Draw():  # функция отрисовывает графики в зависимости от выбранной системы координат
    if Coord == 2:
        DrawDecard(w, h)
    if Coord == 1:
        DrawPolar(w, h)


def DrawDecard(w, h):     # отрисовка в декартовой системе координат
    canvas.delete("all")  # отчистка холста
    canvas.create_line(0, cy, w, cy, fill='black', arrow=BOTH)  # рисуем ось х
    canvas.create_line(cx, 0, cx, h, fill='black', arrow=BOTH)  # рисуем ось у

    y_step = (y_top - y_bottom) / 10
    x_step = (x_right - x_left) / 10
    x = x_left
    while x <= x_right:
        x_canvas = (x - x_left) * dx
        canvas.create_line(x_canvas, cy - 3, x_canvas, cy + 3, fill='black')    # делаем метки на координатной оси х
        canvas.create_text(x_canvas, cy + 15, text=str(round(x, 1)),
                           fill='black')  # подписываем метки на координатной оси х
        x += x_step

    y = y_top
    while y >= y_bottom:
        y_canvas = (y - y_top) * dy
        canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas, fill='black')  # делаем метки на координатной оси у
        canvas.create_text(cx + 25, -y_canvas, text=str(round(y, 1)),
                           fill='black')  # подписываем метки на координатной оси у
        y -= y_step

    canvas.pack()
    root.update()            # обновляем изображение на окне
    GraphDraw(x_tmp, y_tmp)  # рисуем график в декартовой системе координат


def DrawPolar(w, h):
    canvas.delete("all")  # отчистка холста
    canvas.create_line(0, cy, w, cy, fill='grey')  # рисуем градусные оси от центра
    root.update()
    canvas.create_line(cx, 0, cx, h, fill='grey')
    root.update()
    canvas.create_line(250, 0, w - 250, h, fill='grey')
    root.update()
    canvas.create_line(250, h, w - 250, 0, fill='grey')
    root.update()

    canvas.create_text(w - 270, (h / 2) - 10, text="0" + "\u00b0", fill='black')  # подписываем градусные оси
    canvas.update()
    canvas.create_text(w - 270, 10, text="45" + "\u00b0", fill='black')
    canvas.create_text(280, 12, text="135" + "\u00b0", fill='black')
    canvas.create_text((w / 2) - 10, 12, text="90" + "\u00b0", fill='black')
    canvas.create_text(280, (h / 2) - 5, text="180" + "\u00b0", fill='black')
    canvas.create_text(290, h - 20, text="225" + "\u00b0", fill='black')
    canvas.create_text((w / 2) - 13, h - 20, text="270" + "\u00b0", fill='black')
    canvas.create_text(w - 283, h - 20, text="315" + "\u00b0", fill='black')

    y = y_top
    x = 0
    y_step = (y_top - y_bottom) / 10
    x_step = (x_right - x_left) / 10

    while x <= x_right and y <= y_top:  # рисуем круговые оси и подписываем
        y_canvas = (y - y_top) * dy
        x_canvas = (x - x_left) * dx
        xs = x_canvas - cx
        canvas.create_oval(cx - xs, cy - y_canvas, x_canvas, cy + y_canvas, outline="grey")  # круговые оси
        canvas.create_line(x_canvas, cy - 3, x_canvas, cy + 3, fill='black')
        canvas.create_text(x_canvas, cy + 15, text=str(round(x, 1)), fill='black')
        root.update()
        x += x_step
        y -= y_step

    canvas.pack()
    root.update()    # обновляем изображение на окне
    GraphDrawPolar(x_tmp, y_tmp)  # рисуем график в полярной системе координат


def GraphDraw(x_tmp, y_tmp):
    i = 0
    for x in x_tmp:  # для каждого х вычисляем у и рисуем круги на точках
        y = y_tmp[i]
        x = (x - x_tmp[0]) * dx
        y = (y - y_top) * dy
        canvas.create_oval(x - 2, -(y - 2), x + 2, -(y + 2), fill="red", outline="red")
        i += 1
    root.update()    # обновляем изображение на окне


def GraphDrawPolar(x_tmp, y_tmp):
    i = 0
    for x in x_tmp:  # для каждого х вычисляем у, переносим в полярную систему координат и рисуем круги на точках
        if x == 0:
            i += 1
        else:
            y = y_tmp[i]
            p = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) * dx
            f = (math.atan(math.fabs(y / x)) * (180 / math.pi)) * dy
            canvas.create_oval(p, f, p, f, fill="red", outline="red")  # смещение в полярной системе координат
            i += 1

    root.update()   # обновляем изображение на окне


def move():
    if Coord == 2:
        moveDecard(x_tmp, y_tmp)
    if Coord == 1:
        movePolar(x_tmp, y_tmp)


def moveDecard(x_tmp, y_tmp):
    canvas.create_rectangle(50, 40, 40, 50, fill="blue", outline="blue", tags="s")  # строим квадрат за пределами холста
    i = 0
    for x in x_tmp:
        x = (x - x_tmp[0]) * dx
        y = (y_tmp[i] - y_top) * dy
        position = canvas.coords("s")
        print(position)  # вывод координат квадрата в консоль
        canvas.move("s", (x - 5) - position[0], -(y + 5) - position[1])  # перемещаем квадрат на вычисленные координаты
        canvas.update()  # обновляем изображение на окне
        time.sleep(0.1)  # скорость перемещения квадрата
        i += 1
    root.update()        # обновляем изображение на окне


def movePolar(x_tmp, y_tmp):
    canvas.create_rectangle(50, 40, 40, 50, fill="blue", outline="blue", tags="s")  # строим квадрат за пределами холста
    i = 0
    for x in x_tmp:
        if x == 0:
            i += 1
        else:
            p = math.sqrt(math.pow(x, 2) + math.pow(y_tmp[i], 2)) * dx
            f = (math.atan(math.fabs(y_tmp[i] / x)) * (180 / math.pi)) * dy
            position = canvas.coords("s")
            print(position)  # вывод координат квадрата в консоль
            canvas.move("s", p - position[0], f - position[1])  # перемещаем квадрат на вычисленные координаты
            canvas.update()  # обновляем изображение на окне
            time.sleep(0.1)  # скорость перемещения квадрата
            i += 1
    root.update()            # обновляем изображение на окне



# Первоначальная настройка интерфейса и его запуск
def Window():
    global x_left, x_right, y_bottom, y_top, w, h, dx, dy, cx, cy, canvas, f_top

    root.title("График функции, БПИ20-02 Юрчук Григорий Александрович, вариант 37")
    root.geometry('780x620')           # размер окна

    # Разделяю интерфейс на 2 части, левая с функциональными кнопками и правая, где будет
    # отображаться график
    f_top = Frame(root)                # создаем рамку для красивого вида
    f_top = LabelFrame()               # убираем у рамки обводку
    f_top.pack(side=RIGHT, fill=BOTH)  # устанавливаем расположение рамки

    f_top2 = Frame(root)               # создаем рамку для красивого вида
    f_top2 = LabelFrame()              # убираем у рамки обводку
    f_top2.pack(side=LEFT, fill=BOTH)  # устанавливаем расположение рамки

    w = f_top.winfo_width() + 250      # меняем переменную для ширины окна и увеличиваем ее
    h = f_top.winfo_height()           # меняем переменную для высоты окна

    canvas = Canvas(f_top)             # создаем холст для рисования (правая часть интерфейса)
    canvas.config(width=w, height=h)   # устанавливаем его размеры
    canvas.pack(fill=BOTH)             # устанавливаем расположение рамки

    x_left, x_right = -40, 40          # переменные для хранения левой и правой границы х
    y_bottom, y_top = -40, 40          # переменные для хранения нижней и верхней границы у

    # вычисляем стоимость одного пикселя холста
    dx = w / abs(x_right - x_left)
    dy = h / abs(y_top - y_bottom)

    # вычисляем центр координат
    cx = -x_left * dx
    cy = y_top * dy

    a, b, c, d = StringVar(), StringVar(), StringVar(), StringVar()  # переменные для записи коэффициентов

    Label(f_top2, text="").pack()
    Label(f_top2, text="Общее уравнение эллипса: ").pack()
    Label(f_top2, text="(x^2 / a1^2) + (y^2 / b1^2) = 1").pack()
    Label(f_top2, text="").pack()
    Label(f_top2, text="Общее уравнение пересекающихся").pack()
    Label(f_top2, text="действительных прямых: ").pack()
    Label(f_top2, text="(x^2 / a2^2) - (y^2 / b2^2) = 0").pack()
    Label(f_top2, text="").pack()
    Label(f_top2, text="Итоговая формула: ").pack()
    Label(f_top2, text="1 + x/a1 - a2*x + 1/(-b1) + b2").pack()
    Label(f_top2, text="").pack()
    Label(f_top2, text="Введите коэффициенты: ").pack()

    # поля для ввода коэффициентов
    namea_label = Label(f_top2, text="Введите a1:")
    a_entry = Entry(f_top2, textvariable=a)
    nameb_label = Label(f_top2, text="Введите b1:")
    b_entry = Entry(f_top2, textvariable=b)
    namec_label = Label(f_top2, text="Введите a2:")
    c_entry = Entry(f_top2, textvariable=c)
    named_label = Label(f_top2, text="Введите b2:")
    d_entry = Entry(f_top2, textvariable=d)

    # отображаю поля для ввода коэффициентов
    namea_label.pack()
    a_entry.pack()
    nameb_label.pack()
    b_entry.pack()
    namec_label.pack()
    c_entry.pack()
    named_label.pack()
    d_entry.pack()

    # отступ
    Label(f_top2, text="").pack()

    # выбор систем координат
    Label(f_top2, text="Выберите систему координат:").pack()
    coordinates = StringVar()   # Переменная для значения выбранной системы координат

    # выборы системы координат и их надписи
    Radiobutton(f_top2, text="Полярная система координат", value=1, variable=coordinates).pack()
    Radiobutton(f_top2, text="Декартовая система координат", value=2, variable=coordinates).pack()

    Label(f_top2, text="").pack()
    Label(f_top2, text="").pack(side=BOTTOM)

    # кнопка "Анимация"
    btn2 = Button(f_top2, text='Анимация')
    btn2.pack(side=BOTTOM)                         # привязка к нижнему бару
    btn2.bind('<Button-1>', lambda event: move())  # при нажатии на кнопку начинаем анимаию

    # отступ
    Label(f_top2, text="").pack(side=BOTTOM)

    # кнопка "Выполнить"
    btn = Button(f_top2, text='Выполнить')
    btn.pack(side=BOTTOM)
    btn.bind('<Button-1>', lambda event: Try(a.get(),
                                             b.get(),
                                             c.get(),
                                             d.get(),
                                             coordinates.get()))  # при нажатии на кнопку вызываем функцию Try и
                                                                  # передаём туда все полученные значения

    root.bind("<Configure>", config)    # применение изменений конфигурации
    root.mainloop()                     # отображение сконфигурированного окна


def main():
    Window()


main()
