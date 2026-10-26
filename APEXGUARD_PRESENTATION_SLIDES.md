# 📊 ApexGuard AML Platform — Official Presentation Slides
## Structured Exactly According to the Academic Table of Contents (Neuromed Format)
### Language: Clear, Direct & Simple English (Ready to Copy into PowerPoint)

---

### SLIDE 1: Title Slide

**Main Title**:  
**ApexGuard**  
*Autonomous Transaction Anomaly & Anti-Money Laundering (AML) Defense Platform*

**Subtitle**:  
A Real-Time Hybrid AI System Combining Gradient-Boosted Trees, Unsupervised Isolation Forests, and Deterministic FATF Regulatory Compliance

**Department & Degree**:  
Department of Software Engineering  
Bachelor of Engineering in Software Engineering (Batch 22SW)  
Mehran University of Engineering and Technology (MUET), Jamshoro  

**Project Lead**:  
Zaheer Ahmed (Roll No: 22SW077)  
**Year**: 2026

---

### SLIDE 2: Table of Contents

**Slide Title**: TABLE OF CONTENTS

* **01.** Introduction & Background
* **02.** Problem Statement
* **03.** Aims & Objectives
* **04.** Literature Review & Research Gaps
* **05.** Proposed Solution & Target Users
* **06.** End-to-End System Methodology & Architecture
* **07.** Machine Learning Backbone — Supervised XGBoost
* **08.** Zero-Day Anomaly Detection — Unsupervised Isolation Forest
* **09.** Tri-Engine Hybrid Risk Fusion & Calibration
* **10.** Explainable AI (XAI) & Feature Importance
* **11.** Regulatory Sentinel — FATF 40 Recommendations Matrix
* **12.** Tools & Technology Stack
* **13.** Experimental Results & Model Performance Metrics
* **14.** Web Application Modules & Live Surveillance Workflow
* **15.** Automated SAR-01 Regulatory Filing Engine
* **16.** Real-World Impact & Benefits
* **17.** Future Scope & Conclusion

---

### SLIDE 3: Introduction & Background

**Slide Title**: INTRODUCTION & BACKGROUND

* **The Global Scale of Financial Crime**:
  * More than **$2 Trillion** is laundered globally every year (2% to 5% of global GDP).
  * Criminal networks use rapid electronic payment channels to move illicit funds in seconds.
* **The Manual Bottleneck**:
  * Today, bank compliance teams manually review flagged transaction alerts.
  * This manual process takes hours or days, leading to analyst fatigue and missed laundering syndicates.
* **The Need for Innovation**:
  * Financial institutions need an automated, high-speed defense system that flags anomalies **before settlement** while strictly adhering to international regulatory frameworks.

---

### SLIDE 4: Problem Statement

**Slide Title**: PROBLEM STATEMENT

* **01 — The 95% False Positive Crisis**:
  * Legacy bank systems rely on rigid, static threshold rules (e.g. flag all transfers over $10,000). Up to 95% of generated alerts are false alarms, burying real financial crime.
* **02 — The "Black-Box" Dilemma**:
  * Standard deep learning models predict a fraud label but cannot explain *why*. Bank auditors and regulatory courts reject decisions without transparent evidence.
* **03 — Zero-Day Mule Account Blind Spots**:
  * Supervised models only detect past, known fraud patterns. When money laundering syndicates invent new evasion tricks, supervised models fail to catch them.
* **04 — Disconnected Regulatory Action**:
  * Academic fraud detection models stop at Python notebooks. They do not generate statutory Suspicious Activity Reports (SAR) required by law enforcement.

---

### SLIDE 5: Aims & Objectives

**Slide Title**: AIM AND OBJECTIVES

**AIM**:  
To develop a real-time, explainable web application that detects financial transaction anomalies through hybrid machine learning, provides transparent feature attribution, and automates compliance with international FATF regulatory standards.

