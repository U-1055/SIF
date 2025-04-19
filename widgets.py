import tkinter
from tkinter import Frame, Tk, filedialog, Button, GROOVE, RIDGE, StringVar
from customtkinter import CTkEntry


class EntryButton(Frame):
    """Виджет, при нажатии на кнопку вводящий в Entry путь к выбранной папке."""
    def __init__(self, master: tkinter.Widget, bg='White'):
        super().__init__(master=master)

        self.entry = CTkEntry(self)
        self.entry.grid(row=0, column=0)

        self.button = Button(self, text='...', relief=RIDGE, bg=bg, overrelief=GROOVE, command=self.load_path)
        self.button.grid(row=0, column=1)

    def load_path(self):

        path = filedialog.askdirectory(title='Выберите папку')
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
        super().__init__(master=master, textvariable=self.text, validate='key', validatecommand=(master.register(self.validate), '%P'))

    def get(self) -> str:
        if self.get()[0] == '0':
            return self.get[:-1]
        return self.get()

    def validate(self, char): #ToDo: доделать валидацию
        print(char)
        if char not in self.allowed_chars:
            return False


if __name__ == '__main__':
    root = Tk()
    root.geometry('512x512')
    numentry = NumEntry(root)
    numentry.pack()
    root.mainloop()
