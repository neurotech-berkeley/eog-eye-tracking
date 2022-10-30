from screeninfo import get_monitors
import tkinter as tk
import tkinter.font as font
# from time import time
# from tkinter import Tk, mainloop, TOP

# assuming single monitor
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

offset_x = 0
offset_y = 0
dot_r = 20


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("calibration")
        self.geometry('{}x{}+{}+{}'.format(screen_width, screen_height, offset_x, offset_y))
        print('{}x{}'.format(screen_width, screen_height))
        genFont = font.Font(family='Helvetica', size=12, weight='bold')

        self.attributes('-fullscreen', True)

        # location - pack(), grid(), place()
        self.lbl = tk.Label(self, text="Are you ready?", font=genFont)
        self.lbl.place(relx = 0.5, rely=0.8, anchor=tk.CENTER)

        self.btn = tk.Button(self, text="Start", command=self.start, \
                     font=genFont, width=25, height=2, bg='#000', fg='#00FF00')
        self.btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        self.signal_stages = [] * 8
        self.min_x = offset_x + 50
        self.min_y = offset_y + 50
        self.max_x = screen_width - 50
        self.max_y = screen_height - 50

        self.canvas = tk.Canvas(self, height=screen_height, width=screen_width, bg="#EEE")

    def start(self):
        self.lbl.destroy()
        self.btn.destroy()

        # dot initialization
        x1, y1, x2, y2 = self.min_x - dot_r, self.min_y - dot_r, self.min_x + dot_r, self.min_y + dot_r
        self.dot = self.canvas.create_oval(x1, y1, x2, y2, outline='#EEE', fill="black", state=tk.HIDDEN)

        self.canvas.pack()

        # animation steps
        self.canvas.after(1000, lambda: self.blink(self.dot, 1))
        self.canvas.after(5500, lambda: self.canvas.itemconfig(self.dot, state=tk.NORMAL))
        self.canvas.after(5500, lambda: self.move_dot(self.dot, 1))

    def move_dot(self, dot, stage):
        print('moving')
        MOVE_TIMESTEP = 10
        ox, oy = self.canvas.coords(dot)[0] + dot_r, self.canvas.coords(dot)[1] + dot_r
        if stage == 1:
            start = oy == self.min_y
            bound = oy >= self.max_y
            step_x = 0
            step_y = 10
        elif stage == 2:
            start = ox == self.min_x
            bound = ox >= self.max_x
            step_x = 10
            step_y = 0
        elif stage == 3:
            start = oy == self.max_y
            bound = oy <= self.min_y
            step_x = 0
            step_y = -10
        elif stage == 4:
            start = ox == self.max_x
            bound = ox <= self.min_x
            step_x = -10
            step_y = 0
        elif stage == 5:
            start = ox == self.min_x
            bound = ox >= self.max_x
            step_x = ((self.max_x) - (self.min_x)) / 100
            step_y = ((self.max_y) - (self.min_y)) / 100
        elif stage == 6:
            start = ox == self.max_x
            bound = ox <= self.min_x
            step_x = -10
            step_y = 0
        elif stage == 7:
            start = ox == self.min_x
            bound = ox >= self.max_x
            step_x = ((self.max_x) - (self.min_x)) / 100
            step_y = -((self.max_y) - (self.min_y)) / 100
        elif stage == 8:
            start = ox == self.max_x
            bound = ox <= self.min_x
            step_x = -10
            step_y = 0
        elif stage == 9:
            self.destroy()
            # destroy GUI window and begin coordinate system and reading
            # coord system starts at top left
            return

        # if start:
            # self.signal_stages[stage - 1] = initial signal
        if bound:
            # self.signal_stages[stage - 1] = signal change based on pre-stored initial signal
            # for each stage, divide signal_amount by pixel_change
            self.move_dot(dot, stage + 1)
        else:
            self.canvas.move(dot, step_x, step_y)
            self.canvas.after(MOVE_TIMESTEP, lambda: self.move_dot(dot, stage))

    def blink(self, dot, stage):
        print('blinking')
        TIMESTEP_BLINK = 1000
        if stage == 1:
            pass
        if stage == 2:
            self.canvas.move(dot, 0, (self.max_y - self.min_y))
            # read signal, store down_signal / delta_y
        if stage == 3:
            self.canvas.move(dot, (self.max_x - self.min_x), 0)
            # read signal, store right_signal / delta_x
        if stage == 4:
            self.canvas.move(dot, 0, -(self.max_y - self.min_y))
            # read signal, store up_signal / delta_y
        if stage == 5:
            self.canvas.move(dot, -(self.max_x - self.min_x), 0)
            # read signal, store left_signal / delta_x
            return

        self.canvas.itemconfig(dot, state=tk.NORMAL)
        # self.canvas.after(TIMESTEP_BLINK - 1, lambda: self.canvas.itemconfig(dot, state=tk.HIDDEN))
        self.canvas.after(TIMESTEP_BLINK, lambda: self.blink(dot, stage + 1))

# execute tkinter if run
if __name__ == "__main__":
    app = App()
    app.mainloop()
