import pyautogui
from consts import *


def reduce_sc_colors(color):
    if color[0] > 15:
        return True
    return False


# TODO: test remaining colors to see if they're properly identified
# 7, 8

# Identify tile base on colors from screenshot
def identify_tile(colors):
    # There should only be atmost 2 colors within a single screenshot.
    # This could either be a combination of the color of the number (if one exists)
    # and the brown background (just the background if no number) or just the grass

    # If there are two colors, we know that there is a number and the background
    # The color will always have less pixels than the dirt, quickly sort the list
    # get the first color and return it
    if len(colors) > 1:
        colors.sort()
        if colors[0][1] == FLAG_POLE:
            return "flag"
        return colors[0][1]

    # Otherwise, the tile we have is either the background or grass
    # identify and return accordingly
    else:
        if colors[0][1] in GRASS:
            return "grass"
        elif colors[0][1] in DIRT:
            return "dirt"


while True:
    x = int(input())
    y = int(input())
    print(665 + (x * 25), 370 + (y * 25))
    xpos = 665 + (x * 25)
    ypos = 370 + (y * 25)
    pyautogui.moveTo(xpos, ypos)
    sc = pyautogui.screenshot(region=(xpos - 10.5, ypos - 10.5, 20, 20))
    print(sc)
    sc.save("1.png")
    colors = sc.getcolors()
    ncolors = list(filter(reduce_sc_colors, colors))
    print(ncolors)
    r = identify_tile(ncolors)
    print(r)
