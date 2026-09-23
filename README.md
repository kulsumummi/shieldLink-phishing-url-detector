# 🛡️ ShieldLink – AI-Based Phishing URL Detector

> An intelligent, full-stack web application for real-time URL risk analysis, lexical feature extraction, and phishing detection using Machine Learning.

---

## 📌 Project Overview

**ShieldLink** is an end-to-end web application designed to help users determine whether a URL is **Safe**, **Suspicious**, or **Phishing**. 

The system extracts **9 lexical and structural features** from any submitted URL and processes them through a trained **RandomForest Classifier** combined with a rule-based heuristic engine. It calculates a granular **Risk Score (0–100%)**, provides a detailed breakdown report for transparency, and logs scan history with interactive dashboard analytics.

The application features a resilient dual-database layer supporting both **MySQL** and automatic **local SQLite fallback**, ensuring seamless out-of-the-box execution across development environments.

---

## 🔄 Core Workflow

```text
User Submits URL 
      ↓
Client-side Syntax Validation & Progress Spinner
      ↓
Extract 9 Lexical Features (Length, IP, Shortener, Keywords, Dots, Subdomains, etc.)
      ↓
RandomForest Classifier Model & Heuristic Overrides
      ↓
Calculate Risk Score (0-100%) & Assign Verdict (Safe / Suspicious / Phishing)
      ↓
Save Record to Database (SQLite / MySQL)
      ↓
Display Interactive Feature Breakdown & Analysis Report
      ↓
Update User Dashboard Analytics & Scan History Logs
```

---

## ✨ Features

### 🔐 User Authentication & Session Management
- Secure user registration and login system with password hashing (`werkzeug.security`).
- Flash notification alerts for validation errors, successful logins, and user sessions.
- Session authorization protecting all scanner, dashboard, and history endpoints.

### 🔍 Interactive URL Scanner & Feature Extractor
- Input field with client-side and server-side URL validation.
- Real-time extraction of 9 lexical URL indicators.
- Heuristic adjustments for high-risk attributes (e.g., raw IP domain usage, URL shorteners).

### 📊 Dashboard Analytics
- Dynamic statistics cards calculating:
  - Total Scans Performed
  - Safe Scans Count
  - Suspicious Scans Count
  - Phishing Scans Count
- Quick-action scan input directly from the dashboard view.

### 📋 Detailed Risk Reports
- Visual risk score bar (0–100%).
- Color-coded verdict badge:
  - 🟢 **Safe** (Risk Score < 35%)
  - 🟡 **Suspicious** (Risk Score 35% – 70%)
  - 🔴 **Phishing** (Risk Score > 70%)
- Itemized breakdown table explaining each extracted lexical feature in simple language.

### 📜 Scan History & Data Export
- Filterable history table with real-time search support (`q` search parameter).
- Individual scan deletion capability.
- Instant CSV export download for audit logs and spreadsheet integration.

### ⚡ Resilient Dual-Database Architecture
- Native MySQL support with raw parameterized queries.
- Automatic SQLite fallback (`shieldlink.db`) if MySQL connection fails or is unconfigured.

---

## 🛠️ Tech Stack

| Category | Technology / Library | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.13+, Flask | Modular Web Architecture & Blueprints |
| **Machine Learning** | Scikit-Learn, NumPy, Joblib | RandomForest Classifier (Synthetic Dataset) |
| **Database** | SQLite (Default Fallback) / MySQL | Dual-engine persistence layer |
| **Security** | Werkzeug (`generate_password_hash`) | Password hashing and salt verification |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) | Flexbox/Grid responsive UI with zero dependencies |
| **Data Export** | Python `csv`, `StringIO` | In-memory CSV file generation |

---

## 📂 Project Structure

```text
shieldLink-phishing-url-detector-main/
│
├── app.py                      # Flask Application Entry Point & Blueprint Registration
├── config.py                   # Configuration Settings (Secret Key, DB Credentials)
├── requirements.txt            # Python Dependency Manifest
├── README.md                   # Project Documentation
├── shieldlink.db               # SQLite Local Database File (Auto-generated on startup)
│
├── database/
│   ├── database.py             # Dual DB Helper (MySQL + SQLite Fallback Queries)
│   └── schema.sql              # MySQL Schema Definition Script
│
├── model/
│   ├── feature_extractor.py    # 9 Core Lexical Feature Extraction Functions
│   ├── train_model.py          # Synthetic Dataset Generator & Model Training Script
│   └── phishing_model.pkl       # Serialized RandomForest Classifier Model File
│
├── routes/
│   ├── auth.py                 # Registration, Login, Logout Endpoints
│   ├── dashboard.py            # User Analytics & Dashboard Controller
│   ├── scanner.py              # URL Scanning, Feature Extraction & Report Controller
│   └── history.py              # History View, Search, Delete & CSV Export Controller
│
├── templates/
│   ├── base.html               # Master Layout Template with Nav & Styling
│   ├── login.html              # User Sign In Page
│   ├── register.html           # User Account Creation Page
│   ├── dashboard.html          # User Analytics Overview
│   ├── scan.html               # URL Scanning Interface
│   ├── report.html             # Detailed Scan Analysis & Feature Breakdown Report
│   └── history.html            # Searchable Scan History Log
│
├── static/
│   ├── css/                    # Custom Stylesheets (style.css, auth.css, etc.)
│   └── js/                     # Client-side Interaction Scripts (scanner.js, etc.)
│
└── exports/                    # Output Directory for CSV Exports
```

---

## 🔬 Machine Learning & Lexical Features

ShieldLink evaluates target URLs using **9 core structural indicators**:

