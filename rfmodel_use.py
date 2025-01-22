
# exporting trained model and pipeline
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

import joblib

import sys
import subprocess

# exporting trained model and pipeline
import pickle
from sklearn.base import BaseEstimator, TransformerMixin

web_server_ip = '192.168.175.43'

class Float32AndInfinityHandler(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Convert float64 to float32
        X = X.astype({col: np.float32 for col in X.select_dtypes(include=['float64']).columns})

        # Replace inf and -inf with NaN
        X.replace([np.inf, -np.inf], np.nan, inplace=True)
        return X

# Custom transformer to select specific columns
class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.columns]

# Create the preprocessor for scaling only selected columns
class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, scale_columns):
        self.scale_columns = scale_columns
        self.imputer = SimpleImputer(strategy='mean')
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        # Fit the imputer on the relevant columns
        self.imputer.fit(X[self.scale_columns])
        return self

    def transform(self, X):
        # Impute missing values
        X[self.scale_columns] = self.imputer.transform(X[self.scale_columns])
        # Scale the specified columns
        X[self.scale_columns] = self.scaler.fit_transform(X[self.scale_columns])
        return X

# Load the pipeline
ppl = joblib.load('pipeline_new.joblib')

# Load the tuned RandomForestClassifier model
loadrf = joblib.load('best_rf_new.joblib')

# read the unseen test data csv file
test_data = pd.read_csv(sys.argv[1])

ip_address_sender = test_data['Src IP']
ip_address_receiver = test_data['Dst IP']

test_data.head()

# Fit and transform the data using the pipeline
X_transformed = ppl.fit_transform(test_data)

# X_transformed now contains the preprocessed and scaled data, ready for use in modeling.
X_transformed.head()

# use the loaded model to predict on the transformed X
y_pred = loadrf.predict(X_transformed)
# print(y_pred)

# Label encoding dictionary
label_decoding = {0 : 'BENIGN', 1 : 'Web Attack - Brute Force', 2 : 'Web Attack - XSS', 3 : 'Web Attack - SQL Injection'}

# # Create an inverse dictionary to map from numeric labels back to string labels
# label_decoding = {v: k for k, v in label_encoding.items()}

# # Map the predicted labels to their string names
# y_pred_labels = [label_decoding[label] for label in y_pred]

# # Create a DataFrame with the decoded predictions
# predictions_df = pd.DataFrame(y_pred_labels, columns=["Predicted_Label"])

# # Export to CSV
# predictions_df.to_csv('predictions.csv', index=False)

sent_ips = set()

for i in range(len(y_pred)):
    pred = y_pred[i]
    if pred != 0:
        current_ip = ip_address_sender[i]
        if current_ip == web_server_ip:
            current_ip = ip_address_receiver[i]
            if current_ip == web_server_ip:
                continue
        type_of_attack = label_decoding[pred]
        if current_ip in sent_ips:
            continue
        else:
            sent_ips.add(current_ip)
            # send email 
            subprocess.run(["./sendNotif.sh", sys.argv[2], current_ip, type_of_attack])
            print(current_ip, type_of_attack)

    
