import joblib
import os
loaded_model = joblib.load(os.path.join(
    os.path.dirname(__file__), 'model_dump'))


def predict(query):
    exp = float(query.get("exp"))
    print(exp)
    predicted_value = loaded_model.predict([[exp]])
    return str(predicted_value[0])
