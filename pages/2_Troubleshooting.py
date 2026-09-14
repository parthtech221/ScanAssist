import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF
from difflib import get_close_matches

st.title("🔧 Troubleshooting")

# =====================================
# LOAD PROCEDURES
# =====================================

with open("procedures.json", "r", encoding="utf-8") as f:
    procedures = json.load(f)

# =====================================
# SESSION STATE
# =====================================

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

# =====================================
# SMART SEARCH
# =====================================

def find_procedure(user_input):

    if user_input in procedures:
        return user_input

    user_lower = user_input.lower()

    for procedure in procedures.keys():

        proc_lower = procedure.lower()

        if user_lower in proc_lower:
            return procedure

        words = user_lower.split()

        if all(word in proc_lower for word in words):
            return procedure

    matches = get_close_matches(
        user_input,
        procedures.keys(),
        n=1,
        cutoff=0.4
    )

    if matches:
        return matches[0]

    return None

# =====================================
# INPUTS
# =====================================

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

if st.button("🔍 Search Procedure"):

    st.session_state.machine = machine
    st.session_state.model = model
    st.session_state.error = error
    st.session_state.searched = True

# =====================================
# SEARCH RESULTS
# =====================================

if st.session_state.searched:

    found_error = find_procedure(
        st.session_state.error
    )

    if found_error:

        data = procedures[found_error]

        risk = data["risk"]
        category = data["category"]
        severity = data["severity"]
        est_time = data["estimated_time"]

        st.success("Procedure Found")

        if found_error != st.session_state.error:

            st.info(
                f"Closest Match: {found_error}"
            )

        # ==============================
        # METRICS
        # ==============================

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Risk",
                risk
            )

        with c2:
            st.metric(
                "Category",
                category
            )

        with c3:
            st.metric(
                "Severity",
                f"{severity}/100"
            )

        with c4:
            st.metric(
                "Estimated Time",
                est_time
            )

        st.divider()

        # ==============================
        # PRIORITY SCORE
        # ==============================

        st.subheader("🚨 Engineer Priority Score")

        st.progress(
            severity / 100
        )

        st.write(
            f"Priority Score: {severity}/100"
        )

        if severity >= 90:

            st.error(
                "Critical Priority"
            )

        elif severity >= 60:

            st.warning(
                "Medium Priority"
            )

        else:

            st.success(
                "Low Priority"
            )

        st.divider()

        # ==============================
        # AI RECOMMENDATION ENGINE
        # ==============================

        st.subheader(
            "🤖 AI Recommendation"
        )

        if risk == "High":

            st.error(
                "Immediate engineer inspection recommended."
            )

            st.write(
                "- High severity issue detected"
            )

            st.write(
                "- Stop non-essential operations"
            )

            st.write(
                "- Escalate immediately"
            )

        elif risk == "Medium":

            st.warning(
                "Complete troubleshooting steps before escalation."
            )

            st.write(
                "- Follow all procedures carefully"
            )

            st.write(
                "- Monitor system behavior"
            )

            st.write(
                "- Escalate if unresolved"
            )

        else:

            st.success(
                "Continue standard troubleshooting."
            )

            st.write(
                "- Low operational risk"
            )

            st.write(
                "- Engineer escalation not immediately required"
            )

        st.divider()

        # ==============================
        # SIMILAR ISSUES
        # ==============================

        st.subheader(
            "🔎 Similar Issues"
        )

        for procedure_name, info in procedures.items():

            if (
                info["category"]
                == category
                and procedure_name != found_error
            ):

                st.write(
                    f"• {procedure_name}"
                )

        st.divider()

        # ==============================
        # CHECKLIST
        # ==============================

        st.subheader(
            "📋 Troubleshooting Checklist"
        )

        completed_steps = []

        total_steps = len(
            data["steps"]
        )

        for index, step in enumerate(
            data["steps"]
        ):

            checked = st.checkbox(
                step,
                key=f"{found_error}_{index}"
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
            f"Completed {len(completed_steps)} of {total_steps} steps"
        )

        st.divider()

        # ==============================
        # RESOLUTION CHANCE
        # ==============================

        st.subheader(
            "📈 Estimated Resolution Chance"
        )

        chance = int(
            progress * 100
        )

        st.metric(
            "Resolution Probability",
            f"{chance}%"
        )

        st.divider()

        # ==============================
        # RESOLUTION STATUS
        # ==============================

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
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Machine:
{st.session_state.machine}

Model:
{st.session_state.model}

Error:
{found_error}

Risk:
{risk}

Category:
{category}

Severity:
{severity}/100

Estimated Resolution Time:
{est_time}

Completed Steps:
"""

                if completed_steps:

                    for step in completed_steps:

                        report += f"\n[DONE] {step}"

                else:

                    report += "\nNo steps completed"

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
                ) as file:

                    file.write(report)

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

                pdf.output(
                    pdf_file
                )

                st.success(
                    "✅ Report Generated"
                )

                st.download_button(
                    "⬇ Download TXT",
                    report,
                    file_name="Engineer_Report.txt"
                )

                with open(
                    pdf_file,
                    "rb"
                ) as pdf_download:

                    st.download_button(
                        "⬇ Download PDF",
                        pdf_download,
                        file_name="Engineer_Report.pdf",
                        mime="application/pdf"
                    )

    else:

        st.error(
            "❌ No matching procedure found."
        )

        st.info(
            "Try keywords such as cooling, helium, power, network, scanner."
        )