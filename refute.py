import tkinter as tk

import globe

def create_frame(root):
    frame = tk.Frame(root, bg="#B2DFDB")
    frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(
        frame, 
        text="You are in a refute.", 
        font=("Helvetica", 18, "italic"), 
        bg="#B2DFDB", 
        fg="#004D40"
    )
    label.pack(pady=50)

    quote = tk.Label(
        frame,
        text="“Peace comes from within. Do not seek it without.” – Buddha",
        font=("Helvetica", 12),
        bg="#B2DFDB",
        fg="#00695C",
        wraplength=350,
        justify="center"
    )
    quote.pack(pady=10)

    button = tk.Button(frame, text="Exit Relax", command=lambda: globe.app.show_frame("Main"))
    button.pack(pady=10)

    return frame