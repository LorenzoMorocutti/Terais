



import tkinter as tk
import time

root = tk.Tk()

# Set the dimensions of the drawing window
window_width = 1920
window_height = 950

# Create the drawing canvas
canvas = tk.Canvas(root, width=window_width, height=window_height, bg='white')
canvas.pack()



def button_click():
    msg = canvas.create_text(100, 80, anchor="nw", fill="darkgreen", font=('Meiryo', 10, 'bold'), text="registered")
    root.after(2000, canvas.delete, msg)



# *********************************

button1 = tk.Button(root, text="register", command=button_click)
button1_window = canvas.create_window(120, 100, anchor="nw", window=button1)

root.mainloop()

