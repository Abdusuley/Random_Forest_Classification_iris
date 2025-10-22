from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import json
import os

app = Flask(__name__)

# Global model variable
model = None
model_info = None

def load_model():
    """Load the trained model and info"""
    global model, model_info
    
    try:
        # Check if model file exists, if not train it
        if not os.path.exists('random_forest_model.pkl'):
            print("Model not found. Training model...")
            from train_model import train_and_save_model
            train_and_save_model()
        
        model = joblib.load('random_forest_model.pkl')
        
        with open('model_info.json', 'r') as f:
            model_info = json.load(f)
            
        print("Model loaded successfully!")
        print(f"Model accuracy: {model_info['accuracy']}")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
        model_info = None

# Load model when module is imported
load_model()

@app.route('/')
def home():
    """Home page with prediction form"""
    return render_template('index.html', model_info=model_info)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get features from request
        if request.is_json:
            data = request.get_json()
        else:
            # Handle form data
            data = {
                'features': [
                    float(request.form.get('sepal_length', 0)),
                    float(request.form.get('sepal_width', 0)),
                    float(request.form.get('petal_length', 0)),
                    float(request.form.get('petal_width', 0))
                ]
            }
        
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        features = data['features']
        
        # Validate input
        if len(features) != model_info['n_features']:
            return jsonify({
                'error': f'Expected {model_info["n_features"]} features, got {len(features)}'
            }), 400
        
        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)[0]
        probabilities = model.predict_proba(features_array)[0]
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'prediction_class': model_info['target_names'][prediction],
            'probabilities': {
                model_info['target_names'][i]: float(prob) 
                for i, prob in enumerate(probabilities)
            },
            'feature_names': model_info['feature_names'],
            'model_accuracy': model_info['accuracy']
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    if model is not None and model_info is not None:
        return jsonify({
            'status': 'healthy', 
            'model_loaded': True,
            'accuracy': model_info['accuracy']
        })
    else:
        return jsonify({'status': 'unhealthy', 'model_loaded': False}), 500

@app.route('/model-info')
def get_model_info():
    """Get model information"""
    if model_info is not None:
        return jsonify(model_info)
    else:
        return jsonify({'error': 'Model info not available'}), 500

@app.route('/predict-form', methods=['POST'])
def predict_form():
    """Endpoint for form submissions"""
    try:
        features = [
            float(request.form['sepal_length']),
            float(request.form['sepal_width']),
            float(request.form['petal_length']),
            float(request.form['petal_width'])
        ]
        
        # Create JSON request for the predict function
        class MockJson:
            def __init__(self, data):
                self.data = data
            
            def get_json(self):
                return self.data
        
        request._get_json = lambda: {'features': features}
        
        return predict()
    
    except Exception as e:
        return jsonify({'error': f'Invalid form data: {str(e)}'}), 400

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)