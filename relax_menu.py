import tkinter as tk

def create_relaxing_frame(root):
    frame = tk.Frame(root, bg="#B2DFDB")

    label = tk.Label(
        frame, 
        text="Take a deep breath...\nYou're in Frame 1", 
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

    return frame
