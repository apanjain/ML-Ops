## Test User Files Description

## Structure
- `train.py` : Has the ML training code, should dump the trained model as a dump file using joblib (or other serializing-deserializing modules) which will be used by the prediction.py
- `requirement.txt` : List of dependencies (python libraries) required for the training.
- `salaryDataSet.csv` : Dataset used for training.  
- `prediction.py`: Should expose a predict function, that takes in a dictionary argument and returns a string as a predicted result.
