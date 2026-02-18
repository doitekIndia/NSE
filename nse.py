import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import zipfile

# --- APP CONFIG ---
st.set_page_config(page_title="BhavCopy Pro", page_icon="📈", layout="centered")

st.title("📈 BhavCopy Pro")
st.markdown("### NSE Equity Daily Archive Downloader")

# --- UI SETTINGS ---
with st.sidebar:
    st.header("Settings")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-07-02"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-07-02"))
    st.info("Note: NSE files are usually available after 6:00 PM IST on trading days.")

# NSE Connection Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/"
}

def fetch_bhavcopy(date_obj):
    date_str = date_obj.strftime("%Y%m%d")
    url = f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{date_str}_F_0000.csv.zip"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.content
    except:
        return None
    return None

# --- EXECUTION ---
if st.button("Download BhavCopy Range"):
    if start_date > end_date:
        st.error("Error: Start date cannot be after end date.")
    else:
        dates = pd.date_range(start_date, end_date)
        zip_buffer = BytesIO()
        count = 0
        
        progress = st.progress(0)
        
        with zipfile.ZipFile(zip_buffer, "w") as master_zip:
            for i, d in enumerate(dates):
                if d.weekday() >= 5: continue # Skip weekends
                
                content = fetch_bhavcopy(d)
                if content:
                    master_zip.writestr(f"BhavCopy_{d.strftime('%Y%m%d')}.zip", content)
                    count += 1
                progress.progress((i + 1) / len(dates))

        if count > 0:
            st.success(f"Successfully retrieved {count} files!")
            st.download_button(
                label="📥 Save ZIP to Computer",
                data=zip_buffer.getvalue(),
                file_name=f"BhavCopy_Pro_Export.zip",
                mime="application/zip"
            )
        else:
            st.warning("No files found for the selected dates. Market might have been closed.")
