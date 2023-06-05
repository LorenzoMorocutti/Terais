#!/usr/bin/env python3

import os
import time
import pandas as pd
import random
import wx
from psychopy import event, visual, monitors, core
import datetime
import sys
import numpy as np
import subprocess
#from statemachine import StateMachine, State
import csv

participant = sys.argv[1]

####### CHANGE THE PATH
path_folder_participant = "/root/StimuliVal/Images/" + participant
os.mkdir(path_folder_participant)

seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # 0 is ambulance, 1 is owl, 2 is flower
random.shuffle(seq)
categories = ['Ambulance', 'Tractor', 'Owl',
              'Train', 'Sheep', 'LightBulb',
              'Lion', 'BirthdayCake',
              'Bee', 'Mermaid', 'Flower',
              'Spider', 'Leaf', 'Pizza', 
              'Face', 'Bus', 'PalmThree']


number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
button = []

global win

####### CHANGE THE PATH 
script_path = "/root/StimuliVal/drawing.py"

drawing_enjoyment = 0
drawing_frequency = 0
drawing_percentage = 0

difficulty_ranking = [0, 0, 0]
enjoyment_ranking = [0, 0, 0]
likeability_ranking = [0, 0, 0]

latency_time = [0, 0, 0]
total_drawing_time = [0, 0, 0]
number_of_strokes = [0, 0, 0]


def drawing_questions(n):
    text = visual.TextStim(win, text="How difficult it was to draw the " + categories[n] + "? \n"
                            "(1 - not difficult, 7 - extremely difficult)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                              pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                difficulty_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    text = visual.TextStim(win, text="How much did you enjoy drawing the " + categories[n] + "? \n"
                            "(1 - not enjoyed, 7 - extremely enjoyed)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                              pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                enjoyment_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    text = visual.TextStim(win, text="How much do you like your drawing of the " + categories[n] + "? \n"
                            "(1 - not liked, 7 - liked a lot)",
                           color=(1, 1, 1), pos=(0.0, 15.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()


    image = visual.ImageStim(win, image=path_folder_participant + "/" + categories[n] + ".png", size=(600, 337),
                             units='pix', pos=(0.0, -5.0))
    image.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                              pos=[-720 + space, -300], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                likeability_ranking[n] = k + 1
                touch = True

    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    return


def drawing_activity(i):

    win.close()
    print("window closed, ready to open drawing")

    p = subprocess.Popen(["python3", script_path, str(i), participant], stdout=subprocess.PIPE)
    p.wait()

    output = []
    output = p.stdout.read()

    array = np.fromstring(output.decode(), dtype=float, sep=',')

    print(i)

    latency_time[i] = array[0]
    total_drawing_time[i] = array[1]
    number_of_strokes[i] = array[2]

    configure()

    text = visual.TextStim(win, text="Thank you very much. \nNow please answer to some questions. \n\nClick to continue", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    win.flip()

    wait_touch()

    drawing_questions(i)

    return


def drawing_task(n):

    text = visual.TextStim(win, text="Are you ready to draw? \n\nClick to continue", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    win.flip()

    wait_touch()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)


    text = visual.TextStim(win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)

    text2 = visual.TextStim(win, text=categories[n], color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                           colorSpace='rgb', bold=True, height=5, anchorHoriz="center", wrapWidth=500)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    drawing_activity(n)

    return




def artistic_questions():
    global drawing_enjoyment, drawing_frequency, drawing_percentage

    text = visual.TextStim(win, text="How much do you enjoy free-hand drawing? \n (1 - extremely little, 7 - extremely much)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

    for j in range(0, 7):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 7):
            if myMouse.isPressedIn(button[k]):
                drawing_enjoyment = k+1
                touch = True

    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)

    text = visual.TextStim(win, text="How often do you draw sketches? \n (1 - extremely little, 7 - extremely much)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()

    space = 0

    for i in range(0, 7):
        button.append(visual.ButtonStim(win, text=number[i], color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                        pos=[-720 + space, -250], size=(100, 100), units='pix'))
        space += 240

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
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center",
                           wrapWidth=500)
    text.draw()

    space = 0

    button.append(visual.ButtonStim(win, text="0%", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                                    pos=[-800, -250], size=(100, 100), units='pix'))

    for i in range(0, 10):

        button.append(visual.ButtonStim(win, text=number[i]+"0%", color=[1, 1, 1], colorSpace='rgb', fillColor=[-0.3, -0.3, 0.9],
                              pos=[-640 + space, -250], size=(100, 100), units='pix'))
        space += 160

    for j in range(0, 11):
        button[j].draw()

    win.flip()

    touch = False

    while touch == False:
        for k in range(0, 11):
            if myMouse.isPressedIn(button[k]):
                drawing_percentage = k*10
                touch = True


    button.clear()
    time.sleep(0.5)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)

    text = visual.TextStim(win, text="Thank you very much. \n Now the drawing task will begin. Click to continue.",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=3.5,
                           anchorHoriz="center",
                           wrapWidth=500)
    text.draw()
    win.flip()

    wait_touch()

    return


def black_window():
    black_poly = visual.Polygon(win, edges=4, fillColor="black", pos=[0, 0], size=[400, 105], ori=0)
    black_poly.draw()
    win.flip()  # show the stim
    time.sleep(2)

    return


# function to wait for the touch of the mouse
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
        color=(-0.4, -0.4, 1),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=False,
        fullscr=True
    )

    myMouse = event.Mouse(win)
    myMouse.setPos(newPos=(0, 0))

    return


def main():
    configure()

    text = visual.TextStim(win, text="Welcome to the experiment! It will be asked you to draw \n"
                                     "different subjects and then to answer some simple questions. \n"
                                     "Are you ready? "
                                     " \n\nClick to continue", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=3.5, anchorHoriz="center", wrapWidth=500)
    text.draw()
    win.flip()

    wait_touch()

    artistic_questions()

    for i in seq:
        drawing_task(i)

    art_results = {
        'art_enjoyment': drawing_enjoyment,
        'art_frequency': drawing_frequency,
        'art_percentage': drawing_percentage
    }

    rank_results = {
        'Ambulance difficulty': difficulty_ranking[0],
        'Owl difficulty': difficulty_ranking[1],
        'Flower difficulty': difficulty_ranking[2],

        'Ambulance enjoyment': enjoyment_ranking[0],
        'Owl enjoyment': enjoyment_ranking[1],
        'Flower enjoyment': enjoyment_ranking[2],

        'Ambulance likeability': likeability_ranking[0],
        'Owl likeability': likeability_ranking[1],
        'Flower likeability': likeability_ranking[2]
    }

    time_stroke_results = {
        'Ambulance latency': latency_time[0],
        'Owl latency': latency_time[1],
        'Flower latency': latency_time[2],

        'Ambulance total time': total_drawing_time[0],
        'Owl total time': total_drawing_time[1],
        'Flower total time': total_drawing_time[2],

        'Ambulance total strokes': number_of_strokes[0],
        'Owl total strokes': number_of_strokes[1],
        'Flower total strokes': number_of_strokes[2]
    }

    # Create a data frame from the results
    df_art = pd.DataFrame(art_results, index=[participant])

    df_art.to_csv('art_data.csv', mode='a', header=True)



    # Create a data frame from the results
    df_rank = pd.DataFrame(rank_results, index=[participant])

    df_rank.to_csv('rank_data.csv', mode='a', header=True)



    # Create a data frame from the results
    df_time = pd.DataFrame(time_stroke_results, index=[participant])

    df_time.to_csv('time_data.csv', mode='a', header=True)

if __name__ == '__main__':
    main()

    sys.exit()