import tkinter as tk
from tkinter import Menu
from audio_file import AudioManager


import globe
import relax_menu
import refute

class App:
    def __init__(self, root):
        self.root = root
        self.audio = AudioManager()
        self.root.title("Relax and Refute")
        self.root.geometry("1280x720")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.isLight:bool = True  # Default isLight is light

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
        label = tk.Label(frame, text="Relax and Refute", font=("Arial", 16))
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
        menu_bar.add_command(label="Toggle Theme", command=self.toggle_theme)

    def show_frame(self, name):
        self.frames[name].tkraise()

    def toggle_theme(self):
        if self.isLight:
            self.isLight = True
            bg_color = "#ffffff"
            fg_color = "#000000"
            self.audio.play_theme("light")
        else:
            self.isLight = False
            bg_color = "#000000"
            fg_color = "#ffffff"
            self.audio.play_theme("dark")

        self.root.config(bg="black")
        for frame in self.frames.values():
            frame.config(bg=bg_color)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg=bg_color)
                if isinstance(widget, tk.Label):
                    widget.config(bg=bg_color, fg=fg_color)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    globe.app = App(root)
    root.mainloop()
