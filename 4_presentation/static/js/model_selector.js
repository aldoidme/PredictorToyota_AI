document.addEventListener("DOMContentLoaded", () => {
  const tables = window.TOYOTA_TABLES || [];
  const NO_DATA = "Informacion no disponible actualmente";
  const demandTable = tables.find((t) => t.title === "Resumen de demanda");
  const compareTable = tables.find((t) => t.title === "Nuevo vs usado");
  const predictionTable = tables.find((t) => t.title === "Prediccion demanda");

  const chips = Array.from(document.querySelectorAll(".model-chip"));
  const modelTitle = document.getElementById("modelTitle");
  const modelSubtitle = document.getElementById("modelSubtitle");
  const modelRecommendation = document.getElementById("modelRecommendation");
  const demandValue = document.getElementById("demandValue");
  const demandTrend = document.getElementById("demandTrend");
  const usedValue = document.getElementById("usedValue");
  const usedRecommendation = document.getElementById("usedRecommendation");
  const predictionValue = document.getElementById("predictionValue");
  const predictionTrend = document.getElementById("predictionTrend");
  const priceValue = document.getElementById("priceValue");
  const summaryModelName = document.getElementById("summaryModelName");
  const summaryDemand = document.getElementById("summaryDemand");
  const summaryPriceNew = document.getElementById("summaryPriceNew");
  const summaryPriceUsed = document.getElementById("summaryPriceUsed");
  const summaryRecommendation = document.getElementById("summaryRecommendation");
  const compareNewPrice = document.getElementById("compareNewPrice");
  const compareUsedPrice = document.getElementById("compareUsedPrice");
  const compareDiff = document.getElementById("compareDiff");
  const compareStability = document.getElementById("compareStability");
  const compareRecommendation = document.getElementById("compareRecommendation");
  const demandBadge = document.getElementById("demandBadge");
  const demandFill = document.getElementById("demandFill");
  const demandFoot = document.getElementById("demandFoot");
  const finalRecoBadge = document.getElementById("finalRecoBadge");
  const finalRecoTitle = document.getElementById("finalRecoTitle");
  const finalRecoChips = document.getElementById("finalRecoChips");
  const toyotaStatusTitle = document.getElementById("toyotaStatusTitle");
  const toyotaStatusSubtitle = document.getElementById("toyotaStatusSubtitle");
  const toyotaTrend = document.getElementById("toyotaTrend");
  const toyotaAction = document.getElementById("toyotaAction");

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

  function mapDemandLabel(value) {
    if (!value) return NO_DATA;
    const label = String(value).toLowerCase();
    if (label.includes("crece")) return "Alta";
    if (label.includes("cae")) return "Baja";
    if (label.includes("estable")) return "Media";
    return NO_DATA;
  }

  function applyDemandState(stateLabel) {
    if (!demandBadge || !demandFill || !demandFoot) return;

    demandBadge.classList.remove("high", "medium", "low");

    if (stateLabel === "Alta") {
      demandBadge.textContent = "Demanda alta";
      demandBadge.classList.add("high");
      demandFill.style.width = "80%";
      demandFoot.textContent = "Alta demanda: buen momento para evaluar compra.";
      return;
    }

    if (stateLabel === "Media") {
      demandBadge.textContent = "Demanda media";
      demandBadge.classList.add("medium");
      demandFill.style.width = "55%";
      demandFoot.textContent = "Demanda estable: compra sin presion.";
      return;
    }

    if (stateLabel === "Baja") {
      demandBadge.textContent = "Demanda baja";
      demandBadge.classList.add("low");
      demandFill.style.width = "30%";
      demandFoot.textContent = "Demanda baja: conviene negociar precio.";
      return;
    }

    demandBadge.textContent = NO_DATA;
    demandFill.style.width = "0%";
    demandFoot.textContent = NO_DATA;
  }

  function updateFinalRecommendation(demandLabel, compareLabel, stabilityLabel) {
    if (!finalRecoBadge || !finalRecoTitle || !finalRecoChips) return;

    const chips = [];
    if (demandLabel && demandLabel !== NO_DATA) {
      chips.push(`Demanda ${demandLabel.toLowerCase()}`);
    }
    if (stabilityLabel && stabilityLabel !== NO_DATA) {
      chips.push(`Mercado ${stabilityLabel.toLowerCase()}`);
    }
    if (compareLabel && compareLabel !== NO_DATA) {
      chips.push(compareLabel);
    }

    finalRecoTitle.textContent = compareLabel && compareLabel !== NO_DATA
      ? compareLabel
      : NO_DATA;
    finalRecoBadge.textContent = "Recomendacion";
    finalRecoChips.innerHTML = chips.length
      ? chips.map((text) => `<span class="chip">${text}</span>`).join("")
      : `<span class="chip">${NO_DATA}</span>`;
  }

  function updateToyotaStatus(stockTrend, actionLabel) {
    if (!toyotaStatusTitle || !toyotaStatusSubtitle || !toyotaTrend || !toyotaAction) return;

    if (!stockTrend) {
      toyotaStatusTitle.textContent = "Estado estable";
      toyotaStatusSubtitle.textContent = NO_DATA;
      toyotaTrend.textContent = "Tendencia: --";
      toyotaAction.textContent = "Recomendacion: --";
      return;
    }

    const trendLabel = String(stockTrend).toLowerCase();
    if (trendLabel.includes("sube")) {
      toyotaStatusTitle.textContent = "Toyota en crecimiento";
      toyotaStatusSubtitle.textContent = "La tendencia reciente es positiva.";
    } else if (trendLabel.includes("baja")) {
      toyotaStatusTitle.textContent = "Toyota en caida";
      toyotaStatusSubtitle.textContent = "La tendencia reciente es negativa.";
    } else {
      toyotaStatusTitle.textContent = "Toyota estable";
      toyotaStatusSubtitle.textContent = "Variacion moderada en el periodo.";
    }

    toyotaTrend.textContent = `Tendencia: ${stockTrend}`;
    toyotaAction.textContent = `Recomendacion: ${actionLabel || "mantener"}`;
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

  function updateTablesHighlight(modelId) {
    document.querySelectorAll("tr[data-model]").forEach((row) => {
      if (row.dataset.model === modelId) {
        row.classList.add("row-active");
      } else {
        row.classList.remove("row-active");
      }
    });
  }

  function updateModel(modelId, label) {
    if (modelTitle) modelTitle.textContent = label;
    if (modelSubtitle) modelSubtitle.textContent = "Resumen rapido del modelo seleccionado.";

    const demand = findRow(demandTable, modelId);
    const compare = findRow(compareTable, modelId);
    const prediction = findRow(predictionTable, modelId);

    if (demandValue) {
      demandValue.textContent = demand ? normalizeValue(demand.last_units) ?? "--" : "--";
    }
    const demandTrendValue = demand ? normalizeValue(demand.demand_trend) : null;
    const demandLabel = mapDemandLabel(demandTrendValue);
    if (demandTrend) {
      demandTrend.textContent = demandLabel;
    }
    applyDemandState(demandLabel);

    const usedCount = compare ? normalizeValue(compare.used_count) : null;
    const newUnits = compare ? normalizeValue(compare.new_units) : null;
    if (usedValue) {
      usedValue.textContent = usedCount !== null || newUnits !== null
        ? `Usados: ${usedCount ?? "--"} | Nuevos: ${newUnits ?? "--"}`
        : "--";
    }
    if (usedRecommendation) {
      usedRecommendation.textContent = compare
        ? mapRecommendation(normalizeValue(compare.recommendation))
        : NO_DATA;
    }

    if (predictionValue) {
      predictionValue.textContent = prediction ? normalizeValue(prediction.predicted_units) ?? "--" : "--";
    }
    if (predictionTrend) {
      predictionTrend.textContent = prediction ? normalizeValue(prediction.trend) ?? NO_DATA : NO_DATA;
    }

    if (modelRecommendation) {
      modelRecommendation.textContent = compare
        ? `Recomendacion: ${mapRecommendation(normalizeValue(compare.recommendation))}`
        : "Recomendacion: --";
    }

    if (summaryModelName) summaryModelName.textContent = label;
    if (summaryDemand) summaryDemand.textContent = demandLabel;
    if (summaryPriceNew) summaryPriceNew.textContent = "S/ --";
    if (summaryPriceUsed) summaryPriceUsed.textContent = "S/ --";
    const compareLabel = compare
      ? mapRecommendation(normalizeValue(compare.recommendation))
      : NO_DATA;

    if (summaryRecommendation) {
      summaryRecommendation.textContent = compareLabel;
    }

    if (priceValue) priceValue.textContent = "S/ --";

    if (compareNewPrice) compareNewPrice.textContent = "S/ --";
    if (compareUsedPrice) compareUsedPrice.textContent = "S/ --";
    if (compareDiff) compareDiff.textContent = "S/ --";
    if (compareStability) {
      compareStability.textContent = compare
        ? mapStability(normalizeValue(compare.ratio_used_new))
        : NO_DATA;
    }
    if (compareRecommendation) {
      compareRecommendation.textContent = compareLabel;
    }

    const stabilityLabel = compare
      ? mapStability(normalizeValue(compare.ratio_used_new))
      : NO_DATA;

    updateFinalRecommendation(demandLabel, compareLabel, stabilityLabel);

    const stockAction = compareLabel === "Conviene nuevo"
      ? "comprar"
      : compareLabel === "Conviene usado"
        ? "mantener"
        : "mantener";
    updateToyotaStatus(demand ? demand.demand_trend : null, stockAction);
    updateTablesHighlight(modelId);

    if (typeof window.updateSalesChart === "function") {
      window.updateSalesChart(modelId);
    }
  }

  function setActiveChip(chip) {
    chips.forEach((item) => item.classList.remove("active"));
    chip.classList.add("active");
  }

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const modelId = chip.dataset.model;
      const label = chip.dataset.label || modelId;
      setActiveChip(chip);
      updateModel(modelId, label);
    });
  });

  const initialChip = chips.find((chip) => chip.classList.contains("active")) || chips[0];
  if (initialChip) {
    updateModel(initialChip.dataset.model, initialChip.dataset.label || initialChip.dataset.model);
  }
});
