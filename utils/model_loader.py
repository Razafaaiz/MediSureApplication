import joblib

def load_model(path):
    return joblib.load(path)

def load_scaler(path):
    return joblib.load(path)

def load_encoder(path):
    return joblib.load(path)

def load_features(path):
    return joblib.load(path)
