import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Predictor:

  def has_disease(self, row):
    self.train(self)
    return True if self.predict(self,row) == 1 else False

  @staticmethod
  def train(self):
    df = pd.read_csv('./data/dataset.csv')
    dataset = df
    self.standardScaler = StandardScaler()
    columns_to_scale = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
    dataset[columns_to_scale] = self.standardScaler.fit_transform(dataset[columns_to_scale])
    y = dataset['target']
    X = dataset.drop(['target'], axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)
    self.knn_classifier = KNeighborsClassifier(n_neighbors = 8)
    self.knn_classifier.fit(X, y)
    score = self.knn_classifier.score(X_test, y_test)
    print('--Training Complete--')
    print('Score: '+str(score))
  
  @staticmethod
  def predict(self, row):
    user_df = np.array(row).reshape(1,13)
    user_df = self.standardScaler.transform(user_df)
    predicted = self.knn_classifier.predict(user_df)
    print("Predicted: "+str(predicted[0]))
    return predicted[0]
    