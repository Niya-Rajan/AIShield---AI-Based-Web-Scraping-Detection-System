import pickle

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_bot(features):
    return model.predict(features)[0]