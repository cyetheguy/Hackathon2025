import tkinter as tk
from tkinter import Menu
import pygame

import globe
from globe import lerp_to_hex, rgb_to_hex
import relax_menu
import refute
from audio_file import AudioManager
import client

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
        self.client = client.Client('127.0.0.1', 7633)
        
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

        # Create menu
        self.create_menu()
        self.toggle_theme()

        # Show the main frame by default
        self.show_frame("Main")


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
                frame.config(bg=bg_temp)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.config(bg=bg_temp)
                    if isinstance(widget, tk.Label):
                        widget.config(bg=bg_temp, fg=fg_temp)
                    if isinstance(widget, tk.Button):
                        widget.config(background=bg_temp, activebackground=highlight_temp, foreground=fg_temp, borderwidth=3)
            self.root.after(10, root.update_idletasks())
        self.bg_color = bg_target
        self.fg_color = fg_target
        self.highlight = highlight_temp

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    globe.app = App(root)
    root.mainloop()
