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
from statemachine import StateMachine, State


#print("sono in subprocess")
#v = np.array([1, 2, 3])
#print(','.join(map(str, v)))

print("a" + "b")

w=200
h=500

button = []
number = ["1", "2", "3", "4", "5", "6", "7"]

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

text = visual.TextStim(win, text="How much are you confident on your free-hand drawing skills?", color=(0, 0, 0),
                       pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
text.draw()



space = 0
for i in range(0, 7):
    print("prima di butt")
    button.append(visual.ButtonStim(win, text=number[i], color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47], pos=[-720 + space, -250], size=(100, 100), units='pix'))
    space += 240
    print(space)

for j in range(0, 7):
    button[j].draw()

#butt = visual.ButtonStim(win, text=number[0], color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47], pos=[-720 + space, -250], size=(100, 100), units='pix')
#butt.draw()
win.flip()

#myMouse.clickReset
buttons = myMouse.getPressed()

while buttons[0] == False | buttons[1] == False | buttons[2] == False:
    buttons = myMouse.getPressed()