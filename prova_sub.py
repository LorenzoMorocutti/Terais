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


text = visual.TextStim(win, text="How much are you confident on your free-hand drawing skills?", color=(0, 0, 0), pos=(0.0, 11.0),
                       colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", anchorVert="center", wrapWidth=500)
print(text.boundingBox)
text.draw()
win.flip()

#myMouse.clickReset
buttons = myMouse.getPressed()

while buttons[0] == False | buttons[1] == False | buttons[2] == False:
    buttons = myMouse.getPressed()