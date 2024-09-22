# Part-A

import scipy.io
import matplotlib.pyplot as plt

# Load data
H = scipy.io.loadmat('dataset_H.mat')['dataset_H'][0]
A = scipy.io.loadmat('dataset_A.mat')['dataset_A'][0]
stimuli = ['Person', 'text', 'speech']

# Raster plot function
def Rastor(subplot, data, title):
    for i, j in enumerate(data):
        subplot.vlines(j[0], i + 0.5, i + 1.5, color='blue')
    subplot.axvline(0, color='green', linestyle='--')
    subplot.axvline(1000, color='red', linestyle='--')
    subplot.set_title(title)
    subplot.set_ylabel('Trials')
    subplot.set_xlabel('Time (ms)')

# Plot data
fig, subplot = plt.subplots(3, 2, figsize=(15, 10), sharex=True, sharey=True)
for i, j in enumerate(stimuli):
    Rastor(subplot[i, 0], H[i], f'H - {j}')
    Rastor(subplot[i, 1], A[i], f'A - {j}')
plt.tight_layout()
plt.show()



# Part - B

import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Load and extract data
H = [scipy.io.loadmat('dataset_H.mat')['dataset_H'][0][i] for i in range(3)]
A = [scipy.io.loadmat('dataset_A.mat')['dataset_A'][0][i] for i in range(3)]
stimuli = ['Person', 'text', 'speech']

# Computation and Smoothing data
def compute(data, size=50, timeWindow=50):
    time = np.arange(-1000, 3000, size)
    histogram = np.sum([np.histogram(i[0], bins=time)[0] for i in data], axis=0)
    smoothedHistogram = np.convolve(histogram, np.ones(timeWindow) / timeWindow, mode='same')
    return time[:-1], smoothedHistogram

# Plot data
fig, subplot = plt.subplots(3, 2, figsize=(15, 10), sharex=True, sharey=True)
for i, p in enumerate(stimuli):
    for j, (data, area) in enumerate(zip([H, A], ['H', 'A'])):
        time, PSTH = compute(data[i])
        subplot[i, j].plot(time, PSTH, color='blue')
        subplot[i, j].axvline(0, color='green', linestyle='--')
        subplot[i, j].axvline(1000, color='red', linestyle='--')
        subplot[i, j].set_title(f'Region {area} - {p}')
        subplot[i, j].set_ylabel('Neuron Activity')
        subplot[i, j].set_xlabel('Time (ms)')
        subplot[i, j].legend(['Stimulus-Onset', 'Stimulus-Offset'])
plt.tight_layout()
plt.show()




# Part - C

import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Data-Loading
H = [scipy.io.loadmat('dataset_H.mat')['dataset_H'][0][i] for i in range(3)]
A = [scipy.io.loadmat('dataset_A.mat')['dataset_A'][0][i] for i in range(3)]
stimuli = ['Person', 'text', 'speech']
color = {'Person': 'red', 'text': 'green', 'speech': 'blue'}

# Computing average firing rate
def compute(data, size=200, timeInterval=1000):
    time = np.arange(0, timeInterval + size, size)
    result = np.sum([np.histogram(i[0], bins=time)[0] for i in data], axis=0) / len(data)
    return time[:-1], result

# Data-Plotting
fig, subplot = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
for data, area, subplt in zip([H, A], ['H', 'A'], subplot):
    firingRate = {}
    for type, color in color.items():
        time, rate = compute(data[stimuli.index(type)])
        subplt.plot(time, rate, color=color, label=f'{type} ({np.mean(rate):.2f} Hz)')
        firingRate[type] = np.mean(rate)
    preferredType = max(firingRate, key=firingRate.get)
    order = sorted(firingRate, key=firingRate.get, reverse=True)
    subplt.set_title(f'Region {area}\n Most Preferred Stimulus Type : {preferredType}\nOrder of Stimulus Preference : {", ".join(order)}')
    subplt.set_xlabel('Time (ms)')
    subplt.legend()
subplot[0].set_ylabel('Average Firing Rate (Hz)')
plt.tight_layout()
plt.show()

