'''import tkinter

color_mode:bool = False


def init():
    root = tkinter.Tk()
    root.title("Relax and Refute")
    root.geometry("1280x720")
    root.bind_all("<Key>", None)
    return root

def update():



if __name__ == "__main__":
    win = init()
    win.mainloop()'''
import tkinter as tk

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Scheme Changer")

        # Initial boolean value
        self.is_light_mode = True

        # Set up the UI elements
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Hello, Tkinter!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.button = tk.Button(self.frame, text="Toggle Color Scheme", command=self.toggle_colors)
        self.button.pack(pady=20)

        # Apply the initial color scheme
        self.apply_color_scheme()

    def apply_color_scheme(self):
        if self.is_light_mode:
            # Light mode color scheme
            bg_color = "#ffffff"
            fg_color = "#000000"
        else:
            # Dark mode color scheme
            bg_color = "#2e2e2e"
            fg_color = "#ffffff"

        # Apply colors to the frame and widgets
        self.frame.config(bg=bg_color)
        self.label.config(bg=bg_color, fg=fg_color)
        self.button.config(bg=fg_color, fg=bg_color)

    def toggle_colors(self):
        # Toggle the boolean value
        self.is_light_mode = not self.is_light_mode
        # Apply the updated color scheme
        self.apply_color_scheme()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()