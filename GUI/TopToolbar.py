import tkinter as tk
from tkinter.simpledialog import askstring
import customtkinter as ctk
from tkinter import Frame
from AppGlobals import Globals, WidthType
from App.Mix import Mix


class TopToolbar(Frame):
    def __init__(self, parent, mix):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.mix = mix
        self['bg'] = Globals().ToolbarBG
        self.btn_width = 20

        # Add new channel strip button
        self.new_mono_strip_btn = ctk.CTkButton(self, text='+',
                                                command=lambda: self.new_channel_strip(WidthType.Mono),
                                                state=tk.DISABLED, width=self.btn_width)
        self.new_mono_strip_btn.grid(row=0, column=self.grid_size()[0])
        self.new_stereo_strip_btn = ctk.CTkButton(self, text='++',
                                                command=lambda: self.new_channel_strip(WidthType.Stereo),
                                                state=tk.DISABLED, width=self.btn_width)
        self.new_stereo_strip_btn.grid(row=0, column=self.grid_size()[0])

        self.revisions_combo = ctk.CTkComboBox(self,
                                               values=[''],
                                               state=tk.DISABLED,
                                               command=lambda choice: self.select_revision(choice))
        self.revisions_combo.grid(row=0, column=self.grid_size()[0])

        # Open PatchBays Window
        ctk.CTkButton(self, text='p', font=Globals().HeaderFont, fg_color=Globals().ButtonBG, width=self.btn_width,
                  command=self.parent.open_patchbays_window).grid(row=0, column=self.grid_size()[0])

        # New Revision Button
        ctk.CTkButton(self, text='r+', font=Globals().HeaderFont, fg_color=Globals().ButtonBG, width=self.btn_width,
                      command=self.parent.new_revision).grid(row=0, column=self.grid_size()[0])

        self.pack(fill=tk.X, anchor=tk.N)

    def set_mix(self, mix: Mix):
        self.mix: Mix = mix

    def new_channel_strip(self, width):
        strip_name = askstring('New Channel Strip', 'Enter Channel Strip Name:')
        if strip_name is None:
            return
        self.mix.get_current_revision().new_strip(strip_name, width)
        self.parent.show_revisions_frame()

    def enable_revision(self):
        self.new_mono_strip_btn.configure(state=1)
        self.new_stereo_strip_btn.configure(state=1)
        self.revisions_combo.configure(state="readonly")
        self.revisions_combo.configure(values=self.mix.get_revisions_names_list())
        self.revisions_combo.set(self.mix.get_current_revision_name())
        self.revisions_combo.bind('<<ComboboxSelected>>', self.select_revision)

    def disable_revision(self):
        self.new_mono_strip_btn.configure(state=tk.DISABLED)
        self.new_stereo_strip_btn.configure(state=tk.DISABLED)
        self.revisions_combo.configure(state=tk.DISABLED)

    def select_revision(self, choice):
        self.mix.select_revision_by_name(choice)
        self.parent.show_revisions_frame()
