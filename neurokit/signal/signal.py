# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy








# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def discrete_to_continuous(values, value_times, sampling_rate=1000):
    """
    3rd order spline interpolation.

    Parameters
    ----------
    values : dataframe
        Values.
    value_times : list
        Time indices of values.
    sampling_rate : int
        Sampling rate (samples/second).

    Returns
    ----------
    signal : pd.Series
        An array containing the values indexed by time.

    Example
    ----------
    >>> import neurokit as nk
    >>> signal = discrete_to_continuous([4, 5, 1, 2], [1, 2, 3, 4], sampling_rate=1000)
    >>> pd.Series(signal).plot()

    Notes
    ----------
    *Authors*

    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    *Dependencies*

    - scipy
    - pandas
    """
#    values=RRis.copy()
#    value_times=beats_times.copy()
    # Preprocessing
    initial_index = value_times[0]
    value_times = np.array(value_times) - initial_index

    # fit a 3rd degree spline on the data.
    spline = scipy.interpolate.splrep(x=value_times, y=values, k=3, s=0)  # s=0 guarantees that it will pass through ALL the given points
    x = np.arange(0, value_times[-1], 1)
    # Get the values indexed per time
    signal = scipy.interpolate.splev(x=x, tck=spline, der=0)
    # Transform to series
    signal = pd.Series(signal)
    signal.index = np.array(np.arange(initial_index, initial_index+len(signal), 1))

    return(signal)


def power_in_band(power, freq, band):
    power = np.trapz(y=power[(freq >= band[0]) & (freq < band[1])], x=freq[(freq >= band[0]) & (freq < band[1])])
    return (power)