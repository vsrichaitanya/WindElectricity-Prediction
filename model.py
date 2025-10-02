import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
df = pd.read_csv("DATA/T1.csv")

df.columns = ['DATE','POWER',"WIND SPEED","TP","WIND DIRECTION"]
df = df.loc[:,["WIND DIRECTION","WIND SPEED","POWER"]]
df = df[df['POWER']>0]
X = df[['WIND DIRECTION','WIND SPEED']]
y = df['POWER']
X_train ,X_test,y_train,y_test = train_test_split(X,y,test_size=0.30,random_state=30)
model = RandomForestRegressor(n_estimators = 100, random_state = 0,max_depth = 10)
model.fit(X_train,y_train)

filename = 'model.sav'
joblib.dump(model,filename)

