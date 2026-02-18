import streamlit as st
import requests
import pandas as pd
from datetime import datetime, time
import pytz
from io import BytesIO
import zipfile

# --- APP CONFIG ---
st.set_page_config(page_title="BhavCopy Pro", page_icon="📈", layout="wide")

IST = pytz.timezone('Asia/Kolkata')

# --- 2026 NSE HOLIDAY DATA ---
HOLIDAYS_2026 = {
    "2026-01-15": "Maharashtra Municipal Elections",
    "2026-01-26": "Republic Day",
    "2026-03-03": "Holi",
    "2026-03-26": "Shri Ram Navami",
    "2026-03-31": "Shri Mahavir Jayanti",
    "2026-04-03": "Good Friday",
    "2026-04-14": "Dr. Ambedkar Jayanti",
    "2026-05-01": "Maharashtra Day",
    "2026-05-28": "Bakri Id",
    "2026-06-26": "Muharram",
    "2026-09-14": "Ganesh Chaturthi",
    "2026-10-02": "Mahatma Gandhi Jayanti",
    "2026-10-20": "Dussehra",
    "2026-11-10": "Diwali-Balipratipada",
    "2026-11-24": "Guru Nanak Jayanti",
    "2026-12-25": "Christmas"
}

def get_now_ist():
    return datetime.now(IST)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    now_ist = get_now_ist()
    today = now_ist.date()
    
    start_date = st.date_input("From Date", value=today)
    end_date = st.date_input("To Date", value=today)
    
    st.divider()
    st.markdown("### 🗓️ 2026 Market Holidays")
    holiday_df = pd.DataFrame(list(HOLIDAYS_2026.items()), columns=["Date", "Occasion"])
    st.dataframe(holiday_df, hide_index=True, use_container_width=True)

# --- MAIN UI ---
st.title("📈 BhavCopy Pro")
st.info(f"**Current IST:** {now_ist.strftime('%d %b %Y, %H:%M:%S')}")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/"
}

def fetch_data(date_obj):
    ds = date_obj.strftime("%Y%m%d")
    url = f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{ds}_F_0000.csv.zip"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        return r.content if r.status_code == 200 else None
    except:
        return None

if st.button("🚀 Download Selected Range"):
    dates = pd.date_range(start_date, end_date)
    zip_buffer = BytesIO()
    files_found = 0
    
    for d in dates:
        d_str = d.strftime("%Y-%m-%d")
        d_date = d.date()
        
        # Check Weekends
        if d_date.weekday() >= 5:
            st.warning(f"Weekend: {d_str} (Market Closed)")
            continue
            
        # Check Holidays
        if d_str in HOLIDAYS_2026:
            st.error(f"Holiday: {d_str} ({HOLIDAYS_2026[d_str]})")
            continue
            
        # Fetch File
        content = fetch_data(d_date)
        if content:
            with zipfile.ZipFile(zip_buffer, "a") as z:
                z.writestr(f"BhavCopy_{d_date.strftime('%Y%m%d')}.zip", content)
            files_found += 1
        else:
            # Availability logic for today
            expected = IST.localize(datetime.combine(d_date, time(18, 30)))
            if d_date == today and now_ist < expected:
                st.info(f"⏳ {d_str}: Report expected at 06:30 PM IST.")
            else:
                st.error(f"❌ {d_str}: Data not available on NSE servers.")

    if files_found > 0:
        st.success(f"Successfully bundled {files_found} reports!")
        st.download_button("📥 Download ZIP", zip_buffer.getvalue(), f"BhavCopy_Pro_Export.zip")
