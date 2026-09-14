# HealthGuard AI — Healthcare Monitoring AI Agent

HealthGuard AI is an educational healthcare monitoring application built with
Streamlit, SQLite, SQLAlchemy, LangChain, and Google Gemini.

The application provides a personal health dashboard for tracking health
metrics, medications, medication adherence, nutrition records, wellness goals,
and health information. It also provides an optional AI health assistant that
can answer questions using patient-scoped application data and general
health information.

> **Important:** HealthGuard AI is an educational software project. It is not
> a medical device and does not diagnose, prescribe, or replace advice from a
> qualified healthcare professional.

---

## Features

### 👤 Patient Account

- Patient registration and login
- Bcrypt password hashing
- Patient-specific dashboard
- Patient profile information

### 📊 Health Monitoring

- Health metric recording
- Health dashboard
- Metric visualization
- Progress tracking
- Personal wellness goals
- Daily steps and other health metrics

### 💊 Medication Management

- Medication scheduling
- Daily medication dose tracking
- Medication adherence percentage
- Medication history
- Medication interaction lookup
- FDA/openFDA drug-label information when available

### 🥗 Nutrition

- Nutrition logging
- Manual nutrition entry
- Optional Spoonacular nutrition lookup

### 🩺 Medical Information

- Medical-topic lookup using MedlinePlus
- Health information retrieval from external sources
- Educational health information with safety disclaimers

### 🤖 AI Health Assistant

- Optional LangChain-based AI agent
- Google Gemini integration
- Patient-scoped health tools
- Medication information
- Patient health profile information
- Recorded health metrics
- General wellness guidance
- Emergency phrase detection and safety response

The AI assistant is designed to work with application data relevant to the
currently authenticated patient rather than providing unrestricted access to
the database.

### 📄 Reports & Export

- Health reports
- PDF report generation
- CSV health-data export
- JSON report generation
- XML report generation
- Patient health summary
- Medication summary

### ⚙️ Technology

- Python
- Streamlit
- SQLAlchemy
- SQLite
- LangChain
- Google Gemini
- Pandas
- Plotly
- ReportLab
- MedlinePlus
- openFDA
- Optional Spoonacular API
- Pytest
- GitHub Actions

---

# Architecture

```text
                         ┌──────────────────────┐
                         │      Streamlit UI     │
                         │ Dashboard / Chat /    │
                         │ Medications / Goals   │
                         │ Reports / Nutrition   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Application Services │
                         │                      │
                         │ Health Metrics       │
                         │ Medications          │
                         │ Nutrition            │
                         │ Goals                │
                         │ Reports              │
                         │ Interactions         │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    ▼               ▼                ▼
             ┌────────────┐  ┌────────────┐  ┌──────────────┐
             │  SQLite /  │  │ External   │  │ LangChain /  │
             │ SQLAlchemy │  │ APIs       │  │ Gemini Agent │
             └────────────┘  └────────────┘  └───────┬──────┘
                                                     │
                                                     ▼
                                             Patient-scoped
                                                  tools
