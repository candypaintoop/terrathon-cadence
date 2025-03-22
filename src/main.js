async function calculate() {
  const location = document.getElementById("location").value;
  const algaeAmount = parseFloat(document.getElementById("algae-amount").value);
  const wallArea = parseFloat(document.getElementById("wall-area").value);

  if (!location || isNaN(algaeAmount) || isNaN(wallArea)) {
    alert("Please fill in all fields correctly.");
    return;
  }

  const payload = {
    location: location,
    algae_amount: algaeAmount,
    wall_area: wallArea
  };

  // Show the loader
  const loader = document.getElementById("page-loader");
  loader.style.display = "flex";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("result").innerHTML = `
      <div class="result-container">

  <div class="result-box prediction">
    <!-- Priority Badge (no text) -->
    <div class="priority-badge"></div>
    
    <h3>Prediction Result:</h3>
    <p><strong>Algae Type:</strong> ${data.algae_type}</p>
    <p><strong>Panel Type:</strong> ${data.panel_type}</p>
  </div>

  <div class="result-box weather-info">
    <h4>Weather Information:</h4>
    <p><strong>Temperature:</strong> ${data.weather.temperature} °C</p>
    <p><strong>Humidity:</strong> ${data.weather.humidity} %</p>
    <p><strong>Rainfall:</strong> ${data.weather.rainfall} mm</p>
    <p><strong>Sunlight Hours:</strong> ${data.weather.sunlight_hours} hours</p>
  </div>

  <div class="result-box water-quality">
    <h4>Water Quality Data:</h4>
    <p><strong>BOD:</strong> ${data.water_quality.bod} mg/L</p>
    <p><strong>pH:</strong> ${data.water_quality.ph}</p>
    <p><strong>Nitrogen:</strong> ${data.water_quality.nitrogen} mg/L</p>
    <p><strong>Phosphorus:</strong> ${data.water_quality.phosphorus} mg/L</p>
  </div>

</div>

      `;
    } else {
      document.getElementById("result").innerHTML = `
        <p>Error: ${data.error}</p>
      `;
    }
    document.querySelector(".result-container").scrollIntoView({
      behavior: "smooth",
      block: "end"
    });
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("result").innerHTML = `
      <p>An unexpected error occurred. Check console for details.</p>
    `;
  } finally {
    // Hide the loader after everything is done
    loader.style.display = "none";
  }
}
