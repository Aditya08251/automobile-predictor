"""
Flask Backend API for ML Predictor
Serves the machine learning model and handles predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_model import IrisClassifier
import logging
from datetime import datetime

# ============================================
# Flask App Setup
# ============================================

app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# Initialize ML Model
# ============================================

try:
    classifier = IrisClassifier()
    logger.info("✅ ML Model initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize ML Model: {str(e)}")
    classifier = None

# ============================================
# Routes
# ============================================

@app.route('/', methods=['GET'])
def index():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'ok',
        'message': 'ML Predictor API is running',
        'timestamp': datetime.now().isoformat(),
        'service': 'Iris Flower Classifier API'
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint with detailed info
    """
    return jsonify({
        'status': 'healthy',
        'service': 'ML Predictor',
        'model_loaded': classifier is not None,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/model/info', methods=['GET'])
def model_info():
    """
    Get information about the trained model
    """
    if classifier is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        info = classifier.get_model_info()
        return jsonify({
            'status': 'success',
            'data': info
        }), 200
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction for iris flower species
    
    Expected JSON:
    {
        "sepal_length": float,
        "sepal_width": float,
        "petal_length": float,
        "petal_width": float
    }
    """
    if classifier is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'The ML model could not be loaded. Please try again.'
        }), 500
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Please provide flower measurements in JSON format'
            }), 400
        
        # Validate required fields
        required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing fields',
                'missing_fields': missing_fields,
                'required_fields': required_fields
            }), 400
        
        # Validate data types and ranges
        try:
            sepal_length = float(data['sepal_length'])
            sepal_width = float(data['sepal_width'])
            petal_length = float(data['petal_length'])
            petal_width = float(data['petal_width'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Invalid data type',
                'message': 'All fields must be numeric values'
            }), 400
        
        # Validate ranges (based on typical iris flower measurements)
        if not (4.0 <= sepal_length <= 8.0):
            return jsonify({'error': 'Sepal length out of range (4.0-8.0)'}), 400
        if not (2.0 <= sepal_width <= 4.5):
            return jsonify({'error': 'Sepal width out of range (2.0-4.5)'}), 400
        if not (1.0 <= petal_length <= 7.0):
            return jsonify({'error': 'Petal length out of range (1.0-7.0)'}), 400
        if not (0.1 <= petal_width <= 2.6):
            return jsonify({'error': 'Petal width out of range (0.1-2.6)'}), 400
        
        # Make prediction
        result = classifier.predict(sepal_length, sepal_width, petal_length, petal_width)
        
        logger.info(f"Prediction made: {result['prediction']} (confidence: {result['confidence']:.2%})")
        
        return jsonify({
            'status': 'success',
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities'],
            'input': {
                'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Make multiple predictions at once
    
    Expected JSON:
    {
        "predictions": [
            {
                "sepal_length": float,
                "sepal_width": float,
                "petal_length": float,
                "petal_width": float
            },
            ...
        ]
    }
    """
    if classifier is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        predictions_data = data.get('predictions', [])
        
        if not predictions_data:
            return jsonify({'error': 'No predictions provided'}), 400
        
        results = []
        for idx, pred_data in enumerate(predictions_data):
            try:
                result = classifier.predict(
                    float(pred_data['sepal_length']),
                    float(pred_data['sepal_width']),
                    float(pred_data['petal_length']),
                    float(pred_data['petal_width'])
                )
                results.append({
                    'index': idx,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'index': idx,
                    'status': 'error',
                    'error': str(e)
                })
        
        return jsonify({
            'status': 'success',
            'total': len(predictions_data),
            'successful': len([r for r in results if r['status'] == 'success']),
            'results': results
        }), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': 'Batch prediction failed',
            'message': str(e)
        }), 500


# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'path': request.path
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"📨 {request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log response status"""
    logger.info(f"📤 {response.status_code}")
    return response


# ============================================
# Main Entry Point
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 ML Predictor Backend Server Starting...")
    print("="*60)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Model Status: {'✅ Loaded' if classifier else '❌ Failed to load'}")
    print("🌐 Server: http://localhost:5000")
    print("📡 CORS: Enabled for all origins")
    print("="*60)
    print("\nAvailable Endpoints:")
    print("  GET  /                    - Health check")
    print("  GET  /health              - Detailed health info")
    print("  GET  /model/info          - Model information")
    print("  POST /predict             - Make a prediction")
    print("  POST /batch-predict       - Make multiple predictions")
    print("="*60 + "\n")
    
    # Run the app
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=True
    )
