# streamlit_app.py
import streamlit as st
import pandas as pd
from io import BytesIO

# Page config
st.set_page_config(page_title="CSV Export", layout="centered")

# === Dark Mode CSS + Enhanced UI ===
st.markdown("""
<style>
    /* Dark background */
    .main {
        background-color: #0e1117;
        color: #fafafa;
        padding: 2rem;
    }

    /* Header */
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .header h1 {
        margin: 0;
        font-size: 2.3rem;
        font-weight: 700;
        color: white;
    }
    .header p {
        margin: 0.5rem 0 0;
        color: #bfdbfe;
        font-size: 1.1rem;
    }

    /* Upload box */
    .upload-box {
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: #1a1f2d;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .upload-box:hover {
        border-color: #60a5fa;
        background: #1e293b;
        transform: translateY(-2px);
    }
    .upload-box h3 {
        margin: 0 0 0.5rem;
        color: #93c5fd;
    }
    .upload-box p {
        color: #94a3b8;
        margin: 0;
    }

    /* Preview table */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Download button with icon */
    .stDownloadButton>button {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton>button:hover {
        background: #2563eb !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #64748b;
        font-size: 0.9rem;
        border-top: 1px solid #1e293b;
    }
    .footer a {
        color: #60a5fa;
        text-decoration: none;
    }
    .footer a:hover {
        color: #93c5fd;
    }

    /* Success message */
    .success-msg {
        background: #166534;
        color: #dcfce7;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown("""
<div class="header">
    <h1>Export to Final CSV</h1>
    <p>Upload your source file • Get clean output instantly</p>
</div>
""", unsafe_allow_html=True)

# === Upload Area ===
uploaded = st.file_uploader(
    "",
    type=["xlsx", "csv"],
    label_visibility="collapsed"
)

if uploaded:
    with st.spinner("Processing your file..."):
        try:
            # Load data
            df = pd.read_excel(uploaded) if uploaded.name.endswith(".xlsx") else pd.read_csv(uploaded)

            # Rename columns exactly as in your file
            df = df.rename(columns={
                "Customer Country": "Country",
                "CreatedAt": "Created At",
                "Last Update": "Updated at"
            })

            # Build final output
            out = pd.DataFrame({
                "Lead ID": df["Lead ID"],
                "Customer Name": df["Customer Name"],
                "SKU": df["SKU"],
                "Phone": "",  # left blank
                "Country": df["Country"],
                "Status": df["Status"],
                "Created At": df["Created At"],
                "Updated at": df["Updated at"]
            })

            # Show success + preview
            st.markdown('<div class="success-msg">File processed successfully!</div>', unsafe_allow_html=True)
            st.markdown("**Preview (first 8 rows):**")
            st.dataframe(out.head(8), use_container_width=True)

            # Download button with download icon
            csv = out.to_csv(index=False, encoding="utf-8")
            st.download_button(
                label="Download final_output.csv",
                data=BytesIO(csv.encode()),
                file_name="final_output.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error: {e}")
else:
    # Upload prompt
    st.markdown("""
    <div class="upload-box">
        <h3>Drop your file here</h3>
        <p>or click to browse • Supports Excel & CSV</p>
    </div>
    """, unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<div class="footer">
    Created with <span style="color: #f43f5e;">♥</span> by 
    <a href="https://x.com/hassanelb" target="_blank">@hassanelb</a>
</div>
""", unsafe_allow_html=True)
