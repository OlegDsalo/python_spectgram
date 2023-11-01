# Linear Freuqency Generator script
# Command format
# lfm_gen.py -sf <start_freq> -ef <end_freq> -swp <sweep_time> -m <mode>
# start_freq - start frequency of linear frequency modulation. Range: 50..3000 Hz
# end_freq   - end frequency of linear frequency modulation. Range: 51..3000 Hz. Must be bigger than <start frequency>
# sweep_time - time of sweep between start and end frequency. Range: 1..10 seconds.
# mode       - Mode could be "saw" or "swing". In "saw" mode frequency is varied from start to end and immediatelly switches to start again.
#              In "swing" mode frequency is varied from start to end and from end to start.

# Example: python lfm_gen.py -start_freq 100 -ef 101 -mode swing

import struct
import wave
import numpy as np
import math
import matplotlib.pyplot as plt
import argparse

# GLOBAL PARAMETERS:
AMPLITUDE = 10
SAMPLERATE = 44100
START_PHASE = 0

# =============================================================
# 1. Парсення вхідних аргументів
# =============================================================

# list of limits for input arguments:
LIMITS_MAX_START_FREQUENCY = 3000
LIMITS_MIN_START_FREQUENCY = 30

LIMITS_MIN_SWEEP_TIME = 1
LIMITS_MAX_SWEEP_TIME = 10

print('Start script')

# Instantiate the parser
parser = argparse.ArgumentParser(description='Script description')

# Required positional argument

parser.add_argument('-sf', type=int,
                    help='Start frequency argument required', required=True)
parser.add_argument('-ef', type=int,
                    help='End frequency argument  required', required=True)

parser.add_argument('-swp', type=int,
                    help='Sweep time argument required', required=True)

parser.add_argument('-m', type=str,
                    help='Mode argument is missed', required=True)

args = parser.parse_args()

print("Arguments values:")
print('start freq:', args.sf, 'Hz')
print('end freq:', args.ef, 'Hz')
print('sweep time:', args.swp, 's')
print('mode:', args.m)

# Check valid ranges
if LIMITS_MIN_START_FREQUENCY > args.sf or args.sf > LIMITS_MAX_START_FREQUENCY:
    parser.error(
        f"start_freq cannot be larger than  {LIMITS_MAX_START_FREQUENCY} or less than {LIMITS_MIN_START_FREQUENCY}")

if args.sf >= args.ef or args.ef > LIMITS_MAX_START_FREQUENCY:
    parser.error(f"end_freq must  be larger than start_freq={args.sf} and less than  {LIMITS_MAX_START_FREQUENCY}")

if LIMITS_MIN_SWEEP_TIME > args.swp or args.swp > LIMITS_MAX_SWEEP_TIME:
    parser.error(f"sweep_time cannot be larger than {LIMITS_MAX_SWEEP_TIME} or less than {LIMITS_MIN_SWEEP_TIME}")

if args.m != 'swing' and args.m != 'saw':
    parser.error("The mode argument is wrong. It shall be 'swing' or 'saw'")


# =============================================================
# 2. Генерація відліків сигналу
# =============================================================

# generate chosen signal


def generate_saw():
    # Time vector according to sampling frequency
    time_vector = np.linspace(0, args.swp, args.swp * SAMPLERATE)

    # f0 the central value of the carrier frequency
    f0 = (args.ef + args.sf) / 2
    b = (args.ef - args.sf) / args.swp

    # samples = S0*COS(start_freq + 2 * pi * (f0 * time_vector + b / 2 * pow(time_vector, 2))
    samples = AMPLITUDE * np.cos(START_PHASE + 2 * math.pi * (f0 * time_vector + b / 2 * pow(time_vector, 2)))
    return samples


def generate_swing():
    # Time vector according to sampling frequency
    time_vector = np.linspace(0, args.swp, args.swp * SAMPLERATE)

    # f0 the central value of the carrier frequency
    f0 = (args.ef + args.sf) / 2
    b = (args.ef - args.sf) / args.swp
    # Mirrored Time vector to build 2 part
    mirrored_time = args.swp - time_vector
    # samples = S0*COS(start_freq + 2 * pi * (f0 * time_vector + b / 2 * pow(time_vector, 2))
    samples_1 = AMPLITUDE * np.cos(START_PHASE + 2 * math.pi * (f0 * time_vector + b / 2 * pow(time_vector, 2)))
    samples_2 = AMPLITUDE * np.cos(START_PHASE + 2 * math.pi * (f0 * mirrored_time + b / 2 * pow(mirrored_time, 2)))
    samples = np.append(samples_1, samples_2)
    return samples


if args.m == 'saw':
    print('saw generate')
    samples = generate_saw()

if args.m == 'swing':
    print('swing generate')
    samples = generate_swing()

# =============================================================
# 3. Експорт відліків
# =============================================================
# 1. Експортувати у текстовий файл безпосередньо значення відліків. https://www.pythontutorial.net/python-basics/python-write-text-file/
# 2. Експортувати у аудіо файл
# 3. Побудувати графік (за бажанням)


# Saving to text file
try:
    file = open("out.txt", "w+")
    try:
        for item in samples:
            file.write("%s\n" % item)
    finally:
        file.close()
except FileNotFoundError:
    print('Error')

# Saving to wav file

# repeating 5 times
print('sammples',samples)
long_samples =samples
samples_norm = long_samples * (2 ** 15 - 1) / np.max(np.abs(long_samples))
audio = samples_norm.astype(np.int16)
print('len',len(samples))

print('len long',len(long_samples))

print('adoopms',audio)
print('samples_norm',samples_norm)
audio_float = audio.astype(np.float32) / (2 ** 15 - 1)

# Rescale the audio signal to its original range
original_range = np.max(np.abs(samples))
audio_original = audio_float * original_range

# Optionally, you can convert it back to the original data type if needed
audio_original = audio_original.astype(samples.dtype)
print('original audiop',audio_original)




obj = wave.open('test.wav', 'w')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(SAMPLERATE)
for i in audio:
    data = struct.pack('h', i)
    obj.writeframesraw(data)
obj.close()

# build graph
ax1 = plt.subplot(311)
plt.plot(samples)
plt.title('Signal start')
plt.xlabel('Times(s)')
plt.ylabel('Amplitude')
plt.xlim(0, 300)

ax2 = plt.subplot(313)
plt.plot(samples)
plt.title('Signal end')
plt.xlabel('Times(s)')
plt.ylabel('Amplitude')
plt.xlim(args.swp * SAMPLERATE - 300, args.swp * SAMPLERATE)

plt.show()

print('End work')
