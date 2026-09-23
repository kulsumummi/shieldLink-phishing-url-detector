import os
import sys
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Ensure model directory is in path to import feature_extractor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.feature_extractor import extract_url_features, SUSPICIOUS_KEYWORDS, URL_SHORTENERS

# -------------------------------------------------------------
# 1. Dataset Generation (Synthetic / Heuristic-Based)
# -------------------------------------------------------------

SAFE_DOMAINS = [
    'google.com', 'youtube.com', 'facebook.com', 'wikipedia.org', 'amazon.com',
    'yahoo.com', 'reddit.com', 'netflix.com', 'github.com', 'microsoft.com',
    'linkedin.com', 'twitter.com', 'instagram.com', 'apple.com', 'zoom.us',
    'medium.com', 'stackoverflow.com', 'nytimes.com', 'cnn.com', 'bbc.co.uk'
]

SAFE_PATHS = [
    '', '/', '/index.html', '/about', '/contact', '/help', '/search?q=python',
    '/docs/index.php', '/news/latest', '/blog/post-1', '/shop/category'
]

def generate_safe_url():
    """Generate a realistic safe URL."""
    domain = random.choice(SAFE_DOMAINS)
    path = random.choice(SAFE_PATHS)
    # Safe URLs usually use HTTPS, have reasonable lengths, and no suspicious keywords
    return f"https://{domain}{path}"

def generate_phishing_url():
    """Generate a realistic phishing URL mimicking common attacks."""
    attack_type = random.randint(1, 5)
    
    if attack_type == 1:
        # IP Address URL
        ip = f"{random.randint(10, 220)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        path = f"/{random.choice(SUSPICIOUS_KEYWORDS)}"
        return f"http://{ip}{path}"
        
    elif attack_type == 2:
        # Shortened URL
        shortener = random.choice(URL_SHORTENERS)
        return f"http://{shortener}/{random.choice(['xY7z', 'q1W3', 'lO9p', 'aBc4'])}"
        
    elif attack_type == 3:
        # Keyword-stuffing / Domain spoofing with hyphens
        kw1 = random.choice(SUSPICIOUS_KEYWORDS)
        kw2 = random.choice(SUSPICIOUS_KEYWORDS)
        while kw2 == kw1:
            kw2 = random.choice(SUSPICIOUS_KEYWORDS)
        domain = f"secure-{kw1}-{kw2}-verify.net"
        return f"http://{domain}/login.php"
        
    elif attack_type == 4:
        # Subdomain / Dot stuffing
        kw = random.choice(SUSPICIOUS_KEYWORDS)
        target = random.choice(['paypal', 'apple', 'netflix', 'google'])
        domain = f"login.verification.{kw}.{target}.com.update-account.tk"
        return f"http://{domain}/signin"
        
    else:
        # URL obfuscation using '@' symbol
        target_brand = random.choice(['paypal', 'facebook', 'chase'])
        phish_domain = "verify-billing-secure.com"
        return f"http://www.{target_brand}.com@{phish_domain}/login"

def create_dataset(size=1000):
    """Create a balanced dataset of safe and phishing URLs."""
    urls = []
    labels = []
    
    # 50% Safe URLs
    for _ in range(size // 2):
        urls.append(generate_safe_url())
        labels.append(0) # 0 = Safe
        
    # 50% Phishing URLs
    for _ in range(size // 2):
        urls.append(generate_phishing_url())
        labels.append(1) # 1 = Phishing
        
    # Convert to feature vectors
    features_list = []
    for url in urls:
        feat = extract_url_features(url)
        features_list.append(feat['ml_features'])
        
    return np.array(features_list), np.array(labels)

# -------------------------------------------------------------
# 2. Main Training Pipeline
# -------------------------------------------------------------

def main():
    print("=" * 60)
    print(" SHIELDLINK ML MODEL TRAINING")
    print("=" * 60)
    
    # Generate balanced dataset of 2,000 samples
    print("Generating balanced synthetic URL dataset (2,000 samples)...")
    X, y = create_dataset(size=2000)
    
    # Split into Train and Test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"Dataset split: Train={len(X_train)} samples, Test={len(X_test)} samples")
    
    # Initialize and train RandomForestClassifier
    print("Training RandomForestClassifier model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
        min_samples_split=5
    )
    model.fit(X_train, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test)
    
    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    # Save the trained model file
    model_path = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')
    print(f"Saving trained model to: {model_path}...")
    joblib.dump(model, model_path)
    
    print("\nTraining completed successfully! Model is ready for use.")
    print("=" * 60)

if __name__ == '__main__':
    main()
