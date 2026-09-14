import streamlit as st
import os
import pandas as pd

st.title("📄 Reports Center")

# =====================================
# REPORTS FOLDER
# =====================================

os.makedirs(
    "reports",
    exist_ok=True
)

all_files = sorted(
    os.listdir("reports"),
    reverse=True
)

txt_files = [
    f for f in all_files
    if f.endswith(".txt")
]

pdf_files = [
    f for f in all_files
    if f.endswith(".pdf")
]

# =====================================
# DASHBOARD
# =====================================

st.subheader("📊 Report Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "TXT Reports",
        len(txt_files)
    )

with c2:
    st.metric(
        "PDF Reports",
        len(pdf_files)
    )

with c3:
    st.metric(
        "Total Reports",
        len(all_files)
    )

st.divider()

# =====================================
# SEARCH
# =====================================

st.subheader("🔍 Search Reports")

search_term = st.text_input(
    "Search by filename"
)

filtered_files = []

for file in all_files:

    if search_term.lower() in file.lower():

        filtered_files.append(file)

st.divider()

# =====================================
# REPORT LIST
# =====================================

st.subheader("📂 Available Reports")

if not filtered_files:

    st.warning(
        "No reports found."
    )

else:

    for file in filtered_files:

        file_path = os.path.join(
            "reports",
            file
        )

        with st.expander(
            f"📄 {file}"
        ):

            col1, col2, col3 = st.columns(3)

            # ==========================
            # OPEN TXT REPORT
            # ==========================

            with col1:

                if (
                    file.endswith(".txt")
                    and st.button(
                        "👁 Open",
                        key=f"open_{file}"
                    )
                ):

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    st.text_area(
                        "Report Content",
                        content,
                        height=300
                    )

            # ==========================
            # DOWNLOAD
            # ==========================

            with col2:

                with open(
                    file_path,
                    "rb"
                ) as f:

                    st.download_button(
                        "⬇ Download",
                        data=f,
                        file_name=file,
                        key=f"download_{file}"
                    )

            # ==========================
            # DELETE
            # ==========================

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{file}"
                ):

                    os.remove(
                        file_path
                    )

                    st.success(
                        f"{file} deleted"
                    )

                    st.rerun()

st.divider()

# =====================================
# REPORT TABLE
# =====================================

st.subheader(
    "📋 Report Inventory"
)

table_data = []

for file in all_files:

    file_path = os.path.join(
        "reports",
        file
    )

    size_kb = round(
        os.path.getsize(file_path) / 1024,
        2
    )

    report_type = (
        "PDF"
        if file.endswith(".pdf")
        else "TXT"
    )

    table_data.append(
        {
            "File": file,
            "Type": report_type,
            "Size (KB)": size_kb
        }
    )

if table_data:

    df = pd.DataFrame(
        table_data
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No reports available."
    )

st.divider()

# =====================================
# QUICK INSIGHTS
# =====================================

st.subheader(
    "🤖 Report Insights"
)

if len(all_files) == 0:

    st.info(
        "No reports generated yet."
    )

else:

    st.success(
        f"Total stored reports: {len(all_files)}"
    )

    st.info(
        f"PDF reports: {len(pdf_files)}"
    )

    st.info(
        f"TXT reports: {len(txt_files)}"
    )