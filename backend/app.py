from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import logging

# Optional Firebase Admin for verifying ID tokens
FIREBASE_AVAILABLE = False
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth, credentials
    FIREBASE_AVAILABLE = True
    # Initialize app if not already initialized. Uses ADC or service account if provided.
    try:
        if not firebase_admin._apps:
            if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
            else:
                # Try to initialize with no args (uses ADC). If that fails, leave uninitialized.
                firebase_admin.initialize_app()
    except Exception as e:
        logging.warning(f"Firebase admin initialization skipped: {e}")
except Exception:
    FIREBASE_AVAILABLE = False

from database import Base, engine
from disease import router as disease_router
from schemes import router as schemes_router
from schema import (
    ProfitPredictionRequest,
    ProfitPredictionResponse,
    CropRecommendationRequest,
    CropRecommendationResponse
)

# =========================================================
# FastAPI App
# =========================================================
app = FastAPI(title="Maharashtra Agriculture API")

# =========================================================
# Create Database Tables
# =========================================================
Base.metadata.create_all(bind=engine)

# =========================================================
# CORS Configuration
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # development साठी
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- Authentication Helpers --------------------
def verify_firebase_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ", 1)[1]

    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=500,
            detail=("Firebase Admin SDK not available on server. Install `firebase-admin` and "
                    "provide service account credentials via GOOGLE_APPLICATION_CREDENTIALS or initialize the SDK."))

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")

# =========================================================
# Load Profit Prediction Model
# =========================================================
MODEL_PATH = "profit_model.pkl"

CROP_MODEL_PATH = "models/crop_model.pkl"
CROP_ENCODER_PATH = "models/crop_encoder.pkl"
DISTRICT_ENCODER_PATH = "models/district_encoder.pkl"

crop_model = None
crop_encoder = None
district_encoder = None

try:
    crop_model = joblib.load(CROP_MODEL_PATH)
    crop_encoder = joblib.load(CROP_ENCODER_PATH)
    district_encoder = joblib.load(DISTRICT_ENCODER_PATH)
    print("Crop Recommendation Model Loaded Successfully")
except Exception as e:
    print(f"Error loading crop recommendation model: {e}")

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("Profit model loaded successfully")
    except Exception as e:
        print(f"Error loading profit model: {e}")
else:
    print("profit_model.pkl not found")

# =========================================================
# Include Routers
# =========================================================
app.include_router(disease_router, prefix="/api/disease", tags=["Disease"])
app.include_router(schemes_router, prefix="/api/schemes", tags=["Schemes"])

# =========================================================
# Home Route
# =========================================================
@app.get("/")
def home():
    return {"message": "Agriculture ML API is running!"}

# =========================================================
# Profit Prediction Route
# =========================================================
@app.post("/api/predict", response_model=ProfitPredictionResponse)
def predict_profit(data: ProfitPredictionRequest, user=Depends(verify_firebase_token)):
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Profit model not loaded")

        prediction = model.predict([[
            data.crop,
            data.district,
            data.rainfall,
            data.temperature,
            data.area,
            data.market_price
        ]])

        return {"profit": float(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # =========================================================
# Crop Recommendation Route
# =========================================================
@app.post("/api/crop_recommendation", response_model=CropRecommendationResponse)
def crop_recommendation(data: CropRecommendationRequest, user=Depends(verify_firebase_token)):

    try:

        if crop_model is None:
            raise HTTPException(
                status_code=500,
                detail="Crop model not loaded"
            )

        district = district_encoder.transform(
            [data.district]
        )[0]

        prediction = crop_model.predict([[
            district,
            data.rainfall,
            data.temperature,
            data.area,
            data.market_price
        ]])

        crop = crop_encoder.inverse_transform(prediction)

        return {
            "recommended_crop": crop[0]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/api/profile")
def profile(user=Depends(verify_firebase_token)):
    # Returns basic token claims for the authenticated user
    return {"uid": user.get('uid'), "email": user.get('email'), "name": user.get('name')}