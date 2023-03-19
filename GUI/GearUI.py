import AppGlobals
from App import GearItem
from tkinter import Frame
import tkinter as tk
from tkinter import ttk


class GearUI(Frame):
    def __init__(self, parent, gear_item):
        self.bg = AppGlobals.Globals().DarkBG
        self.fg = AppGlobals.Globals().TextColor
        Frame.__init__(self, parent, bg=self.bg)
        self.parent = parent
        self.gear_item: GearItem.GearItem = gear_item
        self.configure(height=80, borderwidth=2, border=1,  highlightthickness=1, highlightbackground=self.fg)
        self.bind('<Double-Button-1>', lambda e: self.parent.edit_gear(self.gear_item))
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        tk.Label(self, text=self.gear_item.name, bg=self.bg, foreground=self.fg).pack(anchor=tk.CENTER, expand=False)
        # tk.Label(self, image=self.img, borderwidth=0).pack(column=0,sticky="e")
        if self.gear_item.img_file is not None:
            self.img = tk.PhotoImage(file=self.gear_item.img_file)
            tk.Label(self, image=self.img, borderwidth=0).pack(anchor=tk.CENTER, expand=False)

    # def dbl_click(self, event):
    #     self.parent.edit_gear(self.gear_item)
    #     print('dbl')