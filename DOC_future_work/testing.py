import numpy as np
import pandas as pd
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# https://towardsdatascience.com/music-in-python-2f054deb41f4


def get_piano_notes():
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]

    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs


def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave

"""
For the C naturals in octaves 4-5-6, what happens if you add the original signals? 
"""
add_arr = []
for i in range(4, 7):
    note_freqs = get_piano_notes()
    # what note do you want to find
    frequency = note_freqs[f'C{i}']

    # put it onto a sine wave
    sine_wave = get_sine_wave(frequency, duration=2, amplitude=1000)

    # append it to an array
    add_arr.append(sine_wave)

    # write the frequency to a file
    wavfile.write('C:/Users/clewis/IdeaProjects/GNS/DOC_future_work/piano_c.wav', rate=44100, data=sine_wave.astype(np.int16))

# add the frequencies that you sampled together, combine the signals as your ear would hear them
added = add_arr[0] + add_arr[1] + add_arr[2]
c4 = add_arr[0]
c5 = add_arr[1]
c6 = add_arr[2]

fig, axs = plt.subplots(4)
fig.suptitle('C natural superimposed and added')
# what am I plotting?
axs[0].plot(added[0:200])
axs[1].plot(c4[0:200])
axs[2].plot(c5[0:200])
axs[3].plot(c6[0:200])
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results2.png', dpi=400, bbox_inches="tight")




# fig = plt.figure(4, figsize=(12, 4))
# gs = gridspec.GridSpec(8, 2)
# gs.update(wspace=.35, hspace=.25)
#
#
#
#
#
#
#
# xtr_subplot = fig.add_subplot(gs[0:2, 0:2])
# plt.plot(added[0:200])
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.title('Sound Wave of Middle C on Piano')
# plt.show()
#
# xtr_subplot = fig.add_subplot(gs[0:2, 0:2])
#
#
# xtr_subplot = fig.add_subplot(gs[0:2, 0:2])
#
#
# xtr_subplot = fig.add_subplot(gs[0:2, 0:2])
#
#
#
# xtr_subplot = fig.add_subplot(gs[0:2, 0:2])
