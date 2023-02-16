import array, time
from machine import Pin
from machine import PWM
import rp2
import math
 
# Configure the number of WS2812 LEDs.
NUM_LEDS = 2
PIN_NUM = 22
PIN_PWM = 11
brightness = 1
 
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

#Create PWM pin
pwm = PWM(Pin(PIN_PWM))
pwm.freq(1000)
 
# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
 
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
 
# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])
 
##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)
 
def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)
 

# Define the colors to be used for the smooth color transition
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 255), (255, 0, 255)]
# Define the delay between color transitions in seconds
DELAY = 0.02

# Define the number of steps for each color transition
STEPS = 50

# Define a function to smoothly transition between two colors
def smooth_color_transition(color1, color2, steps):
    # Calculate the amount to increment each color channel for each step
    r_step = (color2[0] - color1[0]) / steps
    g_step = (color2[1] - color1[1]) / steps
    b_step = (color2[2] - color1[2]) / steps
    # Create a list of tuples representing each step in the transition
    transition = [(int(color1[0] + r_step * i), int(color1[1] + g_step * i), int(color1[2] + b_step * i)) for i in range(steps)]
    return transition

# Initialize the color index to 0
color_index = 0

while True:
    # Get the current color and the next color in the color sequence
    current_color = COLORS[color_index % len(COLORS)]
    next_color = COLORS[(color_index + 1) % len(COLORS)]
    # Smoothly transition between the current and next colors
    transition = smooth_color_transition(current_color, next_color, STEPS)
    for color in transition:
        # Set the color of each pixel in the strip
        pixels_fill(color)
        pixels_show()
        # Pause for the specified delay
        time.sleep(DELAY)
    # Increment the color index
    color_index += 1
    x = math.sin(0.5)
    print(x)

    duty = 0
    direction = 1
    for _ in range(8 * 256):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        pwm.duty_u16(duty * duty)
        time.sleep(0.001)
