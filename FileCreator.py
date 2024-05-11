# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:02:30 2024

@author: gowtham.balachan
"""

import time
import os
import base64
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AnimationCreator:
    def __init__(self, drawing, fps=10, idx=0, lw=5):
        self.drawing = drawing
        self.fps = fps
        self.idx = idx
        self.lw = lw

    def create_animation(self):
        seq_length = 0
        xmax = 0
        ymax = 0
        xmin = math.inf
        ymin = math.inf

        for k in range(0, len(self.drawing)):
            x = self.drawing[k][0]
            y = self.drawing[k][1]

            seq_length += len(x)
            xmax = max([max(x), xmax])
            ymax = max([max(y), ymax])
            xmin = min([min(x), xmin])
            ymin = min([min(y), ymin])

        i = 0
        j = 0

        fig = plt.figure()
        ax = plt.axes(xlim=(xmax + self.lw, xmin - self.lw), ylim=(ymax + self.lw, ymin - self.lw))
        ax.set_facecolor("white")
        line, = ax.plot([], [], lw=self.lw, color='k')  # Set color to black
        ax.grid = False
        ax.set_xticks([])
        ax.set_yticks([])

        def init():
            line.set_data([], [])
            return line,

        def animate(frame):
            nonlocal i, j, line
            x = self.drawing[i][0]
            y = self.drawing[i][1]
            line.set_data(x[0:j], y[0:j])

            if j >= len(x):
                i += 1
                j = 0
                line, = ax.plot([], [], lw=self.lw, color='k')  # Set color to black
            else:
                j += 1
            return line,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=seq_length + len(self.drawing), blit=True)
        plt.close()

        file = f"{time.time()}.gif"
        anim.save(filename=file, writer="pillow")
        base64_string = self.file_to_base64(file)
        os.remove(file)
        return base64_string

    def file_to_base64(self, file_path):
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
                base64_encoded = base64.b64encode(file_content)
                base64_string = base64_encoded.decode("utf-8")
                return base64_string
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
        