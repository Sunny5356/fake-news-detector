"""
Fake News Classifier Training Script
Uses TF-IDF Vectorization and PassiveAggressiveClassifier to detect fake news.
"""

import os
import re
import string
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Basic English stopwords list to avoid mandatory external NLTK downloads
STOPWORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves"
])

def clean_text(text: str) -> str:
    """
    Cleans raw input text:
    - Converts to lowercase
    - Removes URLs and special HTML markers
    - Strips punctuation and digits
    - Filters common English stopwords
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove web links
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags if present
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers/digits
    text = re.sub(r'\d+', '', text)
    
    # Tokenize, strip, and remove stopwords
    tokens = text.split()
    cleaned_tokens = [w for w in tokens if w not in STOPWORDS and len(w) > 2]
    
    return " ".join(cleaned_tokens)

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads dataset from CSV file.
    Expects columns: 'text' and 'label' (or standard datasets like 'FAKE'/'REAL' or 0/1).
    Generates synthetic sample dataset if file is not found.
    """
    if os.path.exists(filepath):
        print(f"[*] Loading dataset from {filepath}...")
        df = pd.read_csv(filepath)
    else:
        print(f"[!] '{filepath}' not found. Generating sample synthetic dataset for instant testing...")
        sample_data = {
            "text": [
                "NASA confirms new planetary rover discovers signs of ancient microbial life in subterranean Mars cave.",
                "Government plans secret alien treaty to replace human workforce with synthetic cyborg clones by next week!",
                "Federal Reserve announces interest rate stabilization following comprehensive quarterly economic analysis.",
                "Miracle diet pill burns 40 pounds overnight with zero exercise, doctors completely stunned by secret herb!",
                "Clinical trial demonstrates 89% efficacy in cutting-edge immunotherapy treatment for melanoma patients.",
                "Breaking: Secret underground bunker found under Capitol hill holding secret lizard society members.",
                "Department of Energy grants $500 million to university research teams developing next-gen solid-state batteries.",
                "SHOCKING: Global elite secretly spraying memory-wiping chemtrails from commercial passenger aircraft!",
                "Stock market indices reach record highs driven by strong technology sector earnings and export volume.",
                "Unbelievable leaked documents prove earth is flat and surrounded by gigantic 300ft military ice wall!"
            ],
            "label": [
                "REAL", "FAKE", "REAL", "FAKE", "REAL", 
                "FAKE", "REAL", "FAKE", "REAL", "FAKE"
            ]
        }
        df = pd.DataFrame(sample_data)

    # Standardize column names
    df.columns = [c.lower().strip() for c in df.columns]
    
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns.")
        
    # Drop empty rows
    df = df.dropna(subset=["text", "label"])
    
    # Normalize labels to uppercase strings ('REAL', 'FAKE')
    df["label"] = df["label"].astype(str).str.strip().str.upper()
    df["label"] = df["label"].replace({"1": "REAL", "0": "FAKE", "TRUE": "REAL", "FALSE": "FAKE"})
    
    return df

def train_and_evaluate(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Preprocesses text, vectorizes with TF-IDF, trains PassiveAggressiveClassifier,
    and returns trained model, vectorizer, and accuracy score.
    """
    print("[*] Preprocessing text corpus...")
    df["cleaned_text"] = df["text"].apply(clean_text)
    
    X = df["cleaned_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"[*] Training on {len(X_train)} samples, testing on {len(X_test)} samples...")

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.7,
        ngram_range=(1, 2),
        max_features=50000
    )

    # Fit and transform
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # PassiveAggressiveClassifier is well-suited for high-dimensional, online text streams
    model = PassiveAggressiveClassifier(max_iter=100, random_state=random_state, C=0.5)
    model.fit(X_train_tfidf, y_train)

    # Predictions & metrics
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print("\n" + "=" * 50)
    print(f" Model Accuracy: {accuracy * 100:.2f}%")
    print("=" * 50)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    return model, vectorizer, accuracy

def save_artifacts(model, vectorizer, model_path: str = "model.joblib", vectorizer_path: str = "vectorizer.joblib"):
    """
    Saves trained classifier and TF-IDF vectorizer to disk using joblib.
    """
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"\n[+] Saved model to '{model_path}'")
    print(f"[+] Saved vectorizer to '{vectorizer_path}'")

def main():
    dataset_file = "news.csv"
    df = load_data(dataset_file)
    model, vectorizer, _ = train_and_evaluate(df)
    save_artifacts(model, vectorizer)
    print("\n[✓] Training pipeline finished successfully.")

if __name__ == "__main__":
    main()
