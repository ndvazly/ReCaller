import tkinter as tk
import customtkinter as ctk
from tkinter import Frame
from AppGlobals import Globals


class TopToolbar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self['bg'] = Globals().ToolbarBG

        # Add new channel strip button
        ctk.CTkButton(self, text='+').grid(row=0, column=self.grid_size()[0])
        ctk.CTkButton(self, text='p', font=Globals().HeaderFont, fg_color=Globals().ButtonBG,
                  command=self.parent.open_patchbays_window).grid(row=0, column=self.grid_size()[0])
        # ctk.CTkButton(self, text='+', font=Globals().HeaderFont, background=Globals().ButtonBG).grid(row=0,
        #                                                                                  column=self.grid_size()[0])
        # ctk.CTkButton(self, text='p', font=Globals().HeaderFont, background=Globals().ButtonBG,
        #           command=self.parent.open_patchbays_window).grid(row=0, column=self.grid_size()[0])

        self.pack(fill=tk.X, anchor=tk.N)
