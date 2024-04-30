import boto3
import json
import pandas as pd
import streamlit as st
from modules_trigger import update_model, execute_model, reset_patients
from utils.module_utils import diseases_dict, download_patients_info, clean_folder, boolen_maps, variable_maps
import requests

st.markdown("<style>.stButton>button {width: 200px;height: 50px;font-size: 16px;background-color: #25a5be;color: white;margin: auto;display: block;}</style>", unsafe_allow_html=True)
s3 = boto3.client("s3")
temp_folder_path = 'utils/temp/'

if 'has_executed' not in st.session_state:
    st.session_state.has_executed = True
    download_patients_info(s3, temp_folder_path)

def processing_module():
    st.title("Patient Data Entry")
    st.divider()
    patient_info, patient_status = st.columns(2)
    with patient_info:
        st.subheader("Patient Data")
        id_val = st.text_input("ID")
        name_val = st.text_input("Name")
        last_name_val = st.text_input("Last Name")
        age_val = st.selectbox("Age", range(1, 100), index=24)
        gender_val = st.selectbox("Gender", ["Male", "Female"])
    with patient_status:
        st.subheader("Patient Status")
        disease_val = st.selectbox("Disease", ["Select Disease"] + list(diseases_dict.keys()))
        fever_val = st.selectbox("Fever", ["Yes", "No"], index=1)
        cough_val = st.selectbox("Cough", ["Yes", "No"], index=1)
        fatigue_val = st.selectbox("Fatigue", ["Yes", "No"], index=1)
        breathing_difficulty_val = st.selectbox("Breathing Difficulty", ["Yes", "No"], index=1)
        blood_pressure_val = st.selectbox("Blood Pressure", ["Low", "Normal", "High"], index=1)
        cholesterol_level_val = st.selectbox("Cholesterol Level", ["Low", "Normal", "High"], index=1)
    ready_to_submit = True
    if all([id_val, name_val, last_name_val, disease_val, fever_val, cough_val, fatigue_val, breathing_difficulty_val, age_val, gender_val, blood_pressure_val, cholesterol_level_val]):
        if disease_val != "Select Disease":
            ready_to_submit = False
    submitted = st.button("Submit", disabled=ready_to_submit)
    if submitted:
        url = 'https://z3utmen9gk.execute-api.us-east-2.amazonaws.com/default/calculator'
        dangerousness = execute_model(
            disease_val, 
            boolen_maps[fever_val], 
            boolen_maps[cough_val], 
            boolen_maps[fatigue_val], 
            boolen_maps[breathing_difficulty_val], 
            str(age_val), 
            variable_maps[blood_pressure_val], 
            variable_maps[cholesterol_level_val]) * 100
        data = {
            "PatientData" : {
                "ID": id_val,
                "Name": name_val,
                "LastName": last_name_val,
                "Disease": disease_val,
                "Fever": boolen_maps[fever_val],
                "Cough": boolen_maps[cough_val],
                "Fatigue": boolen_maps[fatigue_val],
                "BreathingDifficulty": boolen_maps[breathing_difficulty_val],
                "Age": str(age_val),
                "Gender": gender_val,
                "BloodPressure": variable_maps[blood_pressure_val],
                "CholesterolLevel": variable_maps[cholesterol_level_val],
                "Dangerousness": f"{round(dangerousness)}%"
            }
        }
        headers = {
            'x-api-key': 'TTIQa9sHIV8NNQoNdVfrLamr3Fim2QMy3TS5QvR3'
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            st.success(f"Patient added successfully. The calculated dangerousness is: {round(dangerousness)}%")
        else:
            st.error(f"Failed to add patient: {response.status_code}")

    st.divider()
    st.subheader("Want to re-generate model?")
    grant = not st.checkbox("Are you sure to re-generate model? It might take a while.")
    model_generation = st.button("Re-generate model", disabled=grant)
    if model_generation:
        update_model()
        st.success("Model generated successfully.")

    st.divider()
    st.subheader("Want to reset patients list to default?")
    reset_grant = not st.checkbox("Are you sure to reset patients list? You will lose all progress.")
    reset_patients_button = st.button("Reset patients", disabled=reset_grant)
    if reset_patients_button:
        reset_patients()
        st.success("Patients list reset applied.")


def reports_module():
    tabs = st.tabs(["Static Reports", "Filtered Reports"])
    with open(f'{temp_folder_path}patients.json', 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    with tabs[0]:
        st.title("Static Reports")
        st.divider()
        st.subheader("Patient diseases report")
        generate_report_by_attribute(df, "Disease")
        st.divider()
        st.subheader("Patient ages report")
        generate_report_by_attribute(df, "Age")
        st.divider()
        st.subheader("Patient genders report")
        generate_report_by_attribute(df, "Gender")
    with tabs[1]:
        st.title("Filtered Report")
        st.divider()
        st.subheader("Select age filter")
        less_than = st.selectbox("Less than", range(1, 100), disabled=True)
        greater_than = st.selectbox("Greater than", range(1, less_than), disabled=True)
        st.write("Work in progress")



def generate_report_by_attribute(df, attribute):
    attribute_counts = df[attribute].value_counts()
    st.bar_chart(attribute_counts, use_container_width=True)


add_patient = st.sidebar.button("Add new patient")
report_generator = st.sidebar.button("Report generator")
is_add_patient_page = True
if add_patient and not is_add_patient_page:
    is_add_patient_page = True
elif report_generator and is_add_patient_page:
    is_add_patient_page = False

if is_add_patient_page:
    processing_module()
elif report_generator:
    reports_module()
