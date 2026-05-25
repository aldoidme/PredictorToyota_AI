document.addEventListener("DOMContentLoaded", () => {
  const demandChart = document.getElementById("chart-demand");
  if (!demandChart || !window.Plotly) return;

  const originalVisibility = demandChart.data.map(() => true);

  function updateSalesChart(modelId) {
    const visibility = demandChart.data.map((trace) => trace.legendgroup === modelId);
    if (visibility.some(Boolean)) {
      Plotly.restyle(demandChart, { visible: visibility });
    } else {
      Plotly.restyle(demandChart, { visible: originalVisibility });
    }
  }

  window.updateSalesChart = updateSalesChart;

  const activeChip = document.querySelector(".model-chip.active");
  if (activeChip) {
    updateSalesChart(activeChip.dataset.model);
  }
});
