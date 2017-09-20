from __future__ import absolute_import
import pytest
import doctest
import os
import numpy as np
import pandas as pd
import neurokit as nk


run_tests_in_local = True


#==============================================================================
# BIO
#==============================================================================
def test_read_acqknowledge():

    if run_tests_in_local is False:
        data_path = os.getcwdu() + ur"/data/test_bio_data.acq"  # If running from travis
    else:
        data_path = u"data/test_bio_data.acq"  # If running in local

    # Read data
    df, sampling_rate = nk.read_acqknowledge(data_path, return_sampling_rate=True)
    # Resample to 100Hz
    df = df.resample(u"10L").mean()
    df.columns = [u'ECG', u'EDA', u'PPG', u'Photosensor', u'RSP']
    # Check length
    assert len(df) == 35645
    return(df)

# ---------------
def test_bio_process():

    df = test_read_acqknowledge()

    if run_tests_in_local is False:  # If travis
        ecg_quality_model = os.path.abspath('..') + ur"/neurokit/materials/heartbeat_classification.model"
    else:  # If local
        ecg_quality_model = u"default"

    bio = nk.bio_process(ecg=df[u"ECG"], rsp=df[u"RSP"], eda=df[u"EDA"], ecg_sampling_rate=100, rsp_sampling_rate=100,eda_sampling_rate=100, add=df[u"Photosensor"], ecg_quality_model=ecg_quality_model, age=24, sex=u"m", position=u"supine")

    assert len(bio) == 4
    return(bio)

if __name__ == u'__main__':
#    nose.run(defaultTest=__name__)
    doctest.testmod()
    pytest.main()

