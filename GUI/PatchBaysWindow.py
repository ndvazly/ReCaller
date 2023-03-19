import tkinter as tk
import customtkinter as ctk
from AppGlobals import Globals
from App import PatchBay
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
        self.make_window()

    def set_callback(self, callback):
        self.callback = callback

    def make_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("PatchBays")
        self.window.geometry('1200x800')
        self.window.configure(bg=Globals().DarkBG)
        self.draw_patchbay(self.patchbays[0])

    def draw_patchbay(self, patch: PatchBay):
        points_in_row = int(patch.number_of_points / 2)
        break_after_points = int(points_in_row / 2)
        canvas = tk.Canvas(self.window, height=300, width=900, bg=Globals().ButtonBG)
        for row in range(2):
            start_col = 0
            for point in range(points_in_row):
                col = start_col + point + (2 * (point >= break_after_points))
                btn = ctk.CTkButton(canvas, text='o', width=20, height=1)
                btn.grid(row=row+1, column=col, sticky='nesw')
                btn.bind('<Button-1>', self.button_pressed)
                # ctk.CTkButton(canvas, text=point+1, width=1, height=1).grid(row=row+1, column=col, sticky='nesw')
            ctk.CTkLabel(canvas, text='---------').grid(row=row+1, column=break_after_points+1)

        for row in range(2):
            text_row = row * 3
            point = 0
            while point < points_in_row:
                point_idx = point + (row * points_in_row)
                start_range = point + (2 * (point >= break_after_points))
                end_range = start_range
                name = self.patchbays[0].get_point_name(point_idx)
                if point_idx < patch.number_of_points-1:
                    if self.patchbays[0].get_point_name(point_idx) == self.patchbays[0].get_point_name(point_idx+1):
                        for next_point in range(point, points_in_row):
                            if name == self.patchbays[0].get_point_name(next_point + (row*points_in_row)):
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
                else:
                    total_range = 1
                label = ctk.CTkLabel(canvas, text=name, font=Globals().PatchFont, text_color='black')
                label.grid(row=text_row, column=start_range, columnspan=total_range)
                point += 1

        canvas.pack(fill=tk.X)

    def button_pressed(self, event):
        # get_index = str(event.widget).split('.!')
        str_index = [x[9:] for x in str(event.widget).split('.!') if x.startswith('ctkbutton')]
        btn_index = 0 if str_index[0] == '' else int(str_index[0])-1
        print(btn_index)
        if self.callback is not None:
            self.callback(Point(0, btn_index, None))
        if self.mode == 'add' or self.range_start:
            self.window.destroy()
        if self.mode == 'range':
            self.range_start = True

            # for i in range(2):
    #     pairs = 0
    #     for point in range(break_after_points):
    #         col = start_col + point
    #         ctk.CTkLabel(canvas, text=self.patchbays[0].get_point_name(point), font=Globals().PatchFont,
    #                      text_color='black').grid(row=text_row, column=col)
    #         ctk.CTkButton(canvas, text='o', width=1, height=1).grid(row=row + 1, column=col, sticky='nesw')
    #     ctk.CTkLabel(canvas, text='---------').grid(row=row + 1, column=break_after_points + pairs)
    #     start_col = break_after_points + pairs + 1

    # def draw_column_rects(self, canvas, x_origin, y_origin, rect_size, break_after_points):
    #     start_x = x_origin
    #     start_y = y_origin
    #     pad = 3
    #     for i in range(break_after_points):
    #         xpos = start_x + (i*rect_size)
    #         if i % 2 == 0:
    #             canvas.create_rectangle(xpos, start_y, xpos + (rect_size*2), start_y + rect_size+1, outline="red")
    #         canvas.create_rectangle(xpos+pad, start_y+1, xpos+rect_size, start_y+rect_size, outline="#fb0", fill="#fb0")
    #
    #     start_x = x_origin + break_after_points * rect_size + pad * rect_size + pad * 4
    #     for i in range(break_after_points):
    #         xpos = start_x + (i*rect_size)
    #         if i % 2 == 0:
    #             canvas.create_rectangle(xpos, start_y, xpos + (rect_size*2)+1, start_y + rect_size+1, outline="red")
    #         canvas.create_rectangle(xpos+pad, start_y+1, xpos+rect_size, start_y+rect_size, outline="#fb0", fill="#fb0")

    # def draw_patchbay(self, patch: PatchBay):
    #     print(patch)
    #     points_in_row = int(patch.number_of_points / 2)
    #     break_after_points = int(points_in_row / 2)
    #     print(break_after_points)
    #
    #     canvas = tk.Canvas(self.window, height=300, width=900, bg=Globals().ButtonBG)
    #     patch_x = 25
    #     patch_y = 50
    #     rect_size = 22
    #     spacer = rect_size*3.4
    #     jump_spacer = 0
    #     bottom_patch_y = patch_y + rect_size + 25
    #     for i in range(points_in_row):
    #         # x_pos = patch_x + rect_size + (i*(rect_size*2))
    #         x_pos = jump_spacer + patch_x + (rect_size/2) + (i*(rect_size) )
    #         canvas.create_text(x_pos, patch_y / 2, font="Times 7", text="API\n2500")
    #         canvas.create_text(x_pos, bottom_patch_y + 25, font="Times 7", text="API\n2500")
    #         # canvas.create_text(x_pos, patch_y / 2, font="Times 7", text="Lynx\nIn")
    #         if i % 2 == 0:
    #             canvas.create_text(x_pos+(rect_size/2), patch_y - 10, font="Times 7", text=f'{i+1}-{i+2}')
    #             canvas.create_text(x_pos+(rect_size/2), bottom_patch_y + 10, font="Times 7", text=f'{i+1}-{i+2}')
    #         # canvas.create_text(x_pos, patch_y - 10, font="Times 7", text=str(i+1))
    #         if i == break_after_points-1:
    #             jump_spacer = spacer
    #
    #     self.draw_column_rects(canvas, patch_x, patch_y, rect_size, break_after_points)
    #     self.draw_column_rects(canvas, patch_x, patch_y+25, rect_size, break_after_points)
    #     canvas.pack(fill=tk.X)