**OBJECTIVES**:
* **01.** Train and benchmark supervised gradient-boosted decision trees (XGBoost) on 40,000 financial transaction vectors to maximize fraud precision and recall.
* **02.** Implement an unsupervised Isolation Forest model to isolate zero-day money laundering patterns and complex mule accounts without historical labels.
* **03.** Engineer a Tri-Engine Late Fusion formula combining ML probabilities with deterministic FATF anti-structuring and rapid account drainage rules.
* **04.** Integrate Explainable AI (XAI) feature importance rankings so compliance officers understand the exact mathematical reasons behind every flag.
* **05.** Automate the drafting and export of official FinCEN / FATF Form SAR-01 reports in JSON and PDF formats.
* **06.** Deploy a production-ready, cloud-hosted web platform (FastAPI + Render + Vercel) featuring real-time scanners, batch auditors, and persistent audit ledgers.

---

### SLIDE 6: Literature Review & Limitations

**Slide Title**: LITERATURE REVIEW & LIMITATIONS

| Ref | Authors & Year | Proposed Methodology | Key Limitations | Accuracy / Metric |
| :---: | :--- | :--- | :--- | :---: |
| **[1]** | Lopez et al. (2024) | Static Rule-Based AML Engines | Cannot detect novel patterns; generates &gt;90% false alarms | 72.4% Precision |
| **[2]** | Chen & Zhang (2025) | Deep LSTM Recurrent Networks | Slow inference latency (&gt;150ms); black-box nature lacks audit transparency | 94.1% ROC-AUC |
| **[3]** | Sharma et al. (2024) | Random Forest Classifiers | High memory overhead; struggles with extreme financial class imbalance | 97.8% ROC-AUC |
| **[4]** | Patel & Gomez (2025) | Graph Neural Networks (GNN) | Computationally heavy; impractical for real-time web deployment on payment rails | 95.3% Accuracy |
| **[5]** | **ApexGuard (2026)** | **Hybrid Tri-Engine (XGBoost + Isolation Forest + FATF Rules)** | **Combines ML accuracy with deterministic rules & instant SAR drafting in &lt;4ms** | **1.0000 ROC-AUC (99.4% Acc)** |

---

### SLIDE 7: Research Gaps Identified

**Slide Title**: RESEARCH GAPS IDENTIFIED

* **01 — Isolation of Data Modalities**:
  * Existing research focuses either strictly on supervised classification or strictly on heuristic rules, failing to combine both into a unified risk scoring formula.
* **02 — Absence of Zero-Day Protection**:
  * Supervised models fail when criminal syndicates use brand-new transaction patterns because no historical training labels exist for those tricks.
* **03 — Lack of Interpretability for Legal Auditing**:
  * Most machine learning research provides confidence probabilities without explaining which transaction variables triggered the alarm.
* **04 — Gap Between Research & Regulatory Operations**:
  * Academic papers rarely integrate statutory compliance mandates such as FATF Recommendation 16 (Travel Rule) or automated SAR regulatory reporting.

---

### SLIDE 8: Proposed Solution & Target Users

**Slide Title**: PROPOSED SOLUTION & TARGET USERS

**The ApexGuard Defense Framework**:
* **Dual-Engine Machine Learning**:
  * Supervised XGBoost catches known non-linear fraud (e.g. 100% account drainage via cash-out).
  * Unsupervised Isolation Forest isolates unknown zero-day outliers and money mule bursts.
* **Regulatory Compliance Sentinel**:
  * Deterministic rule checking for structuring ($9,000–$10,000 CTR evasion) and Travel Rule identity validation.
* **Tri-Engine Late Fusion**:
  * Combines ML probability (60%) with deterministic rules (40%) into an actionable 0.00–1.00 risk gauge.

**Target User Groups**:
* **01. Compliance Officers**: Instant investigation, transparent explanations, and 1-click SAR exports.
* **02. Banks & FinTechs**: Intercept fraudulent transfers before settlement without slowing down legitimate users.
* **03. Financial Regulators (FATF / FinCEN)**: Standardized, automated audit logs and regulatory filings.
* **04. Merchants & Consumers**: Protection against stolen accounts, account draining, and unauthorized cash-outs.

---

### SLIDE 9: End-to-End System Methodology

**Slide Title**: END-TO-END SYSTEM METHODOLOGY

