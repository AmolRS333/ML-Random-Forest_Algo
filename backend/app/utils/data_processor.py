import pandas as pd
import numpy as np
from typing import Tuple, List
from sklearn.preprocessing import LabelEncoder # Data preprocessing utility for datasets & machine learning

def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    """
    Preprocess the dataset by handling missing values and encoding categorical variables.
    Returns the processed DataFrame and the detected target column.
    """
    # Make a copy to avoid modifying the original
    df_processed = df.copy()
    
    # Detect target column (last column by default)
    target_column = df_processed.columns[-1]
    
    # Handle missing values
    for column in df_processed.columns:
        if df_processed[column].dtype in ['int64', 'float64']:
            # Fill numerical missing values with median
            df_processed[column].fillna(df_processed[column].median(), inplace=True)
        else:
            # Fill categorical missing values with mode
            df_processed[column].fillna(df_processed[column].mode()[0], inplace=True) 
    
    # Encode categorical variables
    label_encoders = {}
    for column in df_processed.columns:
        if df_processed[column].dtype == 'object':
            label_encoders[column] = LabelEncoder()
            df_processed[column] = label_encoders[column].fit_transform(df_processed[column])
    
    return df_processed, target_column 