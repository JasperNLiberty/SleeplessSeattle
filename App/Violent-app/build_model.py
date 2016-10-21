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


#pd.set_option("display.max_columns",101)



if __name__ == "__main__":
        # Load Iris Data
        
        with open('columns.pkl', 'r') as f:
            columns = pickle.load(f)


        X = pd.read_csv("violent_df.csv")
        X=X.iloc[:,1:]
        
        y = pd.read_csv("violent_target.csv", names = ["Target"])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4444)

        logit = LogisticRegression(class_weight = 'balanced')
        logit.fit(X_train, y_train)

        #iris_data = load_iris()
        #features = iris_data.data
        #feature_names = iris_data.feature_names
        #target = iris_data.target
        #target_names = iris_data.target_names

        #knn = KNeighborsClassifier(n_neighbors=3)  # replace with your own ML model here
        #knn.fit(features, target)

        joblib.dump(logit, 'models/violent_model.pkl')
