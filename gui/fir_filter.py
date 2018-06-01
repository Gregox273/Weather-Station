import numpy as np
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


def fir_filter(x, strength):

    #------------------------------------------------
    # Create a FIR filter and apply it to x.
    #------------------------------------------------
        
    
    # The Spacial Sample Rate.
    x = np.concatenate((x,x,x))
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
    
    return filtered_x[int(len(x)/3)+1:int(2*len(x)/3)+1]

