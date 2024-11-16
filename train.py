import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# import the preprocessed data

df=pd.read_csv('notebook\\Data\\preprocessing.csv')

# spliting of dataset into train,test ,split
df_full_train,df_test=train_test_split(df,test_size=0.20,random_state=1)
df_train,df_val=train_test_split(df_full_train,test_size=0.25,random_state=1)
df_train=df_train.reset_index(drop=True)
df_test=df_test.reset_index(drop=True)
df_val=df_val.reset_index(drop=True)

y_train=df_train['tenyearchd'].values
y_test=df_test['tenyearchd'].values
y_val=df_val['tenyearchd'].values

del df_train['tenyearchd']
del df_test['tenyearchd']
del df_val['tenyearchd']

# Training the model
best_C = 10

model=LogisticRegression(C=best_C, solver='liblinear', random_state=1)
model.fit(df_train,y_train)

## Exporting the Trained model
with open('best_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Model has been saved as 'best_model.pkl'")