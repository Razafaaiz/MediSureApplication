import numpy as np

def apply_scaler(scaler, values):
    return scaler.transform([values])

def select_features(feature_list, form_data):
    return [float(form_data[f]) for f in feature_list]
