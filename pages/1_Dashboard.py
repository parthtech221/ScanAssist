import streamlit as st
import json
import os
import pandas as pd

st.title("🩺 ScanAssist Dashboard")
st.caption("Safety-First CT/MRI Troubleshooting Assistant")

# =====================================
# LOAD KNOWLEDGE BASE
# =====================================

with open(
    "procedures.json",
    "r",
    encoding="utf-8"
) as f:

    procedures = json.load(f)

# =====================================
# REPORTS
# =====================================

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
# SYSTEM STATUS
# =====================================

st.subheader("🟢 System Status")

st.success(
    "ScanAssist System Operational"
)

# =====================================
# TOP METRICS
# =====================================

c1, c2, c3, c4 = st.columns(4)

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

    high_risk = len(
        df[df["Risk"] == "High"]
    )

    st.metric(
        "High Risk Issues",
        high_risk
    )

with c4:

    avg_severity = int(
        df["Severity"].mean()
    )

    st.metric(
        "Avg Severity",
        avg_severity
    )

st.divider()

# =====================================
# QUICK ACTIONS
# =====================================

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        "🔧 Go to Troubleshooting page to resolve scanner issues."
    )

with col2:

    st.info(
        "📄 View generated engineer reports."
    )

with col3:

    st.info(
        "📈 Open Analytics for system insights."
    )

st.divider()

# =====================================
# RISK OVERVIEW
# =====================================

st.subheader("🚨 Risk Overview")

risk_counts = (
    df["Risk"]
    .value_counts()
)

st.bar_chart(
    risk_counts
)

st.divider()

# =====================================
# CATEGORY OVERVIEW
# =====================================

st.subheader("🗂 Procedure Categories")

category_counts = (
    df["Category"]
    .value_counts()
)

st.bar_chart(
    category_counts
)

st.divider()

# =====================================
# TOP CRITICAL ISSUES
# =====================================

st.subheader("🔥 Top Critical Procedures")

critical_df = (
    df.sort_values(
        by="Severity",
        ascending=False
    )
    .head(5)
)

for _, row in critical_df.iterrows():

    st.error(
        f"{row['Procedure']}  |  Severity {row['Severity']}/100"
    )

st.divider()

# =====================================
# RECENT KNOWLEDGE BASE
# =====================================

st.subheader("📋 Knowledge Base Overview")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# =====================================
# AI SYSTEM INSIGHTS
# =====================================

st.subheader("🤖 AI Insights")

highest = (
    df.sort_values(
        by="Severity",
        ascending=False
    )
    .iloc[0]
)

lowest = (
    df.sort_values(
        by="Severity",
        ascending=True
    )
    .iloc[0]
)

st.warning(
    f"Highest priority procedure: {highest['Procedure']} ({highest['Severity']}/100)"
)

st.success(
    f"Lowest priority procedure: {lowest['Procedure']} ({lowest['Severity']}/100)"
)

st.info(
    f"Knowledge base contains {len(df)} troubleshooting procedures."
)

st.info(
    f"Generated reports available: {report_count}"
)

st.divider()

# =====================================
# FOOTER
# =====================================

st.caption(
    "ScanAssist v1.0 | CT/MRI Troubleshooting Assistant"
)