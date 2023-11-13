import matplotlib.pyplot as plt
import numpy as np

class Waterfall(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.content = np.random.randint(0, 10, size = (height, width))
        self.im = self.ax.imshow(self.content, cmap="jet" ,vmin=0, vmax=10)

    def update(self, new_content, a_max):
        self.content = new_content
        #self.fig = plt.figure(100, clear = True)
        #self.ax = self.fig.add_subplot()
        self.ax.imshow(self.content, cmap="jet", vmin=0, vmax=a_max)
        #plt.pause(0.005)


