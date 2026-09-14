import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF

st.title("🔧 Troubleshooting")

# =========================
# LOAD PROCEDURES
# =========================

with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

# =========================
# SESSION STATE
# =========================

defaults = {
    "machine": "",
    "model": "",
    "error": "",
    "searched": False,
    "resolved": "No"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# INPUTS
# =========================

machine = st.text_input(
    "Machine Type",
    value=st.session_state.machine
)

model = st.text_input(
    "Machine Model",
    value=st.session_state.model
)

error = st.text_input(
    "Error Message",
    value=st.session_state.error
)

# =========================
# SEARCH
# =========================

if st.button("🔍 Search Procedure"):

    st.session_state.machine = machine
    st.session_state.model = model
    st.session_state.error = error
    st.session_state.searched = True

# =========================
# SHOW RESULT
# =========================

if st.session_state.searched:

    error = st.session_state.error

    if error in procedures:

        data = procedures[error]

        risk = data["risk"]

        st.success("Procedure Found")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Machine",
                st.session_state.machine
            )

        with col2:
            st.metric(
                "Model",
                st.session_state.model
            )

        with col3:
            st.metric(
                "Risk",
                risk
            )

        st.divider()

        # =========================
        # RISK ASSESSMENT
        # =========================

        st.subheader("Risk Assessment")

        if risk == "High":

            st.error(
                "🔴 HIGH RISK"
            )

            st.info(
                "Recommendation: Escalate to engineer immediately."
            )

        elif risk == "Medium":

            st.warning(
                "🟡 MEDIUM RISK"
            )

            st.info(
                "Recommendation: Complete troubleshooting before escalation."
            )

        else:

            st.success(
                "🟢 LOW RISK"
            )

            st.info(
                "Recommendation: Continue normal troubleshooting."
            )

        st.divider()

        # =========================
        # CHECKLIST
        # =========================

        st.subheader(
            "Troubleshooting Checklist"
        )

        completed_steps = []

        total_steps = len(
            data["steps"]
        )

        for index, step in enumerate(
            data["steps"]
        ):

            checkbox_key = (
                f"{error}_step_{index}"
            )

            checked = st.checkbox(
                step,
                key=checkbox_key
            )

            if checked:
                completed_steps.append(
                    step
                )

        progress = (
            len(completed_steps)
            / total_steps
        )

        st.progress(progress)

        st.write(
            f"Completed {len(completed_steps)} / {total_steps} steps"
        )

        st.divider()

        # =========================
        # RESOLUTION
        # =========================

        resolved = st.radio(
            "Issue Resolved?",
            ["Yes", "No"],
            key="resolved"
        )

        if resolved == "Yes":

            st.success(
                "✅ Case Closed Successfully"
            )

        else:

            st.error(
                "❌ Issue Not Resolved"
            )

            if st.button(
                "📄 Generate Engineer Report"
            ):

                report = f"""
SCANASSIST ENGINEER REPORT

Generated:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Machine:
{st.session_state.machine}

Model:
{st.session_state.model}

Error:
{error}

Risk:
{risk}

Completed Steps:
"""

                if completed_steps:

                    for step in completed_steps:

                        report += (
                            f"\n[DONE] {step}"
                        )

                else:

                    report += (
                        "\nNo steps completed"
                    )

                report += """

Status:
UNRESOLVED

Recommendation:
Engineer Inspection Required
"""

                os.makedirs(
                    "reports",
                    exist_ok=True
                )

                timestamp = (
                    datetime.now()
                    .strftime(
                        "%Y%m%d_%H%M%S"
                    )
                )

                txt_file = (
                    f"reports/report_{timestamp}.txt"
                )

                with open(
                    txt_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(report)

                # =========================
                # PDF
                # =========================

                pdf_file = (
                    f"reports/report_{timestamp}.pdf"
                )

                pdf = FPDF()

                pdf.add_page()

                pdf.set_auto_page_break(
                    auto=True,
                    margin=15
                )

                pdf.set_font(
                    "Arial",
                    size=12
                )

                for line in report.splitlines():

                    if line.strip() == "":

                        pdf.ln(5)

                    else:

                        pdf.cell(
                            190,
                            8,
                            txt=line[:100],
                            ln=True
                        )

                pdf.output(
                    pdf_file
                )

                st.success(
                    "✅ Report Generated"
                )

                st.text_area(
                    "Engineer Report",
                    report,
                    height=300
                )

                st.download_button(
                    label="⬇ Download TXT",
                    data=report,
                    file_name="Engineer_Report.txt",
                    mime="text/plain"
                )

                with open(
                    pdf_file,
                    "rb"
                ) as pdf_download:

                    st.download_button(
                        label="⬇ Download PDF",
                        data=pdf_download,
                        file_name="Engineer_Report.pdf",
                        mime="application/pdf"
                    )

    else:

        st.error(
            "❌ Procedure Not Found"
        )