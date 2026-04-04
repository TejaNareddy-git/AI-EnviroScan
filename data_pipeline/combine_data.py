import pandas as pd
from data_pipeline.fetch_pollution import fetch_pollution_data
from data_pipeline.fetch_weather import fetch_weather
from data_pipeline.source_predictor import predict_source

def get_combined_data(lat, lon):

    pollution_df = fetch_pollution_data(lat, lon)

    if pollution_df.empty:
        return pd.DataFrame()

    weather = fetch_weather(lat, lon)
    weather_df = pd.DataFrame([weather])

    final_df = pd.concat([pollution_df, weather_df], axis=1)

    final_df["predicted_source"] = final_df.apply(predict_source, axis=1)

    return final_df