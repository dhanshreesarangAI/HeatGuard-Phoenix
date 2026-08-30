# 🌡️ HeatGuard Phoenix

**AI-Powered Hyperlocal Heat Risk Prediction for Phoenix, Arizona**

Built for FortyGuard Hackathon '26

## 🔗 Live Demo
[heatguard-phoenix.streamlit.app](https://heatguard-phoenix-9trdzc2zoepknrqsu7qzek.streamlit.app)

## 📖 Overview
Phoenix faces extreme urban heat, but most weather tools only show one city-wide temperature. HeatGuard Phoenix uses FortyGuard's Temperature API to deliver hyperlocal (2-meter resolution) heat risk predictions for five Phoenix areas — Downtown Phoenix, Scottsdale, Tempe, Mesa, and Glendale — along with AI-generated safety recommendations.

## ✨ Features
- Real-time hyperlocal temperature data via FortyGuard's Temperature API
- Area-wise risk classification (Low / Medium / High / Extreme)
- AI-generated, risk-specific safety recommendations
- Transparent "Why This Risk Level" explanation
- 3-hour heat forecast
- Interactive color-coded map with area highlighting

## 🛠️ Tech Stack
- Python
- Streamlit (dashboard/UI)
- Folium (interactive maps)
- Pandas (data processing)
- FortyGuard Temperature API (data source)

## 🚀 How to Run Locally
```bash
git clone https://github.com/dhanshreesarangAI/HeatGuard-Phoenix.git
cd HeatGuard-Phoenix
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure
- `collect_data.py` — Pulls temperature data from FortyGuard API for 5 Phoenix areas
- `risk_model.py` — Classifies risk levels and generates recommendations
- `app.py` — Streamlit dashboard (main application)
- `phoenix_heat_data_with_risk.csv` — Processed dataset

## 👤 Author
Dhanshree Sarang — Solo participant, FortyGuard Hackathon '26