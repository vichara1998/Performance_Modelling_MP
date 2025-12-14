from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# --- SIMULATION CONFIGURATION ---

# 240 = Ends at 12:00 PM (Morning Only)
# 480 = Ends at 4:00 PM (Full Day)
SHIFT_DURATION = 240         

NUM_PATIENTS = 40           # High limit (Simulation stops based on time)
NUM_DOCTORS = 2              
NUM_PHARMACISTS = 1          
AVG_ARRIVAL_INTERVAL = 6     
AVG_CONSULT_TIME = 6         
AVG_DISPENSE_TIME = 5        
START_TIME = "08:00"         

def run_simulation():
    doctors_free_until = [0] * NUM_DOCTORS 
    pharmacists_free_until = [0] * NUM_PHARMACISTS
    current_arrival_time = 0 
    data = []

    for i in range(1, NUM_PATIENTS + 1):
        # 1. Patient Arrival
        inter_arrival = max(1, int(random.normalvariate(AVG_ARRIVAL_INTERVAL, 0.5)))
        
        if i == 1:
            next_arrival_time = 0
        else:
            next_arrival_time = current_arrival_time + inter_arrival
            
    
        if next_arrival_time >= SHIFT_DURATION:
            break
            
        current_arrival_time = next_arrival_time
        
        # Consultation Phase
        earliest_doctor_time = min(doctors_free_until)
        doctor_idx = doctors_free_until.index(earliest_doctor_time)
        
        consult_start_time = max(current_arrival_time, earliest_doctor_time)
        
    
        if consult_start_time >= SHIFT_DURATION:
            break 

        wait_consult = consult_start_time - current_arrival_time
        consult_duration = max(2, int(random.normalvariate(AVG_CONSULT_TIME, 0.5)))
        consult_end_time = consult_start_time + consult_duration
        
        doctors_free_until[doctor_idx] = consult_end_time
        
        #Dispensing Phase
        pharmacy_arrival_time = consult_end_time
        earliest_pharmacy_time = min(pharmacists_free_until)
        pharmacy_idx = pharmacists_free_until.index(earliest_pharmacy_time)
        
       
        dispense_start_time = max(pharmacy_arrival_time, earliest_pharmacy_time)

        wait_dispense = dispense_start_time - pharmacy_arrival_time
        dispense_duration = max(2, int(random.normalvariate(AVG_DISPENSE_TIME, 0.5)))
        dispense_end_time = dispense_start_time + dispense_duration
        pharmacists_free_until[pharmacy_idx] = dispense_end_time
        
        #Format Times
        base_time = datetime.strptime(START_TIME, "%H:%M")
        def to_time_str(minutes):
            return (base_time + timedelta(minutes=float(minutes))).strftime("%H:%M")

        data.append({
            "Patient_ID": i,
            "Doctor_ID": f"Dr. {doctor_idx + 1}", 
            "Arrival_Time": to_time_str(current_arrival_time),
            "Consult_start": to_time_str(consult_start_time),
            "Consult_end": to_time_str(consult_end_time),
            "Dispensing_start": to_time_str(dispense_start_time),
            "Dispensing_end": to_time_str(dispense_end_time),
            "Wait_consult(min)": int(wait_consult),
            "Wait_dispense(min)": int(wait_dispense)
        })

    return pd.DataFrame(data)

# --- GLOBAL SIMULATION RUN ---
df = run_simulation()

def refresh_data():
    global df
    df = run_simulation()

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-simulation")
def trigger_simulation():
    refresh_data()
    return jsonify({"status": "Simulation Re-run", "patients": len(df)})

