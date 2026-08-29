import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="HeatGuard Phoenix", page_icon="🌡️", layout="wide")

# Load data
df = pd.read_csv("phoenix_heat_data_with_risk.csv")

# Area coordinates (center points for map)
AREA_COORDS = {
    "Downtown Phoenix": [33.4475, -112.0775],
    "Scottsdale": [33.4975, -111.9225],
    "Tempe": [33.4225, -111.9375],
    "Mesa": [33.4175, -111.8275],
    "Glendale": [33.5425, -112.1875]
}

# Risk level colors
RISK_COLORS = {
    "Low": "green",
    "Medium": "orange",
    "High": "red",
    "Extreme": "darkred"
}

# Header
st.title("🌡️ HeatGuard Phoenix")
st.markdown("### AI-Powered Hyperlocal Heat Risk Prediction for Phoenix, Arizona")
st.markdown("---")

# Layout: two columns
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Select an Area")
    selected_area = st.selectbox("Choose a Phoenix area:", df["area"].tolist())
    
    row = df[df["area"] == selected_area].iloc[0]
    
    st.metric("Current Temperature", f"{row['avg_temp']:.1f}°C")
    
    risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Extreme": "🔴"}
    st.markdown(f"### Risk Level: {risk_color[row['risk_level']]} {row['risk_level']}")
    
    st.info(f"**AI Recommendation:**\n\n{row['recommendation']}")

    # Next 3 hours forecast
    st.markdown("---")
    st.subheader("Next 3 Hours Forecast")
    
    current_hour = 14
    forecast_hours = [15, 16, 17]
    predicted_temps = []
    for h in forecast_hours:
        if h <= 16:
            temp_change = 0.3 * (h - current_hour)
        else:
            temp_change = 0.6 - 0.4 * (h - 16)
        predicted_temps.append(row["avg_temp"] + temp_change)
    
    forecast_cols = st.columns(3)
    for i, (h, t) in enumerate(zip(forecast_hours, predicted_temps)):
        with forecast_cols[i]:
            time_label = f"{h-12}:00 PM"
            st.metric(time_label, f"{t:.1f}°C")

    # Explanation section   # Explanation section
    st.markdown("---")
    st.subheader("Why This Risk Level?")
    
    avg_city_temp = df["avg_temp"].mean()
    temp_diff = row["avg_temp"] - avg_city_temp
    
    if temp_diff > 0.1:
        comparison = f"This area is **{temp_diff:.1f}°C hotter** than the Phoenix city average ({avg_city_temp:.1f}°C)."
    elif temp_diff < -0.1:
        comparison = f"This area is **{abs(temp_diff):.1f}°C cooler** than the Phoenix city average ({avg_city_temp:.1f}°C)."
    else:
        comparison = f"This area is close to the Phoenix city average ({avg_city_temp:.1f}°C)."
    
    st.write(comparison)
    
    explanation_map = {
        "Low": "Temperature is within a safe range for most outdoor activities.",
        "Medium": "Temperature is elevated enough to require basic precautions during peak sun hours.",
        "High": "Temperature poses a real health risk during midday hours, especially for vulnerable groups.",
        "Extreme": "Temperature has reached dangerous levels — heat-related illness risk is significant even for short outdoor exposure."
    }
    
    st.write(f"**Risk basis:** {explanation_map[row['risk_level']]}")
    
    st.markdown("---")
    st.subheader("All Areas Overview")
    st.dataframe(df[["area", "avg_temp", "risk_level"]], hide_index=True)

with col2:
    st.subheader("Phoenix Heat Risk Map")
    
    # Create map centered on Phoenix
    m = folium.Map(location=[33.45, -112.0], zoom_start=10)
    
    for _, area_row in df.iterrows():
        area_name = area_row["area"]
        coords = AREA_COORDS[area_name]
        risk = area_row["risk_level"]
        temp = area_row["avg_temp"]
        
        is_selected = (area_name == selected_area)
        
        folium.CircleMarker(
            location=coords,
            radius=30 if is_selected else 18,
            popup=f"{area_name}: {temp:.1f}°C ({risk} Risk)",
            tooltip=area_name,
            color="blue" if is_selected else RISK_COLORS[risk],
            weight=4 if is_selected else 2,
            fill=True,
            fillColor=RISK_COLORS[risk],
            fillOpacity=0.9 if is_selected else 0.6
        ).add_to(m)
        
        if is_selected:
            folium.map.Marker(
                coords,
                icon=folium.DivIcon(html=f'<div style="font-size: 24px;">📍</div>')
            ).add_to(m)
    
    st_folium(m, width=700, height=500)

st.markdown("---")
st.caption("Data powered by FortyGuard Temperature API | Built for FortyGuard Hackathon '26")