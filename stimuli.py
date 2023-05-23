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

seq=[0,1,2] #0 is ambulance, 1 is owl, 2 is flower
random.shuffle(seq)
categories = ['Ambulance', 'Owl', 'Flower']

candidate = []
number = ["1", "2", "3", "4", "5", "6", "7"]
button = []

global win

script_path = "/home/icub/Desktop/Terais/drawing.py"




#How much do you enjoy hand drawing?
#How often do you draw sketches?
#Imagine 100 other people who have completed the drawing tasks. How many of them do you think would draw better sketches than yours: 0-100
class Experiment(StateMachine):

    index = 0

    # defining constructor
    def __init__(self, ind):
        self.index = ind


    # creating states
    drawing_state = State(initial=True)
    questions_state = State(final=True)

    # transitions of the state
    drawing_state.to(questions_state, cond="drawing_completed") )

    def drawing_completed(self):
        drawing_questions(self.index)

        return



def state_machine(index):
    candidate[index] = Experiment(index)
    return


def artistic_questions(index):

    text = visual.TextStim(win, text="How much are you confident on your free-hand drawing skills?", color=(0, 0, 0), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    space = 0

    for i in range(1, 7):
        button[i] = visual.ButtonStim(win, text=number[i], color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47], pos=[-720+space, -250], size=(100, 100), units='pix')
        button[i].draw()
        space+=240

    win.flip()

    return



def drawing_questions(index):
    return



#function to write something simple on the screen
def write_something(what_to_write):
    count = 0

    text = visual.TextStim(win, text="How much are you confident on your free-hand drawing skills?", color=(0, 0, 0), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", anchorVert="center", wrapWidth=500)
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
    black_poly = visual.Polygon(win, edges=4, fillColor="black", pos=[0, 0], size=[400, 105], ori=0)
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


def write_keyboard():
    count = 0

    text1 = visual.TextStim(win, text="clicca per andare avanti", color=(0, 0, 0), colorSpace='rgb', bold=True, height=5.0)
    text1.draw()
#    button = visual.ButtonStim(win, text="1", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
#                               pos=[-200, -250], size=(100, 100), units='pix')
#    button2 = visual.ButtonStim(win, text="2", color=[0, 0, 0], colorSpace='rgb', fillColor=[0.5, 0.66, 0.47],
#                                pos=[200, -250], size=(100, 100), units='pix')
#    button.draw()
#    button2.draw()
    win.flip()



    print(count)


    print("I'm in write keyboard")

    #subprocess.Popen(["python3", script_path])

    #keys = event.waitKeys(keyList='return')

    #win.flip()

    win.close()

    p = subprocess.Popen(["python3", script_path], stdout=subprocess.PIPE)
    p.wait()

    #print(keys)



    configure()
    text2 = visual.TextStim(win, text="able to reopen psychopy", color=(0, 0, 0), colorSpace='rgb', bold=True, height=5.0)
    text2.draw()
    win.flip()

    wait_touch()

    black_window()


    print("enter pressed")

    time.sleep(0.1)

    return


def configure():

    global win, widthPix, heightPix, monitorWidth, viewdist, monitorname, scrn, mon, myMouse, myKey

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

    artistic_questions()

    for i in seq:
        state_machine(i)


    write_something("Clicca per andare avanti")


    write_keyboard()

    black_window()



if __name__ == '__main__':
    main()

    sys.exit()