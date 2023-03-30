from AppGlobals import Globals
from customtkinter import CTkScrollableFrame
import tkinter as tk
from GUI.StripUI import StripUI


class RevisionFrame(CTkScrollableFrame):
    def __init__(self, parent, revision):
        CTkScrollableFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.revision = revision

        self.make_strips()
        # self.pack(fill=tk.X)

    def make_strips(self):
        for s in self.revision.strips:
            StripUI(self, s)

    def show_strip_settings(self, strip):
        self.parent.show_strip_settings_frame(strip)
