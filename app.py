import pickle
import logging
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask("Heart_Disease_Prediction")
app.config['JSON_SORT_KEYS'] = False  # Maintain parameter order in responses

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Constants
MODEL_FILE = 'best_model.pkl'
SERVICE_NAME = "Heart Disease Prediction API"
API_VERSION = "1.0.0"

# Feature schema with validation rules
FEATURE_SCHEMA = [
    {"name": "male", "type": "binary", "description": "Gender (1=male, 0=female)"},
    {"name": "age", "type": "numeric", "min": 30, "max": 100, "description": "Age in years"},
    {"name": "education", "type": "numeric", "min": 1, "max": 4, "description": "Education level"},
    {"name": "currentsmoker", "type": "binary", "description": "Current smoker status"},
    {"name": "cigsperday", "type": "numeric", "min": 0, "max": 100, "description": "Cigarettes per day"},
    {"name": "bpmeds", "type": "binary", "description": "Blood pressure medication"},
    {"name": "prevalentstroke", "type": "binary", "description": "History of stroke"},
    {"name": "prevalenthyp", "type": "binary", "description": "Hypertensive status"},
    {"name": "diabetes", "type": "binary", "description": "Diabetic status"},
    {"name": "totchol", "type": "numeric", "min": 100, "max": 400, "description": "Total cholesterol"},
    {"name": "bmi", "type": "numeric", "min": 15, "max": 50, "description": "Body Mass Index"},
    {"name": "heartrate", "type": "numeric", "min": 40, "max": 120, "description": "Resting heart rate"},
    {"name": "glucose", "type": "numeric", "min": 50, "max": 400, "description": "Blood glucose level"}
]

# Global model instance
model = None

def load_model():
    """Load machine learning model from file"""
    global model
    try:
        with open(MODEL_FILE, 'rb') as file:
            model = pickle.load(file)
        logger.info("Model loaded successfully")
        return True
    except FileNotFoundError:
        logger.error(f"Model file not found: {MODEL_FILE}")
    except Exception as e:
        logger.exception("Model loading failed")
    return False

def validate_input(data):
    """Validate input data against feature schema"""
    errors = []
    input_keys = set(data.keys())
    expected_keys = {f["name"] for f in FEATURE_SCHEMA}
    
    # Check for missing features
    if missing := expected_keys - input_keys:
        errors.append(f"Missing features: {', '.join(sorted(missing))}")
    
    # Check for extra features
    if extra := input_keys - expected_keys:
        errors.append(f"Unexpected features: {', '.join(sorted(extra))}")
    
    # Validate individual features
    for feature in FEATURE_SCHEMA:
        name = feature["name"]
        if name not in data:
            continue
            
        try:
            value = data[name]
            if feature["type"] == "binary":
                if value not in (0, 1):
                    errors.append(f"'{name}' must be 0 or 1")
            elif feature["type"] == "numeric":
                num_value = float(value)
                if "min" in feature and num_value < feature["min"]:
                    errors.append(f"'{name}' value {num_value} below minimum {feature['min']}")
                if "max" in feature and num_value > feature["max"]:
                    errors.append(f"'{name}' value {num_value} above maximum {feature['max']}")
        except (TypeError, ValueError):
            errors.append(f"'{name}' has invalid numeric format")
    
    return errors

@app.route('/', methods=['GET'])
def home():
    """Service root endpoint with documentation"""
    return jsonify({
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "status": "operational",
        "endpoints": {
            "health_check": {"path": "/health", "method": "GET"},
            "prediction": {"path": "/predict", "method": "POST"}
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Service health monitoring endpoint"""
    return jsonify({
        "service": SERVICE_NAME,
        "status": "ready" if model else "degraded",
        "model_loaded": bool(model),
        "model_file": MODEL_FILE
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Heart disease risk prediction endpoint"""
    # Check model availability
    if not model:
        return jsonify({
            "error": "Service Unavailable",
            "message": "Prediction model not loaded"
        }), 503
    
    # Parse and validate input
    if not (input_data := request.get_json()):
        return jsonify({
            "error": "Invalid Request",
            "message": "No JSON payload provided"
        }), 400
    
    if errors := validate_input(input_data):
        return jsonify({
            "error": "Validation Error",
            "message": "Invalid input parameters",
            "details": errors,
            "expected_features": [{
                "name": f["name"],
                "type": f["type"],
                "description": f["description"],
                "constraints": {
                    "min": f.get("min"),
                    "max": f.get("max")
                }
            } for f in FEATURE_SCHEMA]
        }), 400
    
    try:
        # Prepare input for model
        features = [input_data[f["name"]] for f in FEATURE_SCHEMA]
        feature_names = [f["name"] for f in FEATURE_SCHEMA]
        input_df = pd.DataFrame([features], columns=feature_names)
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        risk_level = "High Risk" if prediction == 1 else "Low Risk"
        
        logger.info(f"Prediction completed - Risk: {risk_level}")
        
        return jsonify({
            "prediction": int(prediction),
            "risk_classification": risk_level,
            "interpretation": (
                "High risk indicates potential heart disease condition"
                if prediction == 1 else
                "Low risk indicates no significant heart disease indicators"
            )
        })
    
    except Exception as e:
        logger.exception("Prediction processing failed")
        return jsonify({
            "error": "Prediction Error",
            "message": "Could not process prediction request"
        }), 500

if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} v{API_VERSION}")
    if load_model():
        logger.info("Service starting on port 8000")
        app.run(host='0.0.0.0', port=8000)
    else:
        logger.critical("Service startup aborted due to model loading failure")