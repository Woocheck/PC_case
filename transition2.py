import time
import neopixel

# Define the number of pixels in the strip
NUM_PIXELS = 1

# Initialize the neopixel object with the number of pixels and the pin used
pixels = neopixel.NeoPixel(machine.Pin(5), NUM_PIXELS)

# Define the colors to be used for the smooth color transition
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 255), (255, 0, 255)]

# Define the delay between color transitions in seconds
DELAY = 0.02

# Define the number of steps for each color transition
STEPS = 50

# Define the initial brightness of the LED
BRIGHTNESS = 0.5

# Define a function to smoothly transition between two colors
def smooth_color_transition(color1, color2, steps):
    # Calculate the amount to increment each color channel for each step
    r_step = (color2[0] - color1[0]) / steps
    g_step = (color2[1] - color1[1]) / steps
    b_step = (color2[2] - color1[2]) / steps
    # Create a list of tuples representing each step in the transition
    transition = [(int(color1[0] + r_step * i), int(color1[1] + g_step * i), int(color1[2] + b_step * i)) for i in range(steps)]
    return transition

# Define a function to adjust the brightness of the LED
def set_brightness(brightness):
    pixels[0] = tuple(int(c * brightness) for c in pixels[0])

# Initialize the color index to 0
color_index = 0

while True:
    # Get the current color and the next color in the color sequence
    current_color = COLORS[color_index % len(COLORS)]
    next_color = COLORS[(color_index + 1) % len(COLORS)]
    # Smoothly transition between the current and next colors
    transition = smooth_color_transition(current_color, next_color, STEPS)
    for color in transition:
        # Set the color and brightness of the LED
        pixels[0] = color
        set_brightness(BRIGHTNESS)
        # Pause for the specified delay
        time.sleep(DELAY)
    # Increment the color index
    color_index += 1
