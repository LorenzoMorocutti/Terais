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
number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
enjoyment_drawing = 0
drawing_frequency = 0
drawing_percentage = 0

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




def artistic_questions():
    text = visual.TextStim(win, text="How much do you enjoy free-hand drawing? \n (1 - extremely little, 7 - extremely much)", color=(0, 0, 0),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240
        print(space)

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                enjoyment_drawing = k+1
                touch = True

    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)

    text = visual.TextStim(win, text="How often do you draw sketches? \n (1 - extremely little, 7 - extremely much)", color=(0, 0, 0),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240
        print(space)

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                drawing_frequency = k+1
                touch = True


    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)

    text = visual.TextStim(win, text="Imagine other 100 people drawing the same sketches as yours: \n"
                                     " how many of them do you think will draw better than you \n "
                                     "(0% - almost no one, 100% - almost everyone)",
                           color=(0, 0, 0), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()

    space = 0

    button.append(visual.ButtonStim(win, text="0%", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
                                    pos=[-800, -250], size=(100, 100), units='pix'))

    for i in range(0, 10):

        button.append(visual.ButtonStim(win, text=number[i]+"0%", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
                              pos=[-640 + space, -250], size=(100, 100), units='pix'))
        space += 160
        print(space)

    for j in range(0, 11):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 11):
            if myMouse.isPressedIn(button[k]):
                drawing_percentage = k
                touch = True

    print(enjoyment_drawing, drawing_frequency, drawing_percentage)

    return

artistic_questions()