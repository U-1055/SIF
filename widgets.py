import tkinter
from tkinter import Frame, Tk, filedialog, Button, GROOVE, RIDGE, StringVar, ttk, constants, Label
from customtkinter import CTkEntry


def string_validation(char):
    """Функция валидации. Пропускает ТОЛЬКО целые числа >= 0"""
    if char == '':
        return True

    try:
        if int(char) >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


class EntryButton(Frame):
    """Виджет, при нажатии на кнопку вводящий в Entry путь к выбранной папке."""

    def __init__(self, master: tkinter.Widget, bg='White'):
        super().__init__(master=master, bg=master['bg'])

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0)

        self.button = ttk.Button(self, text='...', command=self.load_path)
        self.button.grid(row=0, column=1)

    def load_path(self):
        path = filedialog.askdirectory(title='Выберите папку')
        self.entry.delete(0, constants.END)
        self.entry.insert(0, path)

    def get(self) -> str:
        return self.entry.get()

    def insert(self, index, string):
        self.entry.insert(index, string)


class NumEntry(CTkEntry):
    """CTkEntry с валидацией, позволяющей вводить только целые числа."""

    def __init__(self, master):
        self.text = StringVar()
        self.text.set('')
        self.allowed_chars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        super().__init__(master=master, textvariable=self.text, validate='key',
                         validatecommand=(master.register(string_validation), '%P'))

    def get(self) -> int:
        return self.get()

    def validation(self, char):
        return string_validation(char)


class Counter(ttk.Spinbox):
    """ttk.Spinbox с целочисленной валидацией."""

    def __init__(self, master: tkinter.Widget, state: tkinter.constants = constants.NORMAL, from_: float = 0,
                 to: float = 0):
        text_var = StringVar()
        super().__init__(master=master, textvariable=text_var, validate='key',
                         validatecommand=(master.register(self.validation), '%P'),
                         from_=from_, to=to, state=state)

    def get(self) -> int:
        return int(self.get())

    def validation(self, char):
        return string_validation(char)


class FromTo(Frame):
    """Виджет, позволяющий указать начальное (s) и конечное значение (f). Возвращает кортеж (s, f)"""

    def __init__(self, master):
        super().__init__(master=master)

        from_lbl = ttk.Label(self, text='С:')
        to_lbl = ttk.Label(self, text='До:')

        from_lbl.grid(column=0, row=0)
        to_lbl.grid(column=2, row=0)

        self.from_counter = Counter(self, from_=0, to=5000000)
        self.to_counter = Counter(self, from_=0,
                                  to=500000)  #ToDo: исправить, посмотреть в доке как сделать без to=50000000

        self.from_counter.grid(column=1, row=0)
        self.to_counter.grid(column=3, row=0)

    def get(self) -> tuple:
        return (self.from_counter.get(), self.to_counter.get())

    def insert(self, inp: tuple[int, int]):
        self.from_counter.insert(0, str(inp[0]))
        self.from_counter.insert(0, str(inp[1]))


class ParamsList(ttk.Combobox):
    def __init__(self, master: tkinter.Widget, param_widget):
        super().__init__(master=master)

    def __open(self):
        pass

    def __close(self):
        pass

class ErrorWindow(Label):
    """Окно, выводящее динамическое сообщение об ошибке в введённых в настоящий момент значениях"""

    def __init__(self, master):
        super().__init__(master=master)

class NumCombobox(ttk.Combobox):
    """ttk.Combobox с целочисленной неотрицательной валидацией"""
    def __init__(self, master: tkinter.Widget):
        text_var = StringVar()
        super().__init__(master=master, textvariable=text_var, validate='key', validatecommand=(master.register(self.validation), '%P'))

    def validation(self, char):
        return string_validation(char)

class CustomCombobox(ttk.Combobox):
    """ttk.Combobox с кнопкой добавления значения""" #ToDo: доделать

if __name__ == '__main__':
    root = Tk()
    root.geometry('512x512')
    numentry = NumEntry(root)
    numentry.pack()
    root.mainloop()
