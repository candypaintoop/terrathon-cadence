// Wait until the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('Document loaded and ready!');
  
  // Attach event listener to the calculate button
  const calcButton = document.querySelector('.cta-button');
  if (calcButton) {
    calcButton.addEventListener('click', calculate);
  }
});

// Calculate function to process user input
function calculate() {
  // Get input values
  const greyWaterInput = document.getElementById('grey-water');
  const wallAreaInput = document.getElementById('wall-area');
  const resultDiv = document.getElementById('result');

  const greyWater = parseFloat(greyWaterInput.value);
  const wallArea = parseFloat(wallAreaInput.value);

  console.log(`Grey Water: ${greyWater}, Wall Area: ${wallArea}`); // Debugging logs

  // Input validation
  if (isNaN(greyWater) || greyWater <= 0) {
    resultDiv.textContent = "⚠️ Please enter a valid amount of Grey Water (liters).";
    return;
  }

  if (isNaN(wallArea) || wallArea <= 0) {
    resultDiv.textContent = "⚠️ Please enter a valid Wall Area (m²).";
    return;
  }

  // Example calculation logic (customize as needed!)
  // Let's assume the system filters X units of CO2 for each liter and square meter combined
  const co2ReductionFactor = 0.8; // hypothetical factor
  const output = (greyWater * wallArea * co2ReductionFactor).toFixed(2);

  // Show the output result
  resultDiv.innerHTML = `
    ✅ <strong>Estimated CO2 Reduction:</strong> ${output} units
  `;

  // Optional: Reset input fields
  // greyWaterInput.value = '';
  // wallAreaInput.value = '';
}
