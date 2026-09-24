# 🛡️ ShieldLink – AI-Powered Phishing URL Detection System

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-onrender.com-2ea44f?style=for-the-badge&logo=render)](https://shieldlink-phishing-url-detector.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-1.5%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Deployment](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://shieldlink-phishing-url-detector.onrender.com)

> **ShieldLink** is an end-to-end web security application that performs real-time URL risk assessment using a hybrid machine learning classifier (Random Forest) and a custom 9-dimensional lexical feature extractor.

---

### 🌐 Live Production Application
🔗 **Experience the live app:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)

---

## 📌 Executive Summary & Key Engineering Highlights

Designed and developed as a complete full-stack cyber security showcase, **ShieldLink** solves the challenge of real-time malicious link detection without relying on slow external third-party API lookups. By extracting structural and lexical signatures directly from raw URL strings, the application evaluates link safety in under **50 milliseconds**.

### 🌟 Technical Highlights for Recruiters
- **Hybrid Inference Engine**: Integrates a **Random Forest Classifier** trained on synthetic heuristic dataset distributions with a deterministic rule engine to eliminate false negatives on high-risk vectors (e.g. raw IP hostnames and shorteners).
- **Custom Feature Engineering Engine**: Transforms raw URL strings into a 9-dimensional feature matrix evaluating token distributions, protocol status, dot-stuffing, subdomain depth, and suspicious target keywords.
- **Resilient Dual-Database Architecture**: Built with an automatic database failover system — seamlessly switching between enterprise **MySQL** and a zero-configuration local **SQLite** (`shieldlink.db`) backend.
- **Production-Grade Security**: Implements salted password hashing (`werkzeug.security`), strict session guards across endpoints, and parameterized SQL queries to prevent OWASP Top 10 vulnerabilities (SQLi, XSS, Session Hijacking).
- **Modern Clean Light UI**: Responsive, zero-framework, human-designed frontend built with vanilla HTML5, modern CSS flexbox/grid, and DOM JavaScript.
- **Production WSGI Deployment**: Deployed on Render using **Gunicorn** for multi-threaded concurrent request handling.

---

## 🔄 Technical Architecture & System Pipeline

```text
               +---------------------------------------------------+
               |               User Input (Target URL)             |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |    Lexical Feature Extractor Engine (9 Features)  |
               | (Length, IP Host, Shortener, Dots, Keywords, etc.)|
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |       Hybrid Machine Learning Pipeline            |
               |  - Random Forest Classifier (Class & Probability) |
               |  - Deterministic Rule Overrides (IP / Shorteners) |
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
               |     Data Persistence Layer (SQLite / MySQL)       |
               +---------------------------------------------------+
                                         |
                     +-------------------+-------------------+
                     |                                       |
                     v                                       v
      +-----------------------------+         +-----------------------------+
      |  Detailed Analysis Report   |         | Analytics Dashboard & Logs  |
      | (Breakdown Table & Visuals) |         | (CSV Export & History Search)|
      +-----------------------------+         +-----------------------------+
```

---

## 🔬 Machine Learning Feature Engineering Matrix

The feature extraction module (`model/feature_extractor.py`) parses target URLs into **9 distinct numerical indicators**:

| # | Feature Name | Extraction Logic | Cyber Threat Rationale |
| :-: | :--- | :--- | :--- |
| **1** | **URL Length** | Character length `len(url)` | Malicious links use excessive length (>75 chars) to mask destinations. |
| **2** | **HTTPS Protocol** | Binary check for `https://` scheme | Absence of SSL/TLS indicates unencrypted / untrusted transport. |
| **3** | **IP Hostname** | IPv4 / IPv6 validation via `ipaddress` | Phishers frequently host landers directly on raw IP addresses. |
| **4** | **Dot Count** | Count of `.` occurrences in string | High dot counts indicate dot-stuffing and complex directory masking. |
| **5** | **Subdomain Depth** | Hostname token split `len(parts) - 2` | Stacking nested subdomains mimics trusted target brands. |
| **6** | **At-Symbol (`@`)** | Binary check for `@` symbol | Browser RFC syntax uses `@` to discard preceding credentials. |
| **7** | **Hyphen in Host** | Domain string inspection for `-` | Typosquatting and domain spoofing routinely use hyphens. |
| **8** | **URL Shortener** | Domain comparison against known shortener registry | Shorteners conceal destination hostnames from user hover inspection. |
| **9** | **Suspicious Keywords** | Match count of target keywords (`login`, `secure`, `bank`, etc.) | High concentration of credential-harvesting tokens. |

---

## 🛠️ Full Technology Stack

| Domain | Technology / Library | Usage & Purpose |
| :--- | :--- | :--- |
| **Language** | **Python 3.13** | Primary backend and machine learning language |
| **Web Framework** | **Flask 3.0+** | Modular application architecture using Blueprints (`auth`, `dashboard`, `scanner`, `history`) |
| **Machine Learning** | **Scikit-Learn, NumPy, Joblib** | `RandomForestClassifier` pipeline and model serialization |
| **Production WSGI** | **Gunicorn, Waitress** | Enterprise-grade WSGI web server for cloud deployment |
| **Database Layer** | **SQLite3 / MySQL** | Dual-engine persistence layer with automatic failover query wrapper |
| **Security** | **Werkzeug Security** | Salted password hashing (`pbkdf2:sha256`) and session management |
| **Frontend UI** | **HTML5, CSS3, JavaScript** | Clean modern light-mode interface (Flexbox, CSS Grid, DOM Manipulation) |
| **Cloud Hosting** | **Render** | Automated CI/CD pipeline from GitHub repository |