| # | Feature Name | Description | Phishing Indicator |
| :-: | :--- | :--- | :--- |
| **1** | **URL Length** | Total character count of URL string | Long URLs (>75 chars) often obscure true destinations |
| **2** | **HTTPS Protocol** | Presence of SSL/TLS encryption scheme | HTTP links lack transport layer encryption |
| **3** | **IP Address Domain** | Uses numeric IP instead of domain name | High correlation with malicious host redirects |
| **4** | **Dot Count** | Number of `.` characters in URL | Excessive dots indicate dot-stuffing attacks |
| **5** | **Subdomain Count** | Number of nested subdomains | Stacking subdomains mimics legitimate brands |
| **6** | **At-Symbol (`@`)** | Presence of `@` in URL string | Causes browser to ignore preceding credentials |
| **7** | **Hyphen in Domain** | Presence of `-` in hostname | Used to create lookalike / typosquatted domains |
| **8** | **URL Shortener** | Domain matches known shortener services | Conceals destination URL from initial user view |
| **9** | **Suspicious Keywords** | Count of keywords (`login`, `secure`, `bank`, etc.) | Used to deceive users during credential harvesting |

---

## ⚙️ Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python 3.8+** (Python 3.13 recommended)
- **pip** package manager
- *(Optional)* **MySQL Server** (Not required — SQLite will automatically handle storage if MySQL is inactive)

---

### Step-by-Step Installation

#### 1. Clone the Repository & Navigate to Directory
```bash
git clone https://github.com/your-username/shieldLink-phishing-url-detector.git
cd shieldLink-phishing-url-detector
```

#### 2. Create & Activate Virtual Environment *(Optional but Recommended)*
- **Windows**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Database *(Optional)*
By default, the application connects to local **SQLite** (`shieldlink.db`) with zero setup required.

If you wish to use **MySQL**:
1. Open MySQL and run `database/schema.sql`:
   ```sql
   SOURCE database/schema.sql;
   ```
2. Update `config.py` with your credentials:
   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'your_password'
   MYSQL_DB = 'shieldlink_db'
   ```

#### 5. Train / Regenerate Machine Learning Model
Train the RandomForest classifier on synthetic heuristic samples:
```bash
python model/train_model.py
```
*(This generates `model/phishing_model.pkl` in seconds.)*

#### 6. Run the Flask Web Application
```bash
python app.py
```

#### 7. Access the Application
Open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 🧪 Sample Scan Test Cases

| Target URL | Expected Verdict | Risk Score | Triggered Heuristics |
| :--- | :-: | :-: | :--- |
| `https://google.com/search?q=python` | 🟢 **Safe** | 5% – 15% | Valid HTTPS, Standard Domain, No suspicious tokens |
| `http://192.168.1.1/login` | 🔴 **Phishing** | 85% – 100% | Raw IP Host, HTTP Protocol, Keyword `login` |
| `http://bit.ly/xY7z` | 🟡 **Suspicious** | 45% – 65% | URL Shortener Domain, HTTP Protocol |
| `http://login.verification.paypal.com.update-account.tk/signin` | 🔴 **Phishing** | 90% – 100% | Dot-stuffing, Multiple Subdomains, Suspicious Keywords |

---

## 📸 Screenshots & UI Section

> *(You can add your project screenshots in `static/images/` and embed them below)*

| View | Preview / Description |
| :--- | :--- |
| **Authentication View** | Clean login and registration interface with client validation |
| **Dashboard Analytics** | Overview cards showing total scans, safe, suspicious, and phishing counts |
| **URL Scanner** | Input scanner interface with animated loading state |
| **Detailed Report** | Comprehensive 9-feature breakdown and color-coded risk meter |
| **History & Export** | Filterable history table with instant CSV spreadsheet download |

---

## 🔐 Safety & Security Notice

- **Educational & Portfolio Purpose**: ShieldLink is built as an academic engineering demonstration. The underlying machine learning model is trained on synthetic heuristic dataset samples.
- **Not for Standalone Production Security**: Do not use as a standalone primary firewall or enterprise security filter without integrating live WHOIS domain lookup, DNS blacklists, and active SSL certificate validation.

---

## 🗺️ Roadmap

### 🟢 Version 1.0 (Current Version)
- [x] Flask modular architecture with Blueprints
- [x] 9-Feature URL Lexical Extractor Engine
- [x] RandomForest Classifier integration via Joblib
- [x] Automatic SQLite fallback database layer
- [x] User auth with password hashing
- [x] Searchable history table & CSV export

### 🟡 Version 2.0 (Planned)
- [ ] Active SSL Certificate validation via socket connections
- [ ] Domain creation age calculation via WHOIS queries
- [ ] PhishTank / Google Safe Browsing API integration
- [ ] Browser extension for real-time link hover preview

### 🔵 Version 3.0 (Future Platform)
- [ ] REST API endpoints for external integrations
- [ ] OAuth2 Social Login (Google / GitHub)
- [ ] Deep Learning (LSTM / Transformer) model support for long URLs

---

## 🎯 Purpose & Learning Outcomes

This project was built to explore:
- Machine Learning Integration in Web Frameworks (scikit-learn + Flask).
- Feature Engineering on unstructured text strings (URLs).
- Building resilient database wrappers with automatic SQLite fallback.
- Designing responsive, lightweight web dashboards using pure HTML, CSS, and Vanilla JavaScript.

---

## 👨‍💻 Author

**ShieldLink Development Team**
- GitHub: [https://github.com/](https://github.com/)

---

## 📄 License

This project was developed for educational and portfolio purposes.
