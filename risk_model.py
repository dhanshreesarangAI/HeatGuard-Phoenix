import pandas as pd

# Load collected data
df = pd.read_csv("phoenix_heat_data.csv")

def get_risk_level(temp):
    """Classify temperature into risk categories"""
    if temp < 35:
        return "Low"
    elif temp < 40:
        return "Medium"
    elif temp < 43:
        return "High"
    else:
        return "Extreme"

def get_recommendation(risk_level):
    """Give AI recommendation based on risk"""
    recommendations = {
        "Low": "Safe for outdoor activities. Stay hydrated as a general precaution.",
        "Medium": "Take breaks in shade during peak hours (12 PM - 3 PM). Drink water regularly.",
        "High": "Avoid strenuous outdoor activity between 12 PM - 4 PM. Stay hydrated every 30 minutes.",
        "Extreme": "Avoid all outdoor activity between 12 PM - 4 PM. Seek air-conditioned spaces. Check on elderly/vulnerable individuals."
    }
    return recommendations[risk_level]

# Apply risk scoring
df["risk_level"] = df["avg_temp"].apply(get_risk_level)
df["recommendation"] = df["risk_level"].apply(get_recommendation)

# Save updated data
df.to_csv("phoenix_heat_data_with_risk.csv", index=False)

print("✅ Risk analysis complete!\n")
print(df[["area", "avg_temp", "risk_level"]])
print("\n--- Recommendations ---")
for _, row in df.iterrows():
    print(f"\n{row['area']} ({row['risk_level']} Risk):")
    print(f"  {row['recommendation']}")