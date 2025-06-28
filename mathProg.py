import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FunctionGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("График функции f(x)")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Увеличиваем масштаб всего интерфейса
        self.root.tk.call('tk', 'scaling', 2.0)
        
        # Настройка стилей
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 18))
        self.style.configure("TButton", font=("Segoe UI", 16), padding=8)
        self.style.configure("Header.TLabel", font=("Segoe UI Semibold", 18, "bold"))
        self.style.configure("TEntry", font=("Consolas", 18), padding=6)
        self.style.configure("TLabelFrame.Label", font=("Segoe UI", 18, "italic"))
        
        # Переменная для хранения текущего режима
        self.mode_var = tk.StringVar(value="Формула → График")
        self.create_widgets()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Меню выбора режима
        mode_frame = ttk.Frame(self.root)
        mode_frame.pack(pady=15)
        
        ttk.Label(mode_frame, text="Режим работы:",
                 style="Header.TLabel").pack(side=tk.LEFT, padx=5)
        
        self.mode_menu = ttk.Combobox(
            mode_frame,
            textvariable=self.mode_var,
            values=["Формула → График", "Таблица → График"],
            state="readonly",
            width=25,
            font=("Segoe UI", 14)
        )
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        self.mode_menu.bind("<<ComboboxSelected>>", self.switch_mode)
        
        # Контейнер для содержимого
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Область графика
        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Инициализация контента
        self.current_mode = None
        self.switch_mode()  # Загрузить начальный режим
    
    def switch_mode(self, event=None):
        """Переключение между режимами"""
        new_mode = self.mode_var.get()
        if new_mode == self.current_mode:
            return
        
        # Очистка текущего содержимого
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.current_mode = new_mode
        
        if new_mode == "Формула → График":
            self.create_formula_mode()
        elif new_mode == "Таблица → График":
            self.create_table_mode()
    
    def create_formula_mode(self):
        """Режим ввода через формулу"""
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(pady=10, fill=tk.X)
        
        # Поле ввода функции
        ttk.Label(input_frame, text="Введите функцию f(x):",
                 style="Header.TLabel").pack(anchor=tk.W)
        self.function_entry = ttk.Entry(input_frame, width=40)
        self.function_entry.pack(fill=tk.X, pady=5)
        self.function_entry.insert(0, "x**2")  # Пример по умолчанию
        
        # Диапазон x
        range_frame = ttk.LabelFrame(input_frame, text="Диапазон x (не обязательно)")
        range_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(range_frame, text="От:").pack(side=tk.LEFT, padx=5)
        self.x_min_entry = ttk.Entry(range_frame, width=10)
        self.x_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(range_frame, text="До:").pack(side=tk.LEFT, padx=5)
        self.x_max_entry = ttk.Entry(range_frame, width=10)
        self.x_max_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка построения
        self.plot_btn = ttk.Button(input_frame, text="Построить график",
                                 command=self.plot_from_formula)
        self.plot_btn.pack(pady=10)
        
        # Таблица значений
        table_frame = ttk.LabelFrame(self.content_frame, text="Значения функции")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.table_output = tk.Text(table_frame, height=10, font=("Courier New", 12))
        self.table_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.table_scroll = tk.Scrollbar(table_frame, command=self.table_output.yview)
        self.table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table_output.config(yscrollcommand=self.table_scroll.set)
    
    def is_valid_number(self, entry: ttk.Entry) -> bool:
        val = entry.get().strip()
        if not val:
            return True
        try:
            float(val)
            return True
        except ValueError:
            return False
    
    def plot_from_formula(self):
        """Построение графика по формуле"""
        try:
            if not self.is_valid_number(self.x_min_entry) or not self.is_valid_number(self.x_max_entry):
                messagebox.showerror("Ошибка", "Введите корректные числа в поля диапазона.")
                return
            
            func_str = self.function_entry.get().replace("^", "**")
            
            # Получаем значения диапазона, если указаны
            x_min_str = self.x_min_entry.get().strip()
            x_max_str = self.x_max_entry.get().strip()
            x_min = float(x_min_str) if x_min_str else -10
            x_max = float(x_max_str) if x_max_str else 10
            
            x = np.linspace(x_min, x_max, 500)
            y = eval(func_str, {'x': x, 'np': np, 'sin': np.sin, 'cos': np.cos, 'sqrt': np.sqrt})
            
            self.ax.clear()
            self.ax.plot(x, y, label=f"f(x) = {func_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.legend()
            self.canvas.draw()
            
            # Отображение таблицы
            self.table_output.delete(1.0, tk.END)
            self.table_output.insert(tk.END, "x\t\tf(x)\n")
            for xi, yi in zip(x[:20], y[:20]):  # первые 20 строк
                self.table_output.insert(tk.END, f"{xi:.2f}\t\t{yi:.4f}\n")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{e}")
    
    def create_table_mode(self):
        """Режим ввода через таблицу"""
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(table_frame, text="Введите значения x и f(x) построчно (через пробел):",
                 style="Header.TLabel").pack(anchor=tk.W)
        
        self.manual_table = tk.Text(table_frame, height=15, font=("Courier New", 12))
        self.manual_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        example_text = "Пример:\n-2 4\n-1 1\n0 0\n1 1\n2 4"
        self.manual_table.insert(tk.END, example_text)
        
        self.plot_table_btn = ttk.Button(table_frame, text="Построить по таблице",
                                       command=self.plot_from_table)
        self.plot_table_btn.pack(pady=10)
    
    def plot_from_table(self):
        """Построение графика из табличных данных"""
        try:
            lines = self.manual_table.get(1.0, tk.END).strip().split('\n')
            x_vals, y_vals = [], []
            
            for line in lines:
                if not line.strip() or line.startswith("Пример"):
                    continue
                
                parts = line.strip().split()
                if len(parts) != 2:
                    raise ValueError(f"Неверный формат строки: {line}")
                
                x_vals.append(float(parts[0]))
                y_vals.append(float(parts[1]))
            
            if not x_vals:
                raise ValueError("Не введены данные для построения графика.")
            
            x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))  # Сортировка по x
            
            self.ax.clear()
            self.ax.plot(x_vals, y_vals, 'o-', label="Табличные данные")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.legend()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки таблицы:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionGraphApp(root)
    root.mainloop()