# 🛡️ ShieldLink – AI-Powered Phishing URL Detection System

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-onrender.com-2ea44f?style=for-the-badge&logo=render)](https://shieldlink-phishing-url-detector.onrender.com)
[![Domain](https://img.shields.io/badge/Domain-AI_%26_Machine_Learning-7F52FF?style=for-the-badge&logo=brain&logoColor=white)](https://shieldlink-phishing-url-detector.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-1.5%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Deployment](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://shieldlink-phishing-url-detector.onrender.com)

> **ShieldLink** is an applied **Artificial Intelligence & Machine Learning** web security application that performs real-time URL risk assessment using a hybrid machine learning classifier (Random Forest) and a custom 9-dimensional lexical feature engineering pipeline.

---

### 🌐 Live Production Application
🔗 **Experience the live app:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)

---

## 📌 Executive Summary & Key AI/ML Highlights

Designed and developed as an applied **Artificial Intelligence & Machine Learning** engineering capstone project, **ShieldLink** addresses the critical cybersecurity challenge of real-time malicious link detection without relying on latency-heavy third-party API lookups. 

By performing numerical feature extraction on raw URL strings and feeding them into an optimized Supervised Learning pipeline (`RandomForestClassifier`), the application delivers sub-**50 millisecond inference** with transparent feature breakdown reports.

### 🌟 AI & ML Technical Highlights for Recruiters
- **Supervised Machine Learning Pipeline**: Built using `scikit-learn` with a tuned `RandomForestClassifier` (`n_estimators=100`, `max_depth=8`), evaluated across classification metrics (Precision, Recall, F1-Score).
- **Domain-Specific Feature Engineering**: Custom NLP/lexical parser (`model/feature_extractor.py`) that converts unstructured URL strings into a 9-dimensional numerical feature vector.
- **Dataset Synthesis & Heuristic Design**: Synthetic dataset generator (`model/train_model.py`) creating balanced distributions of safe vs. phishing URL patterns (IP hosts, domain spoofing, dot-stuffing, shorteners).
- **Hybrid AI Inference Engine**: Merges ML model class probabilities (`predict_proba`) with deterministic safety heuristics to eliminate false negatives on extreme risk vectors.
- **Model Serialization & Production Serving**: Automated model training and artifact serialization (`phishing_model.pkl` via `joblib`), seamlessly integrated into a live web application backend.
- **Full-Stack AI Application Engineering**: Production deployment on Render using Gunicorn WSGI, Flask modular Blueprints, and a resilient dual-database layer (MySQL + local SQLite fallback).

---

## 🔄 AI Inference Architecture & System Pipeline

```text
               +---------------------------------------------------+
               |            Raw Input URL (Unstructured)           |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |      Lexical Feature Extractor Module             |
               | (9-Dimensional Numerical Feature Matrix Engine)   |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |        Supervised ML Classifier Engine            |
               |  - Scikit-Learn RandomForestClassifier Inference  |
               |  - Probability Estimation via predict_proba()     |
               |  - Deterministic Safety Rule Overrides            |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |     Risk Score Engine & Verdict Classification    |
               |        (Safe < 35% | Suspicious | Phishing > 70%) |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |      Data Persistence (SQLite / MySQL Driver)     |
               +---------------------------------------------------+
                                         |
                     +-------------------+-------------------+
                     |                                       |
                     v                                       v
      +-----------------------------+         +-----------------------------+
      |  Itemized Feature Breakdown |         | Analytics Dashboard & Logs  |
      | (XAI & Transparency Report) |         | (CSV Export & History Search)|
      +-----------------------------+         +-----------------------------+
```

---

## 🔬 Machine Learning Feature Engineering Matrix

The feature extraction module (`model/feature_extractor.py`) parses raw URLs into **9 numerical ML features**:

| # | Feature Name | Representation / Math | AI Security Rationale |
| :-: | :--- | :--- | :--- |
| **1** | **URL Length** | $L = \text{len}(\text{url})$ | Malicious links exhibit high character length ($L > 75$) to conceal destinations. |
| **2** | **HTTPS Protocol** | $x_2 \in \{0, 1\}$ | Binary indicator of SSL/TLS transport encryption scheme. |
| **3** | **IP Hostname** | $x_3 \in \{0, 1\}$ | Binary indicator of IPv4/IPv6 host address vs registered domain name. |
| **4** | **Dot Count** | $x_4 = \text{count}(`.`)$ | High dot frequency correlates with directory masking and sub-domain abuse. |
| **5** | **Subdomain Depth** | $d = \max(0, \text{len}(\text{parts}) - 2)$ | Deep subdomain hierarchy is used to spoof brand authority. |
| **6** | **At-Symbol (`@`)** | $x_6 \in \{0, 1\}$ | RFC syntax feature where `@` discards prior user credentials. |
| **7** | **Hyphen in Domain** | $x_7 \in \{0, 1\}$ | Binary marker for typosquatting / lookalike domain hyphenation. |
| **8** | **URL Shortener** | $x_8 \in \{0, 1\}$ | Lookup against URL shortener registry concealing destination host. |
| **9** | **Suspicious Keywords** | $k = \sum \mathbb{I}(\text{keyword} \in \text{URL})$ | Count matching high-risk target tokens (`login`, `secure`, `bank`, etc.). |

---

## 🛠️ Full Technology Stack

| Domain | Technology / Library | Usage & AI/ML Purpose |
| :--- | :--- | :--- |
| **Primary Language** | **Python 3.13** | Core language for AI/ML modeling and web framework |
| **Machine Learning** | **Scikit-Learn, NumPy, Joblib** | `RandomForestClassifier`, matrix ops, model serialization |
| **Web Framework** | **Flask 3.0+** | RESTful/Modular backend integration for live ML inference |
| **Production Server** | **Gunicorn, Waitress** | Production WSGI server for serving AI model endpoints |
| **Database Layer** | **SQLite3 / MySQL** | Dual-engine persistence layer with automatic failover wrapper |
| **Security & Auth** | **Werkzeug Security** | Salted password hashing (`pbkdf2:sha256`) and session security |
| **Frontend UI** | **HTML5, CSS3, JavaScript** | Modern light-mode interface for visualizing ML predictions & reports |
| **Cloud Deployment** | **Render** | Cloud hosting platform with automated build and deployment |

---

## 📂 Codebase Structure & ML Artifacts

```text
shieldLink-phishing-url-detector/
│
├── app.py                      # Flask Application Entry Point & Web Server Controller
├── config.py                   # Environment & Configuration Management
├── requirements.txt            # Python Dependency Manifest
├── Procfile                    # Production Gunicorn WSGI Server Command
├── render.yaml                 # One-click Render Cloud Deployment Blueprint
├── README.md                   # Project Documentation
├── shieldlink.db               # Local SQLite Database (Auto-created on startup)
│
├── model/
│   ├── feature_extractor.py    # 9-Dimensional Feature Engineering Module
│   ├── train_model.py          # Synthetic Data Generator & ML Training Pipeline
│   └── phishing_model.pkl       # Serialized Random Forest Classifier Artifact
│
├── database/
│   ├── database.py             # Dual DB Helper (MySQL + SQLite Failover Engine)
│   └── schema.sql              # MySQL Database Schema DDL
│
├── routes/
│   ├── auth.py                 # User Authentication & Security Endpoints
│   ├── dashboard.py            # Analytics Metrics Controller
│   ├── scanner.py              # ML Model Inference & Risk Scoring Controller
│   └── history.py              # Scan History, Search Filter & CSV Export Controller
│
├── templates/                  # Jinja2 Frontend Templates
│   ├── login.html              # Login Interface
│   ├── register.html           # User Registration Interface
│   ├── dashboard.html          # Dynamic Analytics Dashboard
│   ├── scan.html               # Interactive URL Scanner View
│   ├── report.html             # Explainable AI (XAI) Feature Report
│   └── history.html            # Searchable Scan History Table
│
└── static/
    ├── css/                    # Modern Light Mode CSS Stylesheets
    └── js/                     # Client-Side Interactions & Loader Scripts
```

---

## 🧪 Model Evaluation & Test Benchmarks

| Test URL Input | Classification Verdict | Risk Score | Extracted Feature Signature |
| :--- | :-: | :-: | :--- |
| `https://google.com/search?q=python` | 🟢 **Safe** | **5% – 15%** | Valid HTTPS, Standard Domain, Zero Risk Tokens |
| `http://192.168.1.1/login` | 🔴 **Phishing** | **85% – 100%** | Raw IP Host, HTTP Scheme, Keyword `login` |
| `http://bit.ly/xY7z` | 🟡 **Suspicious** | **45% – 65%** | Shortener Registry Domain, HTTP Scheme |
| `http://login.verification.paypal.com.update-account.tk/signin` | 🔴 **Phishing** | **90% – 100%** | Dot-stuffing, 4 Subdomains, Multiple Phishing Tokens |

---

## ⚙️ Local Setup & Model Training Guide

### Prerequisites
- **Python 3.8+** (Python 3.13 recommended)
- **Git**

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kulsumummi/shieldLink-phishing-url-detector.git
   cd shieldLink-phishing-url-detector
   ```

2. **Create & Activate Virtual Environment:**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train Machine Learning Model:**
   Generate synthetic URL dataset and train/serialize `phishing_model.pkl`:
   ```bash
   python model/train_model.py
   ```

5. **Launch Application:**
   ```bash
   python app.py
   ```

6. **Access Locally:**
   Open browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🌐 Cloud Deployment

The repository includes pre-configured deployment blueprints for **Render**:

- **Build Command:** `pip install -r requirements.txt && python model/train_model.py`
- **Start Command:** `gunicorn app:app`
- **Live URL:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)

---

## 🔐 Disclaimer & Future Extensions

- **Academic & AI Portfolio Project**: Built to demonstrate practical application of Supervised Learning, Feature Engineering, and ML Model Serving.
- **Future AI Extensions**: Integration of Deep Learning models (LSTM / Transformer-based sequence classifiers for raw URL character embeddings) and WHOIS domain age features.

---

## 👨‍💻 Author & Contact

**Kulsum Ummi**  
*Artificial Intelligence & Machine Learning (AI & ML) Engineering*  
- **GitHub**: [@kulsumummi](https://github.com/kulsumummi)  
- **Live Project**: [ShieldLink Live AI Application](https://shieldlink-phishing-url-detector.onrender.com)
