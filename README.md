# Risk Management Demo — Streamlit App

This small demo implements a risk management scenario for a **Regional Health Clinic**. It includes:
- Risk identification (assets and threats)
- Risk assessment (likelihood × impact scoring)
- Risk control recommendations (mitigate, transfer, accept)
- Exportable risk management plan (JSON / CSV)

## How to run (locally)

1. Create a Python virtual environment (recommended) and activate it.
2. Install requirements:
```
pip install -r requirements.txt
```
3. Run Streamlit:
```
streamlit run app.py
```
4. The app will open in your browser (usually at http://localhost:8501).

## Files
- `app.py` — Streamlit frontend
- `risk_engine.py` — Risk logic and defaults
- `requirements.txt` — Python dependencies
- `README.md` — This file

## Notes
This is a demonstration project and NOT production-ready. For production:
- Integrate with CMDB for asset inventory
- Use authenticated user management and secure storage
- Store outputs to a database and integrate with ticketing/IR workflows
