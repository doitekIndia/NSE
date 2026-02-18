import streamlit as st
import requests
import pandas as pd
from datetime import date
from io import BytesIO
import zipfile

# --- APP CONFIG ---
st.set_page_config(page_title="BhavCopy Pro", page_icon="📈", layout="centered")

st.title("📈 BhavCopy Pro")
st.markdown("### NSE Equity Daily Archive Downloader")

# --- UI SETTINGS ---
with st.sidebar:
    st.header("Settings")
    
    # Automatically set to the current date when the user opens the app
    today = date.today()
    
    start_date = st.date_input("Start Date", value=today)
    end_date = st.date_input("End Date", value=today)
    
    st.info(f"Today is: {today.strftime('%A, %d %b %Y')}")
    st.caption("Note: NSE files are typically available after 6:00 PM IST.")

# NSE Connection Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/"
}

def fetch_bhavcopy(date_obj):
    # Formats date to YYYYMMDD for the URL
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
if st.button("🚀 Download BhavCopy Range"):
    if start_date > end_date:
        st.error("Error: Start date cannot be after end date.")
    elif end_date > today:
        st.warning("Future dates are not available. Please select today or a past date.")
    else:
        # Create a range of dates
        dates = pd.date_range(start_date, end_date)
        zip_buffer = BytesIO()
        count = 0
        
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        with zipfile.ZipFile(zip_buffer, "w") as master_zip:
            for i, d in enumerate(dates):
                # Skip weekends (Saturday=5, Sunday=6)
                if d.weekday() >= 5:
                    continue
                
                progress_text.text(f"Fetching: {d.strftime('%Y-%m-%d')}...")
                content = fetch_bhavcopy(d)
                
                if content:
                    master_zip.writestr(f"BhavCopy_{d.strftime('%Y%m%d')}.zip", content)
                    count += 1
                
                # Update progress
                progress_bar.progress((i + 1) / len(dates))

        progress_text.empty()

        if count > 0:
            st.success(f"Success! Collected {count} files.")
            st.download_button(
                label=f"📥 Download {count} Reports (ZIP)",
                data=zip_buffer.getvalue(),
                file_name=f"BhavCopy_Pro_{start_date}_to_{end_date}.zip",
                mime="application/zip"
            )
        else:
            st.error("No files found. Check if the market was closed or if the report hasn't been uploaded yet.")
