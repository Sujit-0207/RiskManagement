import pandas as pd

# Default scenario for a Regional Health Clinic
DEFAULT_ASSETS = [
    {"Asset": "Electronic Health Records (EHR) Database", "Value": "High", "Owner": "IT"},
    {"Asset": "On-prem SharePoint Document Portal", "Value": "High", "Owner": "Records"},
    {"Asset": "Patient Workstations (Clinical)", "Value": "Medium", "Owner": "Operations"},
    {"Asset": "Medical Imaging Storage (PACS)", "Value": "High", "Owner": "Radiology"},
    {"Asset": "Billing & Financial Systems", "Value": "High", "Owner": "Finance"},
]

DEFAULT_THREATS = [
    {"Threat": "Ransomware / Data encryption", "Category": "Malware"},
    {"Threat": "Unauthorized access via unpatched web app (e.g., SharePoint zero-day)", "Category": "Vulnerability Exploit"},
    {"Threat": "Insider data exfiltration", "Category": "Insider"},
    {"Threat": "Phishing leading to credential compromise", "Category": "Social Engineering"},
    {"Threat": "Third-party vendor compromise", "Category": "Supply Chain"},
]

def risk_level_from_score(score: int):
    if score >= 16:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 6:
        return "Medium"
    return "Low"

def recommend_action(risk_level: str):
    # Simple mapping
    if risk_level == "Critical":
        return "Mitigate / Avoid", "Consider immediate isolation, emergency patching, rebuild; high-priority budget"
    if risk_level == "High":
        return "Mitigate / Transfer", "Apply controls, consider cyber-insurance for residual risk"
    if risk_level == "Medium":
        return "Mitigate", "Apply technical and procedural controls; schedule within 30 days"
    return "Accept", "Monitor and review periodically"

def compute_risk_scores(scores_df: pd.DataFrame, assets_df: pd.DataFrame, threats_df: pd.DataFrame):
    df = scores_df.copy()
    df['risk_level'] = df['risk_score'].apply(risk_level_from_score)
    recs = df['risk_level'].apply(recommend_action)
    df[['recommended_action', 'recommended_note']] = pd.DataFrame(recs.tolist(), index=df.index)
    # Estimate simple cost for mitigation (USD) based on asset value & risk level
    value_map = {"Low": 500, "Medium": 5000, "High": 25000}
    def est_cost(row):
        # base cost per asset value plus multiplier for risk
        base = value_map.get(row.get('Value', 'Medium'), 5000)
        mult = {"Low": 0.1, "Medium": 0.5, "High": 1.0, "Critical": 2.0}.get(row['risk_level'], 0.5)
        return int(base * mult)
    # Try to attach asset Value from assets_df
    assets_map = {i: r for i, r in assets_df.to_dict(orient='index').items()}
    df['Value'] = df['asset_id'].map(lambda x: assets_map.get(x, {}).get('Value', 'Medium'))
    df['estimated_cost_USD'] = df.apply(est_cost, axis=1)
    # Compose final notes column with recommendation
    df['recommended_action'] = df['risk_level'].map(lambda rl: "Mitigate" if rl in ["High","Critical","Medium"] else "Accept")
    df['notes_full'] = df['recommended_note'] + " | Estimated mitigation cost: $" + df['estimated_cost_USD'].astype(str)
    # Keep relevant columns
    return df[['asset','threat','likelihood','impact','risk_score','risk_level','recommended_action','notes_full','estimated_cost_USD']]

def summary_plan(org_name, owner, controls_df):
    plan = {
        "organization": org_name,
        "prepared_by": owner,
        "summary": {
            "total_risks": int(controls_df.shape[0]),
            "critical": int((controls_df['risk_level']=="Critical").sum()),
            "high": int((controls_df['risk_level']=="High").sum()),
            "medium": int((controls_df['risk_level']=="Medium").sum()),
            "low": int((controls_df['risk_level']=="Low").sum()),
            "estimated_total_mitigation_USD": int(controls_df['estimated_cost_USD'].sum())
        },
        "detailed_controls": controls_df.to_dict(orient='records')
    }
    return plan

def export_plan(plan_obj, path):
    import json
    with open(path, 'w') as f:
        json.dump(plan_obj, f, indent=2)
    return path
