# Copyright (C) 2021 Hugo Dahl for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Source: https://github.com/ajs256/matrixportal-weather-display

# ############## IMPORTS ###############

# BASICS (these are all built in)
import time  # The function to use the onboard RTC to give us time values
import board  # Pin definitions
import terminalio  # Provides the font we use
import busio  # Provides SPI for talking to the ESP32
import digitalio  # Provides pin I/O for the ESP32
import rtc  # Lets us keep track of the time
import neopixel  # To drive the onboard NeoPixel.

# INTERNET
import adafruit_requests as requests  # For getting data from the Internet
from adafruit_esp32spi import adafruit_esp32spi  # For talking to the ESP32
import adafruit_esp32spi.adafruit_esp32spi_socket as socket  # For using the ESP32 for internet connections
from adafruit_io.adafruit_io import IO_HTTP  # For talking to Adafruit IO
from config import config  # The config file, see the README for what to put here
from secrets import secrets  # secrets, etc.

# DISPLAY
from adafruit_display_text import label  # For showing text on the display
import displayio  # Main display library
import framebufferio  # For showing things on the display
import rgbmatrix  # For talking to matrices specifically
from adafruit_bitmap_font import bitmap_font  # Fonty goodness

# CONTROLS

from adafruit_verticalprogressbar import ProgressBar

# ############## DISPLAY SETUP ###############

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

print("Setting up RGB matrix")

# This next call creates the RGB Matrix object itself. It has the given width
# and height.
#
# These lines are for the Matrix Portal. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=3,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2,
    ],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
)

font_list = ["helvR10", "helvB12", "IBMPlexMono-Medium-24_jep", "6x10", "cozette"]

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix)

print("Adding display group")

group = displayio.Group(max_size=5)  # Create a group to hold all our labels

display.show(group)

print("Creating progress bar and adding to group")
progress_bar = ProgressBar((2, 4), (20, 20), margin=False)
progress_bar.progress = 0.0
group.insert(0, progress_bar)

progress_bar_value = 0.0
progress_bar_incr = 3.0

while True:
    if progress_bar_value > 100:
        progress_bar_value = 100
        progress_bar_incr *= -1

    if progress_bar_value < 0:
        progress_bar_value = 0
        progress_bar_incr *= -1

    progress_bar.progress = progress_bar_value
    progress_bar_value += progress_bar_incr
    time.sleep(0.5)
