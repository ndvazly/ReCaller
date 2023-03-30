import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from App.ChannelStrip import ChannelStrip
import AppGlobals


class StripSettingsFrame(CTkScrollableFrame):
    def __init__(self, parent, strip: ChannelStrip):
        CTkScrollableFrame.__init__(self, parent.main_frame)
        self.parent = parent
        self.strip: ChannelStrip = strip
        self.settings_widgets = [None] * 4
        ctk.CTkLabel(self,
                     text=f'{self.strip.name} Inserts Settings',
                     font=AppGlobals.Globals().HeaderFont).pack()
        ctk.CTkButton(self, text='x', command=self.close).pack()
        self.make_settings_frames()
        self.save_settings()

    def make_settings_frames(self):
        self.make_insert_settings_frame('Insert A', 0)

    def make_insert_settings_frame(self, insert_name, insert_index):
        self.settings_widgets[insert_index] = []
        frame = ctk.CTkFrame(self)
        ctk.CTkLabel(frame, text=insert_name).grid(row=0, column=0, sticky='nesw', columnspan=4)
        if self.strip.inserts[insert_index] == '':
            return
        gear_name = self.strip.get_gear_name(self.strip.inserts[insert_index])
        gear = self.parent.studio.get_gear_by_name(gear_name)
        r = 1
        col = 0
        setting_index = 0
        for s in gear.settings:
            if col > 2:
                r += 1
                col = 0
            value_type = s['value']
            value = self.strip.settings[insert_index][setting_index]['value']
            if value == '':
                value = s['init']
            if value_type == 'Text':
                ctk.CTkLabel(frame, text=s['name']).grid(row=r, column=0+col)
                entry = ctk.CTkEntry(frame, width=40)
                entry.grid(row=r, column=1+col)
                entry.insert(0, value)
                self.settings_widgets[insert_index].append(entry)
            elif value_type == 'On/Off':
                checkbox = ctk.CTkCheckBox(frame, text=s['name'])
                if value == '1':
                    checkbox.select()
                checkbox.grid(row=r, column=0+col)
                self.settings_widgets[insert_index].append(checkbox)
            elif value_type == 'List':
                options = s['init'].split(',')
                ctk.CTkLabel(frame, text=s['name']).grid(row=r, column=0+col)
                combo = ctk.CTkComboBox(frame, values=options, width=60)
                combo.grid(row=r, column=1+col)
                if value != s['init']:
                    combo.set(value)
                self.settings_widgets[insert_index].append(combo)
            col += 2
            setting_index += 1
        frame.pack()

    def save_settings(self):
        for i in range(4):
            if self.settings_widgets[i] is None:
                continue
            index = 0
            # Iterate insert's widgets
            for w in self.settings_widgets[i]:
                # Save widget data into channel strip's settings
                self.strip.settings[i][index]['value'] = w.get()
                print(self.strip.settings[i][index])
                index += 1
        print('save_settings')

    def close(self):
        self.save_settings()
        self.parent.show_revisions_frame()