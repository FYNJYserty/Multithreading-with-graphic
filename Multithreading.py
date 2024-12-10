import random
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog

# Глобальные переменные для синхронизации
lock = threading.Lock()
last_completed_task = None # Переменная для хранения последней завершившейся задачи
last_completed_task_h = None # Переменная для хранения последней завершившейся задачи H
last_completed_task_f = None # Переменная для хранения последней завершившейся задачи F
last_completed_task_g = None # Переменная для хранения последней завершившейся задачи G
# Создание класса задачи
class Task(threading.Thread):
# Инициализация конструктора
    def __init__(self, name, progress_var, func, *args,
        parent_task_name=None, child_task_name=None):
        super().__init__()
        self.name = name # Имя задачи
        self.progress_var = progress_var # Переменная для заполнения шкалы прогесса
        self.func = func # Функция задачи
        self.args = args # Аргументы, передаваемые в функцию задачи
        self.result = None # Результат выполнения функции
        self.finished = False # Флаг проверки выполнения задачи
        self.parent_task_name = parent_task_name # Задача, что инициировала выполнение данной
        self.child_task_name = child_task_name # Задача, которую инициирует данная
    # Обработка завершения потока
    def run(self):
        total_duration = random.randint(2, 6) # Случайная длительностью от 2 до 6 секунд
        start_time = time.time()
        start_time2 = time.strftime("%H:%M:%S") # Вывод времени в часах, минутах, секундах
        for i in range(total_duration * 10): # Увеличиваем количество шагов для плавности
            time.sleep(0.1) # Задержка для имитации работы
            self.progress_var.set((i + 1) / (total_duration * 10) * 100)
        # Обновляем прогрессбар в процентах
        self.result = self.func(*self.args) # Выполняем функцию и сохраняем результат
        self.finished = True # Задача завешена
        self.progress_var.set(100) # Завершение задачи
        end_time = time.time()
        end_time2 = time.strftime("%H:%M:%S")
        elapsed_time = end_time - start_time # Вычисление времени выполнения
        # Вывод результатов в текстовое поле
        self.log(f"{self.name} завершена.\n" +
            f"Время начала выполнения: {start_time2}.\n" + # Время начала выполнения задачи
            f"Имя задачи, которая инициировала выполнение: {self.parent_task_name}\n" + # Имя родительской задачи
            f"Результат выполнения: {self.result}\n" + # Результат выполнения заданной функции
            f"Имя задачи, которую инициирует данная задача: {self.child_task_name}\n" + # Имя дочерней задачи
            f"Длительность: {elapsed_time:.2f} секунд.\n" + # Длительность задачи
            f"Время конца выполнения: {end_time2}.\n") # Время окончания выполнения задачи

        # Переменная для определения, какая из параллельных задач выполнилась последней
        global last_completed_task
        last_completed_task = self.name

    # Запись
    def log(self, message):
        with lock:
            text_output.insert(tk.END, message + "\n")
            text_output.see(tk.END)
# Функции задач
# Функция задачи А
def generate_matrix(n):
    return [[random.randint(0, 10) for _ in range(n)] for _ in range(n)]
# Функция задачи В
def generate_r1(n):
    return [random.choice([True, False]) for _ in range(n)]
# Функция задачи С
def generate_r2(n):
    return [random.choice([True, False]) for _ in range(n)]
# Функция задачи D
def f1(M, R1, R2):
    return sum(sum(row) for row in M)
# Функция задачи E
def f2(M, R1):
    return sum(R1)
# Функция задачи F
def f3(M, R2):
    return sum(R2)

# Функция задачи G
def f4(f1_result):
    return f1_result * 2
# Функция задачи H
def f5(f2_result):
    return f2_result * 2
# Функция задачи K
def f6(f3_result, f4_result, f5_result):
    return f3_result + f4_result + f5_result
