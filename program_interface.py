import time
from tkinter import Tk, Frame, messagebox, ttk, StringVar
from tkinter.constants import *
from customtkinter import CTkEntry, CTkLabel, CTkTextbox, CTkCheckBox, CTkButton, CTkProgressBar
from datetime import datetime
from threading import Thread

from widgets import EntryButton, NumEntry, Counter, FromTo, AddableCombobox, TwiceNumEntry, FourthNumEntry, CustomCombobox

root = Tk()

width = root.winfo_screenwidth() // 100
height = root.winfo_screenheight() // 100

root.geometry(f'{width * 70}x{height * 70}+{width * 15}+{height * 15}')
root.title('Система фильтрации изображений')

frm_color_1 = '#D1D1D1'
frm_color_2 = '#E1E1E1'
frm_color_3 = '#A6A2A3'
btn_color_en = '#3299FF'
btn_color_dis = '#ABABAB'
border_color = '#7F7E83'

title_font = ('Arial', 18)
common_font = ('Arial', 14)

root.configure(background=frm_color_1)

root.grid_columnconfigure(index=0, weight=3)
root.grid_rowconfigure(index=0, weight=4)


def preparer_stub():
    time.sleep(5)
    return

class MainWindow:
    """Основное окно. Требуется для ввода параметров и запуска обработки."""
    def __init__(self):
        self.in_progress = 'Выполняется...'
        self.start = 'Начать обработку'

        self.main_frm = Frame(bg=frm_color_2, highlightthickness=5, highlightcolor=frm_color_3)
        self.main_frm.grid(row=0, column=0)

        self.main_lbl = CTkLabel(self.main_frm, text='Параметры обработки', font=title_font)
        self.main_lbl.grid(column=0, row=0, columnspan=6)

        main_param_lbl = CTkLabel(self.main_frm, text='Основные параметры')
        main_param_lbl.grid(row=1, column=0, columnspan=6)

        filters_param_lbl = CTkLabel(self.main_frm, text='Фильтры')

        help_btn = CTkButton(self.main_frm, text='Справка')
        help_btn.grid(row=8, column=0, columnspan=2, sticky=W + E)

        self.start_btn = CTkButton(self.main_frm, fg_color=btn_color_en, text=self.start, command=self.start_preparing)
        self.start_btn.grid(row=8, column=4, columnspan=2, sticky=W + E)

        self.prep_stat = ttk.Progressbar(self.main_frm)
        self.prep_stat.grid(row=8, column=2, columnspan=2, sticky=W+E)

        self.text = CTkTextbox(self.main_frm)
        self.text.grid(row=9, column=0, columnspan=4, sticky=W+E)

        self.params()

    def params(self): #ToDo: дописать виджеты
        """Размещает виджеты параметров обработки. В словаре params_list ключами являются названия параметров, отображаемых в интерфейсе,
           значениями - виджеты, принимающие их. """

        self.params_list = {'Целевая папка:': [EntryButton(self.main_frm, btn_color_en), 'input_dir'],
                       'Обработать изображения:': [FromTo(self.main_frm), 'total_images'],
                       'Процессы:': [Counter(self.main_frm, state='readonly', from_=1, to=8, width=3), 'threads']}

        self.filters_list = {'Обработать:': [Counter(self.main_frm, from_=1, to=50000), 'prepared'],
                        'Формат:': [ttk.Combobox(self.main_frm, values=['JPEG', 'PNG', 'BMP'], state='readonly'), 'format'],
                        'Разрешение:': [CustomCombobox(self.main_frm, widget=TwiceNumEntry), 'size'],
                        'Размер:': [AddableCombobox(self.main_frm), 'weight'],
                        'Название:': [AddableCombobox(self.main_frm), 'name'],
                        'Расширение:': [AddableCombobox(self.main_frm), 'extension'],
                        'Кратность номера:': [AddableCombobox(self.main_frm), 'number_multiplicity'],
                        'Содержание:': [AddableCombobox(self.main_frm, values=['A', 'N', 'F']), 'content'],
                        'Изменить размер:': [CustomCombobox(self.main_frm, widget=TwiceNumEntry), 'resize'],
                        'Обрезать:': [CustomCombobox(self.main_frm, widget=FourthNumEntry), 'crop'],
                        'Конвертировать:': [ttk.Combobox(self.main_frm, values=['JPEG', 'PNG', 'BMP'], state='readonly'), 'reformat'],
                        'Переименовать:': [ttk.Entry(self.main_frm), 'rename'],
                        'Выгрузить в': [EntryButton(self.main_frm, btn_color_en), 'output_dir']}

        column = 0
        for key in list(self.params_list.keys()):
            label = CTkLabel(self.main_frm, text=key)
            label.grid(row=2, column=column, sticky=W)

            widget = self.params_list[key][0]
            widget.grid(row=2, column=column + 1, sticky=W+E)

            self.params_list[key][0] = widget
            column += 2

        column = 0
        for i, key in enumerate(list(self.filters_list.keys())):
            if column == 6:
                column = 0

            label = CTkLabel(self.main_frm, text=key)
            label.grid(row=(i // 3) + 3, column=column, sticky=W)

            if len(self.filters_list[key]) > 0: # Введено временно, до готовности всех виджетов
                widget = self.filters_list[key][0] #ToDo: доделать размещение
                widget.grid(row=(i // 3) + 3, column=column + 1, sticky=W+E)
                self.filters_list[key][0] = widget

            column += 2
        # Создание флажков save и delete
        self.save = StringVar(value='1')
        self.delete = StringVar(value='0')

        save_check = ttk.Checkbutton(self.main_frm, variable=self.save, text='Выгружать изображения')
        save_check.grid(row=7, column=3, sticky=W)

        delete_check = ttk.Checkbutton(self.main_frm, variable=self.delete, text='Удалять изображение из целевой папки')
        delete_check.grid(row=7, column=4, sticky=W, columnspan=2)

    def start_preparing(self):
        """Начинает обработку. Импортирует Preparer, меняет параметры кнопки, запускает отсчёт времени выполнения."""
      #ToDo: время обработки
      #  try:
        self.start_time = time.time()
        self.start_btn.configure(text=self.in_progress, state=DISABLED, fg_color=btn_color_dis)
        thread = Thread(target=self.prep_stat.start)
        thread.start()
        self.text.insert(END, '\nНачало обработки...')
        prep_thread = Thread(target=self.starting)
        prep_thread.start()
        self.counting = False
      #  except:
            #messagebox.showerror('Непредвиденная ошибка обработки', f'Возникла непредвиденная ошибка обработки набора'

    def starting(self):
        from program_logic import Preparer
        Preparer(
            [{'input_dir': r"C:\Users\filat\OneDrive\Документы\Проект\target_dir", 'total_images': '', 'threads': 2,
              'filters':  # -----------------------------------------------------------------------------------------
                  [
                      {'format': '',
                       'size': '',
                       'weight': '',
                       'name': '',
                       'extension': '',
                       'number_multiplicity': '',
                       'content': ['A', 'N', 'F'],
                       'prepared': '',
                       'actions':  # -----------------------------------------------------------------------------------
                           {'resize': '',
                            'crop': '',
                            'reformat': 'PNG',
                            'rename': '',
                            'save': True,
                            'delete': False,
                            'output_dir': r"C:\Users\filat\OneDrive\Документы\Проект\output_dir"}}
                  ]}])
        self.prep_stat.stop()
        self.start_btn.configure(text=self.start, state=NORMAL, fg_color=btn_color_en)
        self.text.insert(END, f'\nКонец обработки\nВремя: {round(time.time() - self.start_time)} c.')
class MessageWindow:

    def __init__(self):
        self.main_frm = Frame(root, bg=frm_color_2)
        self.main_frm.grid(row=1, column=0, sticky=W)
        self.widgets()

    def widgets(self):

        self.message_box = CTkTextbox(self.main_frm, border_color=border_color, state=DISABLED, border_width=5)
        self.message_box.grid(row=1, column=0, columnspan=2, sticky=W+E)

        self.progress_bar = CTkProgressBar(self.main_frm)# псевдокод
        self.progress_bar.grid(row=0, sticky=W+E)

        self.error_tag = self.message_box.tag_config('error')
        self.warning_tag = self.message_box.tag_config('warning')

    def update_progress(self, value: float):
        self.progress_bar.set(value)

    def print_message(self, message: str, message_type: str = 'message'):
        self.message_box.insert(END, message)
        if message_type != 'message':
            self.message_box.tag_add(message_type, END, f'{END} + {len(message)}s%')
class HelpWindow():
    def __init__(self):
        pass

if __name__ == '__main__':
    main_window = MainWindow()
    root.mainloop()