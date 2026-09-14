import streamlit as st
import json
import os
import pandas as pd

st.title("📊 Dashboard")

# Load Procedures
with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

# Reports Folder
os.makedirs("reports", exist_ok=True)

report_files = [
    f for f in os.listdir("reports")
    if f.endswith(".txt")
]

# Risk Counts
high_risk = sum(
    1
    for p in procedures.values()
    if p["risk"] == "High"
)

medium_risk = sum(
    1
    for p in procedures.values()
    if p["risk"] == "Medium"
)

low_risk = sum(
    1
    for p in procedures.values()
    if p["risk"] == "Low"
)

# Top Metrics
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Procedures", len(procedures))

with c2:
    st.metric("Reports", len(report_files))

with c3:
    st.metric("High Risk", high_risk)

with c4:
    st.metric("Medium Risk", medium_risk)

st.divider()

# Risk Distribution Chart
st.subheader("📈 Risk Distribution")

risk_df = pd.DataFrame(
    {
        "Risk": ["High", "Medium", "Low"],
        "Count": [
            high_risk,
            medium_risk,
            low_risk
        ]
    }
)

st.bar_chart(
    risk_df.set_index("Risk")
)

st.divider()

# Knowledge Base Table
st.subheader("📋 Knowledge Base Overview")

data = []

for name, info in procedures.items():

    data.append(
        {
            "Procedure": name,
            "Risk": info["risk"],
            "Steps": len(info["steps"])
        }
    )

df = pd.DataFrame(data)

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# Recent Reports
st.subheader("📄 Recent Reports")

if report_files:

    for report in sorted(report_files, reverse=True)[:5]:
        st.write(f"📄 {report}")

else:
    st.info("No reports generated yet.")