import streamlit as st
import pandas as pd
import numpy as np
from data_pipeline.combine_data import get_combined_data
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# ---------- GLOBAL UI FIX ----------
st.markdown("""
<style>

/* Move content upward */
.block-container {
    padding-top: 1rem !important;
}

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin: 10px;
}

/* Sidebar buttons */
div.stButton {
    width: 100% !important;
}
div.stButton > button {
    width: 100% !important;
    height: 45px;
    border-radius: 10px;
    margin-bottom: 10px;
    text-align: left;
    padding-left: 15px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------- CITY DATA ----------
city_coords = {
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867)
}

# ---------- SIDEBAR ----------
with st.sidebar:

    selected_city = st.selectbox("🌍 Select City", list(city_coords.keys()))
    lat, lon = city_coords[selected_city]

    st.markdown("---")

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.menu = "Dashboard"

    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.menu = "Analytics"

    if st.button("🗺 Map", use_container_width=True):
        st.session_state.menu = "Map"

    if st.button("🚨 Alerts", use_container_width=True):
        st.session_state.menu = "Alerts"

    if st.button("🔮 Predictor", use_container_width=True):
        st.session_state.menu = "Predictor"

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

menu = st.session_state.menu

# ---------- LOAD DATA ----------
df = get_combined_data(lat, lon)

if df.empty:
    st.error("No real-time data available")
    st.stop()

# ---------- DATA ----------
pm25 = df.loc[0, "pm25"]
pm10 = df.loc[0, "pm10"]
no2 = df.loc[0, "no2"]
co = df.loc[0, "co"]
so2 = df.loc[0, "so2"]
o3 = df.loc[0, "o3"]

source = df.loc[0, "predicted_source"]
temp = df.loc[0, "temperature"]
humidity = df.loc[0, "humidity"]

# ---------- RISK ----------
def get_risk(pm):
    if pm > 150:
        return "HIGH"
    elif pm > 80:
        return "MODERATE"
    else:
        return "LOW"

risk = get_risk(pm25)

# ---------- TITLE ----------
st.markdown("""
<h1 style='text-align: center;'>🌍 EnviroScan</h1>
<p style='text-align: center;'>AI-Powered Environmental Monitoring System</p>
""", unsafe_allow_html=True)

# ---------- DASHBOARD ----------
if menu == "Dashboard":

    st.markdown(f"## 🌍 Pollution Overview - {selected_city}")

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"<div class='metric-card'><h4>PM2.5</h4><h2>{pm25}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'><h4>PM10</h4><h2>{pm10}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-card'><h4>NO2</h4><h2>{no2}</h2></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric-card'><h4>CO</h4><h2>{co}</h2></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    col5.markdown(f"<div class='metric-card'><h4>SO2</h4><h2>{so2}</h2></div>", unsafe_allow_html=True)
    col6.markdown(f"<div class='metric-card'><h4>O3</h4><h2>{o3}</h2></div>", unsafe_allow_html=True)
    col7.markdown(f"<div class='metric-card'><h4>Source</h4><h2>{source}</h2></div>", unsafe_allow_html=True)
    col8.markdown(f"<div class='metric-card'><h4>Risk</h4><h2>{risk}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    colA, colB = st.columns(2)
    colA.metric("Temperature", f"{temp} °C")
    colB.metric("Humidity", f"{humidity} %")

    # ---------- ANALYTICS ----------
elif menu == "Analytics":

    st.title(f"📊 Analytics - {selected_city}")

    # -------- TREND --------
    st.subheader("📈 Pollution Trends")

    trend_data = pd.DataFrame({
        "PM2.5": np.random.randint(max(1,int(pm25-10)), int(pm25+10), 10),
        "PM10": np.random.randint(max(1,int(pm10-10)), int(pm10+10), 10),
        "NO2": np.random.randint(max(1,int(no2-5)), int(no2+5), 10),
        "CO": np.random.randint(max(1,int(co-50)), int(co+50), 10),
        "SO2": np.random.randint(max(1,int(so2-5)), int(so2+5), 10),
        "O3": np.random.randint(max(1,int(o3-5)), int(o3+5), 10)
    })

    st.line_chart(trend_data)

    # -------- PIE CHART --------
        # -------- SOURCE DISTRIBUTION --------
    st.subheader("🌍 Source Distribution")

    source_labels = ["Vehicular", "Industrial", "Agricultural", "Burning", "Natural"]
    source_values = np.random.randint(10, 40, 5)

    pie_df = pd.DataFrame({
        "Source": source_labels,
        "Value": source_values
    })

    st.bar_chart(pie_df.set_index("Source"))

    # ---------- ALERTS ----------
elif menu == "Alerts":

    st.title(f"🚨 Alerts - {selected_city}")

    # -------- MAIN ALERT --------
    if risk == "HIGH":
        st.markdown('<div class="alert-high">🚨 HIGH POLLUTION ALERT! Stay indoors.</div>', unsafe_allow_html=True)

    elif risk == "MODERATE":
        st.markdown('<div class="alert-mid">⚠ Moderate pollution detected. Take precautions.</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="alert-low">✅ Air quality is safe.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # -------- QUICK INSIGHTS --------
    st.subheader("📌 Pollution Insights")

    st.write(f"**PM2.5 Level:** {pm25}")
    st.write(f"**Main Source:** {source}")
    st.write(f"**Risk Level:** {risk}")

    st.markdown("---")

    # -------- SOURCE DISTRIBUTION --------
    st.subheader("🌍 Source Distribution")

    source_labels = ["Vehicular", "Industrial", "Agricultural", "Burning", "Natural"]
    source_values = np.random.randint(10, 40, 5)

    pie_df = pd.DataFrame({
        "Source": source_labels,
        "Value": source_values
    })

    st.bar_chart(pie_df.set_index("Source"))

    st.markdown("---")

    # -------- RECOMMENDATION --------
    st.subheader("💡 Recommendations")

    if risk == "HIGH":
        st.error("Avoid outdoor activities. Use masks and air purifiers.")
    elif risk == "MODERATE":
        st.warning("Limit prolonged outdoor exposure.")
    else:
        st.success("Safe to go outside.")

# ---------- MAP ----------
elif menu == "Map":

    st.title("🗺 Smart Pollution Map")

    col1, col2 = st.columns(2)

    with col1:
        show_all = st.checkbox("Show All Cities", value=True)

    with col2:
        pollutant_option = st.selectbox(
            "Select Pollutant",
            ["Overall (All Pollutants)", "PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
        )

    def get_value(df, pollutant):
        return {
            "PM2.5": df.loc[0, "pm25"],
            "PM10": df.loc[0, "pm10"],
            "NO2": df.loc[0, "no2"],
            "CO": df.loc[0, "co"],
            "SO2": df.loc[0, "so2"],
            "O3": df.loc[0, "o3"]
        }[pollutant]

    def compute_score(df):
        return (
            df.loc[0, "pm25"]/150 +
            df.loc[0, "pm10"]/150 +
            df.loc[0, "no2"]/200 +
            df.loc[0, "co"]/500 +
            df.loc[0, "so2"]/100 +
            df.loc[0, "o3"]/200
        )

    m = folium.Map(location=[20, 78], zoom_start=5)

    all_data = []
    city_scores = []

    for city, (clat, clon) in city_coords.items():

        temp_df = get_combined_data(clat, clon)
        if temp_df.empty:
            continue

        if pollutant_option == "Overall (All Pollutants)":
            val = compute_score(temp_df)
        else:
            val = get_value(temp_df, pollutant_option)

        all_data.append([clat, clon, val])
        city_scores.append((city, clat, clon, val))

    max_val = max([d[2] for d in all_data]) if all_data else 1

    from folium.plugins import HeatMap
    HeatMap([[a,b,c/max_val] for a,b,c in all_data]).add_to(m)

    top_city = max(city_scores, key=lambda x: x[3])

    for city, clat, clon, val in city_scores:
        color = "red" if city == top_city[0] else "blue"
        folium.Marker([clat, clon], tooltip=city,
                      popup=f"{city}: {round(val,2)}",
                      icon=folium.Icon(color=color)).add_to(m)

    # ---------- MAP + LEGEND ----------
    map_col, legend_col = st.columns([4,1])

    with map_col:
        st_folium(m, width=900, height=500)

    with legend_col:
        st.markdown("### 🌈 Legend")
        st.markdown("""
        🔴 High Pollution  
        🟠 Moderate  
        🔵 Low  
        
        📍 Red Marker → Highest city  
        📍 Blue → Others
        """)

    st.info("Composite pollution index (all pollutants combined)")

# ---------- PREDICTOR ----------
elif menu == "Predictor":

    st.title(f"🔮 Future Prediction - {selected_city}")

    pollutant = st.selectbox("Select Pollutant", ["PM2.5","PM10","NO2","CO","SO2","O3"])
    future_date = st.date_input("Future Date")

    temp_input = st.slider("Temperature", 10, 45, int(temp))
    humidity_input = st.slider("Humidity", 10, 100, int(humidity))
    traffic = st.slider("Traffic", 0, 100, 50)

    if st.button("Predict"):

        base = {"PM2.5":pm25,"PM10":pm10,"NO2":no2,"CO":co,"SO2":so2,"O3":o3}[pollutant]

        pred = base + (traffic*0.2) - (humidity_input*0.1) + (temp_input*0.1)

        st.metric("Prediction", round(pred,2))