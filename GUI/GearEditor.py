import tkinter
from tkinter import filedialog as fd
import customtkinter as ctk
from customtkinter import CTkFrame
from customtkinter import CTkScrollableFrame
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
        self.pady = 5

        self.name_var = tkinter.StringVar()
        self.point_names_stringvar = []
        self.select_point_window: PatchBaysWindow = None
        self.add_range_start: Point = None
        self.add_range_end: Point = None
        self.make_title_frame()

    def make_title_frame(self):
        self.title_frame = ctk.CTkFrame(self)
        ctk.CTkButton(self.title_frame, text='x', width=20,
                      command=self.parent.show_revisions_frame).grid(row=0, column=1, sticky='e')
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
        self.make_points_frame()
        # print(gear)

    def show_image(self):
        if self.gear.img_file is not None:
            img = tkinter.PhotoImage(file=self.gear.img_file)
            ctk.CTkLabel(self.title_frame, image=img, text='').grid()
            # ctk.CTkLabel(self, image=img, text='').pack(anchor=ctk.CENTER, expand=False, pady=self.pady)

    def make_points_frame(self):
        self.points_frame = CTkFrame(self)
        self.point_names_stringvar = []
        ctk.CTkButton(self.points_frame, text="+", command=self.select_point, width=1).grid(row=0, column=0)
        ctk.CTkButton(self.points_frame, text="...", command=self.select_range, width=1).grid(row=0, column=1)
        ctk.CTkLabel(self.points_frame, text="In/Outs").grid(row=0, column=2, columnspan=4)
        r = 1
        for p in self.gear.points:
            ctk.CTkButton(self.points_frame, text='-', width=1,
                          command=lambda x=p: self.delete_point(p)).grid(row=r, column=0)
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

    def refresh(self):
        self.points_frame.destroy()
        self.add_range_start = None
        self.add_range_end = None
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
