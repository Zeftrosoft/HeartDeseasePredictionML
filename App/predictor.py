import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_csv('./data/dataset.csv')
#dataset = df
dataset = pd.get_dummies(df, columns = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'])
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
standardScaler = StandardScaler()
columns_to_scale = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
dataset[columns_to_scale] = standardScaler.fit_transform(dataset[columns_to_scale])

y = dataset['target']
X = dataset.drop(['target'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)

knn_classifier = KNeighborsClassifier(n_neighbors = 8)
knn_classifier.fit(X, y)
score = knn_classifier.score(X_test, y_test)
predicted = knn_classifier.predict(X_test)
print(score)
#X_test.to_csv(r''+"test.csv", mode='a', index=None, header=True)