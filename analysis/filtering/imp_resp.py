import pandas as pd
from pylab import figure
import numpy as np
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

## http://scipy-cookbook.readthedocs.io/items/FIRFilter.html

nsamples = 128

impulse = np.zeros(nsamples)
impulse[int(nsamples/2)] = 1

sample_rate = nsamples
t = arange(nsamples) / (sample_rate)

#------------------------------------------------
# Create a FIR filter and apply it to x.
#------------------------------------------------

# The Nyquist rate of the signal.
nyq_rate = sample_rate / 2.0

# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.  We'll design the filter
# with a 0.25 Hz transition width.
width = (nsamples/20)/nyq_rate

# The desired attenuation in the stop band, in dB.
ripple_db = 25.0

# Compute the order and Kaiser parameter for the FIR filter.
N, beta = kaiserord(ripple_db, width)

# The cutoff frequency of the filter.
cutoff_hz = nsamples/10

# Use firwin with a Kaiser window to create a lowpass FIR filter.
taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

# Use lfilter to filter x with the FIR filter.
filtered_x = lfilter(taps, 1.0, impulse)


#------------------------------------------------
# Plot the original and filtered signals.
#------------------------------------------------

# The phase delay of the filtered signal.
delay = 0.5 * (N-1) / sample_rate

figure(1)
# Plot the original signal.
##plot(t, x, linewidth=1)
# Plot the filtered signal, shifted to compensate for the phase delay.
#plot(t[N-1:]-delay, filtered_x[N-1:], 'r-')
# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
#plot(t[int((len(x)/3))+N+1:int((len(x)/3))+N+1+len(temp)], filtered_x[int((len(x)/3))+N+1:int((len(x)/3))+N+1+len(temp)], 'g', linewidth=2)

plot(t, impulse, linewidth=1)
plot(t-delay, filtered_x, 'r-')
print("nsamples = {}".format(nsamples))
print("width = {}".format(width))
print("cutoff hz = {}".format(cutoff_hz))
print("Filter order = {}".format(N))
print("Kaiser beta = {}".format(beta))

xlabel('t')
grid(True)


# print(len(filtered_x[int((len(x)/3))+N+1:int((len(x)/3))+N+1+len(temp)]))
# print(len(temp))
# print(N)
show()
