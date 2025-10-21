from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import re
from typing import Dict, Any
import os

app = FastAPI(
    title="Spam Email Detection API",
    description="A simple API for detecting spam emails using Naive Bayes classifier",
    version="1.0.0"
)

model_data = None


class EmailRequest(BaseModel):
    """Request model for email classification"""
    message: str


class EmailResponse(BaseModel):
    """Response model for email classification"""
    message: str
    prediction: str
    confidence: float
    is_spam: bool
    cleaned_words: list
    word_count: int


def load_model():
    """Load the trained model from pickle file"""
    global model_data
    try:
        model_path = "models/spam_classifier_model.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def clean_text(text: str) -> list:
    """Clean and preprocess text"""
    if model_data is None:
        raise ValueError("Model not loaded")

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    stop_words = model_data['stop_words']
    words = [w for w in words if w not in stop_words and len(w) > 3]
    return words


def vectorize_message(message: list) -> np.ndarray:
    """Convert message to feature vector"""
    if model_data is None:
        raise ValueError("Model not loaded")

    vocab_array = model_data['vocabulary']
    word_to_idx = model_data['word_to_idx']

    vec = np.zeros(len(vocab_array), dtype=int)
    for word in message:
        if word in word_to_idx:
            vec[word_to_idx[word]] += 1
    return vec


def classify_email(vector: np.ndarray) -> tuple:
    """Classify email as spam or ham"""
    if model_data is None:
        raise ValueError("Model not loaded")

    p0_vector = model_data['p0_vector']
    p1_vector = model_data['p1_vector']
    p_spam = model_data['p_spam']

    # Calculate log probabilities
    p1 = np.sum(vector * np.log(p1_vector)) + np.log(p_spam)
    p0 = np.sum(vector * np.log(p0_vector)) + np.log(1.0 - p_spam)

    # Determine prediction
    is_spam = p1 > p0
    prediction = 1 if is_spam else 0

    # Calculate confidence (difference between probabilities)
    confidence = abs(p1 - p0)

    return prediction, confidence, is_spam


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    success = load_model()
    if not success:
        print("Warning: Failed to load model on startup")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Spam Email Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Classify an email message",
            "/health": "GET - Check API health status",
            "/model-info": "GET - Get model information"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model_data is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded
    }


@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "vocabulary_size": len(model_data['vocabulary']),
        "prior_spam_probability": float(model_data['p_spam']),
        "features": len(model_data['p0_vector']),
        "stopwords_count": len(model_data['stop_words'])
    }


@app.post("/predict", response_model=EmailResponse)
async def predict_spam(request: EmailRequest):
    """Predict if an email is spam or ham"""
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        cleaned_words = clean_text(request.message)

        vector = vectorize_message(cleaned_words)

        prediction, confidence, is_spam = classify_email(vector)

        response = EmailResponse(
            message=request.message,
            prediction="SPAM" if is_spam else "HAM",
            confidence=float(confidence),
            is_spam=is_spam,
            cleaned_words=cleaned_words,
            word_count=len(cleaned_words)
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
