import streamlit as st
import json
import os

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ScanAssist",
    page_icon="🩺",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

os.makedirs("reports", exist_ok=True)

report_count = len(
    [
        f for f in os.listdir("reports")
        if f.endswith(".txt")
    ]
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown(
    """
    <style>

    .hero {
        padding: 30px;
        border-radius: 15px;
        background: linear-gradient(135deg,#0f172a,#1e3a8a);
        color:white;
        text-align:center;
        margin-bottom:20px;
    }

    .feature-box {
        padding:20px;
        border-radius:10px;
        border:1px solid #ddd;
        text-align:center;
        height:180px;
    }

    .metric-box {
        padding:15px;
        border-radius:10px;
        background:#f8f9fa;
        border:1px solid #ddd;
        text-align:center;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# HERO SECTION
# =====================================

st.markdown(
    """
    <div class="hero">
        <h1>🩺 ScanAssist</h1>
        <h3>Safety-First CT/MRI Troubleshooting Assistant</h3>
        <p>
        Helping technologists follow approved troubleshooting procedures,
        reduce downtime, and generate engineer handover reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# TOP METRICS
# =====================================

st.subheader("📊 System Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Knowledge Base",
        len(procedures)
    )

with c2:
    st.metric(
        "Reports Generated",
        report_count
    )

with c3:
    st.metric(
        "System Status",
        "Online"
    )

with c4:
    st.metric(
        "Version",
        "1.0"
    )

st.divider()

# =====================================
# FEATURES
# =====================================

st.subheader("✨ Core Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-box">
        <h3>🔧</h3>
        <h4>Troubleshooting</h4>
        <p>Search approved CT/MRI troubleshooting procedures.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
        <h3>🤖</h3>
        <h4>AI Guidance</h4>
        <p>Receive intelligent recommendations based on issue severity.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-box">
        <h3>📄</h3>
        <h4>Engineer Reports</h4>
        <p>Generate structured escalation reports instantly.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="feature-box">
        <h3>📈</h3>
        <h4>Analytics</h4>
        <p>Track risk levels, trends, and operational insights.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =====================================
# WORKFLOW
# =====================================

st.subheader("🔄 How ScanAssist Works")

st.markdown(
    """
    ### Step 1
    Enter machine type, model, and error message.

    ⬇️

    ### Step 2
    ScanAssist finds the best troubleshooting procedure.

    ⬇️

    ### Step 3
    Follow the guided checklist and safety recommendations.

    ⬇️

    ### Step 4
    If unresolved, generate an engineer escalation report.

    ⬇️

    ### Step 5
    Track reports and analytics from the dashboard.
    """
)

st.divider()

# =====================================
# KNOWLEDGE BASE PREVIEW
# =====================================

st.subheader("📚 Knowledge Base Preview")

preview_data = []

for name, info in procedures.items():

    preview_data.append(
        {
            "Procedure": name,
            "Risk": info["risk"],
            "Category": info["category"],
            "Severity": info["severity"]
        }
    )

st.dataframe(
    preview_data,
    use_container_width=True
)

st.divider()

# =====================================
# QUICK ACCESS
# =====================================

st.subheader("🚀 Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        "🔧 Open Troubleshooting page to resolve issues."
    )

with col2:
    st.info(
        "📄 Open Reports page to manage generated reports."
    )

with col3:
    st.warning(
        "📈 Open Analytics page for system insights."
    )

st.divider()

# =====================================
# FOOTER
# =====================================

st.caption(
    "ScanAssist v1.0 | CT/MRI Troubleshooting Assistant | Internship Project"
)