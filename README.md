AGRITECH_TR Team Rules
1. काम सुरू करण्यापूर्वी
नेहमी:
git pull origin main
यामुळे नवीन code मिळेल.
________________________________________
2. काम झाल्यावर
git add .
git commit -m “काम काय केलं ते लिहा”
git push origin main
________________________________________
3. एकाच file वर एकाच वेळी काम करू नका
Harshal → index.html
Member 1 → style.css
Member 2 → script.js
________________________________________
4. Code delete करू नका
दुसऱ्याचा code विचारल्याशिवाय delete किंवा edit करू नका.
________________________________________
5. GitHub Password Share करू नका
Password, Token, Recovery Code कोणालाही देऊ नका.
________________________________________
6. Push करण्यापूर्वी
git pull origin main
करा.
________________________________________
7. Commit Message नीट लिहा
✓ Homepage completed
✓ Navbar added
✓ CSS updated
✓ Weather page added
✗ abc
✗ update
✗ test


tumch kam chalu hoya adhi he kakrych 
git pull origin main
________________________________________
tumch kam jahl ki he karych 
git add .
git commit -m "meaningful message"
git push origin main

========================================
AGRITECH TR - PROJECT DETAILS
========================================

## Project Overview

AgriTech TR is a smart agriculture platform designed for farmers in Maharashtra. It provides weather information, market prices, crop recommendations, profit estimation, crop-risk analysis, disease detection, agriculture news, and government scheme information.

## Technology Stack

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Chart.js for charts and data visualization
- Firebase Authentication
- Browser Geolocation API

The frontend is located in the `frontend/` directory. It is a multi-page web application and does not use React or another frontend framework.

### Backend

- Python
- FastAPI for REST APIs
- Uvicorn as the application server
- Pydantic for request and response validation
- SQLAlchemy for database access
- SQLite for local data storage
- Joblib for saving and loading trained ML models
- OpenCV and Pillow for image processing
- Firebase Admin SDK for authentication-token verification

The main backend service is in `backend/ml/main.py`. The repository also contains an older API entry point in `backend/app.py`.

### External Services

- OpenWeatherMap API for current weather and forecasts
- Agmarknet API for agricultural market prices
- News APIs for agriculture news
- Firebase Authentication for user login

## Algorithms and ML Models

### 1. Crop Recommendation

File: `backend/training/train_crop.py`

Algorithm: **Random Forest Classifier**

The model recommends a crop using:

- District
- Rainfall
- Temperature
- Farm area
- Market price

The district and crop names are converted to numeric values using `LabelEncoder`. The dataset is divided into 80% training data and 20% testing data. The model uses 150 decision trees and is saved as `crop_model.pkl`.

### 2. Profit Prediction

File: `backend/ml/profit_model.py`

Algorithm: **Random Forest Regressor**

The trained model predicts profit using:

- Crop
- District
- Rainfall
- Temperature
- Farm area
- Market price

It uses 100 decision trees, an 80/20 train-test split, and is saved using Joblib.

The project also contains a formula-based predictor in `backend/ml/profit_predictor.py`. This version estimates yield, revenue, costs, price fluctuation, and profit using crop data and weather factors.

### 3. Risk Prediction

File: `backend/ml/risk_predictor.py`

Risk prediction is currently a **rule-based weighted scoring system**, not a trained ML model. It considers:

- Rainfall risk: 25%
- Temperature risk: 20%
- Humidity risk: 15%
- Pest risk: 30%
- Market risk: 10%

The final score is classified as low, medium, or high risk. The system also generates recommendations such as pest monitoring, irrigation management, crop insurance, and consultation with an agriculture officer.

### 4. Crop Disease Detection

File: `backend/ml/disease_detector.py`

Disease detection currently uses **OpenCV computer vision and HSV color segmentation**. It is not a CNN or deep-learning model.

The process is:

1. Decode the uploaded Base64 image.
2. Resize it to 256 x 256 pixels.
3. Convert the image to HSV color space.
4. Compare pixels against predefined disease color ranges.
5. Estimate confidence and affected-pixel percentage.
6. Return the disease, severity, treatment, and recommendations.

Supported categories include leaf spot, rust, powdery mildew, blight, and healthy crop.

## Database and Security

SQLAlchemy models store weather data, market data, users, and prediction history in SQLite. Firebase Authentication manages user login, and protected backend endpoints can verify Firebase ID tokens.

## Important Backend Note

There are two backend entry points in the repository:

- `backend/ml/main.py`: newer version with `/api/v1/` routes
- `backend/app.py`: older version with routes such as `/api/predict`

The active prediction behavior depends on which entry point is used to start the server. Crop recommendation uses the trained Random Forest classifier, while some profit and risk endpoints use the formula-based or rule-based predictors.

## Short Project Description

AgriTech TR is a full-stack smart farming platform built with HTML, CSS, JavaScript, Python FastAPI, SQLAlchemy, and SQLite. It combines Random Forest machine-learning models, rule-based agricultural risk analysis, OpenCV image processing, real-time weather data, market prices, and Firebase authentication to support farming decisions.
