import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time

import globe
import client

message = None
heated:float = 0
last_sent = time.time()

# Note: Copied from repository of English profanity/ banned words and phrases, we DO NOT CONDONE THE USE OF THEM
bad_words = ["Arsehole",
"Asshat",
"Asshole",
"Bastard",
"Big black cock",
"Bitch",
"Bloody",
"Blowjob",
"Bollocks",
"Bugger",
"Bullshit",
"Chicken shit",
"Clusterfuck",
"Cock",
"Cocksucker",
"Coonass",
"Cornhole",
"Cox–Zucker machine",
"Cracker",
"Crap",
"Cunt",
"Damn",
"Dick",
"Dumbass",
"Enshittification",
"Faggot",
"Feck",
"Fuck",
"Fuck her right in the pussy",
"Fuck Joe Biden",
"Fuck, marry, kill",
"Fuckery",
"Grab \'em by the pussy",
"Healslut",
"If You See Kay",
"Jesus fucking christ",
"Kike",
"Motherfucker",
"Nigga",
"Nigger",
"Paki",
"Poof",
"Poofter",
"Prick",
"Pussy",
"Ratfucking",
"Retard",
"Russian warship, go fuck yourself",
"Serving cunt",
"Shit",
"Shit happens",
"Shithouse",
"Shitposting",
"Shitter",
"Shut the fuck up",
"Shut the hell up",
"Slut",
"Son of a bitch",
"Spic",
"Taking the piss",
"Twat",
"Unclefucker",
"Wanker",
"Whore"]

def create_frame(root):
    global message
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    message = tk.StringVar(root)
    
    # Configure rows and columns of the frame
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    
    # Add a button in the top-left corner
    top_left_button = tk.Button(frame, text="< Exit ", font=("Arial", 12), command=lambda: globe.app.show_frame("Main"))
    top_left_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    
    # Add a title in the top-middle
    title_label = tk.Label(frame, text="Refute", font=("Arial", 16))
    title_label.grid(row=0, column=1, sticky="n", padx=10, pady=10)
    
    # Add an entry box in the bottom-left corner
    bottom_left_entry = tk.Entry(frame, font=("Arial", 12), textvariable=message)
    bottom_left_entry.grid(row=2, column=0, columnspan=2, sticky="sw", padx=10, pady=10)
    
    # Add a button in the bottom-right corner
    bottom_right_button = tk.Button(frame, text="Send", font=("Arial", 12), command=check_message)
    bottom_right_button.grid(row=2, column=2, sticky="se", padx=10, pady=10)
    
    return frame

def check_message() -> bool:
    global message
    global bad_words
    global heated
    global last_sent
    
    heated -= 0.1
    msg = message.get()
    cur_time = time.time()
    
    # Track what triggered the warning
    trigger_reason = ""
    
    ## check for spam
    if cur_time - last_sent < 10:
        heated += 1.1
        trigger_reason = "spamming messages too quickly"
    last_sent = cur_time

    # Check for bad words
    msg_low = set(msg.lower().split())
    bad_words_count = len(msg_low.intersection(word.lower() for word in bad_words))
    heated += 1.1 * bad_words_count
    if bad_words_count > 0:
        trigger_reason = "using inappropriate language" if not trigger_reason else f"{trigger_reason} and using inappropriate language"

    if heated > 9:
        # Default message if for some reason we don't have a specific reason
        warning_msg = "Your actions are not calm. Take a chill pill, homie."
        
        if trigger_reason:
            warning_msg = f"Please calm down - you're {trigger_reason}.\nTake a moment to relax before continuing."
            
        messagebox.showwarning("Chill Out", warning_msg)
        globe.app.enter_chill_mode()
    
    globe.conversation.send_message(msg)
