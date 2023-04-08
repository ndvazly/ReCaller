import tkinter
from tkinter import filedialog as fd
import customtkinter as ctk
from customtkinter import CTkFrame
from customtkinter import CTkScrollableFrame

import AppGlobals
from App.Point import Point

# import AppGlobals
from AppGlobals import *
from App.GearItem import GearItem
from GUI.PatchBaysWindow import PatchBaysWindow


class GearEditor(CTkScrollableFrame):
    def __init__(self, parent):
        ctk.CTkScrollableFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.gear: GearItem = None
        self.title_frame = None
        self.points_frame = None
        self.settings_frame = None
        self.gear_type_frame = None
        self.gear_width_frame = None
        self.pady = 5

        self.name_var = tkinter.StringVar()
        self.gear_type_var = tkinter.IntVar()
        self.gear_width_var = tkinter.IntVar()
        self.point_names_stringvar = []
        self.settings_widgets: list = []

        self.select_point_window: PatchBaysWindow = None
        self.add_range_start: Point = None
        self.add_range_end: Point = None
        self.make_title_frame()

    def make_title_frame(self):
        self.title_frame = ctk.CTkFrame(self)
        ctk.CTkButton(self.title_frame, text='x', width=20,
                      command=self.close).grid(row=0, column=1, sticky='e')
        ctk.CTkLabel(self.title_frame, text="Gear Editor", font=Globals().HeaderFont).grid(row=0, column=0)
        # ctk.CTkButton(self, text="Browse Image...", command=self.select_image).pack(pady=self.pady)
        self.title_frame.pack()

    def edit_gear(self, gear: GearItem):
        self.gear = gear
        self.name_var.set(gear.name)
        self.name_var.trace_add("write", self.set_gear_name)
        ctk.CTkEntry(self.title_frame, textvariable=self.name_var).grid(pady=self.pady)
        # ctk.CTkEntry(self, textvariable=self.name_var).pack(pady=self.pady)

        self.show_image()
        ctk.CTkButton(self.title_frame, text="Browse Image...", command=self.select_image).grid()
        self.make_gear_width_frame()
        self.make_gear_type_frame()
        self.make_settings_frame()
        self.make_points_frame()
        # print(gear.points)

    def show_image(self):
        if self.gear.img_file is not None:
            img = tkinter.PhotoImage(file=self.gear.img_file)
            ctk.CTkLabel(self.title_frame, image=img, text='').grid()
            # ctk.CTkLabel(self, image=img, text='').pack(anchor=ctk.CENTER, expand=False, pady=self.pady)

    def make_gear_type_frame(self):
        self.gear_type_frame = CTkFrame(self)
        ctk.CTkLabel(self.gear_type_frame, text='Gear Type').grid(sticky='nesw', columnspan=5)
        value_index = 0
        for t in AppGlobals.Categories:
            ctk.CTkRadioButton(self.gear_type_frame,
                               text=t.name,
                               variable=self.gear_type_var,
                               command=self.select_gear_type,
                               value=value_index).grid(row=1, column=value_index)
            value_index += 1
        self.gear_type_var.set(self.gear.category.value-1)
        self.gear_type_frame.pack(pady=10)

    def make_gear_width_frame(self):
        self.gear_width_frame = CTkFrame(self)
        ctk.CTkLabel(self.gear_width_frame, text='Gear Width').grid(sticky='nesw', columnspan=5)
        value_index = 0
        for t in AppGlobals.WidthType:
            ctk.CTkRadioButton(self.gear_width_frame,
                               text=t.name,
                               variable=self.gear_width_var,
                               command=self.select_gear_width,
                               value=value_index).grid(row=1, column=value_index)
            value_index += 1
        self.gear_width_var.set(self.gear.width_type.value-1)
        self.gear_width_frame.pack(pady=20)

    def make_points_frame(self):
        self.points_frame = CTkFrame(self)
        self.point_names_stringvar = []
        ctk.CTkButton(self.points_frame, text="+", command=self.select_point, width=1).grid(row=0, column=0)
        ctk.CTkButton(self.points_frame, text="...", command=self.select_range, width=1).grid(row=0, column=1)
        ctk.CTkLabel(self.points_frame, text="In/Outs").grid(row=0, column=2, columnspan=4)
        r = 1
        for p in self.gear.points:
            ctk.CTkButton(self.points_frame, text='-', width=1,
                          command=lambda x=p: self.delete_point(x)).grid(row=r, column=0)
            ctk.CTkLabel(self.points_frame, text=f'{r}').grid(row=r, column=1, ipadx=10, sticky="w")
            ctk.CTkButton(self.points_frame, text=f'{p.type.name}',
                          command=lambda x=p: self.change_inout(x)).grid(row=r, column=2, ipadx=10, sticky="w")
            ctk.CTkLabel(self.points_frame, text=f'Patch: {p.patch_id+1}').grid(row=r, column=3, ipadx=10)
            ctk.CTkLabel(self.points_frame, text=f'Point: {p.point+1}').grid(row=r, column=4, ipadx=10)
            name_StringVar = ctk.StringVar()
            name_StringVar.set(p.name)
            name_StringVar.trace_add("write", self.set_point_name)
            self.point_names_stringvar.append(name_StringVar)
            ctk.CTkEntry(self.points_frame, textvariable=name_StringVar).grid(row=r, column=5, ipadx=10)
            r += 1
        self.points_frame.pack()

    def make_settings_frame(self):
        self.settings_frame = CTkFrame(self)
        self.settings_widgets = []
        ctk.CTkButton(self.settings_frame, text="+", command=self.add_new_setting, width=1).grid(row=0, column=0)
        ctk.CTkLabel(self.settings_frame, text="Settings").grid(row=0, column=2, columnspan=4)
        r = 1
        self.settings_frame.pack(pady=40)
        for s in self.gear.settings:
            ctk.CTkButton(self.settings_frame, text='-', width=1,
                          command=lambda x=s: self.delete_setting(s)).grid(row=r, column=0)
            ctk.CTkLabel(self.settings_frame, text=f'{r}').grid(row=r, column=1, ipadx=10, sticky="w")
            name_entry = ctk.CTkEntry(self.settings_frame)
            name_entry.grid(row=r, column=2, ipadx=10, sticky="w")
            name_entry.insert(0, s['name'])
            value_combo = ctk.CTkComboBox(self.settings_frame,
                                          values=self.gear.get_settings_options_list(),
                                          state="readonly")
            value_combo.set(s['value'])
            value_combo.grid(row=r, column=3, ipadx=10)
            init_entry = ctk.CTkEntry(self.settings_frame)
            init_entry.grid(row=r, column=4, ipadx=10, sticky="w")
            init_entry.insert(0, s['init'])
            self.settings_widgets.append({'name': name_entry, 'value':value_combo, 'init': init_entry})
            r += 1

    def select_gear_type(self):
        self.gear.category = AppGlobals.Categories(self.gear_type_var.get()+1)
        print(self.gear.category)

    def select_gear_width(self):
        self.gear.width_type = AppGlobals.WidthType(self.gear_width_var.get()+1)
        print(self.gear.width_type)

    def add_new_setting(self):
        self.save_settings()
        self.gear.settings.append({'name': '', 'value': self.gear.get_settings_options_list()[0], 'init': '0'})
        self.refresh()

    def delete_setting(self, s):
        self.gear.settings.remove(s)
        self.refresh()

    def save_settings(self):
        index = 0
        for s in self.settings_widgets:
            self.gear.settings[index]['name'] = s['name'].get()
            self.gear.settings[index]['value'] = s['value'].get()
            self.gear.settings[index]['init'] = s['init'].get()
            index += 1

    def refresh(self):
        self.points_frame.destroy()
        self.settings_frame.destroy()
        self.add_range_start = None
        self.add_range_end = None
        self.make_settings_frame()
        self.make_points_frame()

    def select_image(self):
        filename = fd.askopenfilename()
        self.gear.img_file = filename
        self.show_image()

    def change_inout(self, point):
        if point.type == Socket.Input:
            point.type = Socket.Output
        else:
            point.type = Socket.Input
        self.refresh()

    def set_point_name(self, var, index, mode):
        print(var)
        for i in range(len(self.gear.points)):
            print(self.point_names_stringvar[i].get())
            self.gear.points[i].name = self.point_names_stringvar[i].get()

    def set_gear_name(self, var, index, mode):
        self.gear.name = self.name_var.get()

    def delete_point(self, p):
        self.gear.points.remove(p)
        self.refresh()

    def add_point(self, point):
        self.gear.add_point(point)
        self.parent.studio.populate_patches()
        self.refresh()

    def add_range(self, point):
        if self.add_range_start is None:
            self.add_range_start = point
            return
        if self.add_range_end is None:
            self.add_range_end = point
            for i in range(self.add_range_start.point, self.add_range_end.point+1):
                p = Point(point.patch_id, i, point.type)
                self.gear.add_point(p)
            self.parent.studio.populate_patches()
            self.refresh()

    def select_point(self):
        self.select_point_window = PatchBaysWindow(self, self.parent.studio.patchbays, mode='add')
        self.select_point_window.set_callback(self.add_point)

    def select_range(self):
        self.select_point_window = PatchBaysWindow(self, self.parent.studio.patchbays, mode='range')
        self.select_point_window.set_callback(self.add_range)

    def close(self):
        self.save_settings()
        self.parent.show_revisions_frame()