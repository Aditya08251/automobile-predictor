# ML Predictor - Machine Learning Web Application

A modern, user-friendly web application for machine learning predictions using Iris flower classification. This project demonstrates the integration of a responsive frontend with a powerful machine learning backend.

![ML Predictor](https://img.shields.io/badge/Flask-Backend-black?style=flat-square&logo=flask)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-blue?style=flat-square)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=flat-square)

## 🎯 Features

- **Modern, Responsive UI**: Beautiful design that works on desktop, tablet, and mobile devices
- **Real-time Predictions**: Instant iris flower species classification
- **Confidence Scoring**: Get confidence levels for each prediction
- **Interactive Interface**: Smooth animations and user-friendly forms
- **RESTful API**: Well-documented backend API endpoints
- **Machine Learning Model**: Trained Random Forest classifier for high accuracy

## 📁 Project Structure

```
ml_web_app/
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── css/
│   │   └── styles.css      # Modern, responsive styling
│   └── js/
│       └── script.js       # Frontend logic and API communication
├── backend/
│   ├── app.py              # Flask application and API routes
│   ├── ml_model.py         # Machine learning model and classifier
│   └── requirements.txt     # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Setup

#### 1. Clone or Download the Project

```bash
cd ml_web_app
```

#### 2. Set Up the Backend

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Train the Model (First Time Only)

The ML model will automatically train on first run, but you can manually train it:

```bash
python ml_model.py
```

This will:
- Load the Iris dataset
- Train a Random Forest classifier
- Save the model and scaler to disk
- Display training and testing accuracy

#### 4. Start the Backend Server

```bash
python app.py
```

You should see output like:
```
============================================================
🚀 ML Predictor Backend Server Starting...
============================================================
⏰ Time: 2026-03-12 10:30:45
📊 Model Status: ✅ Loaded
🌐 Server: http://localhost:5000
📡 CORS: Enabled for all origins
============================================================

Available Endpoints:
  GET  /                    - Health check
  GET  /health              - Detailed health info
  GET  /model/info          - Model information
  POST /predict             - Make a prediction
  POST /batch-predict       - Make multiple predictions
```

#### 5. Open the Frontend

Simply open `frontend/index.html` in your web browser:

**Option 1**: Double-click the file
```bash
frontend/index.html
```

**Option 2**: Open in browser manually
```bash
# Use a simple HTTP server to serve the files
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 📱 Using the Application

### Making a Prediction

1. **Enter Flower Measurements**:
   - Sepal Length (cm): 4.0 - 7.9
   - Sepal Width (cm): 2.0 - 4.4
   - Petal Length (cm): 1.0 - 6.9
   - Petal Width (cm): 0.1 - 2.5

2. **Click "Predict Species"** button

3. **View Results**:
   - Species name with appropriate emoji
   - Confidence score (0-100%)
   - Detailed information about the species

### Example Measurements

**Iris Setosa**:
```
Sepal Length: 5.1 cm
Sepal Width: 3.5 cm
Petal Length: 1.4 cm
Petal Width: 0.2 cm
```

**Iris Versicolor**:
```
Sepal Length: 5.9 cm
Sepal Width: 3.0 cm
Petal Length: 4.2 cm
Petal Width: 1.5 cm
```

**Iris Virginica**:
```
Sepal Length: 6.3 cm
Sepal Width: 3.3 cm
Petal Length: 6.0 cm
Petal Width: 2.5 cm
```

## 🔌 API Endpoints

### 1. Health Check
```http
GET /
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "message": "ML Predictor API is running",
  "timestamp": "2026-03-12T10:30:45.123456",
  "service": "Iris Flower Classifier API"
}
```

### 2. Model Information
```http
GET /model/info
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "model_type": "Random Forest Classifier",
    "n_estimators": 100,
    "max_depth": 10,
    "classes": ["Setosa", "Versicolor", "Virginica"],
    "feature_names": ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
  }
}
```

### 3. Single Prediction
```http
POST /predict
Content-Type: application/json

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response**:
```json
{
  "status": "success",
  "prediction": "Setosa",
  "confidence": 0.98,
  "probabilities": {
    "Setosa": 0.98,
    "Versicolor": 0.02,
    "Virginica": 0.0
  },
  "input": {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  },
  "timestamp": "2026-03-12T10:30:45.123456"
}
```

### 4. Batch Predictions
```http
POST /batch-predict
Content-Type: application/json

{
  "predictions": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 5.9,
      "sepal_width": 3.0,
      "petal_length": 4.2,
      "petal_width": 1.5
    }
  ]
}
```

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations, and flexbox/grid
- **JavaScript (ES6+)**: Dynamic interactions and API calls
- **Fetch API**: Async HTTP requests to backend

### Backend
- **Flask 2.3.3**: Python web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Scikit-learn 1.3.1**: Machine learning library
- **NumPy**: Numerical computing
- **Joblib**: Model serialization

## 📊 Machine Learning Model

### Model Details
- **Algorithm**: Random Forest Classifier
- **Trees**: 100 decision trees
- **Max Depth**: 10 levels
- **Training Data**: Iris Dataset (150 samples)
- **Test Accuracy**: ~97%

### Input Features
1. Sepal Length (cm)
2. Sepal Width (cm)
3. Petal Length (cm)
4. Petal Width (cm)

### Output Classes
1. **Iris Setosa** 🌸 - Smallest species, coastal areas
2. **Iris Versicolor** 🌺 - Medium-sized, wetland habitats
3. **Iris Virginica** 🌼 - Largest species, southeastern US

## 🐛 Troubleshooting

### Issue: "Backend server is not running"
**Solution**: Make sure to start the Flask server in the backend folder:
```bash
cd backend
python app.py
```

### Issue: CORS errors in console
**Solution**: Ensure Flask-CORS is installed:
```bash
pip install Flask-CORS
```

### Issue: "Module not found" errors
**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 is already in use
**Solution**: Either stop the process using port 5000, or modify the port in `app.py`:
```python
app.run(host='localhost', port=5001)  # Change to 5001
```
Then update the frontend API URL in `frontend/js/script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001';
```

### Issue: Model training fails
**Solution**: Make sure you have internet connection (to download the Iris dataset) and enough disk space.

## 📈 Performance Metrics

- **Model Accuracy**: 97%
- **Average Prediction Time**: <100ms
- **Page Load Time**: <1 second
- **API Response Time**: <200ms

## 🔒 Security Notes

- Input validation on both frontend and backend
- CORS is enabled for development (restrict in production)
- No sensitive data stored locally
- Model inputs are validated for reasonable ranges

## 📚 Learning Concepts

This project demonstrates:
- Frontend-Backend architecture
- RESTful API design
- Machine learning model deployment
- CORS and client-server communication
- Responsive web design
- Form validation and error handling
- JSON data exchange
- HTML5 semantic elements
- CSS Grid and Flexbox layouts
- ES6+ JavaScript features

## 🚀 Future Enhancements

- [ ] Docker containerization
- [ ] Authentication and user accounts
- [ ] Prediction history and analytics
- [ ] Multiple ML models support
- [ ] Data visualization (charts, graphs)
- [ ] Model performance monitoring
- [ ] Advanced ML models (SVM, Neural Networks)
- [ ] Mobile app version
- [ ] Model explainability (SHAP values)
- [ ] Database integration

## 📝 License

This project is open source and available for educational and commercial use.

## 👥 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

## 📧 Support

For issues, questions, or suggestions, please refer to the GitHub repository or contact the development team.

---

**Happy Predicting! 🎉**

Built with ❤️ using Flask, Scikit-learn, and Modern Web Technologies