---

## 📂 Modular Codebase Structure

```text
shieldLink-phishing-url-detector/
│
├── app.py                      # Flask Application Entry Point & Blueprint Registrar
├── config.py                   # Environment & Configuration Management
├── requirements.txt            # Python Dependency Specification
├── Procfile                    # Gunicorn Production WSGI Process File
├── render.yaml                 # One-click Render Cloud Deployment Blueprint
├── README.md                   # Project Documentation
├── shieldlink.db               # SQLite Local Database (Auto-instantiated on startup)
│
├── database/
│   ├── database.py             # Dual Database Driver (MySQL + SQLite Failover Engine)
│   └── schema.sql              # MySQL DDL Relational Schema Script
│
├── model/
│   ├── feature_extractor.py    # 9-Dimensional Lexical URL Parsing Engine
│   ├── train_model.py          # Dataset Synthesizer & Random Forest Trainer Script
│   └── phishing_model.pkl       # Serialized Random Forest Classifier Artifact
│
├── routes/
│   ├── auth.py                 # Registration, Login, Logout & Password Security Controller
│   ├── dashboard.py            # User Analytics & Metrics Controller
│   ├── scanner.py              # URL Submission, ML Inference & Risk Scoring Controller
│   └── history.py              # Scan Audit Log, Search Filter & CSV Export Controller
│
├── templates/                  # Jinja2 HTML Templates
│   ├── login.html              # Clean Authentication View
│   ├── register.html           # User Registration View
│   ├── dashboard.html          # Dynamic Analytics Dashboard
│   ├── scan.html               # URL Input & Analysis Scanner
│   ├── report.html             # Itemized Feature Breakdown Report
│   └── history.html            # Searchable Audit History Table
│
└── static/
    ├── css/                    # Clean Light Mode CSS Stylesheets (auth, dashboard, scanner, history)
    └── js/                     # Client-side Interactive DOM Scripts
```

---

## ✨ Features & User Capabilities

### 🔐 1. Authentication & Security
- User registration and login flow with salted password hashing.
- Route protection via session authorization middleware.
- Flash notification feedback for user interactions.

### 🔍 2. Real-Time URL Scanner
- Interactive URL submission form with syntax validation and loading indicators.
- Real-time feature extraction and machine learning classification.
- Color-coded verdict indicators:
  - 🟢 **Safe** (Risk Score < 35%)
  - 🟡 **Suspicious** (Risk Score 35% – 70%)
  - 🔴 **Phishing** (Risk Score > 70%)

### 📊 3. Executive Dashboard Analytics
- Dynamic statistics cards calculating:
  - Total Scans Performed
  - Total Safe URLs Detected
  - Total Suspicious Links Flagged
  - Total Phishing Threats Blocked

### 📜 4. Audit History & Data Export
- Filterable history table with real-time string search query filtering (`?q=...`).
- Individual scan deletion capability.
- Instant **CSV spreadsheet download** export for security audit logging.

---

## 🧪 Sample Evaluation Benchmark

| Target URL Input | Expected Verdict | Risk Score | Key Extracted Signatures |
| :--- | :-: | :-: | :--- |
| `https://google.com/search?q=python` | 🟢 **Safe** | **5% – 15%** | Valid HTTPS, Recognized Domain, No Suspicious Tokens |
| `http://192.168.1.1/login` | 🔴 **Phishing** | **85% – 100%** | Raw IP Host, HTTP Protocol, Keyword `login` |
| `http://bit.ly/xY7z` | 🟡 **Suspicious** | **45% – 65%** | Shortener Domain, HTTP Protocol |
| `http://login.verification.paypal.com.update-account.tk/signin` | 🔴 **Phishing** | **90% – 100%** | Dot-stuffing, 4 Subdomains, Multiple Phishing Keywords |

---

## ⚙️ Local Setup & Execution Guide

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

4. **Verify / Train Machine Learning Model:**
   ```bash
   python model/train_model.py
   ```

5. **Launch Flask Server:**
   ```bash
   python app.py
   ```

6. **Access Locally:**
   Open browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🌐 Cloud Deployment (Render)

ShieldLink is pre-configured for instant deployment on **Render**:

- **Build Command:** `pip install -r requirements.txt && python model/train_model.py`
- **Start Command:** `gunicorn app:app`
- **Live URL:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)

---

## 🔐 Security & Disclaimer

- **Portfolio & Academic Purpose**: Built as a computer science engineering portfolio project. The underlying Random Forest model is trained on representative synthetic heuristic distributions.
- **Production Integration**: For enterprise deployment, this service can be paired with active WHOIS domain age queries, Google Safe Browsing API checks, and DNS blacklists.

---

## 👨‍💻 Author & Contact

**Kulsum Ummi**  
*Computer Science & Engineering*  
- **GitHub**: [@kulsumummi](https://github.com/kulsumummi)  
- **Live Project**: [ShieldLink Application](https://shieldlink-phishing-url-detector.onrender.com)
