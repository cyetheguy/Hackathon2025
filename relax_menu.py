import tkinter as tk
import random
import globe
import threading
import time
import math
import openai
from itertools import cycle

class InteractiveOrb:
    def __init__(self, canvas):
        self.canvas = canvas
        self.origin = (150, 150)
        self.current_center = (150, 150)
        self.base_radius = 60
        self.current_radius = 60
        self.is_dragging = False
        self.drag_point = None
        self.orb_color = "#88E0EF"
        self.shadow_color = "#3DCCC7"
        self.ripple_points = 36
        self.surface_ripples = []
        self.stretch_factor = 0
        self.elasticity = 0.2
        self.max_stretch = 3.0
        
        self.depth_layers = [
            {"color": "#C4F1F9", "radius_ratio": 0.9, "ripple_ratio": 0.7},
            {"color": "#88E0EF", "radius_ratio": 0.7, "ripple_ratio": 0.5},
            {"color": "#3DCCC7", "radius_ratio": 0.5, "ripple_ratio": 0.3}
        ]
        
        self.orb_ids = []
        self.highlight_id = None
        self.bubble_ids = []
        self.start_animation()
        
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def create_orb(self):
        for item in self.orb_ids + [self.highlight_id] + self.bubble_ids:
            self.canvas.delete(item)
        self.orb_ids = []
        self.bubble_ids = []
        
        dx = self.current_center[0] - self.origin[0]
        dy = self.current_center[1] - self.origin[1]
        stretch_dir = math.atan2(dy, dx) if (dx != 0 or dy != 0) else 0
        self.stretch_factor = min(math.sqrt(dx**2 + dy**2) / (self.base_radius * 2), self.max_stretch)
        
        for layer in self.depth_layers:
            points = []
            radius = self.base_radius * layer["radius_ratio"] * (1 + self.stretch_factor * 0.3)
            
            for i in range(self.ripple_points):
                angle = (2 * math.pi * i) / self.ripple_points
                stretch_effect = math.cos(angle - stretch_dir) * self.stretch_factor
                base_radius = radius * (1 + stretch_effect * 0.5)
                
                ripple = 0
                for r in self.surface_ripples:
                    ripple += r["amplitude"] * math.sin(angle * r["frequency"] + r["phase"]) * \
                             math.exp(-r["decay"] * r["age"])
                
                current_radius = base_radius * (1 + ripple * layer["ripple_ratio"])
                x = self.current_center[0] + current_radius * math.cos(angle)
                y = self.current_center[1] + current_radius * math.sin(angle)
                points.extend([x, y])
            
            self.orb_ids.append(self.canvas.create_polygon(
                *points, fill=layer["color"], outline="", smooth=True
            ))
        
        self.add_highlight(stretch_dir)
        self.add_surface_detail()
    
    def add_highlight(self, angle):
        highlight_size = self.base_radius * 0.5
        hl_x = self.current_center[0] + math.cos(angle) * highlight_size * 0.7
        hl_y = self.current_center[1] + math.sin(angle) * highlight_size * 0.7
        
        self.highlight_id = self.canvas.create_oval(
            hl_x - highlight_size * 0.6, hl_y - highlight_size * 0.3,
            hl_x + highlight_size * 0.6, hl_y + highlight_size * 0.3,
            fill="white", outline="", stipple="gray50"
        )
    
    def add_surface_detail(self):
        for _ in range(3):
            bubble_size = random.uniform(3, 8)
            angle = random.uniform(0, math.pi/2)
            distance = random.uniform(0.3, 0.7) * self.base_radius
            
            x = self.current_center[0] + distance * math.cos(angle)
            y = self.current_center[1] - distance * math.sin(angle)
            
            # Changed from rgba to solid white with stipple for transparency effect
            self.bubble_ids.append(self.canvas.create_oval(
                x - bubble_size, y - bubble_size,
                x + bubble_size, y + bubble_size,
                fill="white", outline="", stipple="gray50"
            ))
    
    def add_ripple(self, amplitude=5, frequency=3, decay=0.2):
        self.surface_ripples.append({
            "amplitude": amplitude / 100,
            "frequency": frequency,
            "decay": decay,
            "phase": random.uniform(0, math.pi),
            "age": 0
        })
    
    def update_ripples(self):
        self.surface_ripples = [r for r in self.surface_ripples if r["age"] * r["decay"] < 5]
        for r in self.surface_ripples:
            r["age"] += 1
    
    def start_animation(self):
        self.animate()
    
    def animate(self):
        self.update_ripples()
        
        if random.random() < 0.1 and len(self.surface_ripples) < 3:
            self.add_ripple(amplitude=2, frequency=2, decay=0.1)
        
        if not self.is_dragging and (self.current_center != self.origin):
            dx = self.origin[0] - self.current_center[0]
            dy = self.origin[1] - self.current_center[1]
            self.current_center = (
                self.current_center[0] + dx * self.elasticity,
                self.current_center[1] + dy * self.elasticity
            )
            
            if math.sqrt(dx**2 + dy**2) < 5:
                self.current_center = self.origin
            elif random.random() < 0.3:
                self.add_ripple(amplitude=3, frequency=4, decay=0.15)
        
        self.create_orb()
        self.canvas.after(30, self.animate)
    
    def on_click(self, event):
        x, y = event.x, event.y
        distance = math.sqrt((x - self.current_center[0])**2 + (y - self.current_center[1])**2)
        
        if distance <= self.base_radius * (1 + self.stretch_factor):
            self.is_dragging = True
            self.drag_point = (x - self.current_center[0], y - self.current_center[1])
            click_angle = math.atan2(y - self.current_center[1], x - self.current_center[0])
            self.add_ripple(amplitude=8, frequency=5, decay=0.2)
    
    def on_drag(self, event):
        if self.is_dragging and self.drag_point:
            x, y = event.x, event.y
            target_x = x - self.drag_point[0]
            target_y = y - self.drag_point[1]
            
            dx = target_x - self.origin[0]
            dy = target_y - self.origin[1]
            distance = math.sqrt(dx**2 + dy**2)
            max_distance = self.base_radius * 3
            
            if distance > max_distance:
                angle = math.atan2(dy, dx)
                target_x = self.origin[0] + math.cos(angle) * max_distance
                target_y = self.origin[1] + math.sin(angle) * max_distance
            
            self.current_center = (
                self.current_center[0] + (target_x - self.current_center[0]) * 0.3,
                self.current_center[1] + (target_y - self.current_center[1]) * 0.3
            )
            
            if random.random() < 0.4:
                self.add_ripple(
                    amplitude=5 + distance/10,
                    frequency=3 + distance/50,
                    decay=0.15
                )
    
    def on_release(self, event):
        self.is_dragging = False
        self.add_ripple(amplitude=10, frequency=4, decay=0.1)


def create_relaxing_frame(root):
    frame = tk.Frame(root, bg="#B2DFDB")
    frame.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(
        frame, 
        text="Take a deep breath...", 
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

    tip_label = tk.Label(
        frame,
        font=("Helvetica", 12, "italic"),
        bg="#B2DFDB",
        fg="#00796B",
        wraplength=350,
        justify="center"
    )
    tip_label.pack(pady=20)

    button = tk.Button(frame, text="Exit Relax", command=lambda: globe.app.show_frame("Main"))
    button.pack(pady=10)

    canvas = tk.Canvas(frame, width=300, height=300, bg="white", bd=0, highlightthickness=0)
    canvas.pack(pady=20)

    orb = InteractiveOrb(canvas)

    return frame  
