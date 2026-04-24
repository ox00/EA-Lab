const state = {
  data: null,
  selectedCaseIndex: 0,
  selectedFrontierIndex: null,
  asciiCache: new Map(),
  preview: {
    mode: "autoplay",
    map: null,
    tileSize: 20,
    viewportWidth: 960,
    viewportHeight: 320,
    cameraX: 0,
    autoplaySpeed: 1.6,
    animationId: null,
    lastTimestamp: null,
    actor: null,
    keys: new Set(),
  },
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

function renderCompareGrid() {
  const compareGrid = document.getElementById("compare-grid");
  compareGrid.innerHTML = "";

  state.data.compare_summary.forEach((row) => {
    const card = document.createElement("article");
    card.className = "compare-card";
    card.innerHTML = `
      <p class="frontier-title">${row.title}</p>
      <p class="frontier-meta">${row.objective_mode}</p>
      <p class="frontier-meta">diff_err=${formatNumber(row.difficulty_error)}</p>
      <p class="frontier-meta">curve=${formatNumber(row.difficulty_curve_error)}</p>
      <p class="frontier-meta">family=${formatNumber(row.family_balance)}</p>
      <p class="frontier-meta">hv=${formatNumber(row.front_hv)}</p>
    `;
    compareGrid.appendChild(card);
  });
}

function buildMetricCards(caseData) {
  const metricCards = document.getElementById("metric-cards");
  metricCards.innerHTML = "";

  const metrics = [
    ["objective_mode", caseData.objective_mode || "-"],
    ["difficulty_error", formatNumber(caseData.evaluation.difficulty_error)],
    ["curve_error", formatNumber(caseData.evaluation.difficulty_curve_error)],
    ["family_balance", formatNumber(caseData.evaluation.family_balance)],
    ["emptiness_error", formatNumber(caseData.evaluation.emptiness_error)],
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
        ${caseData.objective_mode} · seed=${caseData.config.seed}
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
    `Mode ${caseData.objective_mode}, population ${caseData.config.population_size}, mutation ${caseData.config.mutation_rate}, ` +
    `seed ${caseData.config.seed}, generations ${caseData.config.generations}.`;
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
      segmentMetadata: caseData.best_level.segment_metadata || [],
      asciiPath: caseData.best_level.ascii_path,
      asciiText: caseData.best_level.ascii_text,
    };
  }

  const frontierItem = caseData.frontier[state.selectedFrontierIndex];
  return {
    label: `Frontier Rank ${frontierItem.rank}`,
    imagePath: frontierItem.png_path,
    evaluation: frontierItem.evaluation,
    constraints: frontierItem.constraints,
    chromosome: frontierItem.chromosome,
    segmentMetadata: frontierItem.segment_metadata || [],
    asciiPath: frontierItem.ascii_path,
    asciiText: frontierItem.ascii_text,
  };
}

function familySequence(segmentMetadata) {
  return segmentMetadata.map((item) => item.family);
}

function tierSequence(segmentMetadata) {
  return segmentMetadata.map((item) => item.difficulty_tier);
}

async function loadAsciiMap(asciiPath) {
  if (!asciiPath) {
    return null;
  }
  if (state.asciiCache.has(asciiPath)) {
    return state.asciiCache.get(asciiPath);
  }

  const response = await fetch(asciiPath);
  const text = await response.text();
  const rows = text
    .trim()
    .split(/\r?\n/)
    .map((line) => line.split(""));
  state.asciiCache.set(asciiPath, rows);
  return rows;
}

function parseAsciiText(asciiText) {
  if (!asciiText) {
    return null;
  }
  return asciiText
    .trim()
    .split(/\r?\n/)
    .map((line) => line.split(""));
}

function solidTile(tile) {
  return ["#", "B", "?", "P"].includes(tile);
}

function tileAt(map, col, row) {
  if (!map || row < 0 || col < 0) return ".";
  if (row >= map.length || col >= map[0].length) return ".";
  return map[row][col];
}

function spawnActor(map) {
  let startCol = 1;
  let startRow = map.length - 3;
  for (let row = 0; row < map.length; row += 1) {
    for (let col = 0; col < map[row].length; col += 1) {
      if (map[row][col] === "S") {
        startCol = col;
        startRow = row;
      }
    }
  }
  return {
    x: startCol * state.preview.tileSize,
    y: startRow * state.preview.tileSize - state.preview.tileSize * 0.8,
    vx: 0,
    vy: 0,
    width: state.preview.tileSize * 0.72,
    height: state.preview.tileSize * 0.9,
    onGround: false,
  };
}

