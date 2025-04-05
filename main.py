import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import Menu, messagebox
import pygame
import threading
import time

import globe
from globe import lerp_to_hex, rgb_to_hex
import relax_menu
import refute
from audio_file import AudioManager
import client
import conversation

pygame.mixer.init()
pygame.mixer.music.set_volume(1)

class App:
    def __init__(self, root):
        self.root = root
        self.audio = AudioManager()
        self.root.title("Relax and Refute")
        self.root.geometry("1280x720")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.isLight:bool = True  # Default isLight is light
        ##self.client = client.Client('127.0.0.1', 7633)
        self.username = tk.StringVar(self.root)
        
        # Colors
        self.bg_color = globe.black
        self.fg_color = globe.black
        self.hglt_color = globe.white
        

        # Create frames
        self.frames = {
            "Main": self.create_main(),
            "Relax": relax_menu.create_relaxing_frame(self.root),
            "Refute": refute.create_frame(self.root),
        }

        globe.conversation = conversation.Conversation(self.frames["Refute"])

        # Show the main frame by default
        self.show_frame("Main")

        # Create menu
        self.create_menu()
        self.toggle_theme()

        


    def create_main(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        label = tk.Label(frame, text="Relax and Refute", font=globe.title_font)
        label.pack(pady=50)
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=50, anchor="center")
        relaxButton = tk.Button(button_frame, text="Relax", font=("Arial", 16), command=lambda: self.show_frame("Relax"))
        relaxButton.pack(padx=50, side=tk.LEFT)
        refuteButton = tk.Button(button_frame, text="Refute", font=("Arial", 16), command=lambda: self.show_frame("Refute"))
        refuteButton.pack(padx=50, side=tk.LEFT)
        
        return frame

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        frame_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Themes", menu=frame_menu)
        frame_menu.add_command(label="Light Theme", command=lambda: self.toggle_theme(True))
        frame_menu.add_command(label="Dark Theme", command=lambda: self.toggle_theme(False))

        audio_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Audio Volume", menu=audio_menu)
        audio_menu.add_command(label="100%", command=lambda: pygame.mixer.music.set_volume(1))
        audio_menu.add_command(label=" 50%", command=lambda: pygame.mixer.music.set_volume(0.5))
        audio_menu.add_command(label=" 25%", command=lambda: pygame.mixer.music.set_volume(0.25))
        audio_menu.add_command(label="Mute", command=lambda: pygame.mixer.music.set_volume(0))

    def show_frame(self, name):
        self.frames[name].tkraise()
        if not self.username.get() and name == "Refute":
            self.username.set(askstring("Enter Username", "Please enter a name?\nYou will be connected shortly."))
            globe.client.set_name(self.username.get())

    def update_theme(self, bgColor=None, fgColor=None, hgltColor=None) -> None:
        if not bgColor:
            bgColor = rgb_to_hex(self.bg_color)
        if not fgColor:
            fgColor = rgb_to_hex(self.fg_color)
        if not hgltColor:
            hgltColor = rgb_to_hex(self.hglt_color)
        for frame in self.frames.values():
                self.apply_theme(frame, bgColor, fgColor, hgltColor)

    def apply_theme(self, frame, bgColor, fgColor, hgltColor) -> None:
        frame.config(bg=bgColor)
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Frame):
                self.apply_theme(widget, bgColor,fgColor,hgltColor)
            if isinstance(widget, tk.Canvas):
                self.apply_theme_canvas(widget, bgColor, fgColor, hgltColor)
            if isinstance(widget, tk.Label):
                widget.config(bg=bgColor, fg=fgColor)
            if isinstance(widget, tk.Button):
                widget.config(background=bgColor, activebackground=hgltColor, foreground=fgColor, borderwidth=3)
        self.root.after(1, root.update_idletasks())

    def apply_theme_canvas(self, frame, bgColor, fgColor, hgltColor) -> None:
        frame.config(bg=bgColor)
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Frame):
                self.apply_theme_canvas(widget, bgColor,fgColor,hgltColor)
            if isinstance(widget, tk.Frame):
                widget.config(bg=bgColor)
            if isinstance(widget, tk.Label):
                if not widget.cget("text"):
                    widget.config(bg=bgColor, fg=fgColor)
                elif widget.grid_info()["sticky"] == 'e':
                    if not self.isLight:
                        widget.config(bg=rgb_to_hex(globe.dark_turquoise), fg=rgb_to_hex(globe.white))
                    else:
                        widget.config(bg = rgb_to_hex(globe.razorback), fg = rgb_to_hex(globe.white))
                else:
                    widget.config(bg=rgb_to_hex(globe.gray),fg=rgb_to_hex(globe.black))


    def toggle_theme(self, override:bool = None):
        if (override != None):
            self.isLight = override
        if self.isLight:
            self.isLight = False
            bg_target = globe.teal
            fg_target = globe.dark_turquoise
            hglt_target = globe.white
            self.audio.play_theme("light")
        else:
            self.isLight = True
            bg_target = globe.stormy_gray
            fg_target = globe.white
            hglt_target = globe.razorback
            self.audio.play_theme("dark")

        for i in range(0, 100):
            bg_temp = lerp_to_hex(self.bg_color, bg_target, i/100)
            fg_temp = lerp_to_hex(self.fg_color, fg_target, i/100)
            highlight_temp = lerp_to_hex(self.hglt_color, hglt_target, i/100)
            self.root.config(bg=bg_temp)
            for frame in self.frames.values():
                self.apply_theme(frame, bg_temp, fg_temp, highlight_temp)
        self.bg_color = bg_target
        self.fg_color = fg_target
        self.highlight = highlight_temp
    
    def entre_chill_mode(self) -> None:
        bg_target = globe.ice
        fg_target = globe.dark_ice
        hglt_target = globe.blue
    
        for i in range(0, 100):
                bg_temp = lerp_to_hex(self.bg_color, bg_target, i/100)
                fg_temp = lerp_to_hex(self.fg_color, fg_target, i/100)
                highlight_temp = lerp_to_hex(self.hglt_color, hglt_target, i/100)
                self.root.config(bg=bg_temp)
                for frame in self.frames.values():
                    self.apply_theme(frame, bg_temp, fg_temp, highlight_temp)
        self.bg_color = bg_target
        self.fg_color = fg_target
        self.highlight = highlight_temp

        start_time = time.time()
        while refute.heated > 5:
            cur_time = time.time()
            if (cur_time-start_time >= 0.1):
                refute.heated -=1
                start_time = cur_time

        self.toggle_theme(self.isLight)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    globe.app = App(root)
    globe.client = client.Client('127.0.0.1', 7633)
    client_thread = threading.Thread(target=globe.client.receive_message)
    client_thread.start()
    root.mainloop()
