import tkinter as tk
from AppGlobals import *
from GUI import TopToolbar, RackFrame, RevisionFrame, PatchBaysWindow
from GUI.GearEditor import GearEditor
from App import StudioSetup
from App.Revision import Revision


class ReCaller:

    def __init__(self):
        print('recaller')
        self.root = tk.Tk()
        self.root.title('ReCaller')
        self.root.geometry("960x600")
        self.root.configure(bg=Globals().DarkBG)
        self.toolbar = None
        self.main_frame = tk.Frame(self.root, bg='red')
        self.current_frame = None

        self.studio = StudioSetup.StudioSetup('Studio SetUp')
        self.revisions: list[Revision] = [Revision(self.studio)]
        self.make_window()

    def make_window(self):
        self.toolbar = TopToolbar.TopToolbar(self)

        self.main_frame.grid_columnconfigure(0, weight=50)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.show_revisions_frame()

        self.gearlist_frame = RackFrame.RackFrame(self, self.studio)
        self.gearlist_frame.grid(row=0, column=1, sticky="nesw")
        self.main_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.W)

    def refresh(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.gearlist_frame.destroy()
            self.gearlist_frame = RackFrame.RackFrame(self, self.studio)
            self.gearlist_frame.grid(row=0, column=1, sticky="nesw")

    def show_revisions_frame(self):
        self.refresh()
        self.revision_frame = RevisionFrame.RevisionFrame(self.main_frame, self.revisions[0])
        self.revision_frame.grid(row=0, column=0, sticky="nesw")
        self.current_frame = self.revision_frame

    def open_patchbays_window(self):
        PatchBaysWindow.PatchBaysWindow(self.main_frame, self.studio.patchbays)

    def edit_gear(self, gear):
        self.current_frame.destroy()
        self.gear_editor_frame = GearEditor(self)
        self.gear_editor_frame.grid(row=0, column=0, sticky="nesw")
        self.gear_editor_frame.edit_gear(gear)
        self.current_frame = self.gear_editor_frame

    def new_gear(self):
        self.edit_gear(self.studio.new_gear())

    def go(self):
        self.root.mainloop()
