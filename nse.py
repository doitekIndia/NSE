import streamlit as st
import requests
import pandas as pd
from datetime import timedelta
from io import BytesIO
import zipfile

# App Configuration
st.set_page_config(page_title="NSE Multi-Date Downloader", page_icon="📅")

st.title("📈 NSE BhavCopy Range Downloader")
st.markdown("Select a date range to download multiple BhavCopy files at once.")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("Download Settings")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2025-07-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-07-05"))

# NSE Header Configuration
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/all-reports"
}

def get_url(date_obj):
    """Constructs the NSE URL for a specific date."""
    date_str = date_obj.strftime("%Y%m%d")
    return f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{date_str}_F_0000.csv.zip"

def download_file(url):
    """Attempts to download the file from NSE."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# --- MAIN LOGIC ---
if st.button("Download All Files in Range"):
    if start_date > end_date:
        st.error("Error: Start date must be before end date.")
    else:
        # Generate list of dates
        date_list = pd.date_range(start=start_date, end=end_date).tolist()
        
        # We will store successful downloads in an in-memory ZIP
        zip_buffer = BytesIO()
        found_files = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as master_zip:
            for i, current_date in enumerate(date_list):
                # Skip weekends
                if current_date.weekday() >= 5:
                    continue
                
                url = get_url(current_date)
                status_text.text(f"Checking {current_date.strftime('%d-%b-%Y')}...")
                
                content = download_file(url)
                if content:
                    # Save the individual zip into our master zip
                    master_zip.writestr(f"BhavCopy_{current_date.strftime('%Y%m%d')}.zip", content)
                    found_files += 1
                
                # Update progress
                progress = (i + 1) / len(date_list)
                progress_bar.progress(progress)

        if found_files > 0:
            st.success(f"Done! Found {found_files} files.")
            zip_buffer.seek(0)
            
            st.download_button(
                label=f"💾 Download Combined ZIP ({found_files} files)",
                data=zip_buffer,
                file_name=f"NSE_BhavCopies_{start_date}_to_{end_date}.zip",
                mime="application/zip"
            )
        else:
            st.warning("No files found for the selected range. Note: NSE does not publish files on weekends or holidays.")

---

### Key Features of this Version:
1.  **Date Range Picker**: Located in the sidebar for a cleaner UI.
2.  **Weekend Skipping**: Automatically ignores Saturdays and Sundays to speed up the process.
3.  **Master ZIP Creation**: Instead of downloading files one-by-one, it bundles all found BhavCopies into a single `.zip` file for you to download with one click.
4.  **Progress Indicators**: Shows you exactly which date the script is currently processing.

**Would you like me to add a feature that combines all the CSVs into a single Excel file instead of a ZIP?**
