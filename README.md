# 🛡️ ApexGuard — Autonomous Transaction Anomaly & AML Defense Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.7+-EB4034.svg)](https://xgboost.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Deployed](https://img.shields.io/badge/Production-Live%20on%20Render-brightgreen)](https://apexguard-api.onrender.com)

**Enterprise-grade real-time financial transaction anomaly detection, anti–money laundering (AML) surveillance, and regulatory compliance platform.** Combines supervised gradient boosting, unsupervised anomaly isolation, deterministic FATF sentinel matrices, and Explainable AI (SHAP) into an integrated Tri-Engine decision system.

---

### 🌐 Live Production Deployment
* **Live Web App**: [https://apexguard-api.onrender.com](https://apexguard-api.onrender.com)
* **Status**: 100% Uptime (Monitored via UptimeRobot keep-alive on `/health`)
* **Default Analyst Credentials**: `analyst` / `Analyst@123`
* **Default Admin Credentials**: `admin` / `Admin@123`

---

### 🎓 Academic & Research Profile
* **Project Lead / Researcher**: **Zaheer Ahmed** (Roll No: **22SW077**)
* **Degree**: Bachelor of Engineering in Software Engineering (Batch 22SW)
* **Institution**: Mehran University of Engineering and Technology (MUET), Jamshoro
* **Year**: 2026

---

## 📌 Executive Overview & Core Innovation

Traditional banking Anti-Money Laundering (AML) systems suffer from a **95% to 98% false positive rate**, flooding analysts with benign noise. Conversely, pure black-box machine learning models are legally prohibited from autonomous deployment by international central banks because they cannot provide auditable explanations for seized funds or denied transactions.

**ApexGuard** resolves both limitations through a **Tri-Engine Composite Decision Matrix**:

```
[ Incoming Transaction Payload ]
               │
               ▼
   [ Fast Ingestion & Validation ] (FastAPI / Pydantic)
               │
               ▼
  [ 16-Dimensional Feature Vector ]
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
[ Engine 1 ] [ Engine 2 ] [ Engine 3 ]
  XGBoost     Isolation    FATF Rule
 Supervised    Forest      Sentinel
 Score (60%)  Score (10%) Score (30%)
      └────────┼────────┘
               │
               ▼
[ Composite Risk Fusion Engine ]
Score = (0.60 * S_ML) + (0.30 * S_RULE) + (0.10 * S_ISO)
               │
               ▼
[ Multi-Tier Risk Triage & Actions ]
├── NORMAL   (< 0.20): Auto-cleared for real-time settlement
├── LOW      (0.20 - 0.39): Cleared with passive logging
├── MEDIUM   (0.40 - 0.69): Queued for analyst manual triage
└── CRITICAL (>= 0.70 or ML >= 0.80): Outbound hold + Form SAR-01 draft
```

---

## 📊 Empirical Benchmarks (50,000 Transactions)

Evaluated on a 50,000-transaction financial stream with realistic class imbalance:

| Evaluation Metric | Legacy Rule Engine Alone | Supervised XGBoost Alone | Unsupervised Isolation Forest Alone | ApexGuard Hybrid Tri-Engine |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | 99.14% | 99.99% | 94.75% | **94.93%** |
| **Precision** | 16.02% | **100.00%** | 0.16% | **3.69%** (triage filter) |
| **Recall (Sensitivity)** | 78.00% | 96.00% | 4.00% | **97.00% (Highest Interception)** |
| **ROC-AUC Score** | 0.8859 | 0.9939 | 0.5012 | **0.9980 (Near-Perfect Curve)** |
| **True Positives (TP)** | 78 / 100 | 96 / 100 | 4 / 100 | **97 / 100 (Only 3 missed!)** |
| **False Negatives (FN)** | 22 missed | 4 missed | 96 missed | **Only 3 missed!** |
| **Inference Latency** | **< 1.0 ms** | **~2.2 ms** | **~1.5 ms** | **3.8 ms (Inline Real-Time)** |

> **Why 97% Recall Matters**: In Anti-Money Laundering compliance, missing an illicit transfer (False Negative) triggers regulatory fines and criminal facilitation. ApexGuard deliberately prioritizes high recall while managing borderline cases through the automated Analyst Review Queue.

---

## 🏛️ Regulatory Compliance: The FATF Rule Matrix

ApexGuard enforces statutory sentinel checks aligned with the **Financial Action Task Force (FATF 40 Recommendations)** and the **US Bank Secrecy Act (BSA)**:

1. **FATF Recommendation 16 (Wire Transfer Rule / Travel Rule)**:
   - Enforces mandatory verification and threshold reporting for large transactions $\ge \$200,000$ (or adaptive IQR outliers).
2. **BSA 31 U.S.C. 5324 & FATF Rec. 20 (Structuring / Smurfing)**:
   - Detects deliberate evasion of the $\$10,000$ Currency Transaction Report (CTR) threshold by intercepting transfers between $\$9,000$ and $\$9,999$.
3. **FATF Recommendation 10 (Customer Due Diligence & Rapid Drain)**:
   - Intercepts sudden account emptying where an account with balance $> \$1,000$ is drained to $\$0.00$ on an outbound transfer/cash-out.
4. **Ghost Account Sentinel (Destination Balance Anomaly)**:
   - Identifies synthetic destination accounts where funds are transferred to non-updating dummy balances.
5. **Automated Form SAR-01 Generator**:
   - Compiles cryptographic SHA-256 verified Suspicious Activity Reports (SAR) ready for submission to Financial Intelligence Units (FIU).

---

## 💡 Explainable AI (XAI) & Interpretability

Compliant with the **EU AI Act (Article 13 - Transparency)** and the **US Fair Credit Reporting Act**:
* **TreeSHAP Attributions**: Decomposes model predictions into exact feature-level marginal contributions ($\phi_j$).
* **Dominant Feature**: `orig_diff` accounts for **95.13%** of fraud attribution (fraudsters consistently drain full sender balances).
* **Plain-English Explanations**: Converts complex mathematical attributions into human-readable justifications for bank fraud analysts.

---

## 🖥️ Platform Modules & UI Console

The web console provides 5 integrated surveillance modules:

1. **System Overview & Live Telemetry (Tab 1)**:
   - Real-time KPIs, transaction volume, prevented fraud losses, risk tier distributions, and Chart.js radar/bar analytics.
2. **Real-Time Live Transaction Scanner (Tab 2)**:
   - Single-transaction testing console with 1-click presets for **Normal Retail Payment** and **Fraudulent Smurfing/Drainage**. Real-time execution in $< 4\text{ms}$.
3. **Batch CSV Transaction Auditor (Tab 3)**:
   - High-throughput CSV ingestion and scoring for auditing thousands of historical transaction records.
4. **Case Investigation & Triage Hub (Tab 4)**:
   - Analyst workflow for reviewing flagged cases, updating investigation statuses (`CONFIRMED_FRAUD`, `CLEARED_NORMAL`), and recording notes.
5. **FATF Regulatory Compliance Hub (Tab 5)**:
   - Interactive rule threshold tuning, sentinel statistics, and one-click **Form SAR-01 generation and export (JSON/Print)**.

---

## 🚀 Quick Start Guide

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/zaheer-ahmed77/ApexGuard-Smart-Transaction-Anomaly-Detection.git
cd ApexGuard-Smart-Transaction-Anomaly-Detection

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install streamlined dependencies
pip install -r requirements.txt

# Launch the platform
python run_app.py
```

Open your browser at **`http://localhost:8000/`**.

### 2. Docker Deployment

```bash
# Build and run standalone container
docker-compose -f docker-compose.standalone.yml up --build -d
```

---

## 🔌 API Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Enterprise Landing Page | No |
| `GET` | `/login` | Dedicated Authentication & Registration Portal | No |
| `GET` | `/app` | Main Surveillance Console | Optional (Guest mode supported) |
| `GET` | `/health` | Health Check probe (UptimeRobot / Kubernetes) | No |
| `GET` | `/ready` | Readiness probe | No |
| `POST` | `/api/auth/register` | Register new analyst/compliance account | No |
| `POST` | `/api/auth/login` | Authenticate and obtain JWT Bearer token | No |
| `POST` | `/api/predict` | Real-time composite transaction scoring | Optional |
| `POST` | `/api/predict/batch` | High-throughput batch CSV upload & scoring | Optional |
| `GET` | `/api/transactions` | Paginated, filterable transaction audit ledger | Optional |
| `GET` | `/api/transactions/{id}` | Detailed transaction report & audit history | Optional |
| `PATCH`| `/api/transactions/{id}` | Update review status and investigation notes | Optional |
| `GET` | `/api/analytics/summary` | Real-time KPI counters & Chart.js telemetry | Optional |
| `GET` | `/api/model/info` | Trained model weights, metadata & feature rankings | Optional |

---

## 📂 Project Repository Structure

```
ApexGuard-Smart-Transaction-Anomaly-Detection/
├── config/
│   └── config.yaml               # System parameters & threshold configurations
├── src/
│   ├── api/
│   │   └── main.py               # Production FastAPI ASGI backend & REST routes
│   ├── compliance/
│   │   └── explainability.py     # SHAP tree explainer & audit frameworks
│   ├── data/
│   │   └── preprocessor.py       # 16-feature transformation, scaling & outlier capping
│   ├── database/
│   │   ├── auth.py               # bcrypt password hashing & JWT token management
│   │   ├── db.py                 # SQLAlchemy engine & session factory
│   │   ├── models.py             # User, TransactionRecord, and AuditLog schema
│   │   └── seed.py               # Default accounts & demo transaction seeding
│   ├── models/
│   │   ├── ml_anomaly_detection.py # XGBoost, Random Forest & Isolation Forest
│   │   ├── network_analysis.py   # Flow analysis & smurfing hub detection
│   │   └── rule_based_scenarios.py # FATF Sentinel engine & adaptive thresholds
│   └── services/
│       └── inference_service.py  # Tri-Engine composite scoring & override orchestrator
├── static/
│   ├── landing.html              # Enterprise landing portal
│   ├── login.html                # Sign In / Create Account tabbed portal
│   ├── app.html                  # Surveillance console with FATF Compliance Hub
│   ├── css/                      # Modern micro-dot canvas styling
│   └── js/app.js                 # Dynamic UI logic, live charts & SAR exporter
├── models/
│   ├── xgboost_fraud_model.joblib # Serialized XGBoost model
│   ├── random_forest_fraud_model.joblib # Serialized Random Forest model
│   ├── isolation_forest_model.joblib # Serialized Isolation Forest model
│   └── model_metadata.json       # Feature names, importances & metrics
├── notebooks/
│   └── Smart_Transaction_Anomaly_Detection_Colab.ipynb # Training notebook
├── APEXGUARD_PRESENTATION_SLIDES.md # Official 16-slide academic presentation deck
├── PROJECT_DEFENSE_MASTER_DOSSIER.md # Comprehensive 25+ question viva defense guide
├── DEPLOYMENT_GUIDE.md           # Step-by-step Render & Vercel deployment manual
├── apexguard_methodology_diagram.jpg # High-definition system architecture diagram
├── requirements.txt              # Cloud-optimized minimal dependencies
├── render.yaml                   # Render PaaS automated deployment manifest
└── vercel.json                   # Vercel edge reverse-proxy configuration
```

---

## 📖 Presentation & Examination Documents

For academic evaluation and defense preparation, refer to the following comprehensive documents:
* **[PROJECT_DEFENSE_MASTER_DOSSIER.md](PROJECT_DEFENSE_MASTER_DOSSIER.md)**: 25+ in-depth technical questions and answers covering ML mathematical proofs, class imbalance handling, feature importance, and architecture.
* **[APEXGUARD_PRESENTATION_SLIDES.md](APEXGUARD_PRESENTATION_SLIDES.md)**: The exact 16-slide presentation deck designed for PowerPoint.
* **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Deployment steps for Render, Vercel, and UptimeRobot keep-alive monitoring.

---

## ⚖️ License & Intellectual Property

This project is released under the **MIT License**.  
Developed and maintained by **Zaheer Ahmed** (Roll No: **22SW077**), Mehran University of Engineering and Technology (MUET), Jamshoro.
