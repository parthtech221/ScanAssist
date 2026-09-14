import streamlit as st
import json
import pandas as pd

st.title("📈 Analytics")

with open(
    "procedures.json",
    "r",
    encoding="utf-8"
) as f:

    procedures = json.load(f)

risk_data = []

for name, info in procedures.items():

    risk_data.append(
        {
            "Procedure": name,
            "Risk": info["risk"]
        }
    )

df = pd.DataFrame(
    risk_data
)

st.subheader(
    "Risk Distribution"
)

risk_counts = (
    df["Risk"]
    .value_counts()
)

st.bar_chart(
    risk_counts
)

st.subheader(
    "Procedure Table"
)

st.dataframe(df)