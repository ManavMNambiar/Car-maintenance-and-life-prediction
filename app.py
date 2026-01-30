import streamlit as st
import joblib
import pandas as pd

# ---------------------------------
# Page config (MUST be first Streamlit command)
# ---------------------------------
st.set_page_config(page_title="Car Health Prediction", layout="wide")
st.markdown(
    """
    <style>
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(
            120deg,
            #0f4c81,
            #3b82c4,
            #a7c7e7,
            #3b82c4,
            #0f4c81
        );
        background-size: 600% 600%;
        animation: gradientFlow 20s ease infinite;
        color: black;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Force all text to black */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: black !important;
    }

    /* Make input boxes readable */
    input, textarea {
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: black !important;
    }

    /* Buttons */
    button {
        background-color: #1f6fb2 !important;
        color: white !important;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.title("🚗 Car Maintenance & Remaining Life Prediction")
st.markdown("Enter vehicle details below to check component-wise and overall health.")

# ---------------------------------
# Load models
# ---------------------------------
engine_model = joblib.load("engine_model.pkl")
transmission_model = joblib.load("transmission_model.pkl")
brakes_model = joblib.load("brakes_model.pkl")
electronics_model = joblib.load("electronics_model.pkl")
body_model = joblib.load("body_model.pkl")

# Utility functions

def maintenance_status(module, years):
    rules = {
        "Engine": (2, 5),
        "Transmission": (2, 5),
        "Brakes & Suspension": (2.5, 4),
        "Electronics": (2, 4),
        "Body": (3, 6)
    }

    imm, service = rules[module]

    if years < imm:
        return "Immediate Repair"
    elif years < service:
        return "Service Soon"
    else:
        return "Healthy"


st.header("🔧 Engine")

Oil_Level = st.number_input("Oil Level (%)", 0.0, 100.0, 60.0)
Oil_Quality_Score = st.number_input("Oil Quality Score (0–10)", 0.0, 10.0, 7.0)
Avg_Engine_Temp = st.number_input("Average Engine Temperature (°C)", 60.0, 140.0, 90.0)
Engine_Damage_Score = st.number_input("Engine Damage Score (0–10)", 0.0, 10.0, 3.0)
Overheat_Events = st.number_input("Overheat Events", 0, 20, 1, step=1)
Km_Driven = st.number_input("Kilometers Driven", 0.0, 1000000.0, 80000.0)

engine_input_df = pd.DataFrame([{
    "Oil_Level": Oil_Level,
    "Oil_Quality_Score": Oil_Quality_Score,
    "Avg_Engine_Temp": Avg_Engine_Temp,
    "Engine_Damage_Score": Engine_Damage_Score,
    "Overheat_Events": Overheat_Events,
    "Km_Driven": Km_Driven
}])

engine_years = engine_model.predict(engine_input_df)[0]



st.header("⚙️ Transmission")

Gear_Slip_Frequency = st.number_input("Gear Slip Frequency", 0, 30, 1, step=1)
Clutch_Wear_Percentage = st.number_input("Clutch Wear (%)", 0.0, 100.0, 40.0)
Transmission_Temp = st.number_input("Transmission Temperature (°C)", 60.0, 140.0, 90.0)
Axle_Wear_Score = st.number_input("Axle Wear Score (0–10)", 0.0, 10.0, 4.0)

transmission_input_df = pd.DataFrame([{
    "Gear_Slip_Frequency": Gear_Slip_Frequency,
    "Clutch_Wear_Percentage": Clutch_Wear_Percentage,
    "Transmission_Temp": Transmission_Temp,
    "Axle_Wear_Score": Axle_Wear_Score
}])

transmission_years = transmission_model.predict(transmission_input_df)[0]



st.header("🛑 Brakes & Suspension")

Brake_Pad_Wear = st.number_input("Brake Pad Wear (%)", 0.0, 100.0, 50.0)
Brake_Fluid_Level = st.number_input("Brake Fluid Level (%)", 0.0, 100.0, 70.0)
Suspension_Stiffness = st.number_input("Suspension Stiffness (0–10)", 0.0, 10.0, 6.0)
Shock_Absorber_Condition = st.number_input("Shock Absorber Condition (0–10)", 0.0, 10.0, 6.0)

brakes_input_df = pd.DataFrame([{
    "Brake_Pad_Wear": Brake_Pad_Wear,
    "Brake_Fluid_Level": Brake_Fluid_Level,
    "Suspension_Stiffness": Suspension_Stiffness,
    "Shock_Absorber_Condition": Shock_Absorber_Condition
}])

brakes_years = brakes_model.predict(brakes_input_df)[0]
ransmission_years = transmission_model.predict(transmission_input_df)[0]



st.header("🔌 Electronics")

Battery_Health = st.number_input("Battery Health (%)", 0.0, 100.0, 80.0)
Sensor_Error_Rate = st.number_input("Sensor Error Rate (per month)", 0.0, 50.0, 2.0)
Wiring_Condition_Score = st.number_input("Wiring Condition Score (0–10)", 0.0, 10.0, 7.0)

electronics_input_df = pd.DataFrame([{
    "Battery_Health": Battery_Health,
    "Sensor_Error_Rate": Sensor_Error_Rate,
    "Wiring_Condition_Score": Wiring_Condition_Score
}])

electronics_years = electronics_model.predict(electronics_input_df)[0]




st.header("🧱 Body / Structural")

Rust_Level = st.number_input("Rust Level (%)", 0.0, 100.0, 20.0)
Structural_Strength_Score = st.number_input("Structural Strength Score (0–10)", 0.0, 10.0, 8.0)
Damage_Severity = st.number_input("Damage Severity (0–10)", 0.0, 10.0, 2.0)

body_input_df = pd.DataFrame([{
    "Rust_Level": Rust_Level,
    "Structural_Strength_Score": Structural_Strength_Score,
    "Damage_Severity": Damage_Severity
}])

body_years = body_model.predict(body_input_df)[0]



# PREDICTION

if st.button("🔍 Predict Car Health"):
    """
    engine_years = engine_model.predict(engine_input)[0]
    transmission_years = transmission_model.predict(transmission_input)[0]
    brakes_years = brakes_model.predict(brakes_input)[0]
    electronics_years = electronics_model.predict(electronics_input)[0]
    body_years = body_model.predict(body_input)[0]
    """
    car_health = pd.DataFrame({
        "Module": [
            "Engine",
            "Transmission",
            "Brakes & Suspension",
            "Electronics",
            "Body"
        ],
        "Remaining Years": [
            engine_years,
            transmission_years,
            brakes_years,
            electronics_years,
            body_years
        ]
    })

    car_health["Maintenance_Status"] = car_health.apply(
        lambda row: maintenance_status(row["Module"], row["Remaining Years"]),
        axis=1
    )

    st.subheader("📊 Component Health Summary")
    st.dataframe(car_health.style.format({"Remaining Years": "{:.2f}"}))

    # Overall Car Health Calculation
    weights = {
        "Engine": 0.40,
        "Transmission": 0.25,
        "Brakes & Suspension": 0.15,
        "Electronics": 0.10,
        "Body": 0.10
    }

    car_health["Weight"] = car_health["Module"].map(weights)

    status_score = (
        car_health
        .groupby("Maintenance_Status")["Weight"]
        .sum()
    )

    overall_status = status_score.idxmax()

    if status_score.max() >= 0.50:
        final_car_health = overall_status
    else:
        final_car_health = "Mixed / Uncertain"

    st.subheader("🚗 Overall Car Health")

    if final_car_health == "Healthy":
        st.success("✅ Overall Car Health: Healthy")
    elif final_car_health == "Service Soon":
        st.warning("⚠️ Overall Car Health: Service Soon")
    else:
        st.error("🚨 Overall Car Health: Immediate Repair")

   

    st.subheader("🔧 Repair Priority")
    st.dataframe(car_health.sort_values("Remaining Years"))
