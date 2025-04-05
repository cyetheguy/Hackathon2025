import tkinter as tk
import tkinter.font as tkfont
import random
import globe
import threading
import time
import math
from itertools import cycle
import main

class InteractiveOrb:
    def __init__(self, canvas, orb_type="water"):
        self.canvas = canvas
        self.origin = (150, 150)
        self.current_center = (150, 150)
        self.base_radius = 60
        self.current_radius = 60
        self.is_dragging = False
        self.drag_point = None
        self.orb_type = orb_type
        self.orb_id = None
        self.particles = []
        
        # Set colors based on orb type
        if self.orb_type == "water":
            self.orb_color = "#88E0EF"
            self.shadow_color = "#3DCCC7"
            self.depth_layers = [
                {"color": "#C4F1F9", "radius_ratio": 0.9, "ripple_ratio": 0.7},
                {"color": "#88E0EF", "radius_ratio": 0.7, "ripple_ratio": 0.5},
                {"color": "#3DCCC7", "radius_ratio": 0.5, "ripple_ratio": 0.3}
            ]
        else:  # lava
            self.orb_color = "#FF5722"
            self.shadow_color = "#E64A19"
            self.depth_layers = [
                {"color": "#FFCCBC", "radius_ratio": 0.9, "ripple_ratio": 0.7},
                {"color": "#FF8A65", "radius_ratio": 0.7, "ripple_ratio": 0.5},
                {"color": "#FF5722", "radius_ratio": 0.5, "ripple_ratio": 0.3}
            ]
        
        self.ripple_points = 36
        self.surface_ripples = []
        self.stretch_factor = 0
        self.elasticity = 0.2
        self.max_stretch = 3.0
        
        self.orb_ids = []
        self.highlight_id = None
        self.bubble_ids = []
        
        self.create_orb()
        self.setup_interaction()
        self.start_animation()
    
    def setup_interaction(self):
        """Set up mouse event bindings for interaction"""
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def change_type(self, new_type):
        """Change the orb type (water/lava) and update visuals"""
        self.orb_type = new_type
        if self.orb_type == "water":
            self.depth_layers = [
                {"color": "#C4F1F9", "radius_ratio": 0.9, "ripple_ratio": 0.7},
                {"color": "#88E0EF", "radius_ratio": 0.7, "ripple_ratio": 0.5},
                {"color": "#3DCCC7", "radius_ratio": 0.5, "ripple_ratio": 0.3}
            ]
        else:  # lava
            self.depth_layers = [
                {"color": "#FFCCBC", "radius_ratio": 0.9, "ripple_ratio": 0.7},
                {"color": "#FF8A65", "radius_ratio": 0.7, "ripple_ratio": 0.5},
                {"color": "#FF5722", "radius_ratio": 0.5, "ripple_ratio": 0.3}
            ]
        self.create_orb()
    
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
        
        highlight_color = "white" if self.orb_type == "water" else "#FFECB3"
        self.highlight_id = self.canvas.create_oval(
            hl_x - highlight_size * 0.6, hl_y - highlight_size * 0.3,
            hl_x + highlight_size * 0.6, hl_y + highlight_size * 0.3,
            fill=highlight_color, outline="", stipple="gray50"
        )
    
    def add_surface_detail(self):
        for _ in range(3):
            bubble_size = random.uniform(3, 8)
            angle = random.uniform(0, math.pi/2)
            distance = random.uniform(0.3, 0.7) * self.base_radius
            
            x = self.current_center[0] + distance * math.cos(angle)
            y = self.current_center[1] - distance * math.sin(angle)
            
            # Different bubble colors for water vs lava
            if self.orb_type == "water":
                bubble_color = "white"
            else:
                bubble_color = "#FFECB3"  # Yellowish for lava bubbles
            
            self.bubble_ids.append(self.canvas.create_oval(
                x - bubble_size, y - bubble_size,
                x + bubble_size, y + bubble_size,
                fill=bubble_color, outline="", stipple="gray50"
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
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    
    # Initialize with light theme colors
    bg_color = "#B2DFDB"
    fg_color = "#004D40"
    frame.config(bg=bg_color)
    
    # Create a main container frame
    main_container = tk.Frame(frame, bg=bg_color)
    main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    # Quote section at the top
    quote_frame = tk.Frame(main_container, bg=bg_color)
    quote_frame.pack(fill=tk.X, pady=10)
    
    # Title label
    title_label = tk.Label(
        quote_frame, 
        text="Mindful Moment", 
        font=("Helvetica", 18, "italic"), 
        bg=bg_color, 
        fg=fg_color
    )
    title_label.pack(pady=(10, 5))
    
    # Subtitle with breathing reminder
    subtitle_label = tk.Label(
        quote_frame,
        text="Breathe deeply...",
        font=("Helvetica", 14),
        bg=bg_color,
        fg="#00695C"
    )
    subtitle_label.pack(pady=(0, 20))

    # Relaxation tips database (expanded)
    relaxation_database = {
            "Mindfulness": [
                ("The present moment is the only moment available to us.", "Thich Nhat Hanh"),
                ("Feelings come and go like clouds in a windy sky.", "Jon Kabat-Zinn"),
                ("Wherever you are, be there totally.", "Eckhart Tolle"),
                ("Mindfulness isn't difficult, we just need to remember to do it.", "Sharon Salzberg")
            ],
            "Breathing": [
                ("Breathe in deeply to bring your mind home to your body.", "Thich Nhat Hanh"),
                ("The breath is the bridge which connects life to consciousness.", "Thich Nhat Hanh"),
                ("When you own your breath, nobody can steal your peace.", "Unknown"),
                ("Deep breathing brings deep thinking.", "William Wordsworth")
            ],
            "Stress Relief": [
                ("You don't have to control your thoughts. You just have to stop letting them control you.", "Dan Millman"),
                ("It's not the load that breaks you down, it's the way you carry it.", "Lena Horne"),
                ("Stress is caused by being 'here' but wanting to be 'there'.", "Eckhart Tolle"),
                ("Tension is who you think you should be. Relaxation is who you are.", "Chinese Proverb")
            ],
            "Calmness": [
                ("Calm mind brings inner strength and self-confidence.", "Dalai Lama"),
                ("Peace is the result of retraining your mind to process life as it is.", "Unknown"),
                ("The more tranquil a man becomes, the greater is his success.", "James Allen"),
                ("Serenity comes when you trade expectations for acceptance.", "Unknown")
            ],
            "Ancient Wisdom": [
                ("\"The mind is everything. What you think you become.\" - Buddha", "Dhammapada"),
                ("\"Nature does not hurry, yet everything is accomplished.\" - Lao Tzu", "Tao Te Ching"),
                ("\"Be here now.\" - Ram Dass", "1971 spiritual classic"),
                ("\"You have power over your mind - not outside events. Realize this, and you will find strength.\" - Marcus Aurelius", "Meditations"),
                ("\"The present moment is filled with joy and happiness. If you are attentive, you will see it.\" - Thich Nhat Hanh", "Peace Is Every Step"),
            ],
            
            "Modern Science": [
                ("Harvard study: 8 weeks of mindfulness practice shrinks the amygdala (stress center) and grows the prefrontal cortex (rational thinking)", "Psychiatry Research: Neuroimaging, 2011"),
                ("NIH meta-analysis: Meditation reduces anxiety equivalent to antidepressant drugs", "JAMA Internal Medicine, 2014"),
                ("Stanford research: Brief breathing exercises can lower blood pressure as effectively as medication", "Cell Reports Medicine, 2023"),
                ("UCLA findings: Regular meditation slows age-related brain degeneration", "Frontiers in Psychology, 2020"),
                ("Yale study: Mindfulness disrupts default mode network activity linked to rumination", "Science Advances, 2021"),
            ],
            
            "Breathing Techniques": [
                ("4-7-8 Method: Inhale 4s, hold 7s, exhale 8s (activates parasympathetic nervous system)", "Dr. Andrew Weil, Arizona Center for Integrative Medicine"),
                ("Box Breathing: 4s inhale, 4s hold, 4s exhale, 4s pause (used by Navy SEALs for stress control)", "Mark Divine, former SEAL commander"),
                ("Physiological Sigh: Double inhale through nose, long exhale (fastest way to calm down)", "Stanford Neuroscience Lab, 2022"),
                ("Alternate Nostril Breathing: Balances left/right brain hemispheres", "International Journal of Yoga, 2013"),
                ("Coherent Breathing: 5-6 breaths per minute optimizes heart rate variability", "Dr. Richard Brown, Columbia University"),
            ],
            
            "Body Awareness": [
                ("Progressive Muscle Relaxation: Systematically tense/release muscle groups (reduces cortisol)", "Journal of Behavioral Medicine, 2008"),
                ("Body Scan Meditation: Focus attention gradually from toes to head (enhances interoception)", "Dr. Jon Kabat-Zinn, MBSR founder"),
                ("Autogenic Training: Repeat warmth/heaviness phrases (developed by German neurologists)", "Schultz & Luthe, 1932"),
                ("Yoga Nidra: 'Sleep meditation' shown to boost dopamine by 65%", "University of California, 2021"),
                ("Tai Chi: Slow movement meditation improves balance and reduces inflammation", "Harvard Medical School, 2019"),
            ],
            
            "Cognitive Approaches": [
                ("RAIN Technique: Recognize, Allow, Investigate, Nurture (mindful emotion processing)", "Tara Brach, psychologist"),
                ("Cognitive Defusion: Observe thoughts like clouds passing (ACT therapy technique)", "Steven Hayes, Acceptance and Commitment Therapy"),
                ("Loving-Kindness Meditation: Repeating compassionate phrases increases social connectedness", "Barbara Fredrickson, UNC Chapel Hill"),
                ("Noting Practice: Mentally label experiences as 'thinking', 'feeling', etc. (vipassana technique)", "Mahasi Sayadaw, Burmese meditation master"),
                ("Gratitude Journaling: Writing 3 positive things daily rewires brain for optimism", "Dr. Martin Seligman, positive psychology pioneer"),
            ],
            
            "Nature Connection": [
                ("Forest Bathing (Shinrin-yoku): Phytoncides from trees boost immune cells by 40%", "Japanese Ministry of Agriculture, 2004"),
                ("Earthing: Barefoot contact with earth reduces inflammation markers", "Journal of Environmental and Public Health, 2012"),
                ("Blue Mind Theory: Water exposure induces meditative state", "Wallace Nichols, marine biologist"),
                ("Biophilic Design: Plants in workspace reduce stress by 37%", "University of Technology Sydney, 2020"),
                ("Nature Sounds: Birdsong lowers cortisol more than white noise", "King's College London, 2022"),
            ]
        }

    # Container for tip frames
    tips_container = tk.Frame(quote_frame, bg=bg_color)
    tips_container.pack(fill=tk.X)

    # Canvas for the interactive orb
    canvas = tk.Canvas(main_container, width=300, height=300, bg=bg_color, 
                      bd=0, highlightthickness=0)
    canvas.pack(pady=30)

    # Create the interactive orb (default to water)
    orb = InteractiveOrb(canvas, orb_type="water")

    # Instruction label below the orb
    instruction_label = tk.Label(
        main_container,
        text="Gently interact with the orb",
        font=("Helvetica", 10, "italic"),
        bg=bg_color,
        fg="#00796B"
    )
    instruction_label.pack(pady=10)
    
    # Exit button at the bottom

    # Add a button in the top-left corner
    top_left_button = tk.Button(frame, text="< Exit Relaxation", 
        text="Exit Relaxation", 
        command=lambda: globe.app.show_frame("Main"),
        bg=bg_color,
        fg=fg_color,
        activebackground=fg_color,
        activeforeground=bg_color,
        relief=tk.RAISED,
        bd=2,
        font=("Helvetica", 12))
    top_left_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    button = tk.Button(
        
    )
    # button.pack(pady=20, side=tk.BOTTOM)

    def update_theme(is_light):
        nonlocal bg_color, fg_color
        if is_light:
            bg_color = "#B2DFDB"
            fg_color = "#004D40"
            orb.change_type("water")
        else:
            bg_color = "#263238"
            fg_color = "#FF5722"
            orb.change_type("lava")

        frame.config(bg=bg_color)
        main_container.config(bg=bg_color)
        quote_frame.config(bg=bg_color)
        tips_container.config(bg=bg_color)
        title_label.config(bg=bg_color, fg=fg_color)
        subtitle_label.config(bg=bg_color)
        instruction_label.config(bg=bg_color)
        button.config(bg=bg_color, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)
        canvas.config(bg=bg_color)

    def display_random_quotes():
        # Clear existing tips
        for widget in tips_container.winfo_children():
            widget.destroy()

        # Select and display random tips
        selected_categories = random.sample(list(relaxation_database.keys()), 3)
        selected_tips = [random.choice(relaxation_database[cat]) for cat in selected_categories]

        for tip, source in selected_tips:
            tip_frame = tk.Frame(tips_container, bg=bg_color)
            tip_frame.pack(pady=10, fill='x')
            
            tk.Label(
                tip_frame,
                text=f'"{tip}"',
                font=("Helvetica", 12),
                bg=bg_color,
                fg=fg_color,
                wraplength=500,
                justify="center"
            ).pack()
            
            tk.Label(
                tip_frame,
                text=f"~ {source}",
                font=("Helvetica", 10, "italic"),
                bg=bg_color,
                fg="#00796B"
            ).pack(pady=(5, 0))

    # Function to call when frame is shown
    def on_show():
        display_random_quotes()
        if hasattr(globe, 'app') and globe.app is not None:
            update_theme(globe.app.isLight)

    frame.on_show = on_show
    frame.update_theme = update_theme
    
    # Initial display
    on_show()
    
    return frame

