"""Based on code by WarrenWeckesser (http://scipy-cookbook.readthedocs.io/items/FIRFilter.html)"""

import numpy as np
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


def fir_filter(data, strength):

    #------------------------------------------------
    # Create a FIR filter and apply it to x.
    #------------------------------------------------


    # The Spacial Sample Rate.
    x_f = np.flip(data,0)
    x = np.concatenate((x_f,data,x_f))
    nsamples = len(x)
    sample_rate = nsamples

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 0.25 Hz transition width.
    width = (nsamples/(20*strength))/nyq_rate

    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)

    # The cutoff frequency of the filter.
    cutoff_hz = nsamples/(10*strength)

    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)

    print(np.shape(data))
    print(np.shape(filtered_x))

    print(int((len(x)/3))+N+1)
    print(int((len(x)/3))+N+1+len(data))

    if(int((len(x)/3))+N+1+len(data) > len(filtered_x)):
        print("data")
        return data
    else:
        print("filtered")
        return filtered_x[int((len(x)/3))+N+1:int((len(x)/3))+N+1+len(data)]

