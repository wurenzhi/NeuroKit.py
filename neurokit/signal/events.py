# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from itertools import groupby




# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def binarize_signal(signal, treshold=u"auto", cut=u"higher"):
    u"""
    Binarize a channel based on a continuous channel.

    Parameters
    ----------
    signal = array or list
        The signal channel.
    treshold = float
        The treshold value by which to select the events. If "auto", takes the value between the max and the min.
    cut = str
        "higher" or "lower", define the events as above or under the treshold. For photosensors, a white screen corresponds usually to higher values. Therefore, if your events were signalled by a black colour, events values would be the lower ones, and you should set the cut to "lower".

    Returns
    ----------
    list
        binary_signal

    Example
    ----------
    >>> import neurokit as nk
    >>> binary_signal = nk.binarize_signal(signal, treshold=4)

    Authors
    ----------
    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    Dependencies
    ----------
    None
    """
    if treshold == u"auto":
        treshold = (np.max(np.array(signal)) - np.min(np.array(signal)))/2
    signal = list(signal)
    binary_signal = []
    for i in xrange(len(signal)):
        if cut == u"higher":
            if signal[i] > treshold:
                binary_signal.append(1)
            else:
                binary_signal.append(0)
        else:
            if signal[i] < treshold:
                binary_signal.append(1)
            else:
                binary_signal.append(0)
    return(binary_signal)


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def localize_events(events_channel, treshold=u"auto", cut=u"higher", time_index=None):
    u"""
    Find the onsets of all events based on a continuous signal.

    Parameters
    ----------
    events_channel = array or list
        The trigger channel.
    treshold = float
        The treshold value by which to select the events. If "auto", takes the value between the max and the min.
    cut = str
        "higher" or "lower", define the events as above or under the treshold. For photosensors, a white screen corresponds usually to higher values. Therefore, if your events were signalled by a black colour, events values would be the lower ones, and you should set the cut to "lower".
    time_index = array or list
        Add a corresponding datetime index, will return an addional array with the onsets as datetimes.

    Returns
    ----------
    dict
        dict containing the onsets, the duration and the time index if provided.

    Example
    ----------
    >>> import neurokit as nk
    >>> events_onset = nk.events_onset(events_channel)

    Authors
    ----------
    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    Dependencies
    ----------
    None
    """
    events_channel = binarize_signal(events_channel, treshold=treshold, cut=cut)

    events = {u"onsets":[], u"durations":[]}
    if time_index is not None:
        events[u"onsets_time"] = []

    index = 0
    for key, g in (groupby(events_channel)):
        duration = len(list(g))
        if key == 1:
            events[u"onsets"].append(index)
            events[u"durations"].append(duration)
            if time_index is not None:
                events[u"onsets_time"].append(time_index[index])
        index += duration
    return(events)


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def find_events(events_channel, treshold=u"auto", cut=u"higher", time_index=None, number=u"all", after=0, before=None, min_duration=1):
    u"""
    Find and select events based on a continuous signal.

    Parameters
    ----------
    events_channel : array or list
        The trigger channel.
    treshold : float
        The treshold value by which to select the events. If "auto", takes the value between the max and the min.
    cut : str
        "higher" or "lower", define the events as above or under the treshold. For photosensors, a white screen corresponds usually to higher values. Therefore, if your events were signalled by a black colour, events values would be the lower ones, and you should set the cut to "lower".
        Add a corresponding datetime index, will return an addional array with the onsets as datetimes.
    number : str or int
        How many events should it select.
    after : int
        If number different than "all", then at what time should it start selecting the events.
    before : int
        If number different than "all", before what time should it select the events.
    min_duration : int
        The minimum duration of an event (in timepoints).

    Returns
    ----------
    events : dict
        Dict containing events onsets and durations.

    Example
    ----------
    >>> import neurokit as nk
    >>> events = nk.select_events(events_channel)

    Notes
    ----------
    *Authors*

    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    *Dependencies*

    - numpy
    """
    events = localize_events(events_channel, treshold=treshold, cut=cut, time_index=time_index)

    # Warning when no events detected
    if len(events[u"onsets"]) == 0:
        print u"NeuroKit warning: find_events(): No events found. Check your events_channel or adjust trehsold."
        return()

    # Remove less than duration
    toremove = []
    for event in xrange(len(events[u"onsets"])):
        if events[u"durations"][event] < min_duration:
            toremove.append(False)
        else:
            toremove.append(True)
    events[u"onsets"] = np.array(events[u"onsets"])[np.array(toremove)]
    events[u"durations"] = np.array(events[u"durations"])[np.array(toremove)]
    if time_index is not None:
        events[u"onsets_time"] = np.array(events[u"onsets_time"])[np.array(toremove)]

    # Before and after
    if isinstance(number, int):
        after_times = []
        after_onsets = []
        after_length = []
        before_times = []
        before_onsets = []
        before_length = []
        if after != None:
            if events[u"onsets_time"] == []:
                events[u"onsets_time"] = np.array(events[u"onsets"])
            else:
                events[u"onsets_time"] = np.array(events[u"onsets_time"])
            after_onsets = list(np.array(events[u"onsets"])[events[u"onsets_time"]>after])[:number]
            after_times = list(np.array(events[u"onsets_time"])[events[u"onsets_time"]>after])[:number]
            after_length = list(np.array(events[u"durations"])[events[u"onsets_time"]>after])[:number]
        if before != None:
            if events[u"onsets_time"] == []:
                events[u"onsets_time"] = np.array(events[u"onsets"])
            else:
                events[u"onsets_time"] = np.array(events[u"onsets_time"])
            before_onsets = list(np.array(events[u"onsets"])[events[u"onsets_time"]<before])[:number]
            before_times = list(np.array(events[u"onsets_time"])[events[u"onsets_time"]<before])[:number]
            before_length = list(np.array(events[u"durations"])[events[u"onsets_time"]<before])[:number]
        events[u"onsets"] = before_onsets + after_onsets
        events[u"onsets_time"] = before_times + after_times
        events[u"durations"] = before_length + after_length

    return(events)


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def plot_events_in_signal(signal, events, color=u"red"):
    u"""
    Plot events in signal.

    Parameters
    ----------
    signal : array or DataFrame
        Signal array (can be a dataframe with many signals).
    events : list or ndarray
        Events location.
    color : int or list
        Marker color.

    Example
    ----------
    >>> import neurokit as nk
    >>> df = nk.bio_process(ecg=signal, sampling_rate=1000)
    >>> events = df["ECG"]["Rpeaks"]
    >>> plot_events_in_signal(signal, events)

    Notes
    ----------
    *Authors*

    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    *Dependencies*

    - matplotlib
    - pandas
    """
    signal = pd.DataFrame(signal)
    signal.plot()

    events = np.array(events)
    try:
        len(events[0])
        for index, dim in enumerate(events):
            for event in dim:
                if isinstance(color, list):
                    plt.axvline(x=event, color=color[index])
                else:
                    plt.axvline(x=event, color=color)
    except TypeError:
        for event in events:
            if isinstance(color, list):
                plt.axvline(x=event, color=color[0])
            else:
                plt.axvline(x=event, color=color)

