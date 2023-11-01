# Import Module
import struct
from tkinter import *
import time
from threading import *
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from waterfall import Waterfall
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import wave
from scipy.fftpack import fft


# waterfall width and height. Consider make it configurable using GUI.
waterfall_width = 128
waterfall_height = 80

# Create Object
root = Tk()

# Set geometry
root.geometry("700x500")

global TerminateProgram
global WaterFallObject
global My_Canvas
TerminateProgram = False

BLOCK_DIVIDER = 128
def pasrseAudio():
    with wave.open('test.wav', 'rb') as wav_file:
        audio_data = wav_file.readframes(wav_file.getnframes())
        # Process audio_data as needed (e.g., convert to NumPy array)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Convert audio_array to floating-point values in the range Amplitude;
    audio_float = (audio_array / (2 ** 15 - 1)) * 10
    print('audio_float', audio_float)
    print('audio_float/length', len(audio_float));
    return audio_float

def click_process():
    global TerminateProgram
    print("Button clicked")
    TerminateProgram = True

def ploat_graph(data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    # Plot the first subplot (Signal start)
    ax1.plot(data)
    ax1.set_title('Signal start')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Amplitude')
    ax1.set_xlim(0, 300)

    # Plot the second subplot (Signal end)
    ax2.plot(data)
    ax2.set_title('Signal end')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude')
    ax2.set_xlim(5 * 44100 - 300, 5 * 44100)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the plots
    # Spartak: do not use plt.show inside thread
    #plt.show()

# work function
def work():
    global TerminateProgram
    global WaterFallObject
    global My_Canvas

    audio_float = pasrseAudio()
    # Spartak: do not use plot inside thread
    #ploat_graph(audio_float)

    frequency_channels = 1024
    divided_arrays = [audio_float[i:i + frequency_channels] for i in range(0, len(audio_float), frequency_channels)]
    print('arrays',len(divided_arrays))

    #print('fft', len(fft_results[1]))
    print("Thread started")
    time.sleep(1)

    #WaterFallObject.update(fft_results)

    # Initial waterfall content
    fft_results = np.zeros([waterfall_height,waterfall_width])

    fft_block_idx = 0

    while (False == TerminateProgram):
        print("thread is running....")

        y = divided_arrays[fft_block_idx]
        yf = fft(y) / frequency_channels
        yf = 2.0 / frequency_channels * np.abs(yf[:frequency_channels// 2])

        # Prepare waterfall content.
        # As a workaround cut yf to width corresponding to waterfall width.
        yf = yf[:waterfall_width]

        # Scale amplitude to make it visible on the waterfall. Tune it later.
        yf = yf * 500

        # roll waterfall content for one position from down to up.
        fft_results = np.roll(fft_results, -1, axis=0)
        # update the most bottom line in the waterfall with the new FFT data
        fft_results[-1,:] = yf

        # Update waterfall
        WaterFallObject.update(fft_results)
        My_Canvas.draw()
        time.sleep(0.01)

        # Increment current FFT block index.
        fft_block_idx = fft_block_idx + 1
        # Check if all block processed and stop to avoid overflow.
        if (fft_block_idx >= len(divided_arrays)):
            TerminateProgram = True

    print("Thread stop")

def plot():
    print("plot button clicked")

# Create Button
Button(root, text="Exit", command=click_process).pack()

# Create Waterfall object
WaterFallObject = Waterfall(waterfall_width, waterfall_height)

Button(root, text="figure", command=plot).pack()

# creating the Tkinter canvas
# containing the Matplotlib figure
My_Canvas = FigureCanvasTkAgg(WaterFallObject.fig,
                              master=root)

# placing the canvas on the Tkinter window
My_Canvas.get_tk_widget().pack()

# Start processing thread
t1 = Thread(target=work)
t1.start()

# Execute Tkinter
root.mainloop()

print("Exit program")