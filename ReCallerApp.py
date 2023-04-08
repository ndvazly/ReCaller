import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import askokcancel, askyesnocancel
from tkinter import filedialog as fd
from AppGlobals import *
from GUI import TopToolbar, RackFrame, RevisionFrame, PatchBaysWindow
from GUI.GearEditor import GearEditor
from GUI.StripSettingsFrame import StripSettingsFrame
from App import StudioSetup
from App.Mix import Mix
import pickle


class ReCaller:
    def __init__(self):
        print('recaller')
        self.root = tk.Tk()
        self.root.title('ReCaller')
        self.root.geometry("1080x600")
        self.root.configure(bg=Globals().DarkBG)
        self.toolbar: TopToolbar.TopToolbar = None
        self.main_frame = tk.Frame(self.root, bg='red')
        self.current_frame = None

        try:
            with open('studio.pkl', 'rb') as f:
                self.studio: StudioSetup = pickle.load(f)
                self.studio.populate_patches()
                # self.studio.patchbays[0].print_points()
        except FileNotFoundError:
            self.studio = StudioSetup.StudioSetup('Studio SetUp')

        self.mix = Mix(self.studio)
        self.make_menu()
        self.make_window()

    def make_window(self):
        self.toolbar = TopToolbar.TopToolbar(self, self.mix)

        self.main_frame.grid_columnconfigure(0, weight=5)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.show_revisions_frame()

        self.gearlist_frame = RackFrame.RackFrame(self, self.studio)
        self.gearlist_frame.grid(row=0, column=1, sticky="nesw")
        self.main_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.W)

    def make_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='New', command=self.new_mix)
        file_menu.add_command(label='Open...', command=self.open_mix)
        file_menu.add_command(label='Save', command=self.save_mix)
        file_menu.add_command(label='Save As...', command=self.save_mix_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

        mix_menu = tk.Menu(menubar, tearoff=False)
        mix_menu.add_command(label='New Revision', command=self.new_revision)
        mix_menu.add_command(label='Duplicate Revision', command=lambda: self.new_revision(True))
        mix_menu.add_command(label='Delete Revision', command=self.delete_revision)
        mix_menu.add_command(label='Save As Text', command=self.save_rev_as_txt)
        menubar.add_cascade(label='Mix', menu=mix_menu)

        studio_menu = tk.Menu(menubar, tearoff=False)
        studio_menu.add_command(label='Add New PatchBay', command=self.studio.save)
        studio_menu.add_command(label='Open PatchBays Window', command=self.open_patchbays_window)
        studio_menu.add_separator()
        studio_menu.add_command(label='Save Studio Setup', command=self.studio.save)
        menubar.add_cascade(label='Studio', menu=studio_menu)

    def new_mix(self):
        confirm = askyesnocancel(title='Save Changes',
                    message='Save Changes?')
        if confirm is None:
            return
        if confirm:
            if not self.save_mix():
                return
        self.mix = None
        self.mix = Mix(self.studio)
        self.root.title('ReCaller - New Mix')
        self.toolbar.set_mix(self.mix)
        self.toolbar.disable_revision()
        self.show_revisions_frame()

    def save_mix(self) -> bool:
        if self.mix.get_filename() == '':
            return self.save_mix_as()
        self.mix.save()

    def save_mix_as(self) -> bool:
        filename = fd.asksaveasfile(filetypes=[('mix files', '*.mix')])
        if filename is None:
            return
        self.mix.set_filename(filename.name)
        if self.mix.get_filename() == '' or self.mix.get_filename() is None:
            return False
        self.mix.save()
        self.root.title(f'ReCaller - {self.mix.get_filename()}')

    def open_mix(self):
        filename = fd.askopenfilename(filetypes=[('mix files', '*.mix')])
        print(filename)
        with open(filename, 'rb') as f:
            self.mix = pickle.load(f)
            # self.mix.set_studio(self.studio)
            self.toolbar.set_mix(self.mix)
            self.root.title(f'ReCaller - {self.mix.get_filename()}')
            self.toolbar.enable_revision()
            self.show_revisions_frame()

    def new_revision(self, duplicate=False):
        rev_name = askstring('New Revision', 'Enter new revision name:')
        if rev_name is None:
            return
        if duplicate:
            self.mix.duplicate_revision(rev_name)
        else:
            self.mix.new_revision(rev_name)
        self.toolbar.enable_revision()
        self.show_revisions_frame()

    def delete_revision(self):
        confirm = askokcancel(title='Delete Revision',
                    message='Are you sure you want to delete current revision?')
        if confirm:
            self.mix.delete_selected_revision()
            if self.mix.is_empty():
                self.toolbar.disable_revision()
            else:
                self.toolbar.enable_revision()
            self.toolbar.select_revision(self.mix.get_current_revision_name())

    def save_rev_as_txt(self) -> bool:
        # filename = fd.asksaveasfile(defaultextension='mix')
        # self.mix.set_filename(filename.name)
        # if self.mix.get_filename() == '' or self.mix.get_filename() is None:
        #     return False
        self.mix.get_current_revision().revision_str()

    def refresh(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.gearlist_frame.destroy()
            self.gearlist_frame = RackFrame.RackFrame(self, self.studio)
            self.gearlist_frame.grid(row=0, column=1, sticky="nesw")

    def show_strip_settings_frame(self, strip):
        self.current_frame.destroy()
        strip_settings_frame = StripSettingsFrame(self, strip)
        strip_settings_frame.grid(row=0, column=0, sticky="nesw")
        self.current_frame = strip_settings_frame

    def show_revisions_frame(self):
        self.refresh()
        # self.revision_frame = RevisionFrame.RevisionFrame(self, self.revisions[0])
        self.revision_frame = RevisionFrame.RevisionFrame(self, self.mix.get_current_revision())
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
