# streamlit_app.py
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Source to Final CSV", layout="centered")
st.title("Source to Final Output CSV")

st.markdown("""
### Instructions
1. Upload your **source file** (Excel or CSV).  
2. The app will automatically:
   - Rename `Customer Country` to `Country`
   - Rename `CreatedAt` to `Created At`
   - Rename `Last Update` to `Updated at`
   - Leave `Phone` blank
3. Download `final_output.csv`
""")

# File uploader
uploaded = st.file_uploader(
    "Upload **source** file (Excel or CSV)",
    type=["xlsx", "csv"]
)

if uploaded:
    try:
        # Load file
        if uploaded.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)

        st.success("Source file loaded!")
        st.subheader("Source Preview")
        st.dataframe(df.head())

        # --- Exact column names from your file ---
        src_cols = {
            "Lead ID": "Lead ID",
            "Customer Name": "Customer Name",
            "SKU": "SKU",
            "Status": "Status",
            "Customer Country": "Country",      # rename
            "CreatedAt": "Created At",          # rename
            "Last Update": "Updated at"         # rename
        }

        # Check for missing columns
        missing = [src for src in src_cols.keys() if src not in df.columns]
        if missing:
            st.error(
                f"Missing columns in source file:\n"
                f"{', '.join(missing)}\n\n"
                "Check **exact spelling and case**."
            )
            st.stop()

        # Build output
        out = pd.DataFrame()
        out["Lead ID"] = df["Lead ID"]
        out["Customer Name"] = df["Customer Name"]
        out["SKU"] = df["SKU"]
        out["Phone"] = ""  # empty
        out["Country"] = df["Customer Country"]
        out["Status"] = df["Status"]
        out["Created At"] = df["CreatedAt"]
        out["Updated at"] = df["Last Update"]

        # Final column order
        final_order = [
            "Lead ID", "Customer Name", "SKU", "Phone",
            "Country", "Status", "Created At", "Updated at"
        ]
        out = out[final_order]

        st.subheader("Final Output Preview")
        st.dataframe(out.head(10))

        # Download button
        csv_bytes = BytesIO()
        out.to_csv(csv_bytes, index=False, encoding="utf-8")
        csv_bytes.seek(0)

        st.download_button(
            label="Download final_output.csv",
            data=csv_bytes,
            file_name="final_output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload your source file.")