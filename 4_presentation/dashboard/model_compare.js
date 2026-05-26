document.addEventListener("DOMContentLoaded", () => {
  const tables = window.TOYOTA_TABLES || [];
  const NO_DATA = "Informacion no disponible actualmente";
  const profiles = window.TOYOTA_PROFILES || [];
  const demandTable = tables.find((t) => t.title === "Resumen de demanda");
  const compareTable = tables.find((t) => t.title === "Nuevo vs usado");
  const predictionTable = tables.find((t) => t.title === "Prediccion demanda");

  const modelOptions = [
    { id: "HILUX", label: "Toyota Hilux" },
    { id: "YARIS", label: "Toyota Yaris" },
    { id: "COROLLA", label: "Toyota Corolla" },
    { id: "AVANZA", label: "Toyota Avanza" },
    { id: "RAV4", label: "Toyota RAV4" },
    { id: "ETIOS", label: "Toyota Etios" },
    { id: "RUSH", label: "Toyota Rush" },
    { id: "FORTUNER", label: "Toyota Fortuner" },
    { id: "RAIZE", label: "Toyota Raize" },
    { id: "COROLLA_CROSS", label: "Toyota Corolla Cross" },
  ];

  const selectA = document.getElementById("compareModelA");
  const selectB = document.getElementById("compareModelB");

  const titleA = document.getElementById("compareTitleA");
  const titleB = document.getElementById("compareTitleB");
  const headerA = document.getElementById("compareHeaderA");
  const headerB = document.getElementById("compareHeaderB");

  const demandA = document.getElementById("compareDemandA");
  const demandB = document.getElementById("compareDemandB");
  const demandBarA = document.getElementById("compareDemandBarA");
  const demandBarB = document.getElementById("compareDemandBarB");

  const priceA = document.getElementById("comparePriceA");
  const priceB = document.getElementById("comparePriceB");
  const stabilityA = document.getElementById("compareStabilityA");
  const stabilityB = document.getElementById("compareStabilityB");
  const trendA = document.getElementById("compareTrendA");
  const trendB = document.getElementById("compareTrendB");
  const recoA = document.getElementById("compareRecoA");
  const recoB = document.getElementById("compareRecoB");

  const tableDemandA = document.getElementById("compareTableDemandA");
  const tableDemandB = document.getElementById("compareTableDemandB");
  const tablePriceA = document.getElementById("compareTablePriceA");
  const tablePriceB = document.getElementById("compareTablePriceB");
  const tableStabilityA = document.getElementById("compareTableStabilityA");
  const tableStabilityB = document.getElementById("compareTableStabilityB");
  const tableTrendA = document.getElementById("compareTableTrendA");
  const tableTrendB = document.getElementById("compareTableTrendB");
  const tableRecoA = document.getElementById("compareTableRecoA");
  const tableRecoB = document.getElementById("compareTableRecoB");

  function rowToObject(table, row) {
    const obj = {};
    table.columns.forEach((col, index) => {
      obj[col] = row[index];
    });
    return obj;
  }

  function findRow(table, modelId) {
    if (!table) return null;
    const idx = table.columns.indexOf("model_id");
    if (idx === -1) return null;
    const row = table.rows.find((r) => String(r[idx]).toUpperCase() === modelId);
    return row ? rowToObject(table, row) : null;
  }

  function normalizeValue(value) {
    if (value === undefined || value === null || value === "--") return null;
    return value;
  }

  function profileFor(modelId) {
    if (!modelId) return null;
    const key = String(modelId).toUpperCase();
    return profiles.find((item) => String(item.model_id).toUpperCase() === key) || null;
  }

  function pickPrice(profile) {
    if (!profile) return null;
    if (profile.price_new !== null && profile.price_new !== undefined) return profile.price_new;
    if (profile.price_used !== null && profile.price_used !== undefined) return profile.price_used;
    return null;
  }

  function formatPrice(value) {
    if (value === null || value === undefined) return "S/ --";
    const num = Number.parseFloat(value);
    if (Number.isNaN(num)) return "S/ --";
    return `S/ ${Math.round(num)}`;
  }

  function mapDemandLabel(value) {
    if (!value) return NO_DATA;
    const label = String(value).toLowerCase();
    if (label.includes("crece")) return "Alta";
    if (label.includes("cae")) return "Baja";
    if (label.includes("estable")) return "Media";
    return NO_DATA;
  }

  function mapTrendLabel(value) {
    if (!value) return NO_DATA;
    const label = String(value).toLowerCase();
    if (label.includes("crece")) return "Sube";
    if (label.includes("cae")) return "Baja";
    if (label.includes("estable")) return "Estable";
    return NO_DATA;
  }

  function mapRecommendation(value) {
    if (!value) return NO_DATA;
    const label = String(value).toLowerCase();
    if (label.includes("recomendable usado")) return "Conviene usado";
    if (label.includes("recomendable nuevo")) return "Conviene nuevo";
    if (label.includes("mantener")) return "Mantener";
    return String(value);
  }

  function mapStability(ratioValue) {
    if (ratioValue === null || ratioValue === undefined) return NO_DATA;
    const ratio = Number.parseFloat(ratioValue);
    if (Number.isNaN(ratio)) return NO_DATA;
    if (ratio >= 0.8 && ratio <= 1.2) return "Estable";
    return "Variable";
  }

  function demandBarWidth(stateLabel) {
    if (stateLabel === "Alta") return "80%";
    if (stateLabel === "Media") return "55%";
    if (stateLabel === "Baja") return "30%";
    return "0%";
  }

  function fillSelect(select, defaultId) {
    if (!select) return;
    select.innerHTML = "";
    modelOptions.forEach((option) => {
      const opt = document.createElement("option");
      opt.value = option.id;
      opt.textContent = option.label;
      if (option.id === defaultId) opt.selected = true;
      select.appendChild(opt);
    });
  }

  function updateSide(modelId, label, ui) {
    const demand = findRow(demandTable, modelId);
    const compare = findRow(compareTable, modelId);
    const prediction = findRow(predictionTable, modelId);
    const profile = profileFor(modelId);
    const priceValue = pickPrice(profile);

    const demandLabel = mapDemandLabel(demand ? normalizeValue(demand.demand_trend) : null);
    const trendLabel = mapTrendLabel(prediction ? normalizeValue(prediction.trend) : null);
    const stabilityLabel = mapStability(compare ? normalizeValue(compare.ratio_used_new) : null);
    const recommendationLabel = mapRecommendation(compare ? normalizeValue(compare.recommendation) : null);

    if (ui.title) ui.title.textContent = label;
    if (ui.header) ui.header.textContent = label;
    if (ui.demand) ui.demand.textContent = demandLabel;
    if (ui.demandBar) ui.demandBar.style.width = demandBarWidth(demandLabel);
    if (ui.price) ui.price.textContent = formatPrice(priceValue);
    if (ui.stability) ui.stability.textContent = stabilityLabel;
    if (ui.trend) ui.trend.textContent = trendLabel;
    if (ui.reco) ui.reco.textContent = recommendationLabel;

    if (ui.tableDemand) ui.tableDemand.textContent = demandLabel;
    if (ui.tablePrice) ui.tablePrice.textContent = formatPrice(priceValue);
    if (ui.tableStability) ui.tableStability.textContent = stabilityLabel;
    if (ui.tableTrend) ui.tableTrend.textContent = trendLabel;
    if (ui.tableReco) ui.tableReco.textContent = recommendationLabel;
  }

  function updateComparison() {
    const modelA = selectA ? selectA.value : "COROLLA";
    const modelB = selectB ? selectB.value : "YARIS";

    const labelA = modelOptions.find((opt) => opt.id === modelA)?.label ?? modelA;
    const labelB = modelOptions.find((opt) => opt.id === modelB)?.label ?? modelB;

    updateSide(modelA, labelA, {
      title: titleA,
      header: headerA,
      demand: demandA,
      demandBar: demandBarA,
      price: priceA,
      stability: stabilityA,
      trend: trendA,
      reco: recoA,
      tableDemand: tableDemandA,
      tablePrice: tablePriceA,
      tableStability: tableStabilityA,
      tableTrend: tableTrendA,
      tableReco: tableRecoA,
    });

    updateSide(modelB, labelB, {
      title: titleB,
      header: headerB,
      demand: demandB,
      demandBar: demandBarB,
      price: priceB,
      stability: stabilityB,
      trend: trendB,
      reco: recoB,
      tableDemand: tableDemandB,
      tablePrice: tablePriceB,
      tableStability: tableStabilityB,
      tableTrend: tableTrendB,
      tableReco: tableRecoB,
    });
  }

  fillSelect(selectA, "COROLLA");
  fillSelect(selectB, "YARIS");

  if (selectA) selectA.addEventListener("change", updateComparison);
  if (selectB) selectB.addEventListener("change", updateComparison);

  updateComparison();
});