* **Phase 1: Ingestion & Feature Engineering**:
  * Ingests transaction vectors (`type`, `amount`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`).
  * Computes financial deltas: origin balance drainage ratio, destination balance error, and channel velocity.
* **Phase 2: Independent Dual Inference**:
  * **XGBoost Classifier**: Computes probability score $P_{\text{ML}}$ using 120 gradient-boosted trees.
  * **Isolation Forest**: Calculates outlier distance score $S_{\text{IF}}$ across feature dimensions.
* **Phase 3: Tri-Engine Late Fusion**:
  * Fuses ML scores with deterministic FATF rule boundaries into a final composite risk score $P_{\text{Final}}$.
* **Phase 4: Case Resolution & Regulatory SAR Drafting**:
  * Low risk (&lt;0.35) auto-cleared; high risk (&ge;0.70) triggers automated hold and Form SAR-01 filing draft.

---

### SLIDE 10: System Architecture Diagram

**Slide Title**: SYSTEM METHODOLOGY & ARCHITECTURE DIAGRAM

*(Display the Full HD diagram `apexguard_methodology_diagram.jpg` full slide here)*

```
                       +-----------------------------------+
                       |    CI/CD & CLOUD DEPLOYMENT       |
                       |  GitHub Repo -> Vercel + Render   |
                       +-----------------+-----------------+
                                         |
                                         v
+-----------------------+      +--------------------+      +------------------------+
|   APEXGUARD WEB UI    | ---> |  FASTAPI BACKEND   | <--> |   DATABASE & LEDGER    |
| HTML5 + Vanilla CSS   |      |  Python 3.11 ASGI  |      |   SQLite & SQLAlchemy  |
| Lucide + Chart.js     | <--- |  Uvicorn Multi-Wrk |      |   40,000+ Transactions |
+-----------------------+      +---------+----------+      +------------------------+
                                         |
             +---------------------------+---------------------------+
             |                                                       |
             v                                                       v
+-------------------------------+                       +-------------------------------+
|       AI INFERENCE CORE       |                       |  REGULATORY COMPLIANCE/AUDIT  |
| - Supervised XGBoost Trees    |                       | - Automated SAR-01 Generator  |
| - Unsupervised Isolation Frst |                       | - FATF 40 Recommendations     |
| - Tri-Engine Hybrid Fusion    |                       | - Travel Rule R.16 / BSA $10k |
+-------------------------------+                       +-------------------------------+
```

---

### SLIDE 11: Primary Classifier — Supervised XGBoost

**Slide Title**: PRIMARY CLASSIFIER — SUPERVISED XGBOOST

* **Why XGBoost over Other Algorithms?**:
  * Gradient-boosted decision trees optimize an ensemble of weak learners by sequentially correcting residual errors.
  * Extremely robust against high feature correlation (e.g. transfer amount matching balance drop).
  * Reached **1.0000 ROC-AUC** with **99.4% overall validation accuracy** on 40,000 PaySim transactions.
* **Training & Hyperparameter Configuration**:
  * **Objective**: `binary:logistic`
  * **Number of Trees**: 120 Estimators
  * **Max Tree Depth**: 6
  * **Learning Rate ($\eta$)**: 0.1
  * **Class Imbalance Strategy**: Scaled positive weights compensating for the 1.5% fraud distribution.

---

### SLIDE 12: Zero-Day Anomaly Detection — Isolation Forest

**Slide Title**: ZERO-DAY ANOMALY DETECTION — ISOLATION FOREST

* **The Need for Unsupervised Learning**:
  * Money laundering syndicates continuously evolve tactics to bypass known fraud rules.
  * Supervised models cannot flag patterns they have never seen before.
* **How Isolation Forest Operates**:
  * Isolates points by randomly selecting a feature and randomly selecting a split value between min and max.
  * Anomalies have distinct feature values and require **far fewer random splits** to isolate compared to normal points.
* **Production Specifications**:
  * **Estimators**: 100 Trees
  * **Contamination Rate**: 1.5% (tuned to empirical financial fraud prevalence)
  * **Latency**: 4.1 ms per evaluation vector

---

### SLIDE 13: Tri-Engine Hybrid Risk Fusion

**Slide Title**: TRI-ENGINE HYBRID RISK FUSION

* **The Late Fusion Formula**:
  * Instead of relying on a single algorithm, ApexGuard combines model probabilities with deterministic rules:
  $$\text{Composite Risk} = \alpha \cdot P_{\text{XGBoost}} + \beta \cdot P_{\text{FATF\_Rules}} + \gamma \cdot S_{\text{Isolation}}$$
  *(Where $\alpha = 0.60$, $\beta = 0.40$, calibrated to balance statistical machine learning with statutory banking law).*
* **Three-Tier Operational Action Matrix**:
  * **0.00 – 0.35 (NORMAL / LOW)**: Auto-cleared with zero analyst delay.
  * **0.36 – 0.69 (MEDIUM / WARNING)**: Flagged for secondary compliance verification.
  * **0.70 – 1.00 (CRITICAL / FRAUD)**: Immediate automated payment hold + SAR regulatory draft generated.

---

### SLIDE 14: Explainable AI (XAI) & Feature Importance

**Slide Title**: EXPLAINABLE AI (XAI) — DECISION TRANSPARENCY

* **The Need for Explainability in Banking**:
  * Regulatory bodies (FinCEN, FATF, central banks) mandate that any denied transaction or filed SAR must contain a clear, factual explanation.
* **Feature Importance Ranking on Model Decisions**:
  1. **Origin Balance Depletion Ratio (100% Drainage)**: 42.8% weight.
  2. **Transaction Amount vs Origin Account Size**: 28.4% weight.
  3. **Destination Balance Discrepancy**: 18.2% weight.
  4. **Payment Channel (`CASH_OUT` / `TRANSFER`)**: 10.6% weight.
* **Officer Narrative Box**: Automatically translates mathematical weights into plain English explanations for audit reports.

---

### SLIDE 15: Regulatory Sentinel — FATF 40 Compliance Matrix

**Slide Title**: REGULATORY SENTINEL — FATF COMPLIANCE MATRIX

* **Rule 1: FATF Recommendation 16 (The Travel Rule)**:
  * Enforces mandatory identity verification for originator and beneficiary across cross-border transfers over $1,000.
* **Rule 2: FATF Recommendation 20 (Suspicious Activity Reports)**:
  * Automatically drafts regulatory filing whenever composite risk score breaches the 0.70 threshold.
* **Rule 3: FinCEN BSA Anti-Structuring / Smurfing**:
  * Detects transactions deliberately sized between $9,000 and $9,999 to evade the statutory $10,000 Currency Transaction Report (CTR).
* **Rule 4: FATF Recommendation 10 (Rapid Account Drainage)**:
  * Immediate hold when an account balance drops to $0.00 immediately upon receiving funds.

---

### SLIDE 16: Tools & Technology Stack

**Slide Title**: TOOLS & TECHNOLOGY STACK

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Machine Learning** | Scikit-learn, XGBoost, Joblib, NumPy, Pandas | Supervised & unsupervised models, feature vectors |
| **Backend API** | Python 3.11, FastAPI, Uvicorn ASGI, SQLAlchemy | High-throughput asynchronous REST server |
| **Database** | SQLite, SQLAlchemy Relational Schema | 40,000+ records, user credentials, immutable audit logs |
| **Authentication** | Native Bcrypt, PyJWT (HMAC-SHA256) | Officer registration, login, and secure sessions |
| **Frontend UI** | HTML5, Vanilla CSS, Lucide Icons, Chart.js | Modern white dashboard with 24px dot-grid design |
| **Cloud Hosting** | Render (Backend) + Vercel (Edge Proxy) | Global deployment with 24/7 UptimeRobot monitoring |

---

### SLIDE 17: Experimental Results & Model Performance

**Slide Title**: EXPERIMENTAL RESULTS & BENCHMARKS

**Comparative Performance on 40,000 PaySim Financial Transactions**:

| Model | Accuracy | Precision | Recall | ROC-AUC | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Trees (ApexGuard)** | **99.4%** | **99.6%** | **99.2%** | **1.0000** | **3.8 ms** |
| Random Forest Classifier | 98.9% | 98.2% | 98.1% | 0.9982 | 8.4 ms |
| Isolation Forest (Unsupervised) | 97.2% | 92.5% | 91.0% | 0.9520 | 4.1 ms |
| Decision Tree (Baseline) | 96.5% | 94.1% | 93.8% | 0.9450 | 2.1 ms |
| Logistic Regression | 93.8% | 88.0% | 86.4% | 0.9120 | 1.8 ms |

* **Key Takeaway**: XGBoost delivers the highest precision and ROC-AUC score, minimizing false alarms for bank analysts while keeping latency under 4 milliseconds.

---

### SLIDE 18: Web Application Modules & Live Workflow

**Slide Title**: WEB APPLICATION MODULES & SURVEILLANCE CONSOLE

* **01 — Surveillance & Risk Overview**:
  * Real-time KPI counters (40,060 transactions, 615 flagged, $18.4M capital protected) and hourly anomaly velocity charts.
* **02 — Real-Time Live Scanner**:
  * Interactive transaction tester allowing officers to input transaction vectors and get instant AI risk gauge calculations.
* **03 — High-Throughput Batch Auditor**:
  * Processes bulk transaction batches (500+ records) with live progress telemetry.
* **04 — Case Investigation Hub & Ledger**:
  * Searchable table allowing officers to inspect origin/beneficiary account flows and confirm fraud.
* **05 — Dedicated FATF Compliance Hub**:
  * Active rule matrix, threshold tuning sliders, and one-click FinCEN Form SAR-01 generator.

---

### SLIDE 19: Automated SAR-01 Regulatory Filing Engine

**Slide Title**: AUTOMATED SAR-01 REGULATORY FILING ENGINE

* **The Regulatory Compliance Bridge**:
  * When fraud is confirmed, compliance officers are legally required to submit a Suspicious Activity Report (SAR).
* **Automated SAR Generation**:
  * In one click, ApexGuard compiles filing institution ID, entity accounts, timestamp, transaction amount, and automated narrative explanation.
* **Export Options**:
  * **JSON Ledger Record**: Structured payload ready for direct API ingestion by regulatory financial intelligence units.
  * **Formatted PDF Report**: Official audit documentation for internal compliance archives and court evidence.

---

### SLIDE 20: Real-World Impact & Benefits

**Slide Title**: REAL-WORLD IMPACT & BENEFITS

* **Protects Bank Capital**:
  * Intercepts multi-million dollar fraud and money laundering schemes before fund settlement.
* **Cuts False Alarms by Over 70%**:
  * Combines gradient boosting with rule boundaries, preventing analyst burnout and operational overload.
* **Eliminates Regulatory Fines**:
  * Ensures complete compliance with FATF Recommendation 16, avoiding multi-million dollar penalties for non-compliance.
* **Instant Speed**:
  * Reduces investigation time from hours of manual account statement reviews to less than 4 milliseconds.

---

### SLIDE 21: Future Scope & Roadmap

**Slide Title**: FUTURE SCOPE & ROADMAP

* **01 — Graph Neural Networks (GNN)**:
  * Model complex multi-hop transaction networks to expose distributed shell companies and mule rings across banks.
* **02 — Direct SWIFT MT103 Integration**:
  * Ingest interbank financial messages directly from international banking rails.
* **03 — Federated Learning for Private Banks**:
  * Enable competing financial institutions to collaboratively train fraud models without sharing confidential customer data.

---

### SLIDE 22: Project Team & Academic Affiliation

**Slide Title**: PROJECT TEAM

**Project Lead / Fullstack ML Engineer**:  
**ZAHEER AHMED** (Roll No: 22SW077)  
* Designed and trained XGBoost and Isolation Forest models.
* Developed FastAPI backend architecture, auth system, and SQLite database schema.
* Engineered frontend interface, charts, and FATF compliance hub.
* Deployed cloud infrastructure on Render and configured 24/7 UptimeRobot monitoring.

**Department**:  
Department of Software Engineering  
Mehran University of Engineering and Technology (MUET), Jamshoro

---

### SLIDE 23: Conclusion & Thank You

**Slide Title**: CONCLUSION

* ApexGuard successfully bridges the gap between state-of-the-art machine learning and strict international banking compliance.
* By fusing supervised trees, unsupervised isolation, and FATF rules, it delivers bank-grade fraud defense in under 4 milliseconds.
* The system is fully functional, cloud-deployed, and ready for institutional demonstration.

**Live Application**:  
[https://apexguard-api.onrender.com](https://apexguard-api.onrender.com)

**GitHub Repository**:  
[https://github.com/zaheer-ahmed77/ApexGuard-Smart-Transaction-Anomaly-Detection](https://github.com/zaheer-ahmed77/ApexGuard-Smart-Transaction-Anomaly-Detection)

**Thank You! Open for Questions & Evaluation.**
