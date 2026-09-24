# 🛡️ ShieldLink – AI Phishing URL Detection System

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-onrender.com-2ea44f?style=for-the-badge&logo=render)](https://shieldlink-phishing-url-detector.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Deployment](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://shieldlink-phishing-url-detector.onrender.com)

> **ShieldLink** is a full-stack web application designed to detect malicious phishing URLs in real time. It analyzes target links using a **9-feature lexical extractor** and a **Machine Learning Random Forest model** to generate a Risk Score (0–100%) and a detailed safety report.

---

### 🌐 Try the Live Application
🔗 **Live URL:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)

---

## 💡 What is ShieldLink & What Problem Does It Solve?

Phishing attacks trick users into handing over passwords, credit cards, or personal data by using lookalike links. **ShieldLink** provides an instant security scanner where users can paste any link and immediately find out if it is **Safe**, **Suspicious**, or **Phishing**—before clicking on it.

Unlike heavy threat-intel lookup systems that rely on external API delays, ShieldLink analyzes the **structure and lexical properties of the URL itself** in real time (< 50 milliseconds).

---

## ⚡ How It Works (Core Workflow)

```text
 1. User submits URL on the Scanner page
                   ↓
 2. System extracts 9 structural URL features (Length, IP, Shorteners, Keywords, Subdomains)
                   ↓
 3. Trained Scikit-Learn Random Forest Classifier evaluates the feature vector
                   ↓
 4. Rule engine applies safety heuristics (Forces high risk on raw IP hosts & shorteners)
                   ↓
 5. System calculates a Risk Score (0-100%) and assigns a final Verdict:
    - 🟢 SAFE (Risk Score < 35%)
    - 🟡 SUSPICIOUS (Risk Score 35% - 70%)
    - 🔴 PHISHING (Risk Score > 70%)
                   ↓
 6. Results are saved to Database (SQLite / MySQL) & displayed on an Interactive Breakdown Report
```

---

## ✨ Key Features of the Application

### 1. 🔐 User Authentication & Session Security
- User registration and login system with salted password hashing (`werkzeug.security`).
- Flash messaging for error/success notifications.
- Session authorization protecting dashboard, scanner, report, and history routes.

### 2. 🔍 Interactive Real-Time URL Scanner
- Clean input form with client-side syntax checks and loading spinner.
- Instant risk analysis with color-coded verdict badges (Safe / Suspicious / Phishing).
- Heuristic safety overrides for high-risk vectors (e.g. raw IP hostnames, URL shorteners).

### 3. 📋 Detailed Breakdown Reports (Why Was It Flagged?)
- Itemized breakdown table explaining each of the 9 extracted features in simple language:
  - **URL Length** (Long URLs often mask true destinations)
  - **HTTPS Protocol** (Checks for SSL/TLS security)
  - **IP Address Host** (Flags numerical IP hostnames like `192.168.1.1`)
  - **Dot Count** (Detects dot-stuffing and directory obfuscation)
  - **Subdomain Depth** (Identifies stacked subdomains mimicking brands)
  - **At-Symbol (`@`)** (Checks for RFC syntax credential bypasses)
  - **Hyphen in Domain** (Detects typosquatting lookalike domains)
  - **URL Shortener** (Flags services like `bit.ly` or `tinyurl.com`)
  - **Suspicious Keywords** (Detects tokens like `login`, `bank`, `verify`, `account`)

### 4. 📊 Personal Analytics Dashboard
- Dynamic overview cards displaying:
  - **Total Scans Performed**
  - **Safe Links Found**
  - **Suspicious Links Flagged**
  - **Phishing Threats Blocked**

### 5. 📜 Scan History & CSV Data Export
- Filterable history table with real-time search support (`?q=query`).
- Individual scan deletion capability.
- One-click **CSV spreadsheet download** export for audit logs.

### 6. ⚡ Resilient Dual-Database Engine
- Built with automatic database failover: uses **MySQL** when configured, and automatically falls back to zero-config local **SQLite** (`shieldlink.db`) if MySQL is unavailable.

---

## 🔬 The 9 Extracted Lexical URL Features

| # | Feature | How It Is Checked | Why It Matters for Phishing |
| :-: | :--- | :--- | :--- |
| **1** | **URL Length** | Total character length | Phishers use long URLs (>75 chars) to hide malicious paths. |
| **2** | **HTTPS Protocol** | Presence of `https://` scheme | Lack of SSL encryption means data in transit is unsafe. |
| **3** | **IP Address Host** | Host is IPv4 / IPv6 address | Legitimate sites use domain names; raw IPs indicate quick attack setups. |
| **4** | **Dot Count** | Count of `.` characters | Excessive dots are used to disguise actual domain names. |
| **5** | **Subdomain Depth** | Number of nested subdomains | Stacking subdomains (e.g. `login.paypal.site.com`) tricks users. |
| **6** | **At-Symbol (`@`)** | Presence of `@` symbol | Browsers ignore everything before `@`, hiding the real domain. |
| **7** | **Hyphen in Host** | Domain contains `-` | Used to create lookalike domains (e.g. `secure-bank-login.com`). |
| **8** | **URL Shortener** | Domain matches shortener list | Conceals target destination from hover preview. |
| **9** | **Suspicious Keywords**| Matches tokens like `login`, `bank` | High concentration of credential-harvesting target words. |

