# ApexGuard — Autonomous Transaction Anomaly & AML Intelligence Platform

**Enterprise-grade financial fraud surveillance, transaction anomaly detection, and anti–money laundering (AML) compliance platform.** Real-time ML inference (XGBoost + Isolation Forest + FATF Rule Matrices), explainable AI, modern monochrome white theme, and dedicated authentication workflow.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What Is This Project?

Transaction Anomaly Detection is a **production-ready fraud detection system** that combines:

- **Rule-based AML** (large transactions, structuring, layering, high-risk entities)
- **Classical ML** (XGBoost, LightGBM, Random Forest, Isolation Forest)
- **Deep learning** (Autoencoder, LSTM Autoencoder, Transformer)
- **Network analysis** (cycles, fan-in/fan-out, community detection)
- **Explainability** (SHAP, audit logs) and **BI/Reporting** (Power BI, Looker, Streamlit)

It is built for **PaySim-style transaction data**, runs locally or in the cloud (Azure, Docker, Kubernetes), and exposes a **REST API** for real-time scoring.

---

## Performance at a Glance

| Component        | AUC    | Precision | Recall | Flag Rate |
|-----------------|--------|-----------|--------|-----------|
| **ML-based**    | 0.9939 | 1.0       | 0.96   | 0.66%     |
| **Rule-based**  | 0.8859 | 0.16      | 0.78   | 2.29%     |
| **Combined**    | 0.9980 | 0.037     | 0.97   | 18.86%    |

- **Combined system:** AUC 0.9980, Average Precision 0.8240  
- **Multi-model ensemble:** XGBoost, LightGBM, Random Forest, Isolation Forest, Autoencoder, LSTM Autoencoder, Transformer  
- **Fully configurable:** 60+ parameters in `config/config.yaml`, no hardcoded business logic  

---

## Features

- **Real-time fraud detection API** (FastAPI) with `/predict`, `/health`, `/metrics`
- **Rule-based AML scenarios** — large transactions, structuring (smurfing), rapid movement (layering), high-risk entities
- **ML ensemble** — XGBoost, LightGBM, Random Forest, Isolation Forest + **Autoencoder, LSTM Autoencoder, Transformer**
- **Network analysis** — transaction graphs, cycle detection, Louvain communities, centrality
- **Feature store** — online/offline features, versioning, configurable windows
- **Explainability & compliance** — SHAP, per-prediction explanations, audit logging, EU AI Act–oriented
- **BI & reporting** — Parquet/CSV/Excel export, Streamlit dashboard, daily/weekly/monthly reports
- **LLM & RAG** (optional) — GPT-4 risk explanations, ChromaDB-based pattern search
- **DevOps** — Docker, Kubernetes, Terraform, Prometheus/Grafana, Azure-friendly

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional)
- Azure CLI (optional, for cloud deploy)

### Quick Start (Single Command)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the platform
python run_app.py
```

### Application URLs & Credentials:
- **Landing Page**: [http://localhost:8000/](http://localhost:8000/)
- **Dedicated Login**: [http://localhost:8000/login](http://localhost:8000/login)
- **Surveillance Console**: [http://localhost:8000/app](http://localhost:8000/app)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Google Colab Notebook**: `notebooks/Smart_Transaction_Anomaly_Detection_Colab.ipynb`

#### Default Credentials:
- **Chief Compliance Officer (Admin)**: `admin` / `Admin@123`
- **Lead AML Analyst**: `analyst` / `Analyst@123`

### Standalone Docker Deployment:

```bash
docker-compose -f docker-compose.standalone.yml up --build -d
```

---

## Project Structure (Overview)

```
Transaction-Anomaly-Detection/
├── config/config.yaml       # Main config (60+ parameters)
├── src/
│   ├── api/main.py          # FastAPI app
│   ├── compliance/          # Explainability, audit
│   ├── data/                # Preprocessing
│   ├── mlops/               # Model monitoring, drift
│   ├── services/            # Feature store, BI export, LLM, RAG, reporting, merchants
│   ├── utils/               # Helpers, config loader
│   ├── visualization/       # Plots
│   └── main.py              # Pipeline orchestration
├── dashboards/              # Streamlit dashboard
├── databricks/notebooks/    # Ingestion, features, training
├── dbt/                     # Data models (staging, marts)
├── scripts/                 # Download data, reports, BI export
├── tests/                   # Pytest
├── k8s/                     # Kubernetes manifests
├── terraform/               # IaC
└── monitoring/              # Prometheus, Grafana
```

---

## Dataset (PaySim)

Uses **PaySim-style** fields: `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`. Compatible with [PaySim (Kaggle)](https://www.kaggle.com/datasets/ealaxi/paysim1). If the dataset is unavailable, the project can generate synthetic data for testing.

---

## API Usage

```bash
# Start API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

