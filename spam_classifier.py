
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
from sklearn.datasets import load_iris


def prediction(full_email):
  df = pd.read_csv('spam_ham_dataset.csv')

  data = df.head(5)
  print(data)

  data = df.where((pd.notnull(df)), '')

  data.head(10)

  data.info()

  data.shape

  data.loc[data['label'] == 'spam', 'label'] = 0
  data.loc[data['label'] == 'ham', 'label'] = 1

  X = data['text']
  Y = data['label']

  print(X)

  print(Y)

  X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size= 0.2, random_state = 3)

  print(X.shape)
  print(X_train.shape)
  print(X_test.shape)

  feature_extraction = TfidfVectorizer(min_df=1, max_df=0.5, stop_words='english',
                                      lowercase=True, ngram_range=(1, 2))
  feature_extraction.fit(data)
  joblib.dump(feature_extraction, 'feature_extraction.pkl')

  X_train_features = feature_extraction.fit_transform(X_train)
  X_test_features = feature_extraction.transform(X_test)

  # Check for NaN values and handle them
  if Y_train.isnull().values.any():
      Y_train = Y_train.fillna(0)  # or use another strategy like dropping the rows
  if Y_test.isnull().values.any():
      Y_test = Y_test.fillna(0)

  # Now convert to integer type
  Y_train = Y_train.astype('int')
  Y_test = Y_test.astype('int')
  Y_train = Y_train.astype('int')
  Y_test = Y_test.astype('int')

  print(X_train)

  print(X_train_features)

  iris = load_iris()
  model = MultinomialNB()
  model.fit(iris.data, iris.target)
  joblib.dump(model, 'model.pkl')

  model.fit(X_train_features, Y_train)

  prediction_on_training_data = model.predict(X_train_features)
  accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)

  print('Accuracy on training data: ', accuracy_on_training_data)

  prediction_on_test_data = model.predict(X_test_features)
  accuracy_on_test_data = accuracy_score(Y_test, prediction_on_test_data)

  print('Accuracy on test data: ', accuracy_on_test_data)

  input = [full_email]

  input_data_features = feature_extraction.transform(input)

  prediction = model.predict(input_data_features)

  print(prediction)

  

  if prediction[0] == 1:
    return("Real")
  else:
    return("Spam")

