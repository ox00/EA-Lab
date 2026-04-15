const state = {
  data: null,
  selectedCaseIndex: 0,
  selectedFrontierIndex: null,
};

function formatNumber(value, digits = 4) {
  if (value === null || value === undefined) {
    return "-";
  }
  if (typeof value !== "number") {
    return String(value);
  }
  return value.toFixed(digits);
}

function formatJson(value) {
  return JSON.stringify(value, null, 2);
}

function currentCase() {
  return state.data.cases[state.selectedCaseIndex];
}

function metricCard(label, value) {
  const card = document.createElement("article");
  card.className = "metric-card";

  const metricLabel = document.createElement("p");
  metricLabel.className = "metric-label";
  metricLabel.textContent = label;

  const metricValue = document.createElement("p");
  metricValue.className = "metric-value";
  metricValue.textContent = value;

  card.append(metricLabel, metricValue);
  return card;
}

function buildMetricCards(caseData) {
  const metricCards = document.getElementById("metric-cards");
  metricCards.innerHTML = "";

  const metrics = [
    ["difficulty_error", formatNumber(caseData.evaluation.difficulty_error)],
    ["structural_diversity", formatNumber(caseData.evaluation.structural_diversity)],
    ["emptiness_error", formatNumber(caseData.evaluation.emptiness_error)],
    ["emptiness", formatNumber(caseData.evaluation.emptiness)],
    ["front_hv", formatNumber(caseData.final_front_hv)],
    ["front_spread", formatNumber(caseData.final_front_spread)],
  ];

  metrics.forEach(([label, value]) => {
    metricCards.appendChild(metricCard(label, value));
  });
}

function renderCaseList() {
  const caseList = document.getElementById("case-list");
  caseList.innerHTML = "";

  state.data.cases.forEach((caseData, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "case-button";
    if (index === state.selectedCaseIndex) {
      button.classList.add("active");
    }
    button.innerHTML = `
      <p class="frontier-title">${caseData.title}</p>
      <p class="frontier-meta">
        pop=${caseData.config.population_size}, mut=${caseData.config.mutation_rate}, seed=${caseData.config.seed}
      </p>
    `;
    button.addEventListener("click", () => {
      state.selectedCaseIndex = index;
      state.selectedFrontierIndex = null;
      render();
    });
    caseList.appendChild(button);
  });
}

function renderCaseSummary(caseData) {
  document.getElementById("case-tag").textContent = caseData.algorithm.toUpperCase();
  document.getElementById("case-title").textContent = caseData.title;
  document.getElementById("case-summary").textContent =
    `Population ${caseData.config.population_size}, mutation ${caseData.config.mutation_rate}, ` +
    `seed ${caseData.config.seed}, generations ${caseData.config.generations}. ` +
    `Target difficulty ${formatNumber(caseData.config.target_difficulty, 2)}, ` +
    `target emptiness ${formatNumber(caseData.config.target_emptiness, 2)}.`;

  buildMetricCards(caseData);
}

function selectedCandidate(caseData) {
  if (state.selectedFrontierIndex === null) {
    return {
      label: "Best Level",
      imagePath: caseData.best_level.png_path,
      evaluation: caseData.evaluation,
      constraints: caseData.constraints,
      chromosome: caseData.best_level.chromosome,
      asciiPath: caseData.best_level.ascii_path,
    };
  }

  const frontierItem = caseData.frontier[state.selectedFrontierIndex];
  return {
    label: `Frontier Rank ${frontierItem.rank}`,
    imagePath: frontierItem.png_path,
    evaluation: frontierItem.evaluation,
    constraints: frontierItem.constraints,
    chromosome: frontierItem.chromosome,
    asciiPath: frontierItem.ascii_path,
  };
}

function renderViewer(caseData) {
  const candidate = selectedCandidate(caseData);
  const image = document.getElementById("viewer-image");
  const title = document.getElementById("viewer-title");
  const jsonLink = document.getElementById("viewer-json-link");
  const selectedMetrics = document.getElementById("selected-metrics");
  const selectedChromosome = document.getElementById("selected-chromosome");

  title.textContent = candidate.label;
  image.src = candidate.imagePath;
  image.alt = `${candidate.label} render`;

  if (candidate.asciiPath) {
    jsonLink.href = candidate.asciiPath;
    jsonLink.textContent = "Open ASCII";
  } else {
    jsonLink.removeAttribute("href");
    jsonLink.textContent = "ASCII unavailable";
  }

  selectedMetrics.textContent = formatJson({
    evaluation: candidate.evaluation,
    constraints: candidate.constraints,
  });
  selectedChromosome.textContent = formatJson(candidate.chromosome);
}

function renderFrontierList(caseData) {
  const frontierList = document.getElementById("frontier-list");
  frontierList.innerHTML = "";

  caseData.frontier.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "frontier-button";
    if (index === state.selectedFrontierIndex) {
      button.classList.add("active");
    }
    button.innerHTML = `
      <p class="frontier-title">Rank ${item.rank}</p>
      <p class="frontier-meta">
        diff_err=${formatNumber(item.evaluation.difficulty_error)}, 
        div=${formatNumber(item.evaluation.structural_diversity)}, 
        empty_err=${formatNumber(item.evaluation.emptiness_error)}
      </p>
    `;
    button.addEventListener("click", () => {
      state.selectedFrontierIndex = index;
      renderViewer(caseData);
      renderFrontierList(caseData);
    });
    frontierList.appendChild(button);
  });
}

function render() {
  renderCaseList();
  const caseData = currentCase();
  renderCaseSummary(caseData);
  renderViewer(caseData);
  renderFrontierList(caseData);
}

async function boot() {
  if (window.BROWSER_DATA) {
    state.data = window.BROWSER_DATA;
    render();
    return;
  }

  const response = await fetch("./browser_data.json");
  state.data = await response.json();
  render();
}

boot().catch((error) => {
  document.getElementById("case-title").textContent = "Failed to load browser data";
  document.getElementById("case-summary").textContent = String(error);
});
