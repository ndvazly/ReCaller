from AppGlobals import Globals
from tkinter import Frame
import tkinter as tk
from GUI.GearUI import GearUI
from App import StudioSetup


class RackFrame(Frame):
    def __init__(self, parent, studio):
        Frame.__init__(self, parent.main_frame)
        self.parent = parent
        self['bg'] = Globals().ToolbarBG
        self.studio: StudioSetup.StudioSetup = studio
        self.gear_frames: list(GearUI) = []
        self.grid_columnconfigure(0, weight=1)
        tk.Label(self, text='G E A R', font=Globals().HeaderFont, bg=self['bg'], fg=Globals().TextColor).grid(row=0, column=0)

        self.populate_gear_list()

    def add_gear_ui(self, gear_ui):
        col, row = self.grid_size()
        gear_ui.grid(row=row, column=0, sticky="ew")

    def edit_gear(self, gear):
        self.parent.edit_gear(gear)

    def populate_gear_list(self):
        for gear in self.studio.rack:
            self.add_gear_ui(GearUI(self, gear))
        # gear_ui_frame = GearUI.GearUI(self, self.studio.rack[0])
        # gear_ui_frame2 = GearUI.GearUI(self, self.studio.rack[0])
        # self.add_gear_ui(gear_ui_frame)
        # self.add_gear_ui(gear_ui_frame2)
