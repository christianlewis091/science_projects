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
notes_of_interest = ['C4','F4','A4']

add_arr = []
for i in range(0, len(notes_of_interest)):
    note_freqs = get_piano_notes()
    # what note do you want to find
    frequency = note_freqs[notes_of_interest[i]]

    # put it onto a sine wave
    sine_wave = get_sine_wave(frequency, duration=2, amplitude=1000)

    # append it to an array
    add_arr.append(sine_wave)

    # write the frequency to a file
    wavfile.write('C:/Users/clewis/IdeaProjects/GNS/DOC_future_work/piano_c.wav', rate=44100, data=sine_wave.astype(np.int16))

# add the frequencies that you sampled together, combine the signals as your ear would hear them
c4 = add_arr[0]
c5 = add_arr[1]
c6 = add_arr[2]
added = c4 + c5 + c6

#FFT
t = np.arange(added.shape[0])
freq = np.fft.fftfreq(t.shape[-1])*4000
sp = np.fft.fft(added)

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
fig, axs = plt.subplots(5, sharex=True)

fig.subplots_adjust(hspace=0.5)
fig.suptitle('C natural superimposed and added')
# what am I plotting?
n = 2500
axs[0].plot(added[0:n], c1)
axs[1].plot(c4[0:n], c2)
axs[2].plot(c5[0:n], c3)
axs[3].plot(c6[0:n])
# add labels
axs[0].set_title('Addition of waves')
axs[1].set_title(notes_of_interest[0])
axs[2].set_title(notes_of_interest[1])
axs[3].set_title(notes_of_interest[2])

axs[4].set_title('Fourier Transform')
axs[4].plot(freq, abs(sp.real))
axs[4].set_xlim((0, n))

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xtra/FMaj.png', dpi=400)

"""
Wrap a chord around a polar plot: 
"""
# https://www.youtube.com/watch?v=bDrfYFgcn2I