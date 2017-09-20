# -*- coding: utf-8 -*-
u"""
Subsubmodule for ecg processing.
"""
from __future__ import division
from __future__ import absolute_import
import numpy as np
import pandas as pd
import biosppy
import mne
import scipy

from ..signal import *

# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def rsp_process(rsp, sampling_rate=1000):
    u"""
    Automated processing of RSP signals.

    Parameters
    ----------
    rsp : list or array
        Respiratory (RSP) signal array.
    sampling_rate : int
        Sampling rate (samples/second).

    Returns
    ----------
    processed_rsp : dict
        Dict containing processed RSP features.

        Contains the RSP raw signal, the filtered signal, the respiratory cycles onsets, and respiratory phases (inspirations and expirations).

    Example
    ----------
    >>> import neurokit as nk
    >>>
    >>> processed_rsp = nk.rsp_process(rsp_signal)

    Notes
    ----------
    *Authors*

    - Dominique Makowski (https://github.com/DominiqueMakowski)

    *Dependencies*

    - biosppy
    - numpy
    - pandas

    *See Also*

    - BioSPPY: https://github.com/PIA-Group/BioSPPy
    """
    processed_rsp = {u"df": pd.DataFrame({u"RSP_Raw": np.array(rsp)})}

    biosppy_rsp = dict(biosppy.signals.resp.resp(rsp, sampling_rate=sampling_rate, show=False))
    processed_rsp[u"df"][u"RSP_Filtered"] = biosppy_rsp[u"filtered"]

            #   RSP Rate
#   ============
    rsp_rate = biosppy_rsp[u"resp_rate"]*60  # Get RSP rate value (in cycles per minute)
    rsp_times = biosppy_rsp[u"resp_rate_ts"]   # the time (in sec) of each rsp rate value
    rsp_times = np.round(rsp_times*sampling_rate).astype(int)  # Convert to timepoints
    try:
        rsp_rate = discrete_to_continuous(rsp_rate, rsp_times, sampling_rate)  # Interpolation using 3rd order spline
        processed_rsp[u"df"][u"RSP_Rate"] = rsp_rate
    except TypeError:
        print u"NeuroKit Warning: rsp_process(): Sequence too short to compute respiratory rate."
        processed_rsp[u"df"][u"RSP_Rate"] = np.nan

    '''
        # psd powers
    #   ============
    window_size_psd = 300
    freq_bands = {
        u"0_0.1": [0.0001, 0.1],
        u"0.1_0.2": [0.1, 0.2],
        u"0.2_0.3": [0.2, 0.3],
        u"0.3_0.4": [0.3, 0.4],
        u"0.4_0.5": [0.4, 0.5]}



    for col in freq_bands:  # initialize columns to nan
        processed_rsp[u"df"][col] = np.nan

   
    for i in xrange(len(rsp)):
        if window_size_psd <= i:
            power, freq = mne.time_frequency.psd_array_multitaper(rsp[i - window_size_psd:i+window_size_psd], sfreq=sampling_rate, fmin=0,
                                                                  fmax=0.5, adaptive=False,
                                                                  normalization=u'length')
            for band in freq_bands:
                processed_rsp[u"df"].set_value(col=band,index=i,value=power_in_band(power, freq, freq_bands[band]))

# statistical features
#   ============
    window_size_statistics = 300
    statistics_features = [u'SEM', u'MFD', u'SDFD', u'MSD', u'SDSD', u'SDBA', u'MAXRSP', u'MINRSP', u'DMMRSP',u'Skewness', u'Kurtosis']
    for col in statistics_features:  # initialize columns to nan
        processed_rsp[u"df"][col] = np.nan
    for i in xrange(len(rsp)):
        if window_size_statistics <= i :
            data_rspr = processed_rsp[u'df'][u'RSP_Rate'][i - window_size_statistics :i]
            data_waveform = rsp[i - window_size_statistics:i]
            processed_rsp[u"df"].set_value(col=u'SEM', index=i, value=np.std(data_rspr) / np.sqrt(window_size_statistics))
            processed_rsp[u"df"].set_value(col=u'MFD', index=i, value=np.mean(np.diff(data_rspr)))
            processed_rsp[u"df"].set_value(col=u'SDFD', index=i, value=np.std(np.diff(data_rspr)))
            processed_rsp[u"df"].set_value(col=u'MSD', index=i, value=np.mean(np.diff(data_rspr, 2)))
            processed_rsp[u"df"].set_value(col=u'SDSD', index=i, value=np.std(np.diff(data_rspr, 2)))
            processed_rsp[u'df'].set_value(col=u'SDBA',index=i, value=np.std(data_waveform))
            processed_rsp[u'df'].set_value(col=u'MAXRSP', index=i, value=np.max(data_waveform))
            processed_rsp[u'df'].set_value(col=u'MINRSP', index=i, value=np.min(data_waveform))
            processed_rsp[u'df'].set_value(col=u'DMMRSP', index=i, value= processed_rsp[u'df'][u'MAXRSP'] - processed_rsp[u'df'][u'MINRSP'])
            processed_rsp[u'df'].set_value(col=u'Skewness', index=i, value=scipy.stats.skew(data_rspr))
            processed_rsp[u'df'].set_value(col=u'Kurtosis', index=i, value=scipy.stats.kurtosis(data_rspr))
    '''
    #   RSP Cycles
