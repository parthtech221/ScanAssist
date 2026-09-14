import streamlit as st

st.set_page_config(
    page_title="ScanAssist",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 ScanAssist")

st.markdown("""
### Safety-First CT/MRI Troubleshooting Assistant

Use the sidebar to navigate:

- Dashboard
- Troubleshooting
- Reports
- Analytics
""")

st.info(
    "ScanAssist helps CT/MRI technologists follow approved troubleshooting procedures and generate engineer reports."
)