from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib
from typing import Optional




try :
    model=mlflow.sklearn.load_model("model/mlruns/534016933238502113/8ac221a2311840168abf4ddb8277efce/artifacts/MentalHealth/")
    print("Modelo cargado correctamente")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    raise

#Cargando column transformer
column_transformer=joblib.load("model_utils/columns_transformer.pkl")
print("Column transformer cargado correctamente")


#Declaring class for data validation
class employee(BaseModel):
    Gender:object
    Age:float
    Working_Professional_or_Student:object      
    Academic_Pressure: Optional[float] = None
    Work_Pressure: Optional[float] = None
    Study_Satisfaction: Optional[float] = None
    Job_Satisfaction: Optional[float] = None
    Sleep_Duration:object
    Dietary_Habits:object
    Degree:object
    Suicidal_Thoughts:object
    Work_Study_Hours:float
    Financial_Stress:float
    Family_History_of_Mental_Illness:object
    Age_WorkPressure: Optional[float] = None
    Age_AcademicPressure: Optional[float] = None

#Creating FastAPI instance
app=FastAPI()

@app.post("/predict")

#Creating prediction function
def predict_employee(input_data:employee):
    try:
        #Receiving data
        data = pd.DataFrame([input_data.model_dump(by_alias=True)])
        # print("Datos recibidos para la predicción:", data)
        # print(data.shape)
        # print(data.info())
        # print(type(data))

        #Transforming data
        x_encoded=column_transformer.transform(data)
        # print("tipo de x_encoded",type(x_encoded))
        # print("shape de x_encoded",x_encoded.shape)
        # print("x_encoded",x_encoded)

        #Making prediction
        prediction = model.predict_proba(x_encoded)
        print("Predicción realizada:", prediction)

        # Convertir el resultado de la predicción a una lista
        prediction_list = prediction.tolist()[0]

        depression_probability= round(prediction_list[1]*100,2)
        print(type(depression_probability))

        return depression_probability
    
    
    except Exception as e:
        print(f"Error al hacer la predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error al hacer la predicción: {e}")


print("Column transformer cargado correctamente")