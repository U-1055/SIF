from tkinter import Tk, Frame, messagebox
from tkinter.constants import *
from customtkinter import CTkFrame, CTkLabel, CTkTextbox, CTkCheckBox, CTkButton
from datetime import datetime
from program_logic import Preparer

root = Tk()

width = root.winfo_screenwidth() // 100
height = root.winfo_screenheight() // 100

root.geometry(f'{width * 70}x{height * 70}+{width * 15}+{height * 15}')
root.title('Система фильтрации изображений')

frm_color_1 = '#D1D1D1'
frm_color_2 = '#E1E1E1'
frm_color_3 = '#A6A2A3'
btn_color_en = '#EFF1FE'
btn_color_dis = '#ABABAB'
border_color = '#7F7E83'

root_frm = Frame(root, bg=frm_color_1)
root_frm.pack(fill=BOTH, expand=True)

class Interface():
    def __init__(self):
        self.main_frm = Frame(root_frm, bg=frm_color_2)
        self.main_frm.grid()

        self.main_window()

    def main_window(self):
        pass

    def start_preparing(self, params):

        try:
            Preparer(params)
        except:
            messagebox.showerror('Непредвиденная ошибка обработки', f'Возникла непредвиденная ошибка обработки набора')

class Validator():
    def __init__(self):
        pass

class MessageWindow():

    def __init__(self):
        self.main_frm = Frame(root_frm, bg=frm_color_2)
        self.main_frm.grid()

    def widgets(self):
        self.message_box = CTkTextbox(self.main_frm, border_color=border_color)
        self.message_box.grid()

    def show_message(self, message: str):
        msg_time = datetime.now()

        pass

if __name__ == '__main__':
    Interface()
    root.mainloop()