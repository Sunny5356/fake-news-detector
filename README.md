# Antigravity Fake News Credibility Engine

A full-stack, machine learning fake news detection platform built with **scikit-learn**, **FastAPI**, and **React (Tailwind CSS + Lucide Icons)**.

---

## 📁 Project Structure

```
fake-news-detector/
├── train.py                # Step 1: Scikit-learn + Pandas ML training pipeline
├── main.py                 # Step 2: FastAPI backend with CORS & sentiment analysis
├── FakeNewsDetector.jsx    # Step 3: Antigravity-themed React component
├── requirements.txt        # Backend dependencies
└── README.md
```

---

## 🚀 Step 1: Model Training (`train.py`)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python train.py
```
- If you have your own dataset, save it as `news.csv` in this folder with columns `text` and `label` (labels can be `REAL`/`FAKE` or `1`/`0`).
- If no CSV file is found, `train.py` automatically generates a synthetic test dataset to produce working `model.joblib` and `vectorizer.joblib` binaries.

---

## ⚡ Step 2: FastAPI Backend (`main.py`)

Run the backend server on port `8000`:
```bash
uvicorn main:app --reload --port 8000
```

### Endpoints:
- `GET /`: Health check and model readiness status.
- `POST /predict`:
  ```json
  {
    "text": "SHOCKING BOMBSHELL: Alien secret treaty leaked by officials!"
  }
  ```
  **Response:**
  ```json
  {
    "prediction": "FAKE",
    "confidence_score": 93.4,
    "suspicious_sentiment": {
      "sensationalism_score": 75.0,
      "emotional_charge": 52.0,
      "all_caps_ratio": 24.3,
      "exclamation_count": 1,
      "flagged_keywords": ["shocking", "secret", "bombshell", "leaked"],
      "risk_level": "High"
    }
  }
  ```

---

## 🌌 Step 3: React Frontend (`FakeNewsDetector.jsx`)

1. Ensure your React application has Tailwind CSS and Lucide icons installed:
```bash
npm install lucide-react
```
2. Import `FakeNewsDetector` in your React app:
```jsx
import FakeNewsDetector from './FakeNewsDetector';

function App() {
  return <FakeNewsDetector />;
}

export default App;
```
3. Run your React frontend (`npm start` or `npm run dev`) at `http://localhost:3000`.
