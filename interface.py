from tkinter import filedialog, Frame, Canvas, Tk, constants, messagebox, Button, Text
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkTextbox
from main import define_image
from PIL import Image, ImageTk

root = Tk()

width = root.winfo_screenwidth() // 100
height = root.winfo_screenheight() // 100

root_width = width * 50
root_height = height * 50

root.geometry(f'{root_width}x{root_height}+{width * 25}+{height * 25}')
root.title('Интерфейс нейронной сети')
root.resizable(False, False)
icon = Image.open('icon.png')
icon = ImageTk.PhotoImage(image=icon)
root.iconphoto(True, ImageTk.PhotoImage(file='icon.png'))

class Interface():

    def __init__(self):

        self.main_frm = Frame(root, bg='#DBEDED')
        self.main_frm.pack(fill=constants.BOTH, expand=True)

        self.frm1 = CTkFrame(self.main_frm, fg_color='#E1E1E3', border_color='Black')
        self.frm1.grid(column=1, row=1)

        self.main_frm.columnconfigure(0, weight=1)
        self.main_frm.columnconfigure(1, weight=1)
        self.main_frm.columnconfigure(2, weight=1)

        self.main_frm.rowconfigure(0, weight=1)
        self.main_frm.rowconfigure(1, weight=1)
        self.main_frm.rowconfigure(2, weight=1)

        self.cvs = Canvas(self.frm1, relief=constants.FLAT, highlightthickness=2, highlightbackground='#D4CED2')
        self.cvs.grid(column=0, row=3, columnspan=2)

        self.inp_button = CTkButton(self.frm1, fg_color='#93BD62', text='Загрузить', command=self.load_image, corner_radius=2,
                                        hover_color='#A5D46E', text_color='Black')
        self.inp_button.grid(column=0, row=0, sticky=constants.E)

        self.answ_filed = CTkLabel(self.frm1, fg_color='#D4CED2', text='\n Загрузите изображение \n', text_color='Black', corner_radius=2,
                                       font=('Arial', 15, 'bold'))
        self.answ_filed.grid(column=0, row=1, columnspan=4, sticky=constants.W+constants.E)

        self.clear_btn = CTkButton(self.frm1, fg_color='#D41D05', text='Удалить', text_color_disabled='#545454', state=constants.DISABLED,
                                       command=self.delete, corner_radius=2, hover_color='#FF2306', text_color='Black')
        self.clear_btn.grid(column=1, row=0, sticky=constants.W)

        self.images_on_cvs = 0

    def load_image(self):

        if self.answ_filed.cget('text') != '\n Загрузите изображение \n':
            self.more_inf_btn.destroy()

        file_path = filedialog.askopenfilename(title='Выберите изображение для загрузки в нейронную сеть',
                                               filetypes=[('JPEG-файлы', '*.*')])

        if file_path != '':
            try:

                image = Image.open(fr'{str(file_path)}', 'r')
                image = image.resize((160, 160))
                self.cvs_image = ImageTk.PhotoImage(image)

                if self.images_on_cvs != 0:
                    self.cvs.delete(self.img_tag)
                    self.images_on_cvs = 0

                self.img_tag = self.cvs.create_image(self.cvs.winfo_width()//2, self.cvs.winfo_height()//2, image=self.cvs_image)

                self.inp_button.configure(command=lambda img=image: self.get_answer(image=img), text='Ввести в сеть')
                self.clear_btn.configure(state=constants.NORMAL)
                self.answ_filed.configure(text='\n Введите изображение в сеть \n')

                self.images_on_cvs = 1
            except:
                messagebox.showerror('Ошибка', f'Не удалось открыть файл по адресу:{file_path}')

    def get_answer(self, image):

        self.inp_button.configure(text='Загрузить', command=self.load_image)

        answer = define_image(image)

        self.letter = answer[0]
        self.tensor = answer[1]
        self.max_val = answer[2]
        self.index = self.tensor.argmax().item()

        self.answ_filed.configure(text=f' Ответ: {self.letter} ')

        self.more_inf_btn = Button(self.frm1, bg='#E1E1E3', relief=constants.FLAT, text='Дополнительная информация об ответе',
                                       fg='Black', command=self.show_info, cursor='hand2')
        self.more_inf_btn.grid(column=0, row=2, columnspan=2, sticky=constants.W + constants.E)

        self.tensor = self.delete_spaces(str(self.tensor))

    def delete_spaces(self, text):
        while '  ' in text:
            text = text.replace('  ', ' ')

        text = list(text)
        spaces = 0
        deleting_chars = ['(', ')', '[', ']', '\n', 't', 'e', 'n', 's', 'o', 'r']

        for i, char in enumerate(text):
            if text[i] in deleting_chars:
                text[i] = ''

        return ''.join(text)

    def show_info(self):

        self.info_frm = CTkFrame(self.main_frm, fg_color='#E1E1E3')
        self.info_frm.grid(column=2, row=1, sticky=constants.W)

        num_lbl = CTkLabel(self.info_frm, fg_color='#E1E1E3', text=f'Индекс большего элемента:\n {self.index}')
        num_lbl.grid(column=0, row=0, columnspan=3)

        tensor_lbl = CTkLabel(self.info_frm, fg_color='#E1E1E3', text='Выходной тензор:')
        tensor_lbl.grid(column=1, row=1)

        tensor_wdgt = CTkTextbox(self.info_frm, fg_color='White', border_width=1, wrap='word', text_color='#999999')
        tensor_wdgt.grid(column=0, row=2, columnspan=3)
        tensor_wdgt.insert(1.0, self.tensor)
        tensor_wdgt.configure(state=constants.DISABLED)

        self.more_inf_btn.configure(command=self.hide_info, text='Скрыть информацию', relief="sunken", bg='#F5F5F7')
        self.clear_btn.configure(state=constants.DISABLED)
        self.inp_button.configure(state=constants.DISABLED)

        Highlight(self.max_val, tensor_wdgt)

    def hide_info(self):

        self.info_frm.destroy()

        self.more_inf_btn.configure(command=self.show_info, text='Дополнительная информация об ответе', relief='flat', bg='#E1E1E3')
        self.clear_btn.configure(state=constants.NORMAL)
        self.inp_button.configure(state=constants.NORMAL)
    def delete(self):

        if self.answ_filed.cget('text') != '\n Введите изображение в сеть \n':
            self.more_inf_btn.destroy()

        self.cvs.delete(self.img_tag)

        self.clear_btn.configure(state=constants.DISABLED)
        self.inp_button.configure(command=self.load_image, text='Загрузить')
        self.answ_filed.configure(text='\n Загрузите изображение \n')

class Highlight():

    def __init__(self, max_val, widget):

        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

        self.max_val = str(max_val)
        self.text = list(widget.get(1.0, constants.END))
        self.widget = widget

        self.highlight()

    def highlight(self):

        self.widget.tag_config('int', foreground='#2A5CDF')
        self.widget.tag_config('max', foreground='#2A5CDF', underline=True)

        for num in self.numbers:
            idx = 1.0
            while idx:
                idx = self.widget.search(num, idx, constants.END)
                if idx:
                    self.widget.tag_add('int', idx)
                    idx = '%s+%dc' % (idx, 1)

        pos = self.widget.search(self.max_val, 1.0, constants.END)
        self.widget.tag_add('max', pos, f'{pos}+{len(self.max_val)+1}c')

Interface()
root.mainloop()