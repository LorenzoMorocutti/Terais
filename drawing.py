import tkinter as tk
import sys
import time
from PIL import Image, ImageTk, ImageGrab

start = time.time()
# Initialize Tkinter
root = tk.Tk()


######### CONFIGURATION OF THE GLOBAL VARIABLES OF THE CANVAS AND SCREENSHOTS ###########

# Set dimensions of the screenshot
savelocation = "/home/icub/Desktop/Terais/Images/participant_01/screen.png"

# Set the dimensions of the drawing window
window_width = 1920
window_height = 950

# Create the drawing canvas
canvas = tk.Canvas(root, width=window_width, height=window_height, bg='white')
canvas.pack()

button = tk.Button(text="If you finished, press the button", command=lambda: quit_program(), height=4)
button.pack()

# Set the color and size for drawing
draw_color = 'black'
draw_size = 5

# Store the coordinates of the previous point
prev_x = None
prev_y = None

# Keep track of the number of strokes
stroke_count = 0

############################### END OF THE CONFIGURATION ################################



############ FUNCTIONS TO DRAW AND TO SAVE THE FINAL DRAWINGS #############
# Define the event handler for mouse movements
def on_mouse_move(event):
    global prev_x, prev_y, stroke_count
    x = event.x
    y = event.y
    if prev_x is not None and prev_y is not None:
        canvas.create_line(prev_x, prev_y, x, y, fill=draw_color, width=draw_size, tags=('stroke', stroke_count))
    prev_x = x
    prev_y = y


# Define the event handler for releasing the mouse button
def on_mouse_release(event):
    global prev_x, prev_y, stroke_count
    prev_x = None
    prev_y = None
    stroke_count += 1
    print(f"Number of strokes: {stroke_count}")

    if stroke_count == 6:
        save_image()
        root.destroy()


# Define the function to make a screenshot, crop it and save it in the right folder
def save_image():
    time.sleep(2)
    ImageGrab.grab().crop((40, 65, 1920, 1015)).save(savelocation)
    temp = time.time() - start
    print(temp)


def quit_program():
    ImageGrab.grab().crop((40, 65, 1920, 1015)).save(savelocation)
    temp = time.time() - start
    print(temp)
    root.destroy()


######################### END OF THE FUNCTIONS #############################

# Bind the mouse movement event to the canvas
canvas.bind('<B1-Motion>', on_mouse_move)

# Bind the mouse release event to the canvas
canvas.bind('<ButtonRelease-1>', on_mouse_release)


root.after(60000, root.destroy)

# Start the main Tkinter event loop
root.mainloop()
