from customtkinter import CTkFrame
import customtkinter as ctk
import tkinter as tk
from AppGlobals import Globals, Socket
from App.ChannelStrip import ChannelStrip
# from App.Point import Point


class StripUI(CTkFrame):
    def __init__(self, parent, strip: ChannelStrip):
        CTkFrame.__init__(self, parent)
        self.parent = parent
        self.strip: ChannelStrip = strip
        self.number_label = None
        self.inputs_list = self.strip.get_available_io_names(Socket.Input)
        self.outputs_list = self.strip.get_available_io_names(Socket.Output)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.in_out_frame = CTkFrame(self, fg_color=Globals().DarkBG)
        self.in_out_frame.grid(row=0, column=0, sticky='nesw')
        self.input_options: ctk.CTkOptionMenu = None
        self.output_options: ctk.CTkOptionMenu = None

        self.inserts_frame = CTkFrame(self, fg_color=Globals().ToolbarBG)
        self.inserts_frame.grid(row=0, column=1, sticky='nesw')
        self.color_frame = CTkFrame(self, fg_color=Globals().DarkBG)
        self.color_frame.grid(row=0, column=2, sticky='nesw')

        self.make_inout_frame(self.in_out_frame)
        self.make_inserts_frame(self.inserts_frame)
        self.make_color_frame(self.color_frame)
        self.pack(expand=True, fill=tk.BOTH, anchor=tk.W, pady=5, ipady=5)

    def make_inout_frame(self, frame):
        # print(self.strip.get_available_inputs_names())
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=self.strip.width.name, font=Globals().PatchFont).grid(row=0, column=0)
        self.name_label = ctk.CTkLabel(frame,
                                       text=self.strip.name,
                                       font=Globals().HeaderFont).grid(row=1, column=0, sticky='nesw', rowspan=2)
        ctk.CTkLabel(frame, text="Out").grid(row=0, column=1)
        self.output_options = ctk.CTkOptionMenu(master=frame,
                                                values=self.outputs_list,
                                                command=self.select_output)
        self.output_options.grid(row=1, column=1)
        self.output_options.set(self.outputs_list[self.strip.output_index])
        ctk.CTkLabel(frame, text="In").grid(row=2, column=1)
        self.input_options = ctk.CTkOptionMenu(master=frame,
                                               values=self.inputs_list,
                                               command=self.select_input)
        self.input_options.grid(row=3, column=1)
        self.input_options.set(self.inputs_list[self.strip.input_index])

    def make_inserts_frame(self, frame):
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text="Inserts", font=Globals().HeaderFont).grid(row=0, column=0, columnspan=2, sticky='nesw')
        ctk.CTkButton(frame, text="...", width=10, command=self.show_settings).grid(row=0, column=4)

        ctk.CTkLabel(frame, text='A').grid(row=1, column=0)
        # combo_a = ctk.CTkComboBox(frame,
        #                           values=self.strip.get_outboard_names(),
        #                           command=lambda choice: self.select_insert(choice, 0))
        # combo_a.grid(row=1, column=1, padx=10, pady=10)
        # if self.strip.inserts[0] is not None:
        #     combo_a.set(self.strip.inserts[0])
        self.create_combo(frame, 0, 1, 1)
        ctk.CTkLabel(frame, text='B').grid(row=2, column=0)
        # combo_b = ctk.CTkComboBox(frame, values=self.strip.get_outboard_names(),
        #                           command=lambda choice: self.select_insert(choice, 2))
        # combo_b.grid(row=1, column=3)
        self.create_combo(frame, 1, 1, 3)
        ctk.CTkLabel(frame, text='C').grid(row=1, column=2)
        # ctk.CTkComboBox(frame, values=self.strip.get_outboard_names(),
        #                 command=lambda choice: self.select_insert(choice, 1)).grid(row=2, column=1)
        self.create_combo(frame, 2, 2, 1)
        ctk.CTkLabel(frame, text='D').grid(row=2, column=2)
        # ctk.CTkComboBox(frame, values=self.strip.get_outboard_names(),
        #                 command=lambda choice: self.select_insert(choice, 3)).grid(row=2, column=3)
        self.create_combo(frame, 3, 2, 3)

    def create_combo(self, frame, index, r, c):
        combo = ctk.CTkComboBox(frame,
                                values=self.strip.get_outboard_names(),
                                command=lambda choice: self.select_insert(choice, index))
        combo.grid(row=r, column=c, padx=10, pady=10)
        if self.strip.inserts[index] is not None:
            combo.set(self.strip.inserts[index])

    def make_color_frame(self, frame):
        ctk.CTkLabel(frame, text="Color").pack()
        ctk.CTkButton(frame,text='', fg_color='pink', height=50, width=50).pack(expand=tk.Y)

    def show_settings(self):
        self.parent.show_strip_settings(self.strip)

    def select_input(self, choice):
        self.strip.select_io(Socket.Input, self.inputs_list.index(choice))

    def select_output(self, choice):
        self.strip.select_io(Socket.Output, self.outputs_list.index(choice))

    def select_insert(self, choice, index):
        # self.strip.select_insert(index, self.get_gear_name(choice), self.get_dual_mono_index(choice))
        self.strip.select_insert(index, choice)

    # def select_insert_A(self, choice):
    #     self.strip.select_insert(0, self.get_gear_name(choice))


    # def inputs_menu(self):
    #     combobox = ctk.CTkOptionMenu(master=self,
    #                                            values=["option 1", "option 2"])
    #     combobox.grid()
    #     combobox.set("option 2")  # set initial value