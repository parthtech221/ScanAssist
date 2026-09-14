import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF

st.title("🔧 Troubleshooting")

with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

machine = st.text_input("Machine Type")
model = st.text_input("Machine Model")
error = st.text_input("Error Message")

if st.button("Search Procedure"):

    if error in procedures:

        data = procedures[error]

        risk = data["risk"]

        st.success("Procedure Found")

        st.metric("Risk Level", risk)

        if risk == "High":
            st.error("Immediate engineer attention required.")
        elif risk == "Medium":
            st.warning("Follow troubleshooting steps carefully.")
        else:
            st.success("Low risk issue.")

        completed = []

        st.subheader("Checklist")

        for step in data["steps"]:

            if st.checkbox(step):
                completed.append(step)

        progress = len(completed) / len(data["steps"])

        st.progress(progress)

        st.write(
            f"Completed {len(completed)} / {len(data['steps'])}"
        )

        resolved = st.radio(
            "Issue Resolved?",
            ["Yes", "No"]
        )

        if resolved == "No":

            if st.button("Generate Engineer Report"):

                report = f"""
SCANASSIST ENGINEER REPORT

Machine: {machine}
Model: {model}
Error: {error}
Risk: {risk}

Completed Steps:
"""

                for step in completed:
                    report += f"\n[DONE] {step}"

                report += """

Status:
UNRESOLVED

Recommendation:
Engineer Required
"""

                os.makedirs(
                    "reports",
                    exist_ok=True
                )

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                txt_file = (
                    f"reports/report_{timestamp}.txt"
                )

                with open(
                    txt_file,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(report)

                pdf_file = (
                    f"reports/report_{timestamp}.pdf"
                )

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font(
                    "Arial",
                    size=12
                )

                for line in report.splitlines():

                    if line.strip():
                        pdf.cell(
                            190,
                            8,
                            txt=line[:100],
                            ln=True
                        )
                    else:
                        pdf.ln(5)

                pdf.output(pdf_file)

                st.success(
                    "Report Generated"
                )