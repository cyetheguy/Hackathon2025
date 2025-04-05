## main app
app = None
client = None

## colors
white = (255, 255, 255)
black = (0,0,0)
teal = (178, 223, 219)
dark_turquoise = (0, 77, 64)
purple = (165, 120, 205)
stormy_gray = (25, 25, 25)
gray = (105, 105, 105)
razorback = (157, 34, 53)

## fonts
title_font = ("Papyrus", 60)

def lerp(tuple1, tuple2, t):
    if not (0 <= t <= 1):
        raise ValueError("The interpolation factor t must be between 0 and 1.")
    if len(tuple1) != len(tuple2):
        raise ValueError("The input tuples must have the same length.")
    return tuple(int(a + (b - a) * t) for a, b in zip(tuple1, tuple2))

def rgb_to_hex(rgb):
    if not (len(rgb) == 3 and all(0 <= value <= 255 for value in rgb)):
        raise ValueError("Input must be a tuple of three integers between 0 and 255.")
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def lerp_to_hex(color1:tuple, color2:tuple, a:int) -> str:
    lerp_tup = lerp(color1, color2, a)
    return rgb_to_hex(lerp_tup)
