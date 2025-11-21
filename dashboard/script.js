const backend = 'http://localhost:8000/api';
let tempChart, humChart;

async function fetchLatest() {
  try {
    const res = await fetch(backend + '/get-latest?n=1');
    const data = await res.json();
    if (!data.length) return;

    let latest = data[0];

    document.getElementById('latest').innerText =
      JSON.stringify(latest, null, 2);

    document.getElementById("last-update").innerText =
      new Date().toLocaleTimeString();

    document.getElementById("system-status").classList.add("online");

    fetchCharts();
    updateAIPanel(latest);
    updateAlerts(latest);

  } catch (e) {
    console.error('Fetch error:', e);
  }
}

async function fetchCharts() {
  try {
    const res = await fetch(backend + '/get-latest?n=20');
    const data = await res.json();
    if (!data.length) return;

    const temps = data.map(x => x.temperature);
    const hums = data.map(x => x.humidity);

    updateCharts(temps, hums);

  } catch (e) {
    console.error("Chart fetch error:", e);
  }
}

function updateAIPanel(latest) {
  const etaField = document.getElementById('eta');
  const riskField = document.getElementById('risk');

  etaField.textContent = latest.eta_minutes
    ? Math.round(latest.eta_minutes)
    : "--";

  let riskText = "";
  let riskClass = "";

  if (latest.spoilage_risk === 0) {
    riskText = "Safe";
    riskClass = "safe";
  } else if (latest.spoilage_risk === 1) {
    riskText = "Warning";
    riskClass = "warning";
  } else {
    riskText = "High Risk";
    riskClass = "danger";
  }

  riskField.textContent = riskText;
  riskField.className = riskClass;

  updateAnomaly(latest);
}

function updateAnomaly(latest) {
  const anomalyField = document.getElementById('anomaly');

  if (
    latest.temperature > 35 ||
    latest.temperature < 2 ||
    latest.humidity > 80 ||
    latest.shock > 2 ||
    latest.spoilage_risk === 2
  ) {
    anomalyField.textContent = "Yes";
    anomalyField.style.color = "#dc2626";
  } else {
    anomalyField.textContent = "No";
    anomalyField.style.color = "#16a34a";
  }
}

function updateAlerts(latest) {
  const alerts = [];

  if (latest.temperature > 35) alerts.push("High Temperature Detected");
  if (latest.humidity > 80) alerts.push("High Humidity Warning");
  if (latest.shock > 2) alerts.push("Shock Detected");
  if (latest.spoilage_risk === 2) alerts.push("High Spoilage Risk");

  const list = document.getElementById("alerts-list");
  list.innerHTML = "";

  if (alerts.length === 0) {
    list.innerHTML = "<li>No alerts</li>";
    return;
  }

  alerts.forEach(a => list.innerHTML += `<li>${a}</li>`);
}

function createCharts() {
  const tctx = document.getElementById('tempChart').getContext('2d');
  const hctx = document.getElementById('humChart').getContext('2d');

  tempChart = new Chart(tctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Temperature (°C)', data: [] }] },
    options: { responsive: true, maintainAspectRatio: false }
  });

  humChart = new Chart(hctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Humidity (%)', data: [] }] },
    options: { responsive: true, maintainAspectRatio: false }
  });
}

function updateCharts(temps, hums) {
  const labels = temps.map((_, i) => i + 1);

  tempChart.data.labels = labels;
  tempChart.data.datasets[0].data = temps;
  tempChart.update();

  humChart.data.labels = labels;
  humChart.data.datasets[0].data = hums;
  humChart.update();
}

window.onload = function () {
  createCharts();
  fetchLatest();
  setInterval(fetchLatest, 3000);
};
