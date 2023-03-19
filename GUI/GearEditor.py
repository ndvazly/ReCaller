import tkinter
import customtkinter as ctk
from customtkinter import CTkFrame
from App.Point import Point

# import AppGlobals
from AppGlobals import *
from App.GearItem import GearItem
from GUI.PatchBaysWindow import PatchBaysWindow


class GearEditor(CTkFrame):
    def __init__(self, parent):
        CTkFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.gear: GearItem = None
        self.points_frame = None

        self.name_var = tkinter.StringVar()
        self.point_names_stringvar = []
        self.select_point_window: PatchBaysWindow = None
        self.add_range_start: Point = None
        self.add_range_end: Point = None
        ctk.CTkLabel(self, text="Gear Editor").pack()

    def edit_gear(self, gear: GearItem):
        self.gear = gear
        self.name_var.set(gear.name)
        ctk.CTkEntry(self, textvariable=self.name_var).pack()
        self.make_points_frame()
        # print(gear)

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
            name_StringVar.trace_add("write", self.set_name)
            self.point_names_stringvar.append(name_StringVar)
            ctk.CTkEntry(self.points_frame, textvariable=name_StringVar).grid(row=r, column=5, ipadx=10)
            r += 1
        self.points_frame.pack()

    def refresh(self):
        self.points_frame.destroy()
        self.make_points_frame()

    def change_inout(self, point):
        if point.type == Socket.Input:
            point.type = Socket.Output
        else:
            point.type = Socket.Input
        self.refresh()

    def set_name(self, var, index, mode):
        print(var)
        for i in range(len(self.gear.points)):
            print(self.point_names_stringvar[i].get())
            self.gear.points[i].name = self.point_names_stringvar[i].get()

    def delete_point(self, p):
        self.gear.points.remove(p)
        self.refresh()

    def add_point(self, point):
        point.type = Socket.Input
        self.gear.add_point(point)
        self.parent.studio.populate_patches()
        self.refresh()

    def add_range(self, point):
        # point.type = Socket.Input
        # self.gear.add_point(point)
        if self.add_range_start is None:
            self.add_range_start = point
            return
        if self.add_range_end is None:
            self.add_range_end = point
            for i in range(self.add_range_start.point, self.add_range_end.point):
                p = Point(point.patch_id, i, Socket.Input)
                self.gear.add_point(p)
            self.refresh()

    def select_point(self):
        self.select_point_window = PatchBaysWindow(self, self.parent.studio.patchbays, mode='add')
        self.select_point_window.set_callback(self.add_point)

    def select_range(self):
        self.select_point_window = PatchBaysWindow(self, self.parent.studio.patchbays, mode='range')
        self.select_point_window.set_callback(self.add_range)
