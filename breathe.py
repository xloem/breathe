#!/usr/bin/env python3

import blessings
import time
import sys
import random
import math

gift = blessings.Terminal(force_styling=True)

class easing:
    def sine_in_out(percent):
        return (1 - math.cos(percent * math.pi)) / 2
    def linear(percent):
        return percent

def brightness_color(brightness):
    colors = (gift.black, gift.dim_white, gift.white)
    color1 = math.floor(brightness * (len(colors) - 1))
    color2 = color1 + 1
    brightness1 = color1 / (len(colors) - 1)
    brightness2 = color2 / (len(colors) - 1)
    if random.random() * (brightness2 - brightness1) + brightness1 < brightness:
        return colors[color2]
    else:
        return colors[color1]

def write(string1, string2, percent, brightness):
    for index in range(max(len(string1),len(string2))):
        character2 = string2[index]
        character1 = string1[index]
        this_brightness = brightness
        if character1 == ' ':
            this_brightness = percent * brightness
            character1 = character2
        elif character2 == ' ':
            this_brightness = brightness - percent * brightness
            character2 = character1
        if random.random() < percent:
            character = character2
        else:
            character = character1
        sys.stdout.write(brightness_color(this_brightness) + character + gift.normal)


def fade_at(string1, string2, brightness1, brightness2, x, y, total_seconds = 0.1, curve = easing.linear):
    start = time.time()
    while True:
        now = time.time()
        if now - start > total_seconds:
            break
        pct = curve((now - start) / total_seconds)
        with gift.location(x,y):
            write(string1, string2, pct, (brightness2 - brightness1) * pct + brightness1)
        sys.stdout.flush()
        time.sleep(0.1)
    with gift.location(x,y):
        write(string1, string2, 1.0, brightness2)
        sys.stdout.flush()


def slide(string, each_seconds = 0.1, curve = easing.linear, undo = False):
    seconds_passed = 0
    for index in range(len(string)):
        fade(string[index], each_seconds, curve, undo)
        seconds_passed += each_seconds
    return seconds_passed
#
#def block(string, count = 30):
#    #for x in range(count):
#    #    line('')
#    #    #time.sleep(1)
#    line('')
#    line(string)
#    line('')
#    time.sleep((count - 2) * 0.1)

# i'd like it to spend more time bright and dark
# maybe supporting curves would be nice
# what does sine_ease_in_out look like
# (1 - cos(pct * pi)) / 2

def fade_between(string1, string2, brightness1, brightness2, seconds = 1, curve = easing.sine_in_out):
    from_left = (gift.width - max(len(string2),len(string1))) // 2
    from_top = gift.height // 2
    fade_at(string1, string2, brightness1, brightness2, from_left, from_top, seconds, curve)

def fade(string, brightness1, brightness2, seconds = 1, curve = easing.sine_in_out):
    fade_between(string, string, brightness1, brightness2, seconds, curve)

#def show(text, total_seconds, fade_seconds, curve = easing.sine_in_out):
#    fade(text, text, 0, 1, from_left, from_top, fade_seconds, curve)
#    time.sleep(max(total_seconds - fade_seconds * 2, 0))
#    fade(text, text, 1, 0, from_left, from_top, fade_seconds, curve)
#
#def fade_in(text, seconds, curve = easing.sine_in_out):
#    from_left = (gift.width - len(text)) // 2
#    from_top = gift.height // 2
#    fade_at(text, text, 0, 1, from_left, from_top, seconds, curve)
#
#def fade_out(text, seconds, curve = easing.sine_in_out):
#    from_left = (gift.width - len(text)) // 2
#    from_top = gift.height // 2
#    fade_at(text, text, 1, 1, from_left, from_top, seconds, curve)

secondary = [
        '',
        'Notice the environment around you'
        ]

with gift.fullscreen():
    with gift.hidden_cursor():
        scale = 1.0
        breathe_in_time = 5
        breathe_out_time = 10
        secondary_index = 0
        # we want to fade secondary while fading primary
        # so we'll need fade objects
        while True:
            fade('Breathe in ', 0, 1, breathe_in_time / 2)
            fade_between('Breathe in ', 'Breathe ou ', 1, 1, breathe_in_time / 4)
            fade_between('Breathe ou ', 'Breathe out', 1, 1, breathe_in_time / 4)
            fade('Breathe out', 1, 0, breathe_out_time)

            ##show('Breathe in more.', 0.3)
            ##line('\nPress enter when your lungs are full.')
            ##sys.stdin.read(1)
            #fade_out('Breathe out.', breathe_out_time / 2)
            #time.sleep(breathe_out_time / 2)
            breathe_in_time = (breathe_in_time + breathe_out_time) / 2
            breathe_out_time = breathe_out_time * 1.05
            #scale = scale * 1.001
            ##line('\nPress enter when your lungs are empty.')
            ##sys.stdin.read(1)
            ##
