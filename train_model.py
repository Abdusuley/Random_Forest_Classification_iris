from model import RandomForestModel
import json

def train_and_save_model():
    """Train the model and save it"""
    print("Training Random Forest Model...")
    
    # Initialize and train model
    rf_model = RandomForestModel()
    X, y, feature_names, target_names = rf_model.load_data()
    
    accuracy, X_test, y_test = rf_model.train(X, y)
    
    # Save the model
    rf_model.save_model('random_forest_model.pkl')
    
    # Save model info
    model_info = {
        'accuracy': float(accuracy),
        'feature_names': feature_names,
        'target_names': target_names.tolist(),
        'n_samples': len(X),
        'n_features': X.shape[1]
    }
    
    with open('model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"Model trained with accuracy: {accuracy:.4f}")
    print("Model saved as 'random_forest_model.pkl'")
    print("Model info saved as 'model_info.json'")

if __name__ == "__main__":
    train_and_save_model()