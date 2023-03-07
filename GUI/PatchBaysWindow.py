from tkinter import Frame
import tkinter as tk
from AppGlobals import Globals
from App import PatchBay


class PatchBaysWindow:
    def __init__(self, parent):
        self.root = parent.root
        self.parent = parent
        self.window = None
        self.patchbays = self.parent.studio.patchbays
        self.make_window()

    def make_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("PatchBays")
        self.window.geometry('1200x800')
        self.window.configure(bg=Globals().DarkBG)

        self.draw_patchbay(self.patchbays[0])

    def draw_column_rects(self, canvas, x_origin, y_origin, rect_size, break_after_points):
        start_x = x_origin
        start_y = y_origin
        pad = 3
        for i in range(break_after_points):
            xpos = start_x + (i*rect_size)
            if i % 2 == 0:
                canvas.create_rectangle(xpos, start_y, xpos + (rect_size*2), start_y + rect_size+1, outline="red")
            canvas.create_rectangle(xpos+pad, start_y+1, xpos+rect_size, start_y+rect_size, outline="#fb0", fill="#fb0")

        start_x = x_origin + break_after_points * rect_size + pad * rect_size + pad * 4
        for i in range(break_after_points):
            xpos = start_x + (i*rect_size)
            if i % 2 == 0:
                canvas.create_rectangle(xpos, start_y, xpos + (rect_size*2)+1, start_y + rect_size+1, outline="red")
            canvas.create_rectangle(xpos+pad, start_y+1, xpos+rect_size, start_y+rect_size, outline="#fb0", fill="#fb0")

    def draw_patchbay(self, patch: PatchBay):
        print(patch)
        points_in_row = int(patch.number_of_points / 2)
        break_after_points = int(points_in_row / 2)
        print(break_after_points)

        canvas = tk.Canvas(self.window, height=300, width=900, bg=Globals().ButtonBG)
        patch_x = 25
        patch_y = 50
        rect_size = 22
        spacer = rect_size*3.4
        jump_spacer = 0
        bottom_patch_y = patch_y + rect_size + 25
        for i in range(points_in_row):
            # x_pos = patch_x + rect_size + (i*(rect_size*2))
            x_pos = jump_spacer + patch_x + (rect_size/2) + (i*(rect_size) )
            canvas.create_text(x_pos, patch_y / 2, font="Times 7", text="API\n2500")
            canvas.create_text(x_pos, bottom_patch_y + 25, font="Times 7", text="API\n2500")
            # canvas.create_text(x_pos, patch_y / 2, font="Times 7", text="Lynx\nIn")
            if i % 2 == 0:
                canvas.create_text(x_pos+(rect_size/2), patch_y - 10, font="Times 7", text=f'{i+1}-{i+2}')
                canvas.create_text(x_pos+(rect_size/2), bottom_patch_y + 10, font="Times 7", text=f'{i+1}-{i+2}')
            # canvas.create_text(x_pos, patch_y - 10, font="Times 7", text=str(i+1))
            if i == break_after_points-1:
                jump_spacer = spacer

        self.draw_column_rects(canvas, patch_x, patch_y, rect_size, break_after_points)
        self.draw_column_rects(canvas, patch_x, patch_y+25, rect_size, break_after_points)
        # canvas.columnconfigure(0, weight=1, uniform='column')
        # canvas.columnconfigure(1, weight=1, uniform='column')
        # start_row = 0
        # for row in range(2):
        #     start_col = 0
        #     for i in range(2):
        #         pairs = 0
        #         for point in range(break_after_points):
        #             col = start_col + point
        #             # if row == 0:
        #             #     tk.Label(canvas, text=f'{point}').grid(row=row, column=col)
        #             #     tk.Label(canvas, text='2500').grid(row=row+1, column=col+1)
        #             # else:
        #             #     tk.Label(canvas, text='API').grid(row=row+3, column=col)
        #             tk.Button(canvas, text='o', width=1, height=1).grid(row=row, column=col)
        #             if (point+1) % 2 == 0:
        #                 pairs += 1
        #                 start_col += 1
        #                 tk.Label(canvas, text='|').grid(row=row, column=col+1)
        #         tk.Label(canvas, text='---------').grid(row=row, column=break_after_points+pairs)
        #         start_col = break_after_points + pairs + 1
        canvas.pack(fill=tk.X)
        # # canvas.pack(fill=tk.X,expand=True)

