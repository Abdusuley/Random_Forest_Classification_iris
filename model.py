import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import joblib
import os

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def load_data(self):
        """Load sample iris dataset"""
        iris = load_iris()
        X = iris.data
        y = iris.target
        feature_names = iris.feature_names
        target_names = iris.target_names
        
        return X, y, feature_names, target_names
    
    def train(self, X, y):
        """Train the Random Forest model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        return accuracy, X_test, y_test
    
    def predict(self, features):
        """Make predictions"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        prediction = self.model.predict([features])
        probabilities = self.model.predict_proba([features])
        
        return prediction[0], probabilities[0]
    
    def save_model(self, filename='random_forest_model.pkl'):
        """Save trained model"""
        if self.is_trained:
            joblib.dump(self.model, filename)
            return True
        return False
    
    def load_model(self, filename='random_forest_model.pkl'):
        """Load pre-trained model"""
        if os.path.exists(filename):
            self.model = joblib.load(filename)
            self.is_trained = True
            return True
        return False