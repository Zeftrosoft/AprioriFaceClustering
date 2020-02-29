import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_csv('./data/dataset.csv')
dataset = df
#dataset = pd.get_dummies(df, columns = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'])
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
standardScaler = StandardScaler()
columns_to_scale = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
dataset[columns_to_scale] = standardScaler.fit_transform(dataset[columns_to_scale])

y = dataset['target']
X = dataset.drop(['target'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)
knn_classifier = KNeighborsClassifier(n_neighbors = 8)
knn_classifier.fit(X, y)
score = knn_classifier.score(X_test, y_test)

v = (70,1,0,145,174,0,1,125,1,2.6,0,0,3)
user_df = np.array(v).reshape(1,13)
print(user_df)

user_df = standardScaler.transform(user_df)
print(user_df)

predicted = knn_classifier.predict(user_df)
print(predicted)
