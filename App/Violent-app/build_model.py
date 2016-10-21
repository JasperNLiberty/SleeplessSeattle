from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.metrics import auc


pd.set_option("display.max_columns",101)



if __name__ == "__main__":
        # Load Iris Data
        	
        with open('dfs.pkl', 'r') as f:
    		dfs = pickle.load(f)

        X = dfs[['TimeOfDay', 'R', 'J', 'B']] #, 'C', 'N', 'K', 'Q', 'M', 'U','E','D','F','L','G','W','O','S','99']]
        y = dfs['Burden']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 4444)

        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)

        #iris_data = load_iris()
        #features = iris_data.data
        #feature_names = iris_data.feature_names
        #target = iris_data.target
        #target_names = iris_data.target_names

        #knn = KNeighborsClassifier(n_neighbors=3)  # replace with your own ML model here
        #knn.fit(features, target)

        joblib.dump(logreg, 'models/time_model.pkl')
