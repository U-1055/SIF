import tkinter
from tkinter import Frame, Tk, filedialog, Button, GROOVE, RIDGE, StringVar, ttk, constants, Label
from customtkinter import CTkEntry
#ToDo: разбраться с явным указанием размеров в виджетах с гридом

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

        self.button = ttk.Button(self, text='...', width=4, command=self.load_path)
        self.button.grid(row=0, column=1)

    def load_path(self):
        path = filedialog.askdirectory(title='Выберите папку')
        self.entry.delete(0, constants.END)
        self.entry.insert(0, path)

    def get(self) -> str:
        return self.entry.get()

    def insert(self, index, string):
        self.entry.insert(index, string)


class NumEntry(ttk.Entry):
    """CTkEntry с валидацией, позволяющей вводить только целые числа."""

    def __init__(self, master):
        self.text = StringVar()
        self.text.set('')
        self.allowed_chars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        super().__init__(master=master, textvariable=self.text, validate='key',
                         validatecommand=(master.register(string_validation), '%P'), width=6)

    def get(self) -> int:
        return self.get()

    def validation(self, char):
        return string_validation(char)


class Counter(ttk.Spinbox):
    """ttk.Spinbox с целочисленной валидацией."""

    def __init__(self, master: tkinter.Widget, state: tkinter.constants = constants.NORMAL, width: int = 10, from_: int = 0,
                 to: int = 0):
        text_var = StringVar()
        super().__init__(master=master, textvariable=text_var, validate='key',
                         validatecommand=(master.register(self.validation), '%P'),
                         from_=from_, to=to, state=state, width=width)

    def get(self) -> int:
        parent = self
        return int(parent.get())

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
        self.to_counter = Counter(self, from_=1,
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

class AddableCombobox(Frame):
    """ttk.Combobox с добавлением пользовательских значений"""
    def __init__(self, master: tkinter.Widget, val_validate=None, values: list[str] = None):
        super().__init__(master=master)

        if values is None:
            values = []

        self.values = values
        self.val_validate = val_validate

        text_var = StringVar()
        self.combobox = ttk.Combobox(self, textvariable=text_var, values=values)
        self.combobox.grid(row=0, column=0)

        self.btn = ttk.Button(self, text='+', state=constants.DISABLED, width=2, command=lambda: self.add_value(self.combobox.get()))
        self.btn.grid(row=0, column=1)
        #ToDo: доделать поведение кнопки
    def add_value(self, value):
        if self.val_validate is not None:
            if self.val_validate(value):
                self.values.append(value)
                self.combobox.configure(values=self.values)
            else:
                self.warning()
        else:
            self.values.append(value)
            self.combobox.configure(values=self.values)
    def warning(self):
        """Общий метод виджетов. Используется для маркировки неверно заполненных виджетов после пост-валидации."""
        pass

    def validation(self, char):
        return string_validation(char)

    def get(self):
        pass

class CustomCombobox(Frame):
    """Аналог ttk.Combobox с возможностью использования различных виджетов и кнопкой добавления значения"""
    #ToDo: доделать
    def __init__(self, master, widget, args: list = (), widgets: list = None):
        super().__init__(master=master)
 #ToDo: доделать фрейм и его расположение
        self.widgets = widgets
        if widgets is None:
            self.widgets = [] #ToDo: продумать

        self.btn = ttk.Button(self, text='▼', command=self._open, width=3)
        self.btn.grid(row=0, column=1, sticky=constants.E)

        self.main_entry = widget(master=self)
        self.main_entry.grid(row=0, column=0, sticky=constants.E)
        self.main_entry.configure(args)

    def _open(self):
        self.widgets_frm = Frame(self.master)
        self.widgets_frm.pack(anchor=constants.W)
        self.btn.configure(command=self._close)

        for i, widget in enumerate(self.widgets): #ToDo: переделать под forget
            wdg = widget(self.widgets_frm)
            wdg.grid(row=i, column=0)

    def _close(self):
        print('1')
        self.widgets_frm.destroy()
        self.btn.configure(command=self._open())

    def _add_widget(self, widget):
        #ToDo: добавление элемента в combobox
        pass

    def get(self):
        pass

class TwiceNumEntry(Frame):
    """Временный виджет, позже будет переделан"""
    def __init__(self, master):
        super().__init__(master=master)
        self.entry1 = NumEntry(self)
        self.entry1.grid(row=0, column=0)

        self.entry2 = NumEntry(self)
        self.entry2.grid(row=0, column=1)

    def get(self):
        return (self.entry1.get(), self.entry2.get())

class FourthNumEntry(Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.entry1 = NumEntry(self)
        self.entry1.grid(row=0, column=0)

        self.entry2 = NumEntry(self)
        self.entry2.grid(row=0, column=1)

        self.entry3 = NumEntry(self)
        self.entry3.grid(row=0, column=2)

        self.entry4 = NumEntry(self)
        self.entry4.grid(row=0, column=3)

    def get(self):
        return (self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())

if __name__ == '__main__':
    root = Tk()
    root.geometry('512x512')
    cbox = CustomCombobox(root, widget=Counter, widgets=[Counter, Counter, Counter])
    cbox.pack()
    root.mainloop()
