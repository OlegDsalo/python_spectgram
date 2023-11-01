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
    plt.show()

# work function
def work():
    audio_float = pasrseAudio()
    ploat_graph(audio_float)

    frequency_channels = 1024
    divided_arrays = [audio_float[i:i + frequency_channels] for i in range(0, len(audio_float), frequency_channels)]
    print('arrays',len(divided_arrays))

    fft_results = []  # To store FFT results for each segment

    for i in range (0,len(divided_arrays)):
        y = divided_arrays[i]
        yf = fft(y) / frequency_channels
        yf = 2.0 / frequency_channels * np.abs(yf[:frequency_channels// 2])
        fft_results.append(yf)


    print('fft', len(fft_results[1]))
    print("Thread started")
    time.sleep(1)

    WaterFallObject.update(fft_results)


    # while (False == TerminateProgram):
    #     print("thread is running....")
    #
    #     # Update waterfall
    #     global WaterFallObject
    #     global My_Canvas
    #     new_content = np.random.randint(0, 10, size=(100, 100))
    #     # print('new content',new_content)
    #     WaterFallObject.update(new_content)
    #     My_Canvas.draw()
    #     time.sleep(1)

    print("Thread stop")

def plot():
    print("plot button clicked")

# Create Button
Button(root, text="Exit", command=click_process).pack()

# Create Waterfall object
WaterFallObject = Waterfall(100,100)

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