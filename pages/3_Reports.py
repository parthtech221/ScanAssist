import streamlit as st
import os

st.title("📄 Reports")

os.makedirs(
    "reports",
    exist_ok=True
)

files = sorted(
    os.listdir("reports"),
    reverse=True
)

if not files:

    st.warning(
        "No reports found."
    )

else:

    for file in files:

        path = os.path.join(
            "reports",
            file
        )

        st.markdown(f"### 📄 {file}")

        if file.endswith(".txt"):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                st.text_area(
                    file,
                    f.read(),
                    height=200
                )