# -*- coding: utf-8 -*-
"""Big_Mart_Sales_Prediction_Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LVaT3ZmomSrBRbQyv35VAG2ZHkNiVkaH
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing Required Libraries
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import keras
import tensorflow
from keras.layers import InputLayer, Dense
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import csv
from google.colab import files
# %matplotlib inline

# Commented out IPython magic to ensure Python compatibility.
# 
# %%python
# 
# import logging
# logger = logging.getLogger(__name__)
# 
# # logging.basicConfig(
# #     filename='Big_Mart_Sales_Prediction.log', # write to this file
# #     filemode='a', # open in append mode
# #     format='%(name)s - %(levelname)s - %(message)s',
# #     level=logging.DEBUG)
# 
# fh = logging.FileHandler('Big_Mart_Sales_Prediction.log')
# format = logging.Formatter('%(asctime)s- %(levelname)s- %(message)s')
# fh.setFormatter(format)
# logger.addHandler(fh)
# # Set the logging level
# logger.setLevel(logging.DEBUG)
# 
# logger.warning('This will get logged to a file')
# ##############################################################################################################################
#

#DATA CLEANING FUNCTION

def data_clean(df):

  ## Missing values
  try:
    for col in df.select_dtypes(include=['float64','int64']).columns:
      df[col].fillna(df[col].mean(),inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
      df[col].fillna(df[col].mode()[0],inplace=True)
    logger.info(f'Missing values imputed for all dtypes in dataframe')
  except Exception as e:
    logger.warning(f'Missing values could not be removed in dataframe',e, stack_info=True, exc_info=True)

  ## Mapping categorical values
  try:
    for col in df.select_dtypes(exclude=['float64','int64']).columns:
      df[col] = pd.Categorical(df[col], categories=df[col].unique()).codes
    logging.info(f'Categorical values mapped in dataframe')
  except Exception as e:
    logging.warning(f'Categorical values didnt map in dataframe.',e, stack_info=True, exc_info=True)

  ## Scaling the values
  try:
    for i in df.columns[1:]:
      df[i] = (df[i] - df[i].min()) / (df[i].max() - df[i].min())
    logger.info(f'Values scaled between 0 and 1 in dataframe')
  except Exception as e:
    logging.warning(f'Unsuccessful scaling of variables in dataframe.',e, stack_info=True, exc_info=True)
#################################################################################################
  return df

"""## 1. Loading the Data and Preprocessing

---


"""

#LOADING THE DATA

url = 'https://raw.githubusercontent.com/Nishi-sys/Deep_Learning/main/DL/2_Big_Mart_Sales_prediction/train_data.csv'
df = pd.read_csv(url,on_bad_lines='skip')

df.dtypes

## Considering the effect of the age od establishment on sales
df['Outlet_Establishment_Year']= (2024 - df['Outlet_Establishment_Year'])

#PREPROCESSING THE DATA
df_1 = data_clean(df)

df_1.head()

"""## 2. Creating training and validation set

---

"""

## Defining dependent and independent variables
X = df_1.drop(['Item_Outlet_Sales','Item_Identifier','Outlet_Identifier'],axis=1) #dropping dependent variable(y) and (unique keys to identify shop and items)
y = df_1['Item_Outlet_Sales']

X.shape, y.shape

df_1['Item_Outlet_Sales']

# Creating training and validation set
# random state to regenerate the same train and validation set
# test size 0.2 will keep 20% data in validation and remaining 80% in train set
#X_train, X_trest, y_train, y_test

#X_train,X_test,y_train,y_test = train_test_split(X,y,stratify=data['Loan_Status'],random_state=10,test_size=0.2)

X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=10,test_size=0.2)

# shape of training and validation set
(X_train.shape, y_train.shape), (X_test.shape, y_test.shape)

"""## 3. Defining the architecture of the model

---


"""

# defining input neurons = no. of input features
input_neurons = X_train.shape[1]

# number of output neurons
# When developing a neural network to solve a regression problem, the output layer should have exactly one node.
#Here we are not trying to map inputs to a variety of class labels, but rather trying to predict a single continuous target value for each sample
# define number of output neurons
output_neurons = 1

# number of hidden layers and hidden neurons
# It is a hyperparameter and we can pick the hidden layers and hidden neurons on our own
# define hidden layers and neuron in each layer
number_of_hidden_layers = 2
neuron_hidden_layer_1 = 15
neuron_hidden_layer_2 = 10

# defining the architecture of the model   #Dense(units=#neuron_hidden_layerORoutput, activation)
from keras.models import Sequential
model = Sequential()
model.add(InputLayer(input_shape=(input_neurons,)))
model.add(Dense(units=neuron_hidden_layer_1, activation='sigmoid')) ##  9*15(weight matrix + 15(bias))
model.add(Dense(units=neuron_hidden_layer_2, activation='sigmoid')) ## 15*10(weight matrix + 10(bias))
model.add(Dense(units=output_neurons, activation='linear'))

model.summary()

"""## 4. Compiling the model (defining loss function, optimizer)

---


"""

#model.compile(loss='binary_crossentropy',optimizer='Adam',metrics=['accuracy'])
model.compile(loss='mse', optimizer='adam', metrics=['mean_squared_error', 'mean_absolute_error'])

"""## 5. Training the model

---


"""

# training the model

# passing the independent and dependent features for training set for training the model

# validation data will be evaluated at the end of each epoch

# setting the epochs as 200

# storing the trained model in model_history variable which will be used to visualize the training process

model_history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200,verbose=0)

"""## 6. Evaluating model performance on validation set

---


"""

plt.plot(model_history.history['mean_absolute_error'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.show()

"""## Testing the model Accuracy:

---


"""

# Error for validation set
predit_X_test=model.predict(X_test)

#from sklearn.metrics import mean_squared_error
#from sklearn.metrics import mean_absolute_error
print("mean_squared_error",mean_squared_error(predit_X_test,y_test),"\n")
print("mean_absolute_error",mean_absolute_error(predit_X_test,y_test))

# DATA TO BE PREDICTED

##For data to be predicted
url = 'https://raw.githubusercontent.com/Nishi-sys/Deep_Learning/main/DL/2_Big_Mart_Sales_prediction/test_data.csv'
df_test= pd.read_csv(url)

df_test['Outlet_Establishment_Year']= (2024 - df_test['Outlet_Establishment_Year'])

df_test.head() #Overview of the data

df_test_X= df_test.drop(['Item_Identifier','Outlet_Identifier'],axis=1)   # this dataset has no no sales column as we need to predict that

df_test_cleaned = data_clean(df_test_X)

# Predicting the sales
predictions = (model.predict(df_test_cleaned))

# Scaling the prediction back

predictions_scaled_back= (predictions * ((df['Item_Outlet_Sales'].max() - df['Item_Outlet_Sales'].min()))) + df['Item_Outlet_Sales'].min()

df_test_result_set = df_test[['Item_Identifier','Outlet_Identifier']]
df_test_result_set['Predicted Sales'] = predictions_scaled_back

df_test_result_set.head()

df_test_result_set.to_csv('df_test_result_set.csv', index=False)
files.download('df_test_result_set.csv')