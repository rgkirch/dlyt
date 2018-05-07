from tkinter import *
from tkinter import ttk
from dlyt import *


def assertion(lb, result):
    result = map(int, lb.curselection())


def test_download_all_button_callback():
    root = Tk()
    some = -1
    lb = Listbox(root, selectmode=EXTENDED)
    lb.insert(END, "hello")
    lb.insert(END, "there")
    lb.pack()
    b = Button(root, text='assert', command=lambda: assertion(lb, some))
    b.pack()
    root.mainloop()
    assert some == [0]
