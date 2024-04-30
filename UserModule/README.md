# Conda environment flow

### Setup
conda create --name user_module_env python=3.8
conda activate user_module_env
conda install pandas scikit-learn xgboost
conda install -c conda-forge boto3
conda install -c conda-forge requests
conda install -c conda-forge streamlit

### Verify

conda list

### Deactivate

conda deactivate