---

## 🧪 Quick Test Cases for Recruiters / Reviewers

Try testing these sample URLs on the [Live App](https://shieldlink-phishing-url-detector.onrender.com):

| Target URL | Expected Verdict | Risk Score | Why It Gets Flagged |
| :--- | :-: | :-: | :--- |
| `https://google.com/search?q=python` | 🟢 **Safe** | **5% – 15%** | Standard domain, valid HTTPS, no suspicious keywords |
| `http://192.168.1.1/login` | 🔴 **Phishing** | **85% – 100%** | Uses raw IP address, HTTP protocol, keyword `login` |
| `http://bit.ly/xY7z` | 🟡 **Suspicious** | **45% – 65%** | URL shortener domain concealing real host |
| `http://login.verification.paypal.com.update-account.tk/signin` | 🔴 **Phishing** | **90% – 100%** | Dot-stuffing, multiple subdomains, suspicious keywords |

---

## 🛠️ Technology Stack

| Domain | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend Framework** | **Python 3.13, Flask** | Route controllers, Blueprints (`auth`, `dashboard`, `scanner`, `history`), sessions |
| **Machine Learning** | **Scikit-Learn, NumPy, Joblib** | `RandomForestClassifier` training, feature vectors, model file serialization |
| **Database** | **SQLite / MySQL** | Dual-driver database layer with automatic SQLite fallback |
| **Security** | **Werkzeug Security** | Salted password hashing (`pbkdf2:sha256`) and session security |
| **Frontend UI** | **HTML5, CSS3, JavaScript** | Clean modern light-mode interface (Flexbox, CSS Grid, DOM scripts) |
| **Production WSGI** | **Gunicorn** | Production web server for cloud deployment |
| **Cloud Hosting** | **Render** | Automatic deployment from GitHub repository |

---

## 📂 Project Structure

```text
shieldLink-phishing-url-detector/
│
├── app.py                      # Flask Application Entry Point & Route Registration
├── config.py                   # Configuration Settings (Secret Key, DB Credentials)
├── requirements.txt            # Python Dependencies
├── Procfile                    # Production Gunicorn Server Startup Command
├── render.yaml                 # Render Deployment Blueprint
├── README.md                   # Project Documentation
├── shieldlink.db               # SQLite Local Database (Created automatically)
│
├── database/
│   ├── database.py             # Database Helper (MySQL + SQLite Fallback Engine)
│   └── schema.sql              # MySQL Table Schema SQL Script
│
├── model/
│   ├── feature_extractor.py    # 9-Feature Lexical URL Parsing Engine
│   ├── train_model.py          # Synthetic Dataset Generator & Model Training Script
│   └── phishing_model.pkl       # Saved RandomForest Classifier Model
│
├── routes/
│   ├── auth.py                 # Login, Registration, Logout Endpoints
│   ├── dashboard.py            # Dashboard Analytics Controller
│   ├── scanner.py              # URL Scanning, Feature Extraction & Report Controller
│   └── history.py              # Scan History, Search Filter & CSV Export Controller
│
├── templates/                  # HTML Page Templates
│   ├── login.html              # Login Page
│   ├── register.html           # Registration Page
│   ├── dashboard.html          # Dashboard Statistics Page
│   ├── scan.html               # URL Scanner Input Page
│   ├── report.html             # Detailed Scan Breakdown Report
│   └── history.html            # Searchable History Table Page
│
└── static/
    ├── css/                    # Modern Light Theme Stylesheets
    └── js/                     # Client-side Interactive Scripts
```

---

## ⚙️ How to Run Locally

### 1. Clone & Navigate
```bash
git clone https://github.com/kulsumummi/shieldLink-phishing-url-detector.git
cd shieldLink-phishing-url-detector
```

### 2. Set Up Virtual Environment
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

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Model *(Optional - Pre-trained model included)*
```bash
python model/train_model.py
```

### 5. Run Flask Web Server
```bash
python app.py
```

Open your browser and visit: **`http://127.0.0.1:5000`**

---

## 👨‍💻 Author & Repository Info

**Ummi Kulsum**  
- **GitHub Repository:** [kulsumummi/shieldLink-phishing-url-detector](https://github.com/kulsumummi/shieldLink-phishing-url-detector)
- **Live Demo Link:** [https://shieldlink-phishing-url-detector.onrender.com](https://shieldlink-phishing-url-detector.onrender.com)
