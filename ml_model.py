# @title
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
import warnings
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from category_encoders import OrdinalEncoder
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline

# Importing the auxiliar and preprocessing librarys

# Models
warnings.filterwarnings("ignore")

url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
df = pd.read_csv(url)


# drop unnecessary and too relevant columns
df = df[['Date', 'CountryName', 'CountryCode', 'C3_Cancel public events', 'C4_Restrictions on gatherings', 'C5_Close public transport',
         'C6_Stay at home requirements', 'C8_International travel controls', 'H1_Public information campaigns', 'StringencyIndexForDisplay']]

# float to integer
int_columns = ['C3_Cancel public events', 'C4_Restrictions on gatherings', 'C5_Close public transport',
               'C6_Stay at home requirements', 'C8_International travel controls', 'H1_Public information campaigns']
df[int_columns] = df[int_columns].astype(pd.Int64Dtype())
df = df[df['StringencyIndexForDisplay'].notnull()]

# create a new target named target

conditions = [
    (df['StringencyIndexForDisplay'] <= 50.0),
    (df['StringencyIndexForDisplay'] > 50.0)
]

values = [0, 1]

df['target'] = np.select(conditions, values)

df = df.dropna(axis=0)

X = df.drop(columns=['target', 'Date', 'CountryName', 'CountryCode', ])
y = df['target']

X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.3, random_state=42)

processor = OrdinalEncoder()
X_train_processed = processor.fit_transform(X_train)
X_val_processed = processor.transform(X_val)

model = GradientBoostingClassifier(
    n_estimators=200, random_state=2, max_depth=7, learning_rate=0.2)

model.fit(X_train_processed, y_train)
