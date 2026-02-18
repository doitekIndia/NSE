📈 BhavCopy Pro
BhavCopy Pro is a lightweight, high-performance web application built with Streamlit to automate the downloading of daily Equity BhavCopy (price reports) from the National Stock Exchange of India (NSE).

Live App: bhavcopypro.streamlit.app

✨ Features
Automated Fetching: Accesses the nsearchives server directly.

Dynamic Date Selection: Defaults to the current date on launch.

Bulk Downloads: Select a "From" and "To" date range to download multiple reports bundled into a single .zip file.

Smart Availability Timer: If a file isn't available yet (before 6:30 PM IST), the app provides a countdown.

Holiday Awareness: Includes a built-in 2026 NSE Market Holiday calendar to explain why data might be missing on specific dates.

Weekend Skipping: Automatically identifies and notifies users of weekend market closures.

Clean UI: Professional dashboard with India Standard Time (IST) synchronization.

🚀 Installation & Local Setup
If you want to run this project locally:

Clone the repository:

Bash
git clone https://github.com/your-username/bhavcopy-pro.git
cd bhavcopy-pro
Install dependencies:

Bash
pip install -r requirements.txt
Run the app:

Bash
streamlit run streamlit_app.py
🛠️ Tech Stack
Python: Core logic.

Streamlit: Web interface and deployment.

Pandas: Date range handling and data structures.

Requests: Handling HTTP calls to NSE archives with custom headers to bypass bot blocks.

Pytz: Precise India Standard Time (IST) synchronization.

📁 Project Structure
Plaintext
├── streamlit_app.py     # Main Python application
├── requirements.txt      # List of Python dependencies
└── README.md             # Project documentation
📋 Requirements.txt
The app requires the following libraries:

Plaintext
streamlit
requests
pandas
pytz
📝 Usage Note
The NSE typically uploads the final BhavCopy for the day between 06:00 PM and 08:00 PM IST. This app is optimized to check for the file and notify the user if the server has not yet published the data.

⚖️ Disclaimer
This tool is for educational and personal use only. BhavCopy Pro is not affiliated with the National Stock Exchange of India (NSE). Users should ensure they comply with NSE's data usage policies.

Developed with ❤️ for the Trading Community.
