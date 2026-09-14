import streamlit as st
import json
import os

st.title("📊 Dashboard")

with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

os.makedirs("reports", exist_ok=True)

report_files = [
    f for f in os.listdir("reports")
    if f.endswith(".txt")
]

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

st.subheader("Knowledge Base Summary")

st.write(f"High Risk Procedures: {high_risk}")
st.write(f"Medium Risk Procedures: {medium_risk}")
st.write(f"Low Risk Procedures: {low_risk}")