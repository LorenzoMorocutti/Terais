#!/usr/bin/env python3

import os
import time
#import panda as pd
import random
import wx
from psychopy import event, visual, monitors, core
import datetime
import sys
import numpy as np
import subprocess

seq=[0,1,2]
random.shuffle(seq)
global win
script_path = "/root/StimuliVal/drawing.py"

def state_machine(seq):
    for i in seq:
        print("ok")


#function to write something simple on the screen
def write_something(what_to_write):
    count = 0

    text = visual.TextStim(win, text=what_to_write, color=(0, 0, 0), colorSpace='rgb', bold=True, height=5.0)
    text.draw()
    button = visual.ButtonStim(win, text="1", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47], pos=[-200, -250], size=(100, 100), units='pix')
    button2 = visual.ButtonStim(win, text="2", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47], pos=[200, -250], size=(100, 100), units='pix')
    button.draw()
    button2.draw()
    win.flip()

    print(count)

    # if myMouse.isPressedIn(button):
    #     count = count + 1
    #     print(count)

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            count = count + 1
            touch = True
    
    print(count)

    time.sleep(0.1)

    return


def black_window():
    black_poly = visual.Polygon(win, edges=4, fillColor="black", pos=[0, 0], size=[105, 105], ori=45)
    black_poly.draw()
    win.flip()  # show the stim
    time.sleep(2)

    return


#function to wait for the touch of the mouse
def wait_touch():
    myMouse.clickReset
    buttons = myMouse.getPressed()
    print(buttons)
    while buttons[0] == False | buttons[1] == False | buttons[2] == False:
        buttons = myMouse.getPressed()

    print(buttons)
    print("click")
    time.sleep(1)

    return


def configure():

    global win, widthPix, heightPix, monitorWidth, viewdist, monitorname, scrn, mon, myMouse

    widthPix = 1920
    heightPix = 1080
    monitorWidth = 50.2
    viewdist = 25.4
    monitorname = 'testMonitor'
    scrn = 0
    mon = monitors.Monitor(monitorname, width=monitorWidth, distance=viewdist)
    mon.setSizePix((widthPix, heightPix))


    win = visual.Window(
        monitor=mon,
        size=(widthPix, heightPix),
        color=(0.58, 0.75, 0.54),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=False,
        fullscr=True
    )

    myMouse = event.Mouse(win)

    return



def main():
    configure()
    write_something("Clicca per andare avanti")
    #black_window()
    #wait_touch()
    draw = subprocess.run(["python3", script_path])
    wait_touch()



if __name__ == '__main__':
    main()