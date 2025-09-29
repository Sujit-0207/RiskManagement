import streamlit as st
import pandas as pd
import numpy as np
import json
from risk_engine import DEFAULT_ASSETS, DEFAULT_THREATS, compute_risk_scores, summary_plan, export_plan

st.set_page_config(page_title="Risk Management Demo — Regional Health Clinic", layout="wide")

st.title("Risk Management Scenario — Regional Health Clinic")
st.write("""This demo implements a small risk management process for a **Regional Health Clinic**.
It includes: Risk Identification, Risk Assessment, Risk Control, and produces a simple risk management plan you can export.""")

st.sidebar.header("Scenario & Controls")
org_name = st.sidebar.text_input("Organization name", "Regional Health Clinic")
owner = st.sidebar.text_input("Prepared by", "Risk Manager")
st.sidebar.markdown("---")

st.header("1) Risk Identification — Assets & Threats")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Key Assets (editable)")
    assets_df = pd.DataFrame(DEFAULT_ASSETS)
    edited_assets = st.data_editor(assets_df, num_rows="dynamic", key="assets_editor")

with col2:
    st.subheader("Potential Threats (editable)")
    threats_df = pd.DataFrame(DEFAULT_THREATS)
    edited_threats = st.data_editor(threats_df, num_rows="dynamic", key="threats_editor")

st.markdown("---")

st.header("2) Risk Assessment — Likelihood & Impact")

st.write("For each (Asset × Threat) pair, select Likelihood and Impact (1-5). The app computes risk score = Likelihood × Impact.")

# Build pairs
pairs = []
for ai, arow in edited_assets.iterrows():
    for ti, trow in edited_threats.iterrows():
        pairs.append({
            "asset_id": ai,
            "asset": arow['Asset'],
            "threat_id": ti,
            "threat": trow['Threat'],
            "default_likelihood": 3,
            "default_impact": 3
        })
pairs_df = pd.DataFrame(pairs)

# Interactive scoring
scores = []
for idx, row in pairs_df.iterrows():
    st.markdown(f"**Asset:** {row['asset']}  —  **Threat:** {row['threat']}")
    c1, c2, c3 = st.columns([1,1,4])
    with c1:
        likelihood = st.slider(f"Likelihood (1-5) [{idx}]", 1, 5, value=row['default_likelihood'], key=f"l_{idx}")
    with c2:
        impact = st.slider(f"Impact (1-5) [{idx}]", 1, 5, value=row['default_impact'], key=f"i_{idx}")
    with c3:
        commentary = st.text_input(f"Notes [{idx}]", "", key=f"note_{idx}")
    scores.append({**row.to_dict(), "likelihood": likelihood, "impact": impact, "notes": commentary})

scores_df = pd.DataFrame(scores)
scores_df['risk_score'] = scores_df['likelihood'] * scores_df['impact']

st.markdown("---")
st.header("3) Risk Control — Suggested Strategies")

# Compute suggested controls using risk engine
controls_df = compute_risk_scores(scores_df, edited_assets, edited_threats)

st.dataframe(controls_df[['asset','threat','likelihood','impact','risk_score','risk_level','recommended_action','estimated_cost_USD']])

st.markdown("**Legend for recommended actions:**\n\n- **Mitigate**: Apply controls to reduce likelihood/impact.\n- **Transfer**: Consider insurance or contractual transfer.\n- **Accept**: Accept residual risk (monitor).\n- **Avoid**: Remove the asset/function or stop the risky activity.")

st.markdown("---")
st.header("4) Risk Management Plan & Export")

plan = summary_plan(org_name, owner, controls_df)
st.json(plan, expanded=False)

colx, coly = st.columns(2)
with colx:
    st.download_button("Download plan (JSON)", json.dumps(plan, indent=2), file_name="risk_plan.json", mime="application/json")
with coly:
    csv_bytes = controls_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download detailed controls (CSV)", csv_bytes, file_name="risk_controls.csv", mime="text/csv")

st.info("This Streamlit app is a demonstration. For production use, integrate with your IR, CMDB, and ticketing systems.")

st.markdown('---')
st.caption("Project: Risk Management Demo — created for demonstration purposes.")