# Функция запуска задач
def start_tasks():
    n = int(entry_n.get()) # Получение размера N
    M = generate_matrix(n)
    R1 = generate_r1(n)
    R2 = generate_r2(n)
    # Создание шкал прогресса для каждой задачи
    progress_a = tk.DoubleVar()
    progress_b = tk.DoubleVar()
    progress_c = tk.DoubleVar()
    progress_d = tk.DoubleVar()
    progress_e = tk.DoubleVar()
    progress_f = tk.DoubleVar()
    progress_g = tk.DoubleVar()
    progress_h = tk.DoubleVar()
    progress_k = tk.DoubleVar()
    # Создание задач A, B, C
    task_a = Task("A", progress_a, generate_matrix, n)
    task_b = Task("B", progress_b, generate_r1, n)
    task_c = Task("C", progress_c, generate_r2, n)
    # Запуск задач A, B, C
    task_a.start()
    task_b.start()
    task_c.start()
    # Обновление прогрессбара для задач A, B, C
    def update_progress_abc():
        progress_bar_a['value'] = progress_a.get()
        progress_bar_b['value'] = progress_b.get()
        progress_bar_c['value'] = progress_c.get()
        if task_a.finished and task_b.finished and task_c.finished:
            # Запуск следующих задач после завершения A, B и C
            M_result = task_a.result
            R1_result = task_b.result
            R2_result = task_c.result
            text_output.insert(tk.END, f"Задача {last_completed_task} активировала задачи D, E, F\n\n")
            text_output.see(tk.END)
            task_d = Task("D", progress_d, f1, M_result, R1_result,
            R2_result, parent_task_name=last_completed_task, child_task_name="G")
            task_e = Task("E", progress_e, f2, M_result, R1_result,
            parent_task_name=last_completed_task, child_task_name="H")
            task_f = Task("F", progress_f, f3, M_result, R2_result,
            parent_task_name=last_completed_task, child_task_name="K")
            task_d.start()
            task_e.start()
            task_f.start()
            update_progress_d(task_d)
            update_progress_e(task_e)
            update_progress_f(task_f)
            return
        root.after(100, update_progress_abc)
    # Запуск задачи D
    def update_progress_d(task_d):
        progress_bar_d['value'] = progress_d.get()
        if task_d.finished:
            start_task_g(task_d)
            return
        root.after(100, update_progress_d, task_d)
    # Запуск задачи E
    def update_progress_e(task_e):
        progress_bar_e['value'] = progress_e.get()
        if task_e.finished:
            start_task_h(task_e)
            return
        root.after(100, update_progress_e, task_e)
    # Запуск задачи F
    def update_progress_f(task_f):
        progress_bar_f['value'] = progress_f.get()
        if task_f.finished:
            global last_completed_task_f
            last_completed_task_f = task_f # Сохраняем ссылку на завершённую задачу F
            # Запускаем проверку завершения задач G, H и F
            update_progress_ghf(last_completed_task_g,
            last_completed_task_h, last_completed_task_f)
            return
        root.after(100, update_progress_f, task_f)
    # Запуск задачи H
    def start_task_h(task_e):
        task_h = Task("H", progress_h, f5, task_e.result,
        parent_task_name="E", child_task_name="K")
        task_h.start()
        update_progress_h(task_h)
    # Обновление прогресса задачи H
    def update_progress_h(task_h):
        progress_bar_h['value'] = progress_h.get()
        if task_h.finished:
            global last_completed_task_h
            last_completed_task_h = task_h # Сохраняем ссылку на завершённую задачу H
            # Запускаем проверку завершения задач G, H и F
            update_progress_ghf(last_completed_task_g,
            last_completed_task_h, last_completed_task_f)
            return
        root.after(100, update_progress_h, task_h)
    # Запуск задачи G
    def start_task_g(task_d):
        task_g = Task("G", progress_g, f4, task_d.result,
        parent_task_name="D", child_task_name="K")
        task_g.start()
        update_progress_g(task_g)
    # Обновление прогресса задачи G
    def update_progress_g(task_g):
        progress_bar_g['value'] = progress_g.get()
        if task_g.finished:
            global last_completed_task_g
            last_completed_task_g = task_g # Сохраняем ссылку на завершённую задачу G
            # Запускаем проверку завершения задач G, H и F
            update_progress_ghf(task_g, last_completed_task_h,
            last_completed_task_f)
            return
        root.after(100, update_progress_g, task_g)
    # Обновление прогресса для задач G, H и F
    def update_progress_ghf(task_g, task_h, task_f):
        if task_g and task_h and task_f and task_g.finished and task_h.finished and task_f.finished:
            task_k = Task("K", progress_k, f6, task_f.result,
            task_g.result, task_h.result, parent_task_name=last_completed_task,
            child_task_name=None)
            text_output.insert(tk.END, f"Задача {last_completed_task} активировала задачу K\n\n")
            text_output.see(tk.END)
            task_k.start()
            update_progress_k(task_k)
            return
        root.after(100, update_progress_ghf, task_g, task_h, task_f)
    # Обновление прогресса задачи K
    def update_progress_k(task_k):
        progress_bar_k['value'] = progress_k.get()
        if task_k.finished:
            return
        root.after(100, update_progress_k, task_k)
    update_progress_abc()
# Функция для сохранения текста в файл
def save_to_file():
    # Открываем диалог для выбора пути и имени файла
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path: # Если выбран файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_output.get(1.0, tk.END)) # Получаем текст из текстового поля и записываем в файл
# Создание формы для отображения прогресса
root = tk.Tk()
root.title("Программирование параллельных процессов (15 вариант)")
root.geometry("900x850")
# Текстовое поле вывода
text_output = scrolledtext.ScrolledText(root, width=100, height=30)
text_output.pack(pady=10)
# Создание поля для ввода значения N
frame = tk.Frame(root)
frame.pack(pady=10)
label_n = tk.Label(frame, text="Введите размер N:")
label_n.pack(side=tk.LEFT)
entry_n = tk.Entry(frame)
entry_n.pack(side=tk.LEFT)
# Кнопка запуска программы
start_button = tk.Button(frame, text="Запустить задачи",
command=start_tasks)
start_button.pack(side=tk.LEFT)
# Кнопка для сохранения текста
save_button = tk.Button(frame, text="Сохранить текст",
command=save_to_file)
save_button.pack(side=tk.LEFT)
# Создание прогрессбаров и подписей к ним
def create_progress_bar(frame_name, label_text):
    frame = tk.Frame(root)
    frame.pack(pady=5)
    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    progress_bar = ttk.Progressbar(frame, length=300, mode='determinate',
    variable=tk.DoubleVar())
    progress_bar.pack(side=tk.LEFT)
    return progress_bar

progress_bar_a = create_progress_bar("frame_a", "Задача A")
progress_bar_b = create_progress_bar("frame_b", "Задача B")
progress_bar_c = create_progress_bar("frame_c", "Задача C")
progress_bar_d = create_progress_bar("frame_d", "Задача D")
progress_bar_e = create_progress_bar("frame_e", "Задача E")
progress_bar_f = create_progress_bar("frame_f", "Задача F")
progress_bar_g = create_progress_bar("frame_g", "Задача G")
progress_bar_h = create_progress_bar("frame_h", "Задача H")
progress_bar_k = create_progress_bar("frame_k", "Задача K")
# Запуск программы
root.mainloop()