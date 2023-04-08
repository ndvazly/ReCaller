import customtkinter as ctk
from customtkinter import CTkScrollableFrame

import AppGlobals
from GUI.StripUI import StripUI


class RevisionFrame(CTkScrollableFrame):
    def __init__(self, parent, revision):
        CTkScrollableFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.revision = revision

        if self.revision is not None:
            ctk.CTkLabel(self, text=self.revision.name, font=AppGlobals.Globals().HeaderFont).pack()
            self.make_strips()

    def make_strips(self):
        for s in self.revision.strips:
            StripUI(self, s)

    def show_strip_settings(self, strip):
        self.parent.show_strip_settings_frame(strip)
