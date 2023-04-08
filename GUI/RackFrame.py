import AppGlobals
from AppGlobals import Globals
from tkinter import Frame
from customtkinter import CTkScrollableFrame
import customtkinter as ctk
from GUI.GearUI import GearUI
from App import StudioSetup


class RackFrame(CTkScrollableFrame):
    def __init__(self, parent, studio):
        CTkScrollableFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.configure(fg_color=Globals().ToolbarBG)
        self.studio: StudioSetup.StudioSetup = studio
        self.gear_frames: list(GearUI) = []
        self.content_frame = None
        self.filters = {}

        for category in AppGlobals.Categories:
            self.filters[category.name] = ctk.BooleanVar()
            self.filters[category.name].set(True)

        ctk.CTkButton(self, text='+', command=self.new_gear, width=10).grid(row=0, column=0, sticky='w')
        ctk.CTkLabel(self, text='G E A R', font=Globals().HeaderFont,
                 fg_color=self['bg']).grid(row=0, column=0)
        self.make_filters_frame()
        self.populate_gear_list()

    def make_filters_frame(self):
        frame = ctk.CTkFrame(self)
        row = 0
        col = 0
        for f in self.filters:
            ctk.CTkCheckBox(frame, text=f,
                            variable=self.filters[f],
                            command=self.filter_change).grid(row=row, column=col)
            col += 1
            row += (col % 3 == 0)
            col %= 3

        frame.grid(row=1, column=0)

    def filter_change(self):
        self.populate_gear_list()

    def new_gear(self):
        self.parent.new_gear()
        self.populate_gear_list()

    def add_gear_ui(self, gear_ui):
        col, row = self.content_frame.grid_size()
        gear_ui.grid(row=row, column=0, sticky="ew")

    def edit_gear(self, gear):
        self.parent.edit_gear(gear)

    def populate_gear_list(self):
        if self.content_frame is not None:
            self.content_frame.destroy()
        self.content_frame = ctk.CTkFrame(self)
        for gear in self.studio.rack:
            category = gear.category.name
            if self.filters[category].get():
                self.add_gear_ui(GearUI(self, gear))
        self.content_frame.grid()
