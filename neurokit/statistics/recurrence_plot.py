from pyunicorn.timeseries.recurrence_plot import RecurrencePlot
def recurrence_plot_features(time_series, threshold=0.05, dim=3,tau=10):
    if len(time_series) > 5000:
        time_series = time_series[-5000:]
    features = {}
    features['dim'] = dim
    features['tau'] = tau
    rp = RecurrencePlot(time_series, threshold=threshold, dim=dim,tau=tau,normalize = True)
    features['RR'] = rp.recurrence_rate()
    features['DET'] = rp.determinism()
    features['LAM'] = rp.laminarity()
    features['TT'] = rp.trapping_time()
    features['RATIO'] = features['DET']/float(features['RR'])
    features['L_avg'] = rp.average_diaglength()
    features['ENTR'] = rp.diag_entropy()
    features['L_max'] = rp.max_diaglength()
    features['Rc_Prob'] = rp.recurrence_probability()
    return features