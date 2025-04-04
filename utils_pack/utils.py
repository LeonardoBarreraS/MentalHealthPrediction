#Machine Learning Libraries
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import IsolationForest
import joblib


rs=42

def ml_tranformation(df):
    
    numerical_columns2=df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_columns2=df.select_dtypes(include=["object"]).columns.tolist()

    
    num_pipeline=Pipeline([
        #("imputer_num", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline=Pipeline([
        #("imputer_cat", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(sparse_output=False, drop="first", handle_unknown="ignore"))
    ])

    column_transformer=ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_columns2),
            ("cat", cat_pipeline, categorical_columns2),

        ], 
    )

    column_transformer.fit(df)
    x_encoded=column_transformer.transform(df)
    #x_test_encoded=column_transformer.transform(df)
    joblib.dump(column_transformer, "./API/model_utils/columns_transformer.pkl")

    return x_encoded


def remove_outliers(x_encoded, y_train):
    isolation_forest=IsolationForest(contamination=0.04, random_state=rs)
    isolation_forest.fit(x_encoded)
    joblib.dump(isolation_forest, "./API/model_utils/isolation_forest.pkl")


    outlier_labels=isolation_forest.predict(x_encoded)
    non_outliers_mask=outlier_labels != -1
    X=x_encoded[non_outliers_mask]
    y=y_train[non_outliers_mask]
    return X,y
