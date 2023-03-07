import tkinter as tk
from AppGlobals import *
from GUI import TopToolbar, RackFrame, RevisionFrame, PatchBaysWindow
from App import StudioSetup


class ReCaller:
    def __init__(self):
        print('recaller')
        self.root = tk.Tk()
        self.root.title('ReCaller')
        self.root.geometry("960x600")
        self.root.configure(bg=Globals().DarkBG)
        self.toolbar = None
        self.main_frame = tk.Frame(self.root, bg='red')

        self.studio = StudioSetup.StudioSetup('Studio SetUp')

        self.make_window()

    def make_window(self):
        self.toolbar = TopToolbar.TopToolbar(self)

        self.main_frame.grid_columnconfigure(0, weight=50)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.stripslist_frame = RevisionFrame.RevisionFrame(self.main_frame)
        self.stripslist_frame.grid(row=0, column=0, sticky="nesw")

        self.gearlist_frame = RackFrame.RackFrame(self.main_frame, self.studio)
        self.gearlist_frame.grid(row=0, column=1, sticky="nesw")
        self.main_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.W)

    def open_patchbays_window(self):
        PatchBaysWindow.PatchBaysWindow(self)

    def go(self):
        self.root.mainloop()
