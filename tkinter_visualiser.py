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
import tkinter as tk

# waterfall width and height. Consider make it configurable using GUI.
waterfall_width = 120
waterfall_height = 80

frequency_channels = 128
max_amplitude = 10

# Create Object
root = Tk()

# Initial value for waterfall_height of spectogram
entry_label = tk.Label(root, text="Enter a value (50-200):", font={"Josefin Sans", 15}, padx=5, pady=5)
entry_label.pack()
entry_value_var = StringVar(root)
entry_value = tk.Entry(root, textvariable=entry_value_var, font={"Josefin Sans", 13})
entry_value.pack()
entry_value.insert(0, "50")


def on_select(event):
    # Get the selected value and update the frequency_channels variable
    selected_indices = listbox.curselection()
    if selected_indices:
        index = listbox.curselection()[0]
        global frequency_channels
        frequency_channels = int(listbox.get(index))
        label.config(text=f"Selected Frequency Channels: {frequency_channels}")
    else:
        print("No item selected in listbox2")


def on_amplitude(event):
    # Get the selected value and update the max_amplitude variable
    selected_indices = listbox2.curselection()
    if selected_indices:
        index2 = listbox2.curselection()[0]
        global max_amplitude
        max_amplitude = int(listbox2.get(index2))
        print('max_amplitude', max_amplitude)
        label2.config(text=f"Selected  max amplitude : {max_amplitude}")
    else:
        print("No item selected in listbox2")


# Initial value for frequency_channels
label = tk.Label(root, text=f"Selected Frequency Channels: {frequency_channels}", font={"Josefin Sans", 15}, padx=5,
                 pady=5)
label.pack()

listbox = tk.Listbox(root, font={"Josefin Sans", 14}, height=4, selectbackground="red")
options = [128, 256, 512, 1024]

for option in options:
    listbox.insert(tk.END, option)

listbox.bind('<<ListboxSelect>>', on_select)
listbox.pack(side=tk.TOP, padx=10)

label2 = tk.Label(root, text=f"Select max apmlitude color in spectrogram: {max_amplitude}", font={"Josefin Sans", 15},
                  padx=5, pady=5)
label2.pack()
listbox2 = tk.Listbox(root, font={"Josefin Sans", 14}, height=4, selectbackground="red")
amplitude_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for amplitude_option in amplitude_options:
    listbox2.insert(tk.END, amplitude_option)

listbox2.bind('<<ListboxSelect>>', on_amplitude)

listbox2.pack(side=tk.TOP, padx=10)

# Set geometry
root.geometry("700x550")

global TerminateProgram
global WaterFallObject
global My_Canvas
TerminateProgram = False


def pasrse_audio():
    with wave.open('test.wav', 'rb') as wav_file:
        audio_data = wav_file.readframes(wav_file.getnframes())
        # Process audio_data as needed (e.g., convert to NumPy array)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
    # Convert audio_array to floating-point values in the range Amplitude;
    audio_float = (audio_array / (2 ** 15 - 1)) * 10
    return audio_float


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
    # plt.show()


# work function
def work():
    global TerminateProgram
    global WaterFallObject
    global My_Canvas

    waterfall_height = int(entry_value_var.get())

    audio_float = pasrse_audio()

    divided_arrays = [audio_float[i:i + frequency_channels] for i in range(0, len(audio_float), frequency_channels)]

    print("Thread started")
    time.sleep(1)

    # Initial waterfall content
    result_as_integer = int(frequency_channels / 2)
    fft_results = np.zeros([waterfall_height, result_as_integer])

    fft_block_idx = 0

    while (False == TerminateProgram):
        print("thread is running....")

        y = divided_arrays[fft_block_idx]
        yf = fft(y) / frequency_channels
        yf = 2.0 / frequency_channels * np.abs(yf[:frequency_channels // 2])

        # Prepare waterfall content.
        yf = yf[:result_as_integer]

        # Scale amplitude to make it visible on the waterfall.
        yf = yf * 500

        # roll waterfall content for one position from down to up.
        fft_results = np.roll(fft_results, -1, axis=0)
        # update the most bottom line in the waterfall with the new FFT data
        fft_results[-1, :] = yf

        # Update waterfall
        WaterFallObject.update(fft_results, max_amplitude)
        My_Canvas.draw()
        time.sleep(0.01)

        # Increment current FFT block index.
        fft_block_idx = fft_block_idx + 1
        # Check if all block processed and stop to avoid overflow.
        if (fft_block_idx >= len(divided_arrays)):
            TerminateProgram = True

    print("Thread stop")


def click_process():
    global TerminateProgram
    print("Button clicked")
    TerminateProgram = True


def plot():
    print("plot button clicked")
    # Start processing thread
    global TerminateProgram
    TerminateProgram = False
    t1 = Thread(target=work)
    t1.start()


# Create Button
Button(root, text="Exit", padx=5, background='red', foreground='white', command=click_process).pack(pady=5)

# Create Waterfall object
WaterFallObject = Waterfall(waterfall_width, waterfall_height)

Button(root, text="figure", padx=5, background='green', foreground='white', command=plot).pack(pady=5)

# creating the Tkinter canvas
# containing the Matplotlib figure
My_Canvas = FigureCanvasTkAgg(WaterFallObject.fig,
                              master=root)

# placing the canvas on the Tkinter window
My_Canvas.get_tk_widget().pack()

# Execute Tkinter
root.mainloop()

print("Exit program")
