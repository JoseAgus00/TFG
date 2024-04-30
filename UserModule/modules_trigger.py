import os
import boto3
import joblib
import pandas as pd
from model_generator import generate_model
from utils.module_utils import download_patients_info, upload_new_model, diseases_dict, clean_folder, download_model, reset_patients_list


temp_folder_path = 'utils/temp/'


def execute_model(disease, fever, cough, fatigue, breathingDifficulty, age, bloodPressure, cholesterolLevel):
    files_in_directory = os.listdir(temp_folder_path)
    file_key = 'xgb_model.pkl'
    if file_key not in files_in_directory:
        s3 = boto3.client("s3")
        download_model(s3, temp_folder_path, file_key)
    model = joblib.load(f'{temp_folder_path}{file_key}')
    new_df = patient_data(disease, fever, cough, fatigue, breathingDifficulty, age, bloodPressure, cholesterolLevel)
    new_X = new_df[['Disease', 'Fever', 'Cough', 'Fatigue', 'BreathingDifficulty', 'Age', 'BloodPressure', 'CholesterolLevel']]
    predicted_score = model.predict(new_X)
    return predicted_score[0]


def update_model():
    s3 = boto3.client("s3")
    temp_folder_path = 'utils/temp/'
    download_patients_info(s3, temp_folder_path)
    generate_model(temp_folder_path)
    upload_new_model(s3, temp_folder_path)
    clean_folder(temp_folder_path)

def reset_patients():
    s3 = boto3.client("s3")
    reset_patients_list(s3)


def patient_data(disease, fever, cough, fatigue, breathing_difficulty, age, blood_pressure, cholesterol_level):
    data = {
        "Disease": disease,
        "Fever": fever,
        "Cough": cough,
        "Fatigue": fatigue,
        "BreathingDifficulty": breathing_difficulty,
        "Age": age,
        "BloodPressure": blood_pressure,
        "CholesterolLevel": cholesterol_level
    }

    data_df = pd.DataFrame([data])
    data_df['Disease'] = data_df['Disease'].map(diseases_dict.get)
    data_df['Fever'] = data_df['Fever'].map({'true': 1, 'false': 0})
    data_df['Cough'] = data_df['Cough'].map({'true': 1, 'false': 0})
    data_df['Fatigue'] = data_df['Fatigue'].map({'true': 1, 'false': 0})
    data_df['BreathingDifficulty'] = data_df['BreathingDifficulty'].map({'true': 1, 'false': 0})
    data_df['Age'] = data_df['Age'].astype(int)
    data_df['BloodPressure'] = data_df['BloodPressure'].astype(int)
    data_df['CholesterolLevel'] = data_df['CholesterolLevel'].astype(int)

    return data_df


#update_model()
#execute_model()
