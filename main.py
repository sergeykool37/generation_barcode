from tkinter import *
from PIL import ImageTk, Image
from os import startfile
from datetime import datetime
from re import sub
from pylibdmtx.pylibdmtx import encode as encode_dm
import base64

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

        def unable():
            self.txt_gtin.config(state=NORMAL)
            self.txt_sn.config(state=NORMAL)
            self.txt_gt_sn.delete(0,END)
            self.txt_gt_sn.config(state=DISABLED)
        def disable():
            self.txt_gt_sn.config(state=NORMAL)
            self.txt_gtin.delete(0,END)
            self.txt_gtin.config(state=DISABLED)
            self.txt_sn.delete(0, END)
            self.txt_sn.config(state=DISABLED)





        time = datetime.now()
        time = sub('\W+', '', str(time))[0:15]
        self.window = Tk()
        self.window.lift()
        self.window.geometry('600x600')
        self.window.title("Генератор DataMatrix")

        self.var=IntVar()
        self.var.set(0)

        self.input_style_gtinsgtin=Radiobutton(text="GTIN SN",variable=self.var,value=0,command=unable)
        self.input_style_gtinsgtin.pack()
        self.input_style_gtinsgtin.place(x=10, y=5)

        self.input_style_gtinsn = Radiobutton(text="GTIN\SN", variable=self.var, value=1,command=disable)

        self.input_style_gtinsn.pack()
        self.input_style_gtinsn.place(x=110, y=5)

        x0=0
        y0=20
        self.lbl = Label(self.window, text="GTIN", font=("Arial Bold", 10))
        self.lbl.place(x=10+x0, y=10+y0)
        self.txt_gtin = Entry(self.window,width=20, font=("Arial Bold", 8),)
        self.txt_gtin.place(x=80+x0, y=10+y0)
        self.txt_gtin.focus()
        self.txt_gtin.bind('<space>', control_input_space)



        self.lbl = Label(self.window, text="SN", font=("Arial Bold", 10))
        self.lbl.place(x=10+x0, y=40+y0)
        self.txt_sn = Entry(width=20, font=("Arial Bold", 8))
        self.txt_sn.place(x=80+x0, y=40+y0)
        self.txt_sn.bind('<space>', control_input_space)

        self.lbl = Label(self.window, text="GTIN\SN", font=("Arial Bold", 10))
        self.lbl.place(x=10 + x0, y=65 + y0)
        self.txt_gt_sn = Entry(width=40, font=("Arial Bold", 8))
        self.txt_gt_sn.place(x=80 + x0, y=65 + y0)
        self.txt_gt_sn.bind('<space>', control_input_space)
        self.txt_gt_sn.config(state=DISABLED)




        self.lbl = Label(self.window, text="BARCODE", font=("Arial Bold", 10))
        self.lbl.place(x=10+x0, y=100+y0)
        self.txt_code = Text(height=3, width=40, font=("Arial Bold", 8))
        self.txt_code.place(x=80+x0, y=100+y0)
        self.txt_code.bind("<Tab>", focus_next_window)
        self.txt_code.bind('<Return>', control_input_enter)
        self.txt_code.bind('<space>', control_input_space)

        self.lbl = Label(self.window, text="BASE64", font=("Arial Bold", 10))
        self.lbl.place(x=10 + x0, y=155 + y0)
        self.txt_bs64 = Text(height=3, width=40, font=("Arial Bold", 8))
        self.txt_bs64.place(x=80 + x0, y=155+ y0)
        self.txt_bs64.config(state=DISABLED)

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
        gtin_sn=self.txt_gt_sn.get()
        if len(gtin)==14 and len(sn)==13:
            barcode = f'01{gtin}21{sn}91ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4='
        elif len(gtin_sn)==27:
            barcode = f'01{gtin_sn[0:14]}21{gtin_sn[14::]}91ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4='
        else:
            barcode = f'НЕКОРРЕКТНЫЙ БАРКОД'
        self.txt_code.insert(1.0, barcode)

    def data_matrix(self):
        self.name_image = generate_datamatrix(self.txt_code.get('1.0', END))

        self.txt_bs64.config(state=NORMAL)
        text=self.txt_code.get('1.0', END).encode("UTF-8")
        text=base64.b64encode(text)
        self.txt_bs64.insert(1.0,text.decode("UTF-8"))
        self.txt_bs64.config(state=DISABLED)

        canvas = Canvas(self.window, height=600, width=600)
        self.image = Image.open(self.name_image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image = canvas.create_image(100, 0, anchor='nw', image=self.photo)
        canvas.place(x=10, y=250)

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
"010460180801039210000000000RH691ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4="
"0104601808010398210000000000RH691ee0592pAY7tJHS6k1dwqQh6PKjTB8nmaVbBfuGpIx/FAcLMc4="