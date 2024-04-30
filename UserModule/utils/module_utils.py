import json
import os


with open('utils/diseases_dict.json', 'r') as f:
    diseases_dict = json.load(f)

boolen_maps = { "Yes" : "true", "No" : "false" }
variable_maps = { "High" : "1", "Normal" : "0", "Low" : "-1" }

def download_patients_info(s3, temp_folder_path):
    source_bucket = 'tfg-files-storage'
    file_key = 'patients.json'
    destination_file_path = f'{temp_folder_path}{file_key}'
    s3.download_file(source_bucket, file_key, destination_file_path)


def download_model(s3, temp_folder_path, file_key):
    source_bucket = 'tfg-model-storage'
    destination_file_path = f'{temp_folder_path}{file_key}'
    s3.download_file(source_bucket, file_key, destination_file_path)


def upload_new_model(s3, temp_folder_path):
    bucket_name = 'tfg-model-storage'
    object_name = 'xgb_model.pkl'
    s3.upload_file(f'{temp_folder_path}{object_name}', bucket_name, object_name)

def reset_patients_list(s3):
    bucket_name = 'tfg-files-storage'
    object_name = 'patients.json'
    s3.upload_file(f'utils/{object_name}', bucket_name, object_name)

def clean_folder(folder_path):
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clean_folder(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")