#   ===========================
    rsp_cycles = rsp_find_cycles(biosppy_rsp[u"filtered"])
    processed_rsp[u"df"][u"RSP_Inspiration"] = rsp_cycles[u"RSP_Inspiration"]

    processed_rsp[u"RSP"] = {}
    processed_rsp[u"RSP"][u"Cycles_Onsets"] = rsp_cycles[u"RSP_Cycles_Onsets"]
    processed_rsp[u"RSP"][u"Expiration_Onsets"] = rsp_cycles[u"RSP_Expiration_Onsets"]
    processed_rsp[u"RSP"][u"Cycles_Length"] = rsp_cycles[u"RSP_Cycles_Length"]/sampling_rate

#   RSP Variability
#   ===========================
    rsp_diff = processed_rsp[u"RSP"][u"Cycles_Length"]

    processed_rsp[u"RSP"][u"Respiratory_Variability"] = {}
    processed_rsp[u"RSP"][u"Respiratory_Variability"][u"RSPV_SD"] = np.std(rsp_diff)
    processed_rsp[u"RSP"][u"Respiratory_Variability"][u"RSPV_RMSSD"] = np.sqrt(np.mean(rsp_diff ** 2))
    processed_rsp[u"RSP"][u"Respiratory_Variability"][u"RSPV_RMSSD_Log"] = np.log(processed_rsp[u"RSP"][u"Respiratory_Variability"][u"RSPV_RMSSD"])


    print "processed_rsp"
    return(processed_rsp)





# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def rsp_find_cycles(signal):
    u"""
    Find Respiratory cycles onsets, durations and phases.

    Parameters
    ----------
    signal : list or array
        Respiratory (RSP) signal (preferably filtered).


    Returns
    ----------
    rsp_cycles : dict
        RSP cycles features.

    Example
    ----------
    >>> import neurokit as nk
    >>> rsp_cycles = nk.rsp_find_cycles(signal)

    Notes
    ----------
    *Authors*

    - Dominique Makowski (https://github.com/DominiqueMakowski)

    *Dependencies*

    - biosppy

    *See Also*

    - BioSPPY: https://github.com/PIA-Group/BioSPPy

    """
    # Compute gradient (sort of derivative)
    gradient = np.gradient(signal)
    # Find zero-crossings
    zeros, = biosppy.tools.zero_cross(signal=gradient, detrend=True)

    # Find respiratory phases
    phases_indices = []
    for i in zeros:
        if gradient[i+1] > gradient[i-1]:
            phases_indices.append(u"Inspiration")
        else:
            phases_indices.append(u"Expiration")

    # Select cycles (inspiration) and expiration onsets
    inspiration_onsets = []
    expiration_onsets = []
    for index, onset in enumerate(zeros):
        if phases_indices[index] == u"Inspiration":
            inspiration_onsets.append(onset)
        if phases_indices[index] == u"Expiration":
            expiration_onsets.append(onset)


    # Create a continuous inspiration signal
    # ---------------------------------------
    # Find initial phase
    if phases_indices[0] == u"Inspiration":
        phase = u"Expiration"
    else:
        phase = u"Inspiration"

    inspiration = []
    phase_counter = 0
    for i, value in enumerate(signal):
        if i == zeros[phase_counter]:
            phase = phases_indices[phase_counter]
            if phase_counter < len(zeros)-1:
                phase_counter += 1
        inspiration.append(phase)

    # Find last phase
    if phases_indices[len(phases_indices)-1] == u"Inspiration":
        last_phase = u"Expiration"
    else:
        last_phase = u"Inspiration"
    inspiration = np.array(inspiration)
    inspiration[max(zeros):] = last_phase

    # Convert to binary
    inspiration[inspiration == u"Inspiration"] = 1
    inspiration[inspiration == u"Expiration"] = 0
    inspiration = pd.to_numeric(inspiration)

    cycles_length = np.diff(inspiration_onsets)

    rsp_cycles = {u"RSP_Inspiration": inspiration,
                  u"RSP_Expiration_Onsets": expiration_onsets,
                  u"RSP_Cycles_Onsets": inspiration_onsets,
                  u"RSP_Cycles_Length": cycles_length}

    return(rsp_cycles)



# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def rsp_EventRelated(epoch, event_length, window_post=4):
    u"""
    Extract event-related respiratory (RSP) changes.

    Parameters
    ----------
    epoch : pandas.DataFrame
        An epoch contains in the epochs dict returned by :function:`neurokit.create_epochs()` on dataframe returned by :function:`neurokit.bio_process()`.
    event_length : int
        In seconds.
    sampling_rate : int
        Sampling rate (samples/second).
    window_post : float
        Post-stimulus window size (in seconds) to include eventual responses (usually 3 or 4).

    Returns
    ----------
    RSP_Response : dict
        Event-locked RSP response features.

    Example
    ----------
    >>> import neurokit as nk
    >>> bio = nk.bio_process(ecg=data["ECG"], rsp=data["RSP"], eda=data["EDA"], sampling_rate=1000, add=data["Photosensor"])
    >>> df = bio["df"]
    >>> events = nk.find_events(df["Photosensor"], cut="lower")
    >>> epochs = nk.create_epochs(df, events["onsets"], duration=7, onset=-0.5)
    >>> for epoch in epochs:
    >>>     bio_response = nk.bio_EventRelated(epoch, event_length=4, window_post=3)

    Notes
    ----------
    *Details*

    - **RSP_Rate_Baseline**: mean RSP Rate before stimulus onset.
    - **RSP_Rate_Min**: Min RSP Rate after stimulus onset.
    - **RSP_Rate_MinDiff**: RSP Rate mininum - baseline.
    - **RSP_Rate_MinTime**: Time of minimum.
    - **RSP_Rate_Max**: Max RSP Rate after stimulus onset.
    - **RSP_Rate_MaxDiff**: Max RSP Rate - baseline.
    - **RSP_Rate_MaxTime**: Time of maximum.
    - **RSP_Rate_Mean**: Mean RSP Rate after stimulus onset.
    - **RSP_Rate_MeanDiff**: Mean RSP Rate - baseline.
    - **RSP_Min**: Value in standart deviation (normalized by baseline) of the lowest point.
    - **RSP_MinTime**: Time of RSP Min.
    - **RSP_Max**: Value in standart deviation (normalized by baseline) of the highest point.
    - **RSP_MaxTime**: Time of RSP Max.
    - **RSP_Inspiration**: Respiration phase on stimulus onset (1 = inspiration, 0 = expiration).
    - **RSP_Inspiration_Completion**: Percentage of respiration phase on stimulus onset.


    *Authors*

    - `Dominique Makowski <https://dominiquemakowski.github.io/>`_

    *Dependencies*

    - numpy
    - pandas

    *See Also*

    References
    -----------
    - Gomez, P., Stahel, W. A., & Danuser, B. (2004). Respiratory responses during affective picture viewing. Biological Psychology, 67(3), 359-373.
    """
    # Initialization
    RSP_Response = {}
    window_end = event_length + window_post

    # RSP Rate
    # =============
    if u"RSP_Rate" in epoch.columns:
        RSP_Response[u"RSP_Rate_Baseline"] = epoch[u"RSP_Rate"].ix[0]
        RSP_Response[u"RSP_Rate_Min"] = epoch[u"RSP_Rate"].ix[0:window_end].min()
        RSP_Response[u"RSP_Rate_MinDiff"] = RSP_Response[u"RSP_Rate_Min"] - RSP_Response[u"RSP_Rate_Baseline"]
        RSP_Response[u"RSP_Rate_MinTime"] = epoch[u"RSP_Rate"].ix[0:window_end].idxmin()
        RSP_Response[u"RSP_Rate_Max"] = epoch[u"RSP_Rate"].ix[0:window_end].max()
        RSP_Response[u"RSP_Rate_MaxDiff"] = RSP_Response[u"RSP_Rate_Max"] - RSP_Response[u"RSP_Rate_Baseline"]
        RSP_Response[u"RSP_Rate_MaxTime"] = epoch[u"RSP_Rate"].ix[0:window_end].idxmax()
        RSP_Response[u"RSP_Rate_Mean"] = epoch[u"RSP_Rate"].ix[0:window_end].mean()
        RSP_Response[u"RSP_Rate_MeanDiff"] = RSP_Response[u"RSP_Rate_Mean"] - RSP_Response[u"RSP_Rate_Baseline"]


    # RSP Phase
    # =============
    if u"RSP_Inspiration" in epoch.columns:
        RSP_Response[u"RSP_Inspiration"] = epoch[u"RSP_Inspiration"].ix[0]

        # Identify beginning and end
        phase_beg = np.nan
        phase_end = np.nan
        for i in epoch[0:window_end].index:
            if epoch[u"RSP_Inspiration"].ix[i] != RSP_Response[u"RSP_Inspiration"]:
                phase_end = i
                break
        for i in epoch[:0].index[::-1]:
            if epoch[u"RSP_Inspiration"].ix[i] != RSP_Response[u"RSP_Inspiration"]:
                phase_beg = i
                break

        RSP_Response[u"RSP_Inspiration_Completion"] = -1*phase_beg/(phase_end - phase_beg)*100


    return(RSP_Response)
