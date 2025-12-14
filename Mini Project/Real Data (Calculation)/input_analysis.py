import pandas as pd
import matplotlib.pyplot as plt

# 1. Load dataset

df = pd.read_csv("data.csv")

df.columns = df.columns.str.strip()

# Convert time columns to datetime
time_cols = [
    "Arrival_time",
    "Consult_start",
    "Consult_end",
    "Dispensing_start",
    "Dispensing_end"
]

for col in time_cols:
    df[col] = pd.to_datetime(df[col], format="%H:%M")


# Calculate durations (minutes)

df["Consult_time"] = (
    df["Consult_end"] - df["Consult_start"]
).dt.total_seconds() / 60

df["Dispense_time"] = (
    df["Dispensing_end"] - df["Dispensing_start"]
).dt.total_seconds() / 60


# Performance metrics

total_patients = len(df)

avg_consult = df["Consult_time"].mean()
avg_dispense = df["Dispense_time"].mean()

avg_wait_consult = df["Wait_consult(min)"].mean()
avg_wait_dispense = df["Wait_dispense(min)"].mean()

# OPD working time
# Morning: 08:00–12:00 = 240 min
# Evening: 13:00–17:00 = 240 min
total_opd_time = 240  # minutes(morning session)

doctor_util = (df["Consult_time"].sum() / total_opd_time) * 100
dispense_util = (df["Dispense_time"].sum() / total_opd_time) * 100

throughput = total_patients / (total_opd_time / 60)

# Bottleneck detection
if doctor_util > dispense_util + 5:
    bottleneck = "Consultation (Doctor)"
elif dispense_util > doctor_util + 5:
    bottleneck = "Dispensing (Pharmacy)"
else:
    bottleneck = "Balanced / No clear bottleneck"


# Print summary

print("\n----- OPD DAILY PERFORMANCE SUMMARY -----")
print(f"Total Patients: {total_patients}")
print(f"Average Consultation Time (min): {avg_consult:.2f}")
print(f"Average Dispensing Time (min): {avg_dispense:.2f}")
print(f"Average Waiting Before Consultation (min): {avg_wait_consult:.2f}")
print(f"Average Waiting Before Dispensing (min): {avg_wait_dispense:.2f}")
print(f"Doctor Utilization (%): {doctor_util:.2f}")
print(f"Dispensing Utilization (%): {dispense_util:.2f}")
print(f"Throughput (patients/hour): {throughput:.2f}")
print(f"Detected Bottleneck: {bottleneck}")


