import requests
import json
import time
import sys

def test_app():
    """Test the Flask application"""
    base_url = "http://localhost:5000"
    
    # Wait for app to start
    print("Waiting for application to start...")
    time.sleep(2)
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Test health endpoint
            print(f"Attempt {attempt + 1}/{max_retries}: Testing health endpoint...")
            health_response = requests.get(f"{base_url}/health", timeout=10)
            print(f"Health check: {health_response.status_code}")
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"Health data: {json.dumps(health_data, indent=2)}")
                break
            else:
                print(f"Health check failed: {health_response.status_code}")
                if attempt == max_retries - 1:
                    print("All health check attempts failed")
                    return False
                time.sleep(2)
        except requests.exceptions.ConnectionError:
            print(f"Connection failed attempt {attempt + 1}. Retrying...")
            if attempt == max_retries - 1:
                print("Could not connect to application")
                return False
            time.sleep(2)
        except Exception as e:
            print(f"Health check error: {e}")
            if attempt == max_retries - 1:
                return False
            time.sleep(2)
    
    try:
        # Test model info
        print("\nTesting model info endpoint...")
        info_response = requests.get(f"{base_url}/model-info", timeout=10)
        print(f"Model info: {info_response.status_code}")
        if info_response.status_code == 200:
            info_data = info_response.json()
            print(f"Model info: {json.dumps(info_data, indent=2)}")
        
        # Test prediction with different examples
        test_cases = [
            {"name": "Setosa", "features": [5.1, 3.5, 1.4, 0.2]},
            {"name": "Versicolor", "features": [6.0, 2.7, 5.1, 1.6]},
            {"name": "Virginica", "features": [6.3, 3.3, 6.0, 2.5]}
        ]
        
        for test_case in test_cases:
            print(f"\nTesting {test_case['name']} prediction...")
            prediction_response = requests.post(
                f"{base_url}/predict",
                json={"features": test_case['features']},
                timeout=10
            )
            
            if prediction_response.status_code == 200:
                result = prediction_response.json()
                print(f"✅ {test_case['name']} prediction successful!")
                print(f"   Predicted: {result['prediction_class']}")
                print(f"   Probabilities:")
                for cls, prob in result['probabilities'].items():
                    print(f"     {cls}: {prob:.4f}")
            else:
                print(f"❌ {test_case['name']} prediction failed: {prediction_response.status_code}")
                print(f"   Error: {prediction_response.text}")
        
        print("\n🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)