function resetPreviewActor() {
  if (!state.preview.map) {
    return;
  }
  state.preview.actor = spawnActor(state.preview.map);
  state.preview.cameraX = 0;
}

function setPreviewMode(mode) {
  state.preview.mode = mode;
  document.getElementById("preview-mode-badge").textContent = mode === "playable" ? "Playable Lite" : "Auto-Scroll";
  document.getElementById("preview-autoplay").classList.toggle("active", mode === "autoplay");
  document.getElementById("preview-playable").classList.toggle("active", mode === "playable");
  if (mode === "playable") {
    resetPreviewActor();
  }
}

function drawSky(ctx, width, height) {
  const gradient = ctx.createLinearGradient(0, 0, 0, height);
  gradient.addColorStop(0, "#8cd4ff");
  gradient.addColorStop(0.7, "#dbf3ff");
  gradient.addColorStop(0.7, "#f0ddb7");
  gradient.addColorStop(1, "#e9ca8e");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);
}

function drawTile(ctx, tile, x, y, size) {
  if (tile === ".") return;

  if (tile === "#") {
    ctx.fillStyle = "#8c5f39";
    ctx.fillRect(x, y, size, size);
    ctx.fillStyle = "#b98854";
    ctx.fillRect(x, y, size, size * 0.2);
    ctx.fillStyle = "#6d4728";
    ctx.fillRect(x, y + size * 0.2, size, size * 0.8);
    return;
  }

  if (tile === "B") {
    ctx.fillStyle = "#a35d32";
    ctx.fillRect(x, y, size, size);
    ctx.strokeStyle = "#704024";
    ctx.lineWidth = 2;
    ctx.strokeRect(x + 1, y + 1, size - 2, size - 2);
    ctx.beginPath();
    ctx.moveTo(x, y + size / 2);
    ctx.lineTo(x + size, y + size / 2);
    ctx.moveTo(x + size / 2, y);
    ctx.lineTo(x + size / 2, y + size / 2);
    ctx.stroke();
    return;
  }

  if (tile === "?") {
    ctx.fillStyle = "#eab84a";
    ctx.fillRect(x, y, size, size);
    ctx.fillStyle = "#fff2b8";
    ctx.font = `bold ${size * 0.62}px Georgia`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("?", x + size / 2, y + size / 2 + 1);
    return;
  }

  if (tile === "o") {
    ctx.fillStyle = "#ffd95c";
    ctx.beginPath();
    ctx.ellipse(x + size / 2, y + size / 2, size * 0.24, size * 0.36, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#fff2ba";
    ctx.lineWidth = 2;
    ctx.stroke();
    return;
  }

  if (tile === "E") {
    ctx.fillStyle = "#b96b52";
    ctx.beginPath();
    ctx.ellipse(x + size / 2, y + size * 0.68, size * 0.34, size * 0.24, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(x + size * 0.4, y + size * 0.62, size * 0.05, 0, Math.PI * 2);
    ctx.arc(x + size * 0.6, y + size * 0.62, size * 0.05, 0, Math.PI * 2);
    ctx.fill();
    return;
  }

  if (tile === "P") {
    ctx.fillStyle = "#2f9d59";
    ctx.fillRect(x, y + size * 0.12, size, size * 0.88);
    ctx.fillStyle = "#45b86d";
    ctx.fillRect(x - size * 0.08, y, size * 1.16, size * 0.26);
    return;
  }

  if (tile === "S") {
    ctx.fillStyle = "#4c73d8";
    ctx.fillRect(x + size * 0.18, y + size * 0.1, size * 0.2, size * 0.8);
    ctx.fillStyle = "#edf4ff";
    ctx.beginPath();
    ctx.moveTo(x + size * 0.38, y + size * 0.16);
    ctx.lineTo(x + size * 0.8, y + size * 0.28);
    ctx.lineTo(x + size * 0.38, y + size * 0.42);
    ctx.closePath();
    ctx.fill();
    return;
  }

  if (tile === "G") {
    ctx.fillStyle = "#df6f4a";
    ctx.fillRect(x + size * 0.16, y + size * 0.08, size * 0.18, size * 0.84);
    ctx.fillStyle = "#fff4cc";
    ctx.beginPath();
    ctx.moveTo(x + size * 0.34, y + size * 0.16);
    ctx.lineTo(x + size * 0.82, y + size * 0.3);
    ctx.lineTo(x + size * 0.34, y + size * 0.44);
    ctx.closePath();
    ctx.fill();
  }
}

function intersectsSolid(map, actor, nextX, nextY) {
  const size = state.preview.tileSize;
  const minCol = Math.floor(nextX / size);
  const maxCol = Math.floor((nextX + actor.width - 1) / size);
  const minRow = Math.floor(nextY / size);
  const maxRow = Math.floor((nextY + actor.height - 1) / size);

  for (let row = minRow; row <= maxRow; row += 1) {
    for (let col = minCol; col <= maxCol; col += 1) {
      if (solidTile(tileAt(map, col, row))) {
        return { row, col };
      }
    }
  }
  return null;
}

function updatePlayable(dt) {
  const map = state.preview.map;
  const actor = state.preview.actor;
  if (!map || !actor) return;

  const moveLeft = state.preview.keys.has("ArrowLeft") || state.preview.keys.has("a") || state.preview.keys.has("A");
  const moveRight = state.preview.keys.has("ArrowRight") || state.preview.keys.has("d") || state.preview.keys.has("D");
  const jump = state.preview.keys.has("ArrowUp") || state.preview.keys.has("w") || state.preview.keys.has("W") || state.preview.keys.has(" ");

  actor.vx = 0;
  const runSpeed = 150;
  if (moveLeft) actor.vx = -runSpeed;
  if (moveRight) actor.vx = runSpeed;

  if (jump && actor.onGround) {
    actor.vy = -255;
    actor.onGround = false;
  }

  actor.vy += 520 * dt;
  actor.vy = Math.min(actor.vy, 320);

  let nextX = actor.x + actor.vx * dt;
  let hit = intersectsSolid(map, actor, nextX, actor.y);
  if (hit) {
    if (actor.vx > 0) {
      nextX = hit.col * state.preview.tileSize - actor.width;
    } else if (actor.vx < 0) {
      nextX = (hit.col + 1) * state.preview.tileSize;
    }
    actor.vx = 0;
  }
  actor.x = Math.max(0, nextX);

  let nextY = actor.y + actor.vy * dt;
  hit = intersectsSolid(map, actor, actor.x, nextY);
  actor.onGround = false;
  if (hit) {
    if (actor.vy > 0) {
      nextY = hit.row * state.preview.tileSize - actor.height;
      actor.onGround = true;
    } else {
      nextY = (hit.row + 1) * state.preview.tileSize;
    }
    actor.vy = 0;
  }
  actor.y = nextY;

  const maxCamera = Math.max(0, map[0].length * state.preview.tileSize - state.preview.viewportWidth);
  state.preview.cameraX = Math.max(0, Math.min(maxCamera, actor.x - state.preview.viewportWidth * 0.35));
}

function updateAutoplay(dt) {
  const map = state.preview.map;
  if (!map) return;
  const maxCamera = Math.max(0, map[0].length * state.preview.tileSize - state.preview.viewportWidth);
  state.preview.cameraX += state.preview.autoplaySpeed * 60 * dt;
  if (state.preview.cameraX >= maxCamera) {
    state.preview.cameraX = 0;
  }
}

function drawActor(ctx, actor, cameraX) {
  const x = actor.x - cameraX;
  const y = actor.y;
  ctx.fillStyle = "#d84b3d";
  ctx.fillRect(x + actor.width * 0.18, y + actor.height * 0.24, actor.width * 0.64, actor.height * 0.68);
  ctx.fillStyle = "#1e4da8";
  ctx.fillRect(x + actor.width * 0.24, y + actor.height * 0.52, actor.width * 0.52, actor.height * 0.4);
  ctx.fillStyle = "#f5d4b0";
  ctx.beginPath();
  ctx.arc(x + actor.width * 0.5, y + actor.height * 0.22, actor.width * 0.22, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#c73b30";
  ctx.fillRect(x + actor.width * 0.12, y + actor.height * 0.04, actor.width * 0.76, actor.height * 0.16);
}

function drawPreview() {
  const canvas = document.getElementById("preview-canvas");
  const ctx = canvas.getContext("2d");
  const map = state.preview.map;
  if (!map) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return;
  }

  drawSky(ctx, canvas.width, canvas.height);

  const tileSize = state.preview.tileSize;
  const startCol = Math.max(0, Math.floor(state.preview.cameraX / tileSize));
  const endCol = Math.min(map[0].length, startCol + Math.ceil(canvas.width / tileSize) + 2);

  for (let row = 0; row < map.length; row += 1) {
    for (let col = startCol; col < endCol; col += 1) {
      const x = col * tileSize - state.preview.cameraX;
      const y = row * tileSize;
      drawTile(ctx, map[row][col], x, y, tileSize);
    }
  }

  if (state.preview.mode === "playable" && state.preview.actor) {
    drawActor(ctx, state.preview.actor, state.preview.cameraX);
  } else {
    const markerX = 80;
    const markerY = canvas.height - tileSize * 2.9;
    drawActor(ctx, { x: markerX + state.preview.cameraX, y: markerY, width: tileSize * 0.72, height: tileSize * 0.9 }, state.preview.cameraX);
  }
}

function animationStep(timestamp) {
  if (state.preview.lastTimestamp === null) {
    state.preview.lastTimestamp = timestamp;
  }
  const dt = Math.min(0.033, (timestamp - state.preview.lastTimestamp) / 1000);
  state.preview.lastTimestamp = timestamp;

  if (state.preview.mode === "playable") {
    updatePlayable(dt);
  } else {
    updateAutoplay(dt);
  }
  drawPreview();
  state.preview.animationId = requestAnimationFrame(animationStep);
}

function stopPreviewLoop() {
  if (state.preview.animationId) {
    cancelAnimationFrame(state.preview.animationId);
  }
  state.preview.animationId = null;
  state.preview.lastTimestamp = null;
}

function startPreviewLoop() {
  stopPreviewLoop();
  state.preview.animationId = requestAnimationFrame(animationStep);
}

async function updatePreview(caseData) {
  const candidate = selectedCandidate(caseData);
  const map = candidate.asciiText ? parseAsciiText(candidate.asciiText) : await loadAsciiMap(candidate.asciiPath);
  state.preview.map = map;
  resetPreviewActor();
  startPreviewLoop();
  drawPreview();
}

function renderViewer(caseData) {
  const candidate = selectedCandidate(caseData);
  const image = document.getElementById("viewer-image");
  const title = document.getElementById("viewer-title");
  const jsonLink = document.getElementById("viewer-json-link");
  const selectedMetrics = document.getElementById("selected-metrics");
  const selectedChromosome = document.getElementById("selected-chromosome");
  const selectedFamilies = document.getElementById("selected-families");
  const selectedTiers = document.getElementById("selected-tiers");

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
  selectedFamilies.textContent = familySequence(candidate.segmentMetadata).join(" -> ");
  selectedTiers.textContent = tierSequence(candidate.segmentMetadata).join(" -> ");

  updatePreview(caseData).catch((error) => {
    document.getElementById("preview-mode-badge").textContent = "Preview Error";
    document.getElementById("preview-hint").textContent = String(error);
  });
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
        diff=${formatNumber(item.evaluation.difficulty_error)} · curve=${formatNumber(item.evaluation.difficulty_curve_error)} · family=${formatNumber(item.evaluation.family_balance)}
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
  renderCompareGrid();
  renderCaseList();
  const caseData = currentCase();
  renderCaseSummary(caseData);
  renderViewer(caseData);
  renderFrontierList(caseData);
}

function bindPreviewControls() {
  document.getElementById("preview-autoplay").addEventListener("click", () => {
    setPreviewMode("autoplay");
  });

  document.getElementById("preview-playable").addEventListener("click", () => {
    setPreviewMode("playable");
  });

  document.getElementById("preview-reset").addEventListener("click", () => {
    resetPreviewActor();
    state.preview.cameraX = 0;
    drawPreview();
  });

  window.addEventListener("keydown", (event) => {
    if (["ArrowLeft", "ArrowRight", "ArrowUp", " ", "a", "A", "d", "D", "w", "W"].includes(event.key)) {
      event.preventDefault();
    }
    state.preview.keys.add(event.key);
  });

  window.addEventListener("keyup", (event) => {
    state.preview.keys.delete(event.key);
  });
}

async function boot() {
  bindPreviewControls();
  setPreviewMode("autoplay");

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
