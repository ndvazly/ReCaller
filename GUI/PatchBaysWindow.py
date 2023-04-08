import tkinter as tk
import customtkinter as ctk

import AppGlobals
from AppGlobals import Globals
from App.PatchBay import PatchBay
from App.Point import Point


class PatchBaysWindow:
    def __init__(self, parent, patchbays, mode='patch'):
        self.root = parent
        self.parent = parent
        self.window = None
        self.patchbays: PatchBay = patchbays
        self.callback = None
        self.mode = mode
        self.range_start = False
        self.socket_type: AppGlobals.Socket = AppGlobals.Socket.Input
        self.socket_type_var = tk.IntVar()
        self.make_window()

    def set_callback(self, callback):
        self.callback = callback

    def make_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("PatchBays")
        self.window.geometry('1200x520')
        self.window.configure(bg=Globals().DarkBG)

        if self.mode != 'patch':
            socket_type_frame = ctk.CTkFrame(self.window)
            ctk.CTkRadioButton(master=socket_type_frame, text="Input",
                               command=self.radiobutton_event, variable=self.socket_type_var, value=0).pack()
            ctk.CTkRadioButton(master=socket_type_frame, text="Output",
                               command=self.radiobutton_event, variable=self.socket_type_var, value=1).pack()
            socket_type_frame.pack(fill=tk.X)

        for patch in self.patchbays:
            self.draw_patchbay(patch)

    def draw_patchbay(self, patch: PatchBay):
        patch_frame = ctk.CTkFrame(self.window)
        ctk.CTkLabel(patch_frame, text=patch.name, font=Globals().HeaderFont).pack(fill=tk.X)
        points_in_row = int(patch.number_of_points / 2)
        break_after_points = int(points_in_row / 2)
        canvas = tk.Canvas(patch_frame, height=300, width=900, bg=Globals().PatchBG)
        for row in range(2):
            for point in range(points_in_row):
                p: Point = Point(patch.id, point+row*points_in_row, AppGlobals.Socket.Input)
                col = point + (2 * (point >= break_after_points))
                btn = ctk.CTkButton(canvas, text='o', width=20, height=1,
                                    command=lambda x=p: self.button_pressed(x))
                btn.grid(row=row+1, column=col, sticky='nesw')
                # ctk.CTkButton(canvas, text=point+1, width=1, height=1).grid(row=row+1, column=col, sticky='nesw')
            ctk.CTkLabel(canvas, text='---------').grid(row=row+1, column=break_after_points+1)

        for row in range(2):
            text_row = row * 3
            point = 0
            while point < points_in_row:
                point_idx = point + (row * points_in_row)
                start_range = point
                col = point + (2 * (point >= break_after_points))
                end_range = start_range
                name = patch.get_point_name(point_idx)
                if point_idx < patch.number_of_points-1:
                    if patch.get_point_name(point_idx) == patch.get_point_name(point_idx+1):
                        for next_point in range(point, points_in_row):
                            if name == patch.get_point_name(next_point + (row*points_in_row)):
                                point = next_point
                                end_range = next_point
                            else:
                                break
                total_range = end_range - start_range
                if total_range:
                    if total_range > 2:
                        name = name + f' 1-{total_range+1}'
                    else:
                        name = name + ' L-R'
                        total_range = 2
                else:
                    total_range = 1
                label = ctk.CTkLabel(canvas, text=name, font=Globals().PatchFont, text_color='black')
                label.grid(row=text_row, column=col, columnspan=total_range, sticky='nesw')
                point += 1

        canvas.pack(fill=tk.X, pady=20,padx=10,ipadx=10,ipady=10)
        patch_frame.pack()

    def radiobutton_event(self):
        self.socket_type = AppGlobals.Socket(self.socket_type_var.get())

    def button_pressed(self, p: Point):
        # print('range_start ', self.range_start)
        p.type = self.socket_type
        print(p)
        print(p.gear)
        if self.callback is not None:
            self.callback(p)
        if self.mode == 'add' or self.range_start:
            self.window.destroy()
        if self.mode == 'range':
            self.range_start = True
