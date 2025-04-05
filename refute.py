import tkinter as tk
from tkinter import ttk

import globe

def create_frame(root):
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    
    # Configure rows and columns of the frame
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)


    ## conversation box
    conversation = tk.Canvas(frame)
    conversation.grid(row=1, column=1, rowspan=2, sticky="nsew")
    scrollbar = ttk.Scrollbar(conversation, orient="vertical", command=conversation.yview)
    
    # Add a button in the top-left corner
    top_left_button = tk.Button(frame, text="< Exit ", font=("Arial", 12), command=lambda: globe.app.show_frame("Main"))
    top_left_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    
    # Add a title in the top-middle
    title_label = tk.Label(frame, text="Refute", font=("Arial", 16))
    title_label.grid(row=0, column=1, sticky="n", padx=10, pady=10)
    
    # Add an entry box in the bottom-left corner
    bottom_left_entry = tk.Entry(frame, font=("Arial", 12))
    bottom_left_entry.grid(row=2, column=0, columnspan=2, sticky="sw", padx=10, pady=10)
    
    # Add a button in the bottom-right corner
    bottom_right_button = tk.Button(frame, text="Send", font=("Arial", 12))
    bottom_right_button.grid(row=2, column=2, sticky="se", padx=10, pady=10)
    
    return frame