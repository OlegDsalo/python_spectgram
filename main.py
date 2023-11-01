import numpy as np
import wave
# Open the WAV file for reading
wav_file = wave.open('sound.wav', 'rb')

# Get basic information about the WAV file
num_channels = wav_file.getnchannels()  # Number of audio channels (1 for mono, 2 for stereo)
sample_width = wav_file.getsampwidth()   # Sample width in bytes (e.g., 2 for 16-bit audio)
frame_rate = wav_file.getframerate()     # Frame rate (samples per second)
num_frames = wav_file.getnframes()       # Total number of audio frames
print(num_channels)
print(sample_width)
print(frame_rate)
print(num_frames)

# Read audio data from the WAV file
audio_data = wav_file.readframes(num_frames)

# Close the WAV file
wav_file.close()

# Now you can work with the audio data
# For example, you can convert it to a NumPy array for further processing
audio_array = np.frombuffer(audio_data, dtype=np.int16)
print(audio_array)
