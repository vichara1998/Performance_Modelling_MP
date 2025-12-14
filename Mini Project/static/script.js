
        const API_BASE = 'http://localhost:5000';
        const chartColors = { blue: 'rgba(52, 152, 219, 0.8)', 
                              red: 'rgba(231, 76, 60, 0.8)',
                              green: 'rgba(46, 204, 113, 0.8)',
                              orange: 'rgba(230, 126, 34, 0.8)',
                              purple: 'rgba(155, 89, 182, 0.8)' };

        // Load Summary
        fetch(`${API_BASE}/summary`).then(res => res.json()).then(data => {
            document.getElementById("tp").innerText = data.total_patients;
            document.getElementById("dc").innerText = data.doctor_count;
            document.getElementById("wc").innerText = data.avg_wait_consult;
            document.getElementById("wd").innerText = data.avg_wait_dispense;
            document.getElementById("ct").innerText = data.avg_consult_time;
            document.getElementById("dt").innerText = data.avg_dispense_time;
            document.getElementById("doc_util").innerText = data.doctor_utilization;
            document.getElementById("pharm_util").innerText = data.pharmacy_utilization;
        });

        // Load Charts
        fetch(`${API_BASE}/distribution`).then(res => res.json()).then(data => {
            new Chart(document.getElementById("consultDistChart"), { type: "doughnut", data: { labels: data.consult_labels, datasets: [{ data: data.consult_counts, backgroundColor: Object.values(chartColors) }] } });
            new Chart(document.getElementById("dispenseDistChart"), { type: "doughnut", data: { labels: data.dispense_labels, datasets: [{ data: data.dispense_counts, backgroundColor: Object.values(chartColors) }] } });
        });

        fetch(`${API_BASE}/charts`).then(res => res.json()).then(data => {
            const avg = arr => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
            new Chart(document.getElementById("comparisonChart"), { type: "bar", data: { labels: ["Wait (Consult)", "Consult Time", "Wait (Dispense)", "Dispense Time"], datasets: [{ label: "Minutes", data: [avg(data.wait_consult), avg(data.consult_times), avg(data.wait_dispense), avg(data.dispense_times)], backgroundColor: [chartColors.red, chartColors.blue, chartColors.orange, chartColors.green] }] } });
            new Chart(document.getElementById("serviceWaitChart"), { type: "bar", data: { labels: ["Consultation", "Dispensing"], datasets: [{ label: "Waiting", data: [avg(data.wait_consult), avg(data.wait_dispense)], backgroundColor: chartColors.red }, { label: "Service", data: [avg(data.consult_times), avg(data.dispense_times)], backgroundColor: chartColors.blue }] } });
            new Chart(document.getElementById("trendChart"), { type: "line", data: { labels: data.wait_consult.map((_, i) => `P${i + 1}`), datasets: [{ label: "Consult Wait", data: data.wait_consult, borderColor: chartColors.blue, fill: false }, { label: "Dispense Wait", data: data.wait_dispense, borderColor: chartColors.orange, fill: false }] } });
        });

        fetch(`${API_BASE}/timeline`).then(res => res.json()).then(data => {
            new Chart(document.getElementById("timelineChart"), { type: "bar", data: { labels: data.patient_ids.map(id => `P${id}`), datasets: [{ label: "Total Time in System", data: data.total_time, backgroundColor: chartColors.purple }] } });
        });

        // Load Table
        fetch(`${API_BASE}/all-data`).then(res => res.json()).then(data => {
            const tbody = document.getElementById("tableBody");
            data.forEach(row => {
                const tr = document.createElement("tr");
                const consultClass = row["Wait_consult(min)"] > 15 ? "wait-high" : "";
                const dispenseClass = row["Wait_dispense(min)"] > 15 ? "wait-high" : "";
                tr.innerHTML = `<td><b>${row.Patient_ID}</b></td><td>${row.Arrival_Time}</td><td><span class="doctor-badge">${row.Doctor_ID}</span></td><td class="${consultClass}">${row["Wait_consult(min)"]} min</td><td>${row.Consult_start}</td><td>${row.Consult_end}</td><td class="${dispenseClass}">${row["Wait_dispense(min)"]} min</td><td>${row.Dispensing_start}</td><td>${row.Dispensing_end}</td>`;
                tbody.appendChild(tr);
            });
        });
    