@app.route("/summary")
def summary():
    def get_minutes(time_str):
        t = datetime.strptime(time_str, "%H:%M")
        start = datetime.strptime(START_TIME, "%H:%M")
        return (t - start).total_seconds() / 60

    if df.empty: return jsonify({"error": "No data"})

    consult_durations = df.apply(lambda x: get_minutes(x["Consult_end"]) - get_minutes(x["Consult_start"]), axis=1)
    dispense_durations = df.apply(lambda x: get_minutes(x["Dispensing_end"]) - get_minutes(x["Dispensing_start"]), axis=1)

    total_consult_time = consult_durations.sum()
    total_dispense_time = dispense_durations.sum()
    
    # Utilization Calculation
    doc_utilization = (total_consult_time / (SHIFT_DURATION * NUM_DOCTORS)) * 100
    
  
    last_pharmacy_activity = get_minutes(df.iloc[-1]["Dispensing_end"])
    pharmacy_active_time = max(SHIFT_DURATION, last_pharmacy_activity)
    pharm_utilization = (total_dispense_time / (pharmacy_active_time * NUM_PHARMACISTS)) * 100

    throughput_per_hour = len(df) / (SHIFT_DURATION / 60)

    summary_data = {
        "total_patients": int(len(df)),
        "doctor_count": NUM_DOCTORS,
        "pharmacist_count": NUM_PHARMACISTS,
        "avg_wait_consult": float(round(df["Wait_consult(min)"].mean(), 2)),
        "avg_wait_dispense": float(round(df["Wait_dispense(min)"].mean(), 2)),
        "avg_consult_time": float(round(consult_durations.mean(), 2)),
        "avg_dispense_time": float(round(dispense_durations.mean(), 2)),
        "max_wait_consult": int(df["Wait_consult(min)"].max()),
        "max_wait_dispense": int(df["Wait_dispense(min)"].max()),
        "doctor_utilization": float(round(doc_utilization, 2)),
        "pharmacy_utilization": float(round(pharm_utilization, 2)),
        "throughput_per_hour": float(round(throughput_per_hour, 2))
    }
    return jsonify(summary_data)

@app.route("/charts")
def charts():
    if df.empty: return jsonify({})
    def get_minutes(time_str):
        t = datetime.strptime(time_str, "%H:%M")
        start = datetime.strptime(START_TIME, "%H:%M")
        return (t - start).total_seconds() / 60
    consult_durations = df.apply(lambda x: get_minutes(x["Consult_end"]) - get_minutes(x["Consult_start"]), axis=1)
    dispense_durations = df.apply(lambda x: get_minutes(x["Dispensing_end"]) - get_minutes(x["Dispensing_start"]), axis=1)
    return jsonify({
        "wait_consult": df["Wait_consult(min)"].astype(int).tolist(),
        "wait_dispense": df["Wait_dispense(min)"].astype(int).tolist(),
        "consult_times": consult_durations.astype(float).tolist(),
        "dispense_times": dispense_durations.astype(float).tolist()
    })

@app.route("/distribution")
def distribution():
    bins = [0, 5, 10, 15, 20, 30, 60, float('inf')]
    labels = ["0-5", "5-10", "10-15", "15-20", "20-30", "30-60", "60+"]
    consult_dist = pd.cut(df["Wait_consult(min)"], bins=bins).value_counts().sort_index()
    dispense_dist = pd.cut(df["Wait_dispense(min)"], bins=bins).value_counts().sort_index()
    return jsonify({
        "consult_labels": labels,
        "consult_counts": consult_dist.astype(int).tolist(),
        "dispense_labels": labels,
        "dispense_counts": dispense_dist.astype(int).tolist()
    })

@app.route("/timeline")
def timeline():
    def get_minutes(time_str):
        t = datetime.strptime(time_str, "%H:%M")
        start = datetime.strptime(START_TIME, "%H:%M")
        return (t - start).total_seconds() / 60
    total_time = df.apply(lambda x: get_minutes(x["Dispensing_end"]) - get_minutes(x["Arrival_Time"]), axis=1)
    return jsonify({
        "patient_ids": list(range(1, len(df) + 1)),
        "total_time": total_time.tolist()
    })

@app.route("/all-data")
def all_data():
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
