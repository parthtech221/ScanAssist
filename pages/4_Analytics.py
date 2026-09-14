import streamlit as st
import json
import pandas as pd
import os

st.title("📈 Analytics Dashboard")

# =====================================
# LOAD DATA
# =====================================

with open(
    "procedures.json",
    "r",
    encoding="utf-8"
) as f:

    procedures = json.load(f)

os.makedirs(
    "reports",
    exist_ok=True
)

report_count = len(
    [
        f for f in os.listdir("reports")
        if f.endswith(".txt")
    ]
)

# =====================================
# BUILD DATAFRAME
# =====================================

rows = []

for procedure, info in procedures.items():

    rows.append(
        {
            "Procedure": procedure,
            "Risk": info["risk"],
            "Category": info["category"],
            "Severity": info["severity"],
            "Estimated Time": info["estimated_time"]
        }
    )

df = pd.DataFrame(rows)

# =====================================
# METRICS
# =====================================

high_risk = len(
    df[df["Risk"] == "High"]
)

medium_risk = len(
    df[df["Risk"] == "Medium"]
)

low_risk = len(
    df[df["Risk"] == "Low"]
)

avg_severity = round(
    df["Severity"].mean(),
    1
)

st.subheader("📊 System Overview")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Procedures",
        len(df)
    )

with c2:
    st.metric(
        "Reports",
        report_count
    )

with c3:
    st.metric(
        "High Risk",
        high_risk
    )

with c4:
    st.metric(
        "Medium Risk",
        medium_risk
    )

with c5:
    st.metric(
        "Avg Severity",
        avg_severity
    )

st.divider()

# =====================================
# RISK DISTRIBUTION
# =====================================

st.subheader(
    "🚨 Risk Distribution"
)

risk_counts = (
    df["Risk"]
    .value_counts()
)

st.bar_chart(
    risk_counts
)

st.divider()

# =====================================
# CATEGORY DISTRIBUTION
# =====================================

st.subheader(
    "🗂 Category Distribution"
)

category_counts = (
    df["Category"]
    .value_counts()
)

st.bar_chart(
    category_counts
)

st.divider()

# =====================================
# SEVERITY ANALYSIS
# =====================================

st.subheader(
    "📈 Severity Analysis"
)

severity_df = (
    df[
        [
            "Procedure",
            "Severity"
        ]
    ]
    .sort_values(
        by="Severity",
        ascending=False
    )
)

st.dataframe(
    severity_df,
    use_container_width=True
)

st.divider()

# =====================================
# TOP CRITICAL ISSUES
# =====================================

st.subheader(
    "🔥 Top Critical Procedures"
)

critical_df = (
    df
    .sort_values(
        by="Severity",
        ascending=False
    )
    .head(5)
)

for _, row in critical_df.iterrows():

    st.error(
        f"{row['Procedure']} | Severity: {row['Severity']}/100"
    )

st.divider()

# =====================================
# KNOWLEDGE BASE TABLE
# =====================================

st.subheader(
    "📋 Complete Knowledge Base"
)

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# =====================================
# INSIGHTS
# =====================================

st.subheader(
    "🤖 System Insights"
)

highest_risk = (
    df.sort_values(
        by="Severity",
        ascending=False
    )
    .iloc[0]
)

st.info(
    f"Highest priority issue: "
    f"{highest_risk['Procedure']} "
    f"({highest_risk['Severity']}/100)"
)

st.success(
    f"Total knowledge base procedures: "
    f"{len(df)}"
)

st.warning(
    f"High-risk procedures requiring immediate escalation: "
    f"{high_risk}"
)