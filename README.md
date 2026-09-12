# HealthGuard AI — Healthcare Monitoring AI Agent

A Streamlit healthcare monitoring project with SQLite/SQLAlchemy, medication tracking, nutrition logging, MedlinePlus lookup, optional Spoonacular nutrition lookup, and an optional LangChain/Gemini assistant.

## Important scope

This is an educational software project. It is **not** a medical device and does not diagnose, prescribe, or replace professional care.

## Features

- Patient registration and login with bcrypt password hashing
- Personal dashboard with health metrics and charts
- Medication schedule and daily dose tracking
- Medication adherence percentage
- Nutrition logging with optional Spoonacular lookup
- Medical-topic search using MedlinePlus
- Optional LangChain/Gemini health assistant with read-only patient tools
- PDF and CSV report downloads
- SQLite database
- Pytest test and GitHub Actions CI
- Streamlit Community Cloud deployment configuration

## 1. Prerequisites

- Python 3.11 or 3.12
- Git
- A Gemini API key if you want the AI Assistant
- A Spoonacular API key if you want automatic nutrition lookup

## 2. Create the environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure secrets locally

Copy `.env.example` to `.env` and add your own keys. Never commit `.env`.

```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
SPOONACULAR_API_KEY=your_key
```

The application still starts without these keys. Without Gemini, the AI page explains that it is not configured; without Spoonacular, nutrition can be entered manually.

## 4. Initialize and seed the database

```bash
python init_db.py
python seed.py
```

Demo login:

```text
Username: demo
Password: DemoPass123!
```

If you have an older database from the prototype, delete `data/healthcare.db` first and run the two commands again. This project intentionally does not include database migrations.

## 5. Run the application

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, normally `http://localhost:8501`.

## 6. Test

```bash
pytest -q
```

## 7. GitHub

```bash
git init
git add .
git commit -m "Initial working HealthGuard AI project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/healthcare-monitoring-ai-agent.git
git push -u origin main
```

Do not commit `.env`, `data/healthcare.db`, or `.streamlit/secrets.toml`.

## 8. Streamlit Community Cloud

1. Push the repository to GitHub.
2. Open Streamlit Community Cloud and choose **Create app**.
3. Select your repository, branch, and `app.py` entrypoint.
4. In Advanced settings / Secrets, add:

```toml
GEMINI_API_KEY = "your_key"
GEMINI_MODEL = "gemini-2.5-flash"
SPOONACULAR_API_KEY = "your_spoonacular_key"
```

5. Deploy.

The local SQLite database is suitable for a student/demo deployment. For multi-user production use, move the database to a managed persistent database and add a proper authentication provider.

## Project structure

```text
healthcare-monitoring-ai-agent/
├── app.py
├── config.py
├── init_db.py
├── seed.py
├── database/
├── auth/
├── agents/
├── api/
├── services/
├── ui/
├── tests/
├── data/
└── .github/workflows/
```

## Safety

The application displays an educational-use disclaimer. Do not use it for emergencies or as a substitute for professional medical advice.
