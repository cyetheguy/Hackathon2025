import tkinter as tk
from tkinter import ttk

class MessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message App with Scrollbar")

        # Main container that holds the canvas and scrollbar.
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas widget and attach a scrollbar
        self.canvas = tk.Canvas(self.main_frame, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # inner_frame is a frame inside the canvas, where messages go.
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Always update the scrollregion when the inner frame changes.
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        # Adjust inner frame's width to match the canvas width.
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def add_message(self, text, align_right):
        # Create a container for the individual message row.
        msg_frame = tk.Frame(self.inner_frame)
        msg_frame.pack(fill=tk.X, padx=10, pady=5)

        if align_right:
            # For right alignment, let column 0 take up extra space.
            msg_frame.columnconfigure(0, weight=1)
            # Create an empty label in column 0 as a spacer.
            dummy = tk.Label(msg_frame, text="")
            dummy.grid(row=0, column=0, sticky="w")
            # Place the actual message in column 1.
            label = tk.Label(msg_frame, text=text, bg="lightblue", padx=10, relief="solid")
            label.grid(row=0, column=1, sticky="e")
        else:
            # For left alignment, let column 1 take up extra space.
            msg_frame.columnconfigure(1, weight=1)
            # Place the message label in column 0.
            label = tk.Label(msg_frame, text=text, bg="lightgrey", padx=10, relief="solid")
            label.grid(row=0, column=0, sticky="w")
            # Create an empty label in column 1 to push the message left.
            dummy = tk.Label(msg_frame, text="")
            dummy.grid(row=0, column=1, sticky="e")

        # Update scrollregion to include the new message.
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Update the scrollregion when the size of the inner_frame changes.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Make the inner_frame match the canvas width.
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)


if __name__ == "__main__":
    root = tk.Tk()
    app = MessageApp(root)

    # Example messages with different alignments
    app.add_message("Hello, I'm on the left!", align_right=False)
    app.add_message("Hey there, I'm on the right!", align_right=True)
    app.add_message("Another left aligned message.", align_right=False)
    app.add_message("A message on the right side appears here.", align_right=True)
    app.add_message("Hello, I'm on the left!", align_right=False)
    app.add_message("Hey there, I'm on the right!", align_right=True)
    app.add_message("Another left aligned message.", align_right=False)
    app.add_message("A message on the right side appears here.", align_right=True)
    app.add_message("Hello, I'm on the left!", align_right=False)
    app.add_message("Hey there, I'm on the right!", align_right=True)
    app.add_message("Another left aligned message.", align_right=False)
    app.add_message("A message on the right side appears here.", align_right=True)
    app.add_message("Hello, I'm on the left!", align_right=False)
    app.add_message("Hey there, I'm on the right!", align_right=True)
    app.add_message("Another left aligned message.", align_right=False)
    app.add_message("A message on the right side appears here.", align_right=True)
    

    root.mainloop()
