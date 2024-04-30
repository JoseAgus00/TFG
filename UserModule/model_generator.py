import json
import joblib
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from utils.module_utils import diseases_dict


def generate_model(temp_folder_path):

    with open(f'{temp_folder_path}patients.json', 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df['Disease'] = df['Disease'].map(diseases_dict.get)
    df['Fever'] = df['Fever'].map({'true': 1, 'false': 0})
    df['Cough'] = df['Cough'].map({'true': 1, 'false': 0})
    df['Fatigue'] = df['Fatigue'].map({'true': 1, 'false': 0})
    df['BreathingDifficulty'] = df['BreathingDifficulty'].map({'true': 1, 'false': 0})
    df['Age'] = df['Age'].astype(int)
    df['BloodPressure'] = df['BloodPressure'].astype(int)
    df['CholesterolLevel'] = df['CholesterolLevel'].astype(int)
    df['Dangerousness'] = df['Dangerousness'].str.rstrip('%').astype('float') / 100.0

    X = df[['Disease', 'Fever', 'Cough', 'Fatigue', 'BreathingDifficulty', 'Age', 'BloodPressure', 'CholesterolLevel']]
    y = df['Dangerousness']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=300,
        learning_rate=0.1,
        max_depth=8
    )
    model.fit(X_train, y_train)
    joblib.dump(model, f'{temp_folder_path}xgb_model.pkl')
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    # print(f"MSE: {mse}")
