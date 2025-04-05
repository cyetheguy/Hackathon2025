import tkinter as tk
from tkinter import Menu

class FrameSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Three Frames with Menu")
        self.root.geometry("1280x720")
        self.theme = "light"  # Default theme is light

        # Create frames
        self.frames = {
            "Frame 1": self.create_frame("lightblue", "This is Frame 1"),
            "Frame 2": self.create_frame("lightgreen", "This is Frame 2"),
            "Frame 3": self.create_frame("lightcoral", "This is Frame 3"),
        }

        # Create menu
        self.create_menu()

        # Create toggle theme button
        self.toggle_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_button.grid(row=1, column=0, pady=10)

        # Show the first frame by default
        self.show_frame("Frame 1")

    def create_frame(self, color, text):
        frame = tk.Frame(self.root, bg=color, width=400, height=300)
        frame.grid(row=0, column=0, sticky="nsew")
        label = tk.Label(frame, text=text, font=("Arial", 16))
        label.pack(pady=50)
        return frame

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        frame_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Frames", menu=frame_menu)

        for name in self.frames:
            frame_menu.add_command(label=name, command=lambda name=name: self.show_frame(name))

    def show_frame(self, name):
        self.frames[name].tkraise()

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.root.config(bg="black")
            self.toggle_button.config(bg="gray", fg="white")
            for frame in self.frames.values():
                frame.config(bg="dimgray")
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg="dimgray", fg="white")
        else:
            self.theme = "light"
            self.root.config(bg="white")
            self.toggle_button.config(bg="lightgray", fg="black")
            for frame in self.frames.values():
                frame.config(bg="lightgray")
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg="lightgray", fg="black")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FrameSwitcherApp(root)
    root.mainloop()
