
# Performance Modelling Mini Project

#  Performance Modelling and Evaluation of an Outpatient Healthcare Process

This repository contains the source code and documentation for the **EEX5362 Performance Modelling Mini Project**.

##  Project Overview
The project simulates patient flow in a hospital Outpatient Department (OPD) to identify bottlenecks and optimize resource allocation. It uses **Discrete Event Simulation (DES)** to model patient arrivals, consultation, and medication dispensing processes.

* **Scenario-** A local hospital OPD (Mirahawattha Divisional Hospital) suffering from long patient queues.
* **Goal-** Analyze current performance (wait times, utilization) and propose resource optimizations.
* **Method-** Python-based simulation with a Flask web dashboard for visualization.

##  Key Features
* **Discrete Event Simulation (DES)-** Custom Python logic modeling stochastic patient arrivals (Poisson Process) and service times (Normal Distribution).
* **Interactive Dashboard-** A Flask-based web interface to view real-time simulation metrics.
* **Data Analysis-** Comparison between Real World Data (collected from manual logs) and Simulation Results.
* **Bottleneck Detection-** Automatic identification of system constraints (e.g., Doctor vs. Pharmacist).

##  Technology Stack
* **Language-** Python 3.x
* **Web Framework-** Flask
* **Data Manipulation-** Pandas, NumPy
* **Visualization-** Chart.js (Frontend), Matplotlib (Analysis)

## 📂 Project Structure
```text
/Performance_Modelling_MP
|   |         
|   └──Mini Project/
|              │
|              ├── opd_simulation.py      # Main application file (Simulation Logic + Flask Routes)
|              |
|              |      
|              ├── templates/
|              │   └── index.html         # Dashboard frontend (HTML)
|              │
|              ├── static/
|              │   ├── style.css          # Styling for the dashboard
|              │   └── script.js          # JavaScript for Chart.js updates
|              │
|              └── Real Data (Calculation)/    
|                   ├── data.csv          # Raw patient data (Anonymized)
|                   |     
|                   └── input_analysis.py  # Script for EDA on raw hospital data (data.csv)
|              
|── README.md                # Project Documentation
|                            
└── sample_dataset.csv       # Sample Dataset
```
## How to Run
* Prerequisites
Ensure you have Python installed. Install the required libraries
```bash
pip install flask pandas numpy matplotlib
```
* First (Real data analysis)
```bash
python input_analysis.py
```
* Second (Simulation run)
```bash
python opd_simulation.py
```
* Open your browser and go to 
```bash
http://127.0.0.1:5000/
```