- **GET /** — API info  
- **GET /health** — Health check  
- **POST /predict** — Real-time fraud score  
- **GET /docs** — Swagger UI  
- **GET /metrics** — Prometheus metrics  

Example:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"step":1,"type":"TRANSFER","amount":5000.0,"nameOrig":"C123456789","oldbalanceOrg":10000.0,"newbalanceOrig":5000.0,"nameDest":"M987654321","oldbalanceDest":0.0,"newbalanceDest":5000.0}'
```

---

## Configuration

All behavior is driven by **`config/config.yaml`**: rule thresholds, ML hyperparameters, risk weights, API settings, monitoring, LLM/RAG toggles, merchant onboarding, etc. No hardcoded business logic. See `config/config.yaml` and `VERIFICATION_CHECKLIST.md` for details.

---

## Technology Stack

- **ML/DL:** scikit-learn, XGBoost, LightGBM, TensorFlow/Keras, PyTorch, SHAP  
- **NLP/LLM:** OpenAI GPT-4, Sentence Transformers, ChromaDB  
- **Data:** Pandas, NumPy, NetworkX, PySpark (Databricks), dbt  
- **API:** FastAPI, Uvicorn, Pydantic  
- **BI/Dashboards:** Streamlit, Parquet/CSV/Excel export  
- **Infra:** Docker, Kubernetes, Terraform, Azure, Prometheus, Grafana  

---

## Documentation

| Resource              | Path |
|-----------------------|------|
| Config reference      | `config/config.yaml` |
| Config checklist      | `VERIFICATION_CHECKLIST.md` |
| API                   | `src/api/main.py` |
| Data analyst role     | `docs/DATA_ANALYST_ROLE.md` |
| Self-service & BI     | `docs/SELF_SERVICE_GUIDE.md`, `docs/DASHBOARD_GUIDE.md` |
| Feature store         | `docs/FEATURE_STORE_GUIDE.md` |
| dbt                   | `dbt/README.md` |
| Terraform             | `terraform/README.md` |

---

## Testing

```bash
pytest tests/
pytest tests/test_config_integration.py -v
pytest --cov=src tests/
```

---

## Security & Compliance

- **GDPR-oriented** — PII masking, data protection  
- **Explainability** — SHAP, audit trails (EU AI Act–friendly)  
- **AML** — Rule-based scenarios, configurable thresholds, reporting hooks  

---

## License

MIT License.

---

---

## Platform & Production Support

- **Status:** Enterprise Production Ready
- **Architecture:** Fast real-time inference (FastAPI + XGBoost + Isolation Forest + AML Rule Engine)
- **Deployment:** Docker, Cloud (AWS / Azure / GCP / Render), Kubernetes ready
- **Compliance:** Explainable AI (SHAP), FATF/AML Rule Sets, Full Audit Logs

---

*Smart Transaction Anomaly Detection — Real-time fraud detection, AML risk scoring, and behavioral anomaly analysis powered by Machine Learning.*

**Version:** 3.0.0 · **Status:** Production-ready
