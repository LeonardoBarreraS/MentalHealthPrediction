import sys
import os

sys.path.append(os.path.abspath(".."))

#Core Libraries
import pandas as pd
import warnings
from utils_pack import *

#Machine Learning Libraries

from sklearn.model_selection import  cross_val_score
from sklearn.metrics import make_scorer, accuracy_score
from xgboost import XGBClassifier


#MLFlow Libraries
import mlflow
import mlflow.sklearn


# Set random seed
rs = 42

#Ignore warnings
warnings.filterwarnings('ignore')

#Concatenate train and test data
df_train=pd.read_csv("./Data/train.csv")
df_test=pd.read_csv("./Data/test.csv")

df=pd.concat([df_train, df_test], ignore_index=True)

#Transforming
df_t=df.copy()

degree_groups = {
    'Class 12': 'High School',
    'B.Ed': 'Bachelor',
    'B.Arch': 'Bachelor',
    'B.Com': 'Bachelor',
    'B.Pharm': 'Bachelor',
    'BCA': 'Bachelor',
    'BBA': 'Bachelor',
    'BSc': 'Bachelor',
    'M.Ed': 'Master',
    'MCA': 'Master'
}

df_t["Degree"]=df_t["Degree"].map(degree_groups)

df_t=df_t[df_t["Sleep Duration"].isin(["Less than 5 hours", "7-8 hours", "More than 8 hours", "5-6 hours"])]
df_t=df_t[df_t["Dietary Habits"].isin(["Moderate","Unhealthy", "Healthy"])]


#Creating new feature
df_t["Age_WorkPressure"]=df_t["Age"]*df_t["Work Pressure"]
df_t["Age_AcademicPressure"]=df_t["Age"]*df_t["Academic Pressure"]


#Renaming columns
df_t=df_t.rename(columns={
    "Working Professional or Student": "Working_Professional_or_Student",
    "Academic Pressure": "Academic_Pressure",
    "Work Pressure": "Work_Pressure",
    "Study Satisfaction": "Study_Satisfaction",
    "Job Satisfaction": "Job_Satisfaction",
    "Sleep Duration": "Sleep_Duration",
    "Dietary Habits": "Dietary_Habits",
    "Have you ever had suicidal thoughts ?":"Suicidal_Thoughts",
    "Work/Study Hours":"Work_Study_Hours",
    "Financial Stress":"Financial_Stress",
    "Family History of Mental Illness":"Family_History_of_Mental_Illness"
})

#Splitting the dataset in Features and Target variables and in Train and Test datasets
df_t["Depression"]=df_t["Depression"].fillna(2)
df_test=df_t[df_t["Depression"]==2]
df_test=df_test.drop(["Depression", "id", "City", "Name" ], axis=1)

df_train_temp=df_t[df_t["Depression"]!=2]
df_y_train=df_train_temp["Depression"]
df_x_train=df_train_temp.drop(["Depression", "id", "City", "Name", "Profession", "CGPA"], axis=1)

#Tranforming the features
x_encoded=utils.ml_tranformation(df_x_train)


# Isolation Forest for anomaly detection and removal
X,y=utils.remove_outliers(x_encoded, df_y_train)

#MLFlow setup
mlflow.set_tracking_uri("API/model/mlruns")
experiment_name = "mental_health_experiment"
try:
    # Crear un experimento en MLFlow    
    mlflow.create_experiment(experiment_name)
except Exception as e:
    # Si el experimento ya existe, no es necesario crear uno nuevo
    print(f"El experimento '{experiment_name}' ya existe.")

# Establece el experimento actual en MLFlow
mlflow.set_experiment(experiment_name)

#Start the MLFlow run
with mlflow.start_run() as run:

    #Modeling with XGBoost
    scoring2=make_scorer(accuracy_score)
    xgb2 = XGBClassifier(use_label_encoder=False, random_state=rs)
    cv_scores2=cross_val_score(xgb2, X, y, cv=5, scoring=scoring2)
    
    #Fit the XGB model and predict
    xgb2.fit(X, y)
    y_pred=xgb2.predict(X)

    #Evaluation of accuracy
    accuracy_cv_scores2=cv_scores2.mean()
    accuracy_xgb=accuracy_score(y, y_pred)

    #MLFlow logging
    mlflow.log_metric("accuracy", float(accuracy_xgb)) #logging accuracy
    mlflow.log_metric("accuracy_cv", float(accuracy_cv_scores2)) #logging cross validation accuracy
    mlflow.sklearn.log_model(xgb2, "MentalHealth") #loogin the model

    #Registering the model
    run_id=run.info.run_id
    model_uri=f"runs:/{run_id}/MentalHealth"
    mlflow.register_model(model_uri, "MentalHealth") #registering the model

mlflow.end_run()