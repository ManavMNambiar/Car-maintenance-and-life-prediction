
def maintenance_status(module, remaining_years):

    rules = {
        "Engine": (2, 4),
        "Transmission": (1, 2),
        "Brakes & Suspension": (1, 3),
        "Electronics": (0.8, 2),
        "Body": (1.5, 4)
    }

    imm, service = rules[module]

    if remaining_years < imm:
        return "Immediate Repair"
    elif remaining_years < service:
        return "Service Soon"
    else:
        return "Healthy"
import joblib

engine_model = joblib.load("engine_model.pkl")
transmission_model = joblib.load("transmission_model.pkl")
brakes_model = joblib.load("brakes_model.pkl")
electronics_model = joblib.load("electronics_model.pkl")
body_model = joblib.load("body_model.pkl")
print("=== ENTER ENGINE DETAILS ===")

Oil_Level = float(input("Oil Level (%) : "))
Oil_Quality_Score = float(input("Oil Quality Score (0–10) : "))
Avg_Engine_Temp = float(input("Average Engine Temperature (°C) : "))
Engine_Damage_Score = float(input("Engine Damage Score (0–10) : "))
Overheat_Events = int(input("Number of Overheat Events : "))
Km_Driven = float(input("Kilometers Driven : "))

engine_input = [[
    Oil_Level,
    Oil_Quality_Score,
    Avg_Engine_Temp,
    Engine_Damage_Score,
    Overheat_Events,
    Km_Driven
]]
print("\n=== ENTER TRANSMISSION DETAILS ===")

Gear_Slip_Frequency = int(input("Gear Slip Frequency : "))
Clutch_Wear_Percentage = float(input("Clutch Wear Percentage (%) : "))
Transmission_Temp = float(input("Transmission Temperature (°C) : "))
Axle_Wear_Score = float(input("Axle Wear Score (0–10) : "))

transmission_input = [[
    Gear_Slip_Frequency,
    Clutch_Wear_Percentage,
    Transmission_Temp,
    Axle_Wear_Score
]]
print("\n=== ENTER BRAKES & SUSPENSION DETAILS ===")

Brake_Pad_Wear = float(input("Brake Pad Wear (%) : "))
Brake_Fluid_Level = float(input("Brake Fluid Level (%) : "))
Suspension_Stiffness = float(input("Suspension Stiffness (0–10) : "))
Shock_Absorber_Condition = float(input("Shock Absorber Condition (0–10) : "))

brakes_input = [[
    Brake_Pad_Wear,
    Brake_Fluid_Level,
    Suspension_Stiffness,
    Shock_Absorber_Condition
]]
print("\n=== ENTER ELECTRONICS DETAILS ===")

Battery_Health = float(input("Battery Health (%) : "))
Sensor_Error_Rate = float(input("Sensor Error Rate (per month) : "))
Wiring_Condition_Score = float(input("Wiring Condition Score (0–10) : "))

electronics_input = [[
    Battery_Health,
    Sensor_Error_Rate,
    Wiring_Condition_Score
]]
print("\n=== ENTER BODY / STRUCTURAL DETAILS ===")

Rust_Level = float(input("Rust Level (%) : "))
Structural_Strength_Score = float(input("Structural Strength Score (0–10) : "))
Damage_Severity = float(input("Damage Severity (0–10) : "))

body_input = [[
    Rust_Level,
    Structural_Strength_Score,
    Damage_Severity
]]


engine_years = engine_model.predict(engine_input)[0]
transmission_years = transmission_model.predict(transmission_input)[0]
brakes_years = brakes_model.predict(brakes_input)[0]
electronics_years = electronics_model.predict(electronics_input)[0]
body_years = body_model.predict(body_input)[0]


print("Engine Remaining Years:", round(engine_years, 2))
print("Transmission Remaining Years:", round(transmission_years, 2))
print("Brakes Remaining Years:", round(brakes_years, 2))
print("Electronics Remaining Years:", round(electronics_years, 2))
print("Body Remaining Years:", round(body_years, 2))


import pandas as pd

car_health = pd.DataFrame({
    "Module": [
        "Engine",
        "Transmission",
        "Brakes & Suspension",
        "Electronics",
        "Body"
    ],
    "Remaining_Years": [
        engine_years,
        transmission_years,
        brakes_years,
        electronics_years,
        body_years
    ]
})

car_health["Maintenance_Status"] = car_health.apply(
    lambda row: maintenance_status(row["Module"], row["Remaining_Years"]),
    axis=1
)

car_health


weights = {
    "Engine": 0.40,
    "Transmission": 0.25,
    "Brakes & Suspension": 0.15,
    "Electronics": 0.10,
    "Body": 0.10
}

car_health["Weight"] = car_health["Module"].map(weights)
weighted_car_health = (
    car_health["Remaining_Years"] * car_health["Weight"]
).sum()

print("Weighted Car Health Score:", round(weighted_car_health, 2))
if "Immediate Repair" in car_health["Maintenance_Status"].values:
    overall_status = "Immediate Repair"
elif "Service Soon" in car_health["Maintenance_Status"].values:
    overall_status = "Service Soon"
else:
    overall_status = "Healthy"

print("Overall Car Status:", overall_status)
repair_priority = car_health.sort_values("Remaining_Years")

repair_priority
final_summary = {
    "Weighted_Car_Health_Score": round(weighted_car_health, 2),
    "Overall_Maintenance_Status": overall_status,
    "Immediate_Repair_Modules": list(
        car_health[car_health["Maintenance_Status"] == "Immediate Repair"]["Module"]
    ),
    "Service_Soon_Modules": list(
        car_health[car_health["Maintenance_Status"] == "Service Soon"]["Module"]
    )
}

final_summary

