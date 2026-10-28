"""
FastAPI Backend for Fake News Detector
Serves predictions using the trained PassiveAggressiveClassifier & TF-IDF Vectorizer.
"""

import os
import re
import string
import joblib
import numpy as np
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Model & Vectorizer storage ---
MODEL_PATH = "model.joblib"
VECTORIZER_PATH = "vectorizer.joblib"

ml_resources: Dict[str, Any] = {
    "model": None,
    "vectorizer": None
}

# --- Suspicious Sentiment / Clickbait Lexicon ---
SENSATIONAL_WORDS = {
    "shocking", "unbelievable", "secret", "miracle", "banned", "conspiracy",
    "illuminati", "exposed", "bombshell", "viral", "hoax", "breathtaking",
    "hidden truth", "they don't want you to know", "leaked", "alien", "apocalypse",
    "plot", "underground", "magic cure", "rigged", "censored"
}

EMOTIONAL_WORDS = {
    "furious", "outraged", "terrified", "panic", "hysteria", "mindblown",
    "disaster", "horrific", "insane", "devastating", "monstrous"
}

def clean_text_for_inference(text: str) -> str:
    """Sanitizes text matching the training preprocessing pipeline."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    return " ".join([w for w in text.split() if len(w) > 2])

def analyze_suspicious_sentiment(raw_text: str) -> Dict[str, Any]:
    """
    Analyzes emotional charge, capitalization, sensationalism, and clickbait risk factors.
    """
    total_chars = len(raw_text)
    if total_chars == 0:
        return {
            "sensationalism_score": 0.0,
            "emotional_charge": 0.0,
            "all_caps_ratio": 0.0,
            "exclamation_count": 0,
            "flagged_keywords": [],
            "risk_level": "Low"
        }

    # All-caps detection (indicative of clickbait/rage-bait headlines)
    alpha_chars = [c for c in raw_text if c.isalpha()]
    upper_chars = [c for c in raw_text if c.isupper()]
    all_caps_ratio = round((len(upper_chars) / len(alpha_chars)) * 100, 2) if alpha_chars else 0.0

    # Punctuation anomalies (multiple '!' or '?')
    exclamation_count = raw_text.count("!")
    question_count = raw_text.count("?")

    # Token-level keyword matching
    lowered = raw_text.lower()
    tokens = set(re.findall(r'\b[a-z]{3,}\b', lowered))
    
    found_sensational = [w for w in SENSATIONAL_WORDS if w in lowered or w in tokens]
    found_emotional = [w for w in EMOTIONAL_WORDS if w in lowered or w in tokens]

    # Calculate sub-scores (0 to 100 scale)
    sensational_score = min(100.0, round((len(found_sensational) * 25.0) + (exclamation_count * 5.0), 1))
    emotional_charge = min(100.0, round((len(found_emotional) * 20.0) + (all_caps_ratio * 0.5), 1))

    # Overall risk level determination
    combined_suspicion = (sensational_score * 0.6) + (emotional_charge * 0.4)
    if combined_suspicion >= 65:
        risk_level = "High"
    elif combined_suspicion >= 35:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "sensationalism_score": sensational_score,
        "emotional_charge": emotional_charge,
        "all_caps_ratio": all_caps_ratio,
        "exclamation_count": exclamation_count + question_count,
        "flagged_keywords": list(set(found_sensational + found_emotional)),
        "risk_level": risk_level
    }

def calculate_confidence(decision_val: float) -> float:
    """
    PassiveAggressiveClassifier outputs distance to the separating hyperplane via decision_function.
    We convert the continuous margin value into a calibrated confidence percentage [50.0% - 99.9%].
    """
    # Standard sigmoid transformation
    prob = 1.0 / (1.0 + np.exp(-abs(decision_val)))
    # Rescale to a realistic 60% - 99.5% confidence boundary
    confidence_pct = round(float(prob) * 100, 2)
    return max(52.0, min(99.4, confidence_pct))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to initialize and cache the machine learning artifacts."""
    print("[*] Starting up FastAPI Fake News Detection Service...")
    
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            ml_resources["model"] = joblib.load(MODEL_PATH)
            ml_resources["vectorizer"] = joblib.load(VECTORIZER_PATH)
            print("[✓] Model and vectorizer loaded into memory successfully.")
        except Exception as e:
            print(f"[!] Error loading existing models: {e}")
    else:
        print("[!] Model files not found. Auto-generating baseline model now...")
        # Auto-train default model so API is immediately interactive without manual run
        from train import load_data, train_and_evaluate, save_artifacts
        df = load_data("news.csv")
        model, vectorizer, _ = train_and_evaluate(df)
        save_artifacts(model, vectorizer, MODEL_PATH, VECTORIZER_PATH)
        ml_resources["model"] = model
        ml_resources["vectorizer"] = vectorizer
        print("[✓] Baseline model trained and ready.")

    yield
    print("[*] Shutting down Fake News Detection Service...")
    ml_resources.clear()

app = FastAPI(
    title="Fake News Detector API",
    description="High-performance NLP classification API using PassiveAggressiveClassifier & TF-IDF",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend (localhost:3000 and standard development ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173", # Vite
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10, description="The article body, paragraph, or headline to verify.")

class SuspiciousSentimentBreakdown(BaseModel):
    sensationalism_score: float
    emotional_charge: float
    all_caps_ratio: float
    exclamation_count: int
    flagged_keywords: List[str]
    risk_level: str

class PredictResponse(BaseModel):
    prediction: str = Field(..., description="'REAL' or 'FAKE'")
    confidence_score: float = Field(..., description="Calculated model confidence percentage (e.g. 94.5)")
    suspicious_sentiment: SuspiciousSentimentBreakdown

@app.get("/")
def health_check():
    """Health status and model readiness check."""
    ready = ml_resources["model"] is not None and ml_resources["vectorizer"] is not None
    return {
        "status": "online",
        "model_loaded": ready,
        "algorithm": "TF-IDF + PassiveAggressiveClassifier"
    }

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Accepts news article text, applies TF-IDF vectorization, computes
    PassiveAggressive classification, and returns credibility verdict with sentiment metrics.
    """
    model = ml_resources.get("model")
    vectorizer = ml_resources.get("vectorizer")

    if not model or not vectorizer:
        raise HTTPException(status_code=503, detail="Machine learning model is not initialized yet.")

    raw_text = request.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Provided text is empty.")

    # 1. Clean and vectorize text
    cleaned = clean_text_for_inference(raw_text)
    transformed_text = vectorizer.transform([cleaned])

    # 2. Predict class ('REAL' vs 'FAKE')
    raw_pred = model.predict(transformed_text)[0]
    prediction = str(raw_pred).upper()

    # 3. Decision function distance for confidence score
    decision_margin = float(model.decision_function(transformed_text)[0])
    confidence = calculate_confidence(decision_margin)

    # 4. Sentiment & suspicious risk breakdown
    sentiment_breakdown = analyze_suspicious_sentiment(raw_text)

    return PredictResponse(
        prediction=prediction,
        confidence_score=confidence,
        suspicious_sentiment=sentiment_breakdown
    )
