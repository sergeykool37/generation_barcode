from tkinter import *
from PIL import ImageTk, Image
from os import startfile
from datetime import datetime
from re import sub
from pylibdmtx.pylibdmtx import encode as encode_dm


class App:

    def __init__(self):
        def control_input_enter(event):
            self.txt_code.delete(END)
            print(self.txt_code.get('1.0', END))
            return 'break'

        def control_input_space(event):
            self.txt_code.delete(END)
            self.txt_sn.delete(END)
            self.txt_gtin.delete(END)
            return 'break'

        def focus_next_window(event):
            event.widget.tk_focusNext().focus()
            return ("break")

        def click_BC(event):
            self.btn_BC.invoke()
            return ('break')

        def click_DM(event):
            self.btn_DM.invoke()
            return ('break')

        def click_print(event):
            self.btn_print.invoke()
            return ('break')

        time = datetime.now()
        time = sub('\W+', '', str(time))[0:15]
        self.window = Tk()
        self.window.lift()
        self.window.geometry('600x600')
        self.window.title("Генератор DataMatrix")

        self.lbl = Label(self.window, text="GTIN", font=("Arial Bold", 10))
        self.lbl.place(x=10, y=10)
        self.txt_gtin = Entry(width=20, font=("Arial Bold", 8))
        self.txt_gtin.place(x=80, y=10)
        self.txt_gtin.focus()
        self.txt_gtin.bind('<space>', control_input_space)

        self.lbl = Label(self.window, text="SN", font=("Arial Bold", 10))
        self.lbl.place(x=10, y=40)
        self.txt_sn = Entry(width=20, font=("Arial Bold", 8))
        self.txt_sn.place(x=80, y=40)
        self.txt_sn.bind('<space>', control_input_space)

        self.lbl = Label(self.window, text="BARCODE", font=("Arial Bold", 10))
        self.lbl.place(x=10, y=80)
        self.txt_code = Text(height=3, width=40, font=("Arial Bold", 8))
        self.txt_code.place(x=80, y=80)
        self.txt_code.bind("<Tab>", focus_next_window)
        self.txt_code.bind('<Return>', control_input_enter)
        self.txt_code.bind('<space>', control_input_space)

        self.btn_BC = Button(self.window, text="BarCode", command=self.barcode)
        self.btn_BC.place(x=350, y=40)
        self.btn_BC.bind('<Return>', click_BC)

        self.btn_DM = Button(self.window, text="DataMatrix", command=self.data_matrix)
        self.btn_DM.place(x=350, y=80)
        self.btn_DM.bind('<Return>', click_DM)

        self.btn_print = Button(self.window, text="Печать", command=self.image_print)
        self.btn_print.place(x=435, y=80)
        self.btn_print.bind('<Return>', click_print)

        self.window.mainloop()

    def barcode(self):
        self.txt_code.delete(1.0, END)
        gtin = self.txt_gtin.get()
        sn = self.txt_sn.get()
        barcode = f'01{gtin}21{sn}91ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4='
        self.txt_code.insert(1.0, barcode)

    def data_matrix(self):
        self.name_image = generate_datamatrix(self.txt_code.get('1.0', END))
        self.lbl.configure(text="DataMatrix")
        canvas = Canvas(self.window, height=600, width=600)
        self.image = Image.open(self.name_image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image = canvas.create_image(100, 0, anchor='nw', image=self.photo)
        canvas.place(x=10, y=200)

    def get_image(self):
        return PhotoImage(self.name_image)

    def image_print(self):
        startfile(self.name_image, "print")


def generate_datamatrix(code):
    encoded = encode_dm(bytes(code.encode()))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    time = datetime.now()
    time = sub('\W+', '', str(time))[0:15]
    name_image = f"DataMatrix_{time}.png"
    img.save(name_image)
    return name_image


test_code = \
    '0104601808010398210000000000RH691ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4='
'0104601808010398210000000000RH691ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4='
app = App()
"04601808010398"
"0000000000RH6"
