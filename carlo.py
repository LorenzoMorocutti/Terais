import time
import wx
import yarp
import os
from psychopy import event, visual, monitors
import datetime
import sys
import pandas as pd
import numpy as np

def info(msg):
    print("[INFO] {}".format(msg))

    return


class graphicInterface(yarp.RFModule):

    def __init__(self):
        yarp.RFModule.__init__(self)

        self.module_name = None
        self.handle_port = None
        self.input_port = None
        self.output_port = None

        self.input_bottle = None
        self.architecture_path = None
        self.saving_path = None
        self.image_path = None
        self.player_name = None
        self.state = None
        self.first_turn = None
        self.turn = None
        self.robot_drew = None
        self.times_human_drew = None

        self.grey1 = None
        self.grey2 = None
        self.monitor_h_cm = None
        self.monitor_w_cm = None
        self.monitor_h_px = None
        self.monitor_w_px = None
        self.b_win = None
        self.win = None
        self.myText = None
        self.myMouse = None
        self.myPolygon = None
        self.categories = None
        self.group_categories = None
        self.social_behavior = None
        self.drawing_aptitude = None
        self.TFRecord_path = None
        self.TF_dictionary = None
        self.mon = None
        self.columns = None
        self.df_all = None
        self.n_drawing = None
        self.turns = None
        self.h_perspective = None
        self.r_perspective = None


    def configure(self, rf):

        self.module_name = rf.check("name",
                                    yarp.Value("graphicInterface"),
                                    "module name (string)").asString()

        self.architecture_path = rf.check("architecture_path",
                                          yarp.Value("/usr/local/src/robot/cognitiveinteraction/container/IRCN-IIT/"),
                                          "Root path of the architecture (string)").asString()

        self.saving_path = rf.check("saving_path",
                                    yarp.Value(
                                        "/usr/local/src/robot/cognitiveinteraction/container/IRCN-IIT/saved_data/"),
                                    "Root path to save data (string)").asString()

        self.image_path = rf.check("image_path",
                                    yarp.Value(
                                        "/usr/local/src/robot/cognitiveinteraction/shareddrawing/python_script/graphicInterface/app/conf/ios/"),
                                    "Root path to load ios images (string)").asString()

        self.monitor_h_cm = rf.check("monitor_h_cm",
                                    yarp.Value(20),
                                    "monitor_h_cm (int)").asInt()

        self.monitor_w_cm = rf.check("monitor_w_cm",
                                    yarp.Value(35),
                                    "monitor_w_cm (int)").asInt()

        self.monitor_h_px = rf.check("monitor_h_px",
                                    yarp.Value(1080),
                                    "monitor_h_px (int)").asInt()

        self.monitor_w_px = rf.check("monitor_w_px",
                                    yarp.Value(1920),
                                    "monitor_w_px (int)").asInt()

        self.distance = rf.check("distance",
                                    yarp.Value(60),
                                    "player distance from the monitor (int)").asInt()
        self.player_name = "test"
        self.categories = ["owl", "mermaid", "ambulance", "bee", "train", "spider"]
        self.group_categories = "X6-1"
        self.social_behavior = 1
        self.drawing_aptitude = 1
        self.state = "black_window"
        self.robot_drew = False
        self.first_turn = "human"
        self.turn = "human"
        self.times_human_drew = 0
        self.n_drawing = 0
        self.turns = []
        self.h_perspective = []
        self.r_perspective = []

        self.grey1 = (-0.7, -0.7, -0.7)
        self.grey2 = (-0.9, -0.9, -0.9)

        self.mon = monitors.Monitor('myMonitor', width=self.monitor_w_cm, distance=self.distance)
        self.mon.setSizePix([self.monitor_w_px, self.monitor_h_px])
        #self.b_win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color="black")
        self.win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color=self.grey1)
        self.myMouse = event.Mouse()
        self.myText = visual.TextStim(self.win, color="snow", bold=True)
        self.myPolygon = visual.Polygon(self.win, edges=4, fillColor=self.grey2,
                                        lineWidth=1.5, lineColor="black", pos=[0, 0], size=[0.3, 0.5], ori=45)

        self.TF_dictionary = {
            "X3-1": "TFRecord_3.1_simplified",
            "X3-2": "TFRecord_3.2_simplified",
            "X3-3": "TFRecord_3.3_simplified",
            "X3-4": "TFRecord_3.4_simplified",
            "X6-1": "TFRecord_6.1_simplified",
            "X6-2": "TFRecord_6.2_simplified",
            "X6-new": "TFRecord_simplified_6_new",
            "X12": "TFRecord_simplified"
        }
        self.columns = ["player_name", "category_group", "social_behaviour", "drawing_aptitude", "n_drawing", "n_turn",
                        "drawer", "h_perspective", "r_perspective", "drawing_score", "interaction_score", "ios_score",
                        "final_cat"]
        self.df_all = pd.DataFrame(columns=self.columns)

        self.handle_port = yarp.Port()
        self.input_port = yarp.BufferedPortBottle()
        self.output_port = yarp.BufferedPortBottle()
        # Create handle port to read message
        self.handle_port.open('/' + self.module_name)
        # Create input port to read info from stateController
        self.input_port.open('/' + self.module_name + '/bottle:i')
        # Create output port to send info to stateController
        self.output_port.open('/' + self.module_name + '/bottle:o')

        info("Initialization complete")

        return True

    def interruptModule(self):
        print("[INFO] Stopping the module")

        self.handle_port.interrupt()
        self.input_port.interrupt()
        self.output_port.interrupt()

        return True

    def close(self):
        self.handle_port.close()
        self.input_port.close()
        self.output_port.close()

        return True

    def getPeriod(self):
        """
           Module refresh rate.

           Returns : The period of the module in seconds.
        """
        return 0.05

    def updateModule(self):

        self.read_input()

        if self.state == "black_window":
            self.black_window()

        elif self.state == "welcome":
            self.write_on_screen_touch("Welcome!  \n Please, touch the screen to start the game")
            time.sleep(1)
            if self.output_port.getOutputCount():
                info_out = self.output_port.prepare()
                info_out.clear()
                info_out.addString("user_ok_welcome")   # for the moment this is not needed
                self.output_port.write()
                self.state = "wait"

        elif self.state == "new_drawing":
            print(self.state)
            self.turns = []
            self.r_perspective = []
            self.h_perspective = []
            self.times_human_drew = 0
            self.remember_categories()
            self.write_on_screen_touch("Are you ready to start a drawing? \nTouch the screen when you are")
            self.n_drawing += 1

            if self.output_port.getOutputCount():
                info_out = self.output_port.prepare()
                info_out.clear()
                info_out.addString("user_ok_new_drawing")
                self.output_port.write()

                if self.first_turn == "human":
                    self.write_on_screen_delay("You are the first drawer \n wait until the white canvas is fully open then draw!",5)
                    self.black_window()
                    time.sleep(5)
                    self.state = "canvas"
                elif self.first_turn == "robot":
                    self.write_on_screen_delay("iCub is the first drawer", 3)
                    self.robot_drew = True
                    self.black_window()
                    time.sleep(5)
                    self.state = "canvas"
                self.turns.append(self.first_turn)

        elif self.state == "go":
            resp = True
            self.win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color=self.grey1)
            self.myMouse = event.Mouse()

            if self.times_human_drew > 1:
                #self.write_on_screen_delay("do you want to continue this drawing?", 3)
                resp = self.question_continue("do you want to continue this drawing?")
            if not resp:
                if self.robot_drew:
                    robot_choice = self.which_category(
                        "what do you think the robot meant to draw with its last stroke?")
                    self.h_perspective.append(robot_choice)
                self.state = "end_drawing"

            else:
                self.times_human_drew += 1
                self.write_on_screen_delay("Now, it's your turn", 2.5)
                self.turns.append("human")
                self.state = "canvas"

        elif self.state == "questions":
            self.win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color=self.grey1)
            self.myMouse = event.Mouse()
            self.questions()

        elif self.state == "wait":
            self.write_on_screen_wait("wait")

        elif self.state == "canvas":
            self.win.close()

        elif self.state == "robot_stop":
            self.win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color=self.grey1)
            self.myMouse = event.Mouse()
            #self.write_on_screen_delay("the robot thinks the drawing is ok like that", 3)
            #self.write_on_screen_delay("do you want to continue the drawing?", 3)
            resp = self.question_continue("the robot thinks the drawing is ok like that. \ndo you want to continue the drawing?")
            self.robot_drew = False
            self.h_perspective.append("skip")
            if resp:
                self.turns.append("human")
                self.state = "canvas"
            else:
                self.state = "end_drawing"


        elif self.state == "end_drawing":

            self.robot_drew = False
            score_drawing = self.question_like(
                "how much do you like this drawing? \n 1 = I really don't like it \n 7 = I really like it")
            print(score_drawing)
            score_interaction = self.question_like(
                "how much have you enjoyed this interaction? \n 1 = I really didn't \n 7 = I really did")
            print(score_interaction)
            score_ios = self.question_ios(
                "relative to this drawing session, how would you characterize your relationship with the robot?")
            print(score_ios)
            final_category = self.which_category("in your opinion, what does the final drawing represent ?")
            print(final_category)

            self.save_data(score_drawing, score_interaction, score_ios, final_category)

            if self.output_port.getOutputCount():
                info_out = self.output_port.prepare()
                info_out.clear()
                info_out.addString("end_drawing")
                self.output_port.write()

            self.state = "wait"

        elif self.state == "end_session":
            participant_path = self.saving_path + self.player_name + "/"
            session_folder = os.listdir(participant_path)[-1] + "/"
            path = participant_path + session_folder + self.player_name + str(self.social_behavior) + \
                   str(self.drawing_aptitude) + ".csv"
            print(path)
            self.df_all.to_csv(path, header=True, index=False)
            self.state = "wait"

        elif self.state == "open_window":
            self.win = visual.Window(monitor=self.mon, size=(self.monitor_w_px, self.monitor_h_px), color=self.grey1)
            self.myMouse = event.Mouse()
            self.state = "wait"

        return True

    def read_input(self):

        if self.input_port.getInputCount():

            self.input_bottle = self.input_port.read(False)
            if self.input_bottle is not None:

                print(self.input_bottle.toString())
                command = self.input_bottle.get(0).asString()
                if command == "categories":
                    self.group_categories = self.input_bottle.get(1).asString()
                    self.read_categories()
                elif command == "new_drawing":
                    self.first_turn = self.input_bottle.get(1).asString()
                    self.social_behavior = self.input_bottle.get(2).asInt()
                    self.drawing_aptitude = self.input_bottle.get(3).asInt()
                    self.player_name = self.input_bottle.get(4).asString()
                    print(self.first_turn)
                elif command == "go":
                    if self.input_bottle.get(1).asString() != "":
                        self.r_perspective.append(self.input_bottle.get(1).asString())  # what the robot drew
                    if self.input_bottle.get(2).asString() != "":
                        self.r_perspective.append(self.input_bottle.get(2).asString())  # what the robot thought human drew
                elif command == "robot_stop":
                    if self.input_bottle.get(1).asString() != "":
                        self.r_perspective.append(self.input_bottle.get(1).asString())  # what the robot drew
                    if self.input_bottle.get(2).asString() != "":
                        self.r_perspective.append(self.input_bottle.get(2).asString())  # what the robot thought human drew

                self.input_bottle.clear()

                self.state = command

        return

    def write_on_screen_touch(self, text):

        self.myText.text = text
        self.myText.draw()
        self.win.flip()  # show the stim
        self.wait_touch()   # wait for mouse click or screen touch
        self.win.flip(clearBuffer=True)

        return

    def write_on_screen_delay(self, text, delay):

        self.myText.text = text
        self.myText.draw()
        self.win.flip()  # show the stim
        time.sleep(delay)
        self.win.flip(clearBuffer=True)

        return

    def write_on_screen_wait(self, text):

        self.myText.text = text
        self.myText.draw()
        self.win.flip(clearBuffer=True)  # show the stim
        time.sleep(0.001)

        return

    def black_window(self):

        black_poly = visual.Polygon(self.win, edges=4, fillColor="black", pos=[0, 0], size=[5,5], ori=45)
        black_poly.draw()
        self.win.flip()  # show the stim

        return

    def wait_touch(self):

        self.myMouse.clickReset
        buttons = self.myMouse.getPressed()
        print(buttons)
        while buttons[0] == False | buttons[1] == False | buttons[2] == False:
            buttons = self.myMouse.getPressed()

        print(buttons)
        print("click")
        time.sleep(0.001)

        return

    def read_categories(self):
        self.TFRecord_path = self.architecture_path + "Classifier/" + self.group_categories + "/" + self.TF_dictionary[
            self.group_categories] + "/"
        with open(self.TFRecord_path + "training.tfrecord.classes", "r") as f:
            lines = f.readlines()
            f.close()
        self.categories = []
        for line in lines:
            self.categories.append(line.strip())
        print(self.categories)

        return

    def questions(self):

        #self.write_on_screen_delay("what did you mean to draw with your last stroke?", 3)
        human_choice = self.which_category("what did you mean to draw with your last stroke?")
        if self.robot_drew:
            #self.write_on_screen_delay("what do you think the robot meant to draw with its last stroke?", 3)
            robot_choice = self.which_category("what do you think the robot meant to draw with its last stroke?")
            self.h_perspective.append(robot_choice)
        self.h_perspective.append(human_choice)

        if self.output_port.getOutputCount():
            info_out = self.output_port.prepare()
            info_out.clear()
            info_out.addString("end_questions")
            info_out.addString(human_choice)
            if self.robot_drew:
                info_out.addString(robot_choice)
            self.output_port.write()
            self.write_on_screen_delay("It's iCub turn", 2.5)
            self.turns.append("robot")
            self.robot_drew = True
            self.state = "canvas"

        return

    def remember_categories(self):

        r_text = visual.TextStim(self.win, color="snow", bold=True)
        r_text.text = "you can only draw these things. remember them! \n touch the screen to continue"
        r_text.pos = [0, 0.6]
        r_text.draw()
        positions = [[-0.5, 0.2], [0, 0.2], [0.5, 0.2], [-0.5, 0.0], [0, 0.0], [0.5, 0.0], [-0.5, -0.2], [0, -0.2],
                     [0.5, -0.2], [-0.5, -0.4], [0, -0.4], [0.5, -0.4]]
        shapes_new = []
        text_list = []
        for c in range(len(self.categories)):
            shapes_new.append(visual.Polygon(self.win, edges=4, fillColor=self.grey2, lineWidth=1.5,
                                             lineColor="black", pos=[0, 0], size=[0.5, 0.2], ori=45))
            shapes_new[c].setPos(positions[c])
            shapes_new[c].draw()
            text_list.append(visual.TextStim(self.win, text=self.categories[c], color="snow", pos=positions[c],
                                             bold=False, anchorHoriz="center", anchorVert="center"))
            text_list[c].draw()
        self.win.flip()  # show the stim
        self.wait_touch()

        return

    def which_category(self, text):

        self.myMouse.clickReset()
        self.myMouse.setPos([0.5, 0.5])

        q_text = visual.TextStim(self.win, color="snow", bold=True)
        q_text.text = text
        q_text.pos = [0, 0.6]
        q_text.draw()

        positions = [[-0.5, 0.2], [0, 0.2], [0.5, 0.2], [-0.5, 0.0], [0.0, 0.0], [0.5, 0.0], [-0.5, -0.2], [0, -0.2],
                     [0.5, -0.2], [-0.5, -0.4], [0, -0.4], [0.5, -0.4]]
        shapes_new = []
        text_list = []
        for c in range(len(self.categories)):

            shapes_new.append(visual.Polygon(self.win, edges=4, fillColor=self.grey2, lineWidth=1.5,
                                             lineColor="black", pos=positions[c], size=[0.5, 0.2], ori=45))
            #shapes_new[c].setPos(positions[c])
            shapes_new[c].draw()
            text_list.append(visual.TextStim(self.win, text=self.categories[c], color="snow", pos=positions[c],
                                             bold=False, anchorHoriz="center", anchorVert="center"))
            text_list[c].draw()
        self.win.flip()  # show the stim

        touch = False
        while not touch:
            # check the list of shapes
            for n in range(len(self.categories)):
            #for n, shape in enumerate(shapes_new):

                # if shapes_new[n].contains(self.myMouse.getPos()):
                if self.myMouse.isPressedIn(shapes_new[n]):
                    touch = True


                    index_choice = shapes_new.index(shapes_new[n])
                    chosen_category = self.categories[index_choice]
                    print("pressed " + str(index_choice) + ", which corresponds to " + chosen_category)
                    break  # exit this loop

                else:  # this runs once at the completion of the for loop
                        # breathe for 1 ms
                    time.sleep(0.001)

        self.win.flip(clearBuffer=True)
        time.sleep(1)

        return chosen_category

    def question_continue(self, text):

        self.myMouse.clickReset
        self.myMouse.setPos([0.6, 0.6])

        q_text = visual.TextStim(self.win, color="snow", bold=True)
        q_text.text = text
        q_text.pos = [0, 0.6]
        q_text.draw()

        positions = [[-0.5, 0], [0.5, 0]]
        options = ["Yes,\nI want to continue\n the drawing", "No,\n I don't want to \ncontinue the drawing"]
        shapes_new = []
        text_list = []

        for c in range(len(options)):

            shapes_new.append(visual.Polygon(self.win, edges=4, fillColor=self.grey2, lineWidth=1.5,
                                             lineColor="black", pos=[0, 0], size=[1, 0.8], ori=45))
            shapes_new[c].setPos(positions[c])
            shapes_new[c].draw()
            text_list.append(visual.TextStim(self.win, text=options[c], color="snow", pos=positions[c], bold=True,
                             anchorHoriz="center", anchorVert="center"))
            text_list[c].draw()
        self.win.flip()  # show the stim

        touch = False
        resp = False
        while not touch:
            # check the list of shapes
            for n in shapes_new:

                if self.myMouse.isPressedIn(n):
                # if shapes_new[n].contains(self.myMouse.getPos()):
                    touch = True
                    index_choice = shapes_new.index(n)
                    choice = options[index_choice]
                    print("pressed " + str(index_choice) + ", which corresponds to " + choice)
                    if "Yes" in choice:
                        resp = True
                    else:
                        resp = False
                    break  # exit this loop

                else:  # this runs once at the completion of the for loop
                    # breathe for 1 ms
                    time.sleep(0.001)

        self.win.flip(clearBuffer=True)
        time.sleep(1)

        return resp

    def question_like(self, text):

        self.myMouse.clickReset
        self.myMouse.setPos([0.6, 0.6])

        q_text = visual.TextStim(self.win, color="snow", bold=True)
        q_text.text = text
        q_text.pos = [0, 0.6]
        q_text.draw()

        positions = [[-0.75, 0], [-0.5, 0], [-0.25, 0], [0, 0], [0.25, 0], [0.5, 0], [0.75, 0]]
        scores = list(range(1, 8))
        shapes_new = []
        text_list = []

        for c in range(len(scores)):
            shapes_new.append(visual.Polygon(self.win, edges=4, fillColor=self.grey2, lineWidth=1.5,
                                             lineColor="black", pos=[0, 0], size=[0.2, 0.2], ori=45))
            shapes_new[c].setPos(positions[c])
            shapes_new[c].draw()
            text_list.append(visual.TextStim(self.win, text=str(scores[c]), color="snow", pos=positions[c], bold=True,
                                             anchorHoriz="center", anchorVert="center"))
            text_list[c].draw()
        self.win.flip()  # show the stim

        touch = False
        while not touch:
            # check the list of shapes
            for n in range(len(scores)):

                if self.myMouse.isPressedIn(shapes_new[n]):
                    touch = True

                    index_choice = shapes_new.index(shapes_new[n])
                    score = str(scores[index_choice])
                    print("pressed " + str(index_choice) + ", which corresponds to " + score)
                    break  # exit this loop

                else:  # this runs once at the completion of the for loop
                    # breathe for 1 ms
                    time.sleep(0.001)

        self.win.flip(clearBuffer=True)
        time.sleep(1)

        return score

    def question_ios(self, text):

        self.myMouse.clickReset
        self.myMouse.setPos([0.6, 0.6])

        q_text = visual.TextStim(self.win, color="snow", bold=True)
        q_text.text = text
        q_text.pos = [0, 0.6]
        q_text.draw()

        positions = [[-0.75, 0], [-0.25, 0], [0.25, 0], [0.75, 0], [-0.5, -0.65], [0, -0.65], [0.5, -0.65]]
        name_images = ["ios1.png", "ios2.png", "ios3.png", "ios4.png", "ios5.png", "ios6.png", "ios7.png"]
        scores = list(range(1, 8))
        images = []
        text_list = []

        for c in range(len(name_images)):
            img = self.image_path + name_images[c]
            images.append(visual.ImageStim(self.win, image=img, size=[0.48, 0.55]))
            images[c].setPos(positions[c])
            images[c].draw()
            #text_list.append(visual.TextStim(self.win, text=str(scores[c]), color="snow", pos=positions[c], bold=True,
            #                                 anchorHoriz="center", anchorVert="center"))
            #text_list[c].draw()
        self.win.flip()  # show the stim

        touch = False
        while not touch:
            # check the list of shapes
            for n in range(len(scores)):

                if self.myMouse.isPressedIn(images[n]):
                    touch = True

                    index_choice = images.index(images[n])
                    score = str(scores[index_choice])
                    print("pressed " + str(index_choice) + ", which corresponds to " + score)
                    break  # exit this loop

                else:  # this runs once at the completion of the for loop
                    # breathe for 1 ms
                    time.sleep(0.001)

        self.win.flip(clearBuffer=True)
        time.sleep(1)

        return score

    def save_data(self, score_drawing, score_interaction, score_ios, final_category):

        info("saving data into pandas df")
        print("turns is long " + str(len(self.turns)))
        print(self.turns)
        print("h_perspective is long " + str(len(self.h_perspective)))
        print(self.h_perspective)
        print("r_perspective is long " + str(len(self.r_perspective)))
        print(self.r_perspective)

        list_n_turns = list(range(len(self.turns)))
        print(list_n_turns)

        list_player_name = []
        list_group_categories = []
        list_social_behaviour = []
        list_drawing_aptitude = []
        list_n_drawing = []
        list_drawing_score = []
        list_interaction_score = []
        list_ios_score = []
        list_final_cat = []

        for i in range(len(self.turns)):
            list_player_name.append(self.player_name)
            list_group_categories.append(self.group_categories)
            list_social_behaviour.append(self.social_behavior)
            list_drawing_aptitude.append(self.drawing_aptitude)
            list_n_drawing.append(self.n_drawing)
            list_drawing_score.append(score_drawing)
            list_interaction_score.append(score_interaction)
            list_ios_score.append(score_ios)
            list_final_cat.append(final_category)

        data = {"player_name": list_player_name, "category_group": list_group_categories, "social_behaviour":
                list_social_behaviour, "drawing_aptitude": list_drawing_aptitude, "n_drawing": list_n_drawing,
                "n_turn": list_n_turns, "drawer": self.turns, "h_perspective": self.h_perspective, "r_perspective":
                self.r_perspective, "drawing_score": list_drawing_score, "interaction_score": list_interaction_score,
                "ios_score": list_ios_score, "final_cat": list_final_cat}
        df_drawing = pd.DataFrame(data=data)
        print(df_drawing)
        self.df_all = self.df_all.append(df_drawing, ignore_index=True)
        print(self.df_all)

        return


if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        info("Unable to find a yarp server exiting ...")
        sys.exit(1)

    yarp.Network.init()

    g_interface = graphicInterface()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('graphicInterface')
    rf.setDefaultConfigFile('graphicInterface.ini')

    if rf.configure(sys.argv):
        g_interface.runModule(rf)

    g_interface.close()
    sys.exit()
