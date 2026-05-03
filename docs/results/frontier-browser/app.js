const state = {
  data: null,
  litePhysicsPlans: null,
  selectedCaseIndex: 0,
  selectedFrontierIndex: null,
  asciiCache: new Map(),
  preview: {
    mode: "physics",
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
    maxJumpableGap: 3,
    replayPath: [],
    replayStepIndex: 0,
    replayEdgeProgress: 0,
    replayPause: 0,
    physicsFrameDt: 1 / 30,
    physicsRunSpeed: 150,
    physicsJumpVelocity: -420,
    physicsGravity: 600,
    physicsMaxFallSpeed: 420,
    physicsActionFrames: 4,
    physicsPlan: [],
    physicsPlanFound: false,
    physicsPlanIndex: 0,
    physicsActionFrame: 0,
    physicsAccumulator: 0,
    physicsPause: 0,
    renderer: null,
    renderClock: 0,
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

function renderEvidence(caseData) {
  const evidence = document.getElementById("replay-evidence");
  const planSummary = document.getElementById("physics-plan-summary");
  const candidate = selectedCandidate(caseData);
  const planRecord = currentPlanRecord(caseData);

  evidence.textContent = [
    "constraint-level evidence",
    "- Reachability Replay uses the same tile-level reachable rule as the hard feasibility checker.",
    "- It is aligned with the EA gate, but it does not model collision along the full jump trajectory.",
    "",
    "lite-physics-level evidence",
    "- Lite Physics Replay searches an action sequence under lightweight collision rules.",
    "- Pipes, walls, bricks, and question blocks can block the route.",
    "- It is stronger than tile-level reachability, but still lighter than full Mario physics.",
  ].join("\n");

  if (!planRecord) {
    planSummary.textContent = "No exported lite-physics plan found for this candidate.";
    return;
  }

  planSummary.textContent = [
    `candidate: ${caseData.id} / ${candidate.candidateId}`,
    `label: ${candidate.label}`,
    `plan_found: ${planRecord.plan_found}`,
    `action_count: ${planRecord.action_count}`,
    `estimated_seconds: ${planRecord.estimated_seconds}`,
    `action_counts: ${formatJson(planRecord.action_counts)}`,
    "",
    "actions:",
    (planRecord.actions || []).join(" "),
  ].join("\n");
}

function selectedCandidate(caseData) {
  if (state.selectedFrontierIndex === null) {
    return {
      candidateId: "best",
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
    candidateId: `frontier_${frontierItem.rank}`,
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

function currentPlanRecord(caseData) {
  if (!state.litePhysicsPlans?.items) {
    return null;
  }
  const candidate = selectedCandidate(caseData);
  const key = `${caseData.id}::${candidate.candidateId}`;
  return state.litePhysicsPlans.items.find((item) => item.key === key) || null;
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

function walkableTile(tile) {
  return [".", "S", "G", "o"].includes(tile);
}

function solidTile(tile) {
  return ["#", "B", "?", "P"].includes(tile);
}

function tileAt(map, col, row) {
  if (!map || row < 0 || col < 0) return ".";
  if (row >= map.length || col >= map[0].length) return ".";
  return map[row][col];
}

function standableAt(map, row, col) {
  if (!map || row < 0 || row >= map.length - 1 || col < 0 || col >= map[0].length) {
    return false;
  }
  return walkableTile(tileAt(map, col, row)) && solidTile(tileAt(map, col, row + 1));
}

function findTilePosition(map, target) {
  if (!map) {
    return null;
  }
  for (let row = 0; row < map.length; row += 1) {
    for (let col = 0; col < map[row].length; col += 1) {
      if (map[row][col] === target) {
        return { row, col };
      }
    }
  }
  return null;
}

function actorGeometry() {
  return {
    width: state.preview.tileSize * 0.72,
    height: state.preview.tileSize * 0.9,
  };
}

function actorPoseForNode(node) {
  const { width, height } = actorGeometry();
  return {
    x: node.col * state.preview.tileSize + (state.preview.tileSize - width) / 2,
    y: (node.row + 1) * state.preview.tileSize - height,
    width,
    height,
  };
}

function candidateMaxJumpGap(caseData) {
  return caseData?.config?.max_jumpable_gap ?? 3;
}

function nodeKey(node) {
  return `${node.row}:${node.col}`;
}

function physicsStateKey(actor) {
  return [
    Math.round(actor.x / 6),
    Math.round(actor.y / 6),
    Math.round(actor.vx / 60),
    Math.round(actor.vy / 60),
    actor.onGround ? 1 : 0,
  ].join("|");
}

function rebuildReplayPath(caseData) {
  const map = state.preview.map;
  state.preview.maxJumpableGap = candidateMaxJumpGap(caseData);
  state.preview.replayPath = [];

  const start = findTilePosition(map, "S");
  const goal = findTilePosition(map, "G");
  if (!start || !goal) {
    return;
  }
  if (!standableAt(map, start.row, start.col) || !standableAt(map, goal.row, goal.col)) {
    return;
  }

  const queue = [start];
  const parents = new Map();
  const visited = new Set([nodeKey(start)]);
  let cursor = 0;

  while (cursor < queue.length) {
    const current = queue[cursor];
    cursor += 1;

    if (current.row === goal.row && current.col === goal.col) {
      break;
    }

    for (const step of [-1, 1]) {
      const next = { row: current.row, col: current.col + step };
      const key = nodeKey(next);
      if (standableAt(map, next.row, next.col) && !visited.has(key)) {
        visited.add(key);
        parents.set(key, current);
        queue.push(next);
      }
    }

    for (let jump = 1; jump <= state.preview.maxJumpableGap; jump += 1) {
      for (const direction of [-1, 1]) {
        const next = { row: current.row, col: current.col + direction * jump };
        const key = nodeKey(next);
        if (standableAt(map, next.row, next.col) && !visited.has(key)) {
          visited.add(key);
          parents.set(key, current);
          queue.push(next);
        }
      }
    }
  }

  const goalKey = nodeKey(goal);
  if (!visited.has(goalKey)) {
    return;
  }

  const path = [];
  let current = goal;
  while (current) {
    path.push(current);
    const parent = parents.get(nodeKey(current));
    current = parent || null;
  }

  state.preview.replayPath = path.reverse();
}

function spawnReachabilityActor(map) {
  const fallback = { row: map.length - 3, col: 1 };
  const startNode = findTilePosition(map, "S") || fallback;
  return {
    ...actorPoseForNode(startNode),
    vx: 0,
    vy: 0,
    onGround: true,
  };
}

function spawnPhysicsActor(map) {
  const fallback = { row: map.length - 3, col: 1 };
  const startNode = findTilePosition(map, "S") || fallback;
  const { width, height } = actorGeometry();
  return {
    x: startNode.col * state.preview.tileSize,
    y: startNode.row * state.preview.tileSize - state.preview.tileSize * 0.8,
    vx: 0,
    vy: 0,
    width,
    height,
    onGround: false,
  };
}

function physicsActionInput(actionLabel, frameIndex) {
  const jumpFrame = frameIndex === 0;
  if (actionLabel === "RJ") {
    return { moveLeft: false, moveRight: true, jump: jumpFrame };
  }
  if (actionLabel === "R" || actionLabel === "RR") {
    return { moveLeft: false, moveRight: true, jump: false };
  }
  if (actionLabel === "J") {
    return { moveLeft: false, moveRight: false, jump: jumpFrame };
  }
  return { moveLeft: false, moveRight: false, jump: false };
}

function physicsActionFrameLimit(actionLabel) {
  return actionLabel === "RR" ? state.preview.physicsActionFrames * 2 : state.preview.physicsActionFrames;
}

function stepPhysicsActor(map, actor, input) {
  const next = { ...actor };
  next.vx = 0;

  if (input.moveLeft) next.vx = -state.preview.physicsRunSpeed;
  if (input.moveRight) next.vx = state.preview.physicsRunSpeed;

  if (input.jump && next.onGround) {
    next.vy = state.preview.physicsJumpVelocity;
    next.onGround = false;
  }

  next.vy = Math.min(next.vy + state.preview.physicsGravity * state.preview.physicsFrameDt, state.preview.physicsMaxFallSpeed);

  let nextX = next.x + next.vx * state.preview.physicsFrameDt;
  let hit = intersectsSolid(map, next, nextX, next.y);
  if (hit) {
    if (next.vx > 0) {
      nextX = hit.col * state.preview.tileSize - next.width;
    } else if (next.vx < 0) {
      nextX = (hit.col + 1) * state.preview.tileSize;
    }
    next.vx = 0;
  }
  next.x = Math.max(0, nextX);

  let nextY = next.y + next.vy * state.preview.physicsFrameDt;
  hit = intersectsSolid(map, next, next.x, nextY);
  next.onGround = false;
  if (hit) {
    if (next.vy > 0) {
      nextY = hit.row * state.preview.tileSize - next.height;
      next.onGround = true;
    } else {
      nextY = (hit.row + 1) * state.preview.tileSize;
    }
    next.vy = 0;
  }
  next.y = nextY;
  return next;
}

function settlePhysicsActor(map, actor) {
  let current = { ...actor };
  for (let step = 0; step < 40; step += 1) {
    current = stepPhysicsActor(map, current, { moveLeft: false, moveRight: false, jump: false });
    if (current.onGround) {
      break;
    }
  }
  return current;
}

function reconstructPhysicsPlan(node) {
  const actions = [];
  let current = node;
  while (current && current.parent) {
    actions.push(current.action);
    current = current.parent;
  }
  return actions.reverse();
}

function buildLitePhysicsPlan() {
  const map = state.preview.map;
  state.preview.physicsPlan = [];
  state.preview.physicsPlanFound = false;

  if (!map) {
    return;
  }

  const goal = findTilePosition(map, "G");
  if (!goal) {
    return;
  }

  const goalX = goal.col * state.preview.tileSize;
  const startActor = settlePhysicsActor(map, spawnPhysicsActor(map));
  const open = [{ priority: 0, cost: 0, actor: startActor, parent: null, action: null }];
  const seen = new Map([[physicsStateKey(startActor), 0]]);
  const actionLabels = ["R", "RJ", "RR", "N", "J"];
  let expansions = 0;

  while (open.length > 0 && expansions < 50000) {
    let bestIndex = 0;
    for (let index = 1; index < open.length; index += 1) {
      if (open[index].priority < open[bestIndex].priority) {
        bestIndex = index;
      }
    }

    const current = open.splice(bestIndex, 1)[0];
    if (current.actor.x >= goalX - 10) {
      state.preview.physicsPlan = reconstructPhysicsPlan(current);
      state.preview.physicsPlanFound = true;
      return;
    }

    actionLabels.forEach((actionLabel) => {
      let actor = current.actor;
      for (let frame = 0; frame < physicsActionFrameLimit(actionLabel); frame += 1) {
        actor = stepPhysicsActor(map, actor, physicsActionInput(actionLabel, frame));
      }

      if (actor.x < current.actor.x - 10) {
        return;
      }

      const cost = current.cost + 1;
      const key = physicsStateKey(actor);
      if ((seen.get(key) ?? Number.POSITIVE_INFINITY) <= cost) {
        return;
      }

      seen.set(key, cost);
      const heuristic = Math.max(0, (goalX - actor.x) / 80);
      open.push({
        priority: cost + heuristic,
        cost,
        actor,
        parent: current,
        action: actionLabel,
      });
    });

    expansions += 1;
  }
}

function resetPreviewActor() {
  if (!state.preview.map) {
    return;
  }
  if (state.preview.mode === "replay") {
    state.preview.actor = spawnReachabilityActor(state.preview.map);
  } else {
    state.preview.actor = settlePhysicsActor(state.preview.map, spawnPhysicsActor(state.preview.map));
  }
  state.preview.cameraX = 0;
  state.preview.replayStepIndex = 0;
  state.preview.replayEdgeProgress = 0;
  state.preview.replayPause = 0;
  state.preview.physicsPlanIndex = 0;
  state.preview.physicsActionFrame = 0;
  state.preview.physicsAccumulator = 0;
  state.preview.physicsPause = 0;
}

function setPreviewMode(mode) {
  state.preview.mode = mode;
  const badge = document.getElementById("preview-mode-badge");
  const hint = document.getElementById("preview-hint");
  badge.textContent =
    mode === "playable"
      ? "Playable Lite"
      : mode === "physics"
        ? "Lite Physics Replay"
        : mode === "replay"
          ? "Reachability Replay"
          : "Auto-Scroll";
  hint.textContent =
    mode === "playable"
      ? "Keys: A/D or arrow keys to move, W / Space / Up to jump. Uses the same lite physics as the replay planner."
      : mode === "physics"
        ? "Action-level replay with pipe and wall collision under lightweight browser physics."
      : mode === "replay"
        ? "Tile-level reachable path from the hard constraint model. Fast, but less realistic."
        : "Camera sweep preview for fast browsing. Use Lite Physics Replay for the stronger pass-through demo.";
  document.getElementById("preview-autoplay").classList.toggle("active", mode === "autoplay");
  document.getElementById("preview-replay").classList.toggle("active", mode === "replay");
  document.getElementById("preview-physics").classList.toggle("active", mode === "physics");
  document.getElementById("preview-playable").classList.toggle("active", mode === "playable");
  if (mode === "playable" || mode === "replay" || mode === "physics") {
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

function updateCameraFromActor() {
  const map = state.preview.map;
  const actor = state.preview.actor;
  if (!map || !actor) {
    return;
  }
  const maxCamera = Math.max(0, map[0].length * state.preview.tileSize - state.preview.viewportWidth);
  state.preview.cameraX = Math.max(0, Math.min(maxCamera, actor.x - state.preview.viewportWidth * 0.35));
}

function updatePlayable(dt) {
  const map = state.preview.map;
  const actor = state.preview.actor;
  if (!map || !actor) return;

  const moveLeft = state.preview.keys.has("ArrowLeft") || state.preview.keys.has("a") || state.preview.keys.has("A");
  const moveRight = state.preview.keys.has("ArrowRight") || state.preview.keys.has("d") || state.preview.keys.has("D");
  const jump = state.preview.keys.has("ArrowUp") || state.preview.keys.has("w") || state.preview.keys.has("W") || state.preview.keys.has(" ");

  state.preview.physicsAccumulator += dt;
  while (state.preview.physicsAccumulator >= state.preview.physicsFrameDt) {
    state.preview.actor = stepPhysicsActor(map, state.preview.actor, { moveLeft, moveRight, jump });
    state.preview.physicsAccumulator -= state.preview.physicsFrameDt;
  }

  updateCameraFromActor();
}

function updateReplay(dt) {
  const path = state.preview.replayPath;
  if (!path.length) {
    updateAutoplay(dt);
    return;
  }

  if (path.length === 1) {
    const pose = actorPoseForNode(path[0]);
    state.preview.actor = { ...state.preview.actor, ...pose, vx: 0, vy: 0, onGround: true };
    return;
  }

  if (state.preview.replayStepIndex >= path.length - 1) {
    state.preview.replayPause += dt;
    const finalPose = actorPoseForNode(path[path.length - 1]);
    state.preview.actor = { ...state.preview.actor, ...finalPose, vx: 0, vy: 0, onGround: true };
    if (state.preview.replayPause >= 1.15) {
      resetPreviewActor();
    }
  } else {
    const fromNode = path[state.preview.replayStepIndex];
    const toNode = path[state.preview.replayStepIndex + 1];
    const fromPose = actorPoseForNode(fromNode);
    const toPose = actorPoseForNode(toNode);
    const deltaCols = Math.abs(toNode.col - fromNode.col);
    const isJump = deltaCols > 1;
    const duration = isJump ? 0.24 + deltaCols * 0.08 : 0.12;

    state.preview.replayEdgeProgress += dt / duration;
    let t = state.preview.replayEdgeProgress;

    if (t >= 1) {
      state.preview.replayStepIndex += 1;
      state.preview.replayEdgeProgress = 0;
      t = 1;
    }

    const x = fromPose.x + (toPose.x - fromPose.x) * t;
    let y = fromPose.y + (toPose.y - fromPose.y) * t;
    if (isJump) {
      const hopHeight = state.preview.tileSize * (0.95 + 0.35 * (deltaCols - 2 >= 0 ? deltaCols - 2 : 0));
      y -= Math.sin(Math.PI * t) * hopHeight;
    }

    state.preview.actor = {
      ...state.preview.actor,
      x,
      y,
      width: fromPose.width,
      height: fromPose.height,
      vx: 0,
      vy: 0,
      onGround: !isJump || t >= 0.98,
    };
  }

  updateCameraFromActor();
}

function updatePhysicsReplay(dt) {
  const map = state.preview.map;
  const actor = state.preview.actor;
  if (!map || !actor) {
    return;
  }

  if (!state.preview.physicsPlanFound || state.preview.physicsPlan.length === 0) {
    updateAutoplay(dt);
    return;
  }

  state.preview.physicsAccumulator += dt;
  while (state.preview.physicsAccumulator >= state.preview.physicsFrameDt) {
    if (state.preview.physicsPlanIndex >= state.preview.physicsPlan.length) {
      state.preview.physicsPause += state.preview.physicsFrameDt;
      if (state.preview.physicsPause >= 1.15) {
        resetPreviewActor();
      }
      state.preview.physicsAccumulator -= state.preview.physicsFrameDt;
      continue;
    }

    const actionLabel = state.preview.physicsPlan[state.preview.physicsPlanIndex];
    const input = physicsActionInput(actionLabel, state.preview.physicsActionFrame);
    state.preview.actor = stepPhysicsActor(map, state.preview.actor, input);
    state.preview.physicsActionFrame += 1;

    if (state.preview.physicsActionFrame >= physicsActionFrameLimit(actionLabel)) {
      state.preview.physicsActionFrame = 0;
      state.preview.physicsPlanIndex += 1;
    }

    state.preview.physicsAccumulator -= state.preview.physicsFrameDt;
  }

  updateCameraFromActor();
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

function drawActor(ctx, actor, cameraX, options = {}) {
  const velocity = options.velocity ?? actor.vx ?? 0;
  const phase = options.phase ?? state.preview.renderClock * 10 + actor.x * 0.015;
  const bob = options.disableBob ? 0 : Math.sin(phase) * Math.min(actor.height * 0.05, 2.5);
  const runTilt = Math.max(-0.2, Math.min(0.2, velocity / 260));
  const x = actor.x - cameraX;
  const y = actor.y + bob;

  ctx.fillStyle = "rgba(30, 35, 34, 0.16)";
  ctx.beginPath();
  ctx.ellipse(x + actor.width * 0.5, y + actor.height * 0.98, actor.width * 0.42, actor.height * 0.12, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.translate(x + actor.width * 0.5, y + actor.height * 0.54);
  ctx.rotate(runTilt * 0.15);
  ctx.fillStyle = "#d84b3d";
  ctx.fillRect(-actor.width * 0.32, -actor.height * 0.3, actor.width * 0.64, actor.height * 0.68);
  ctx.fillStyle = "#1e4da8";
  ctx.fillRect(-actor.width * 0.26, -actor.height * 0.02, actor.width * 0.52, actor.height * 0.4);
  ctx.restore();

  const legSwing = Math.sin(phase) * actor.width * 0.1;
  ctx.strokeStyle = "#173a80";
  ctx.lineWidth = Math.max(2, actor.width * 0.12);
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(x + actor.width * 0.44, y + actor.height * 0.78);
  ctx.lineTo(x + actor.width * 0.34 + legSwing, y + actor.height * 0.98);
  ctx.moveTo(x + actor.width * 0.58, y + actor.height * 0.78);
  ctx.lineTo(x + actor.width * 0.68 - legSwing, y + actor.height * 0.98);
  ctx.stroke();

  ctx.fillStyle = "#f5d4b0";
  ctx.beginPath();
  ctx.arc(x + actor.width * 0.5, y + actor.height * 0.22, actor.width * 0.22, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "#9b2b24";
  ctx.lineWidth = Math.max(2, actor.width * 0.08);
  ctx.beginPath();
  ctx.moveTo(x + actor.width * 0.38, y + actor.height * 0.46);
  ctx.lineTo(x + actor.width * 0.28 - legSwing * 0.35, y + actor.height * 0.64);
  ctx.moveTo(x + actor.width * 0.62, y + actor.height * 0.48);
  ctx.lineTo(x + actor.width * 0.74 + legSwing * 0.35, y + actor.height * 0.64);
  ctx.stroke();

  ctx.fillStyle = "#c73b30";
  ctx.fillRect(x + actor.width * 0.12, y + actor.height * 0.04, actor.width * 0.76, actor.height * 0.16);
  ctx.fillStyle = "#f7e9cf";
  ctx.fillRect(x + actor.width * 0.2, y + actor.height * 0.09, actor.width * 0.16, actor.height * 0.035);
}

function physicsActionLabel(actionLabel) {
  if (actionLabel === "RR") return "Run Long";
  if (actionLabel === "RJ") return "Run + Jump";
  if (actionLabel === "R") return "Run";
  if (actionLabel === "J") return "Jump";
  if (actionLabel === "N") return "Neutral";
  return "Idle";
}

function previewHudLines() {
  const map = state.preview.map;
  if (!map) {
    return [];
  }

  if (state.preview.mode === "physics") {
    const total = state.preview.physicsPlan.length;
    const stepIndex = Math.min(state.preview.physicsPlanIndex, Math.max(0, total - 1));
    const currentAction =
      total === 0
        ? "Unavailable"
        : state.preview.physicsPlanIndex >= total
          ? "Goal Reached"
          : physicsActionLabel(state.preview.physicsPlan[stepIndex]);
    const frameLimit =
      state.preview.physicsPlanIndex >= total || total === 0
        ? 0
        : physicsActionFrameLimit(state.preview.physicsPlan[stepIndex]);
    const actionProgress =
      frameLimit > 0
        ? `${Math.min(state.preview.physicsActionFrame + 1, frameLimit)}/${frameLimit}`
        : "-";
    const overallProgress =
      total > 0
        ? `${Math.min(state.preview.physicsPlanIndex + (frameLimit > 0 ? state.preview.physicsActionFrame / frameLimit : 0), total).toFixed(1)}/${total}`
        : "0/0";
    const percent =
      total > 0
        ? `${((Math.min(state.preview.physicsPlanIndex + (frameLimit > 0 ? state.preview.physicsActionFrame / frameLimit : 0), total) / total) * 100).toFixed(1)}%`
        : "0.0%";
    return [
      "Lite Physics Replay",
      `Action: ${currentAction}`,
      `Action Progress: ${actionProgress}`,
      `Plan Progress: ${overallProgress} (${percent})`,
    ];
  }

  if (state.preview.mode === "replay") {
    const total = state.preview.replayPath.length;
    const step = Math.min(state.preview.replayStepIndex + 1, total);
    const percent = total > 0 ? `${((step / total) * 100).toFixed(1)}%` : "0.0%";
    return [
      "Reachability Replay",
      "Mode: Constraint-Level Path",
      `Node Progress: ${step}/${total}`,
      `Coverage: ${percent}`,
    ];
  }

  if (state.preview.mode === "playable") {
    const actorX = state.preview.actor ? state.preview.actor.x.toFixed(1) : "0.0";
    return [
      "Playable Lite",
      "Mode: Manual Control",
      `Actor X: ${actorX}px`,
      "Keys: A/D/W or Arrows/Space",
    ];
  }

  const maxCamera = Math.max(0, map[0].length * state.preview.tileSize - state.preview.viewportWidth);
  const percent = maxCamera > 0 ? `${((state.preview.cameraX / maxCamera) * 100).toFixed(1)}%` : "0.0%";
  return [
    "Auto-Scroll",
    "Mode: Fast Browse",
    `Camera X: ${state.preview.cameraX.toFixed(1)}px`,
    `Sweep: ${percent}`,
  ];
}

function drawPreviewHud(ctx, canvas) {
  const lines = previewHudLines();
  if (!lines.length) {
    return;
  }

  const panelX = 16;
  const panelY = 14;
  const lineHeight = 18;
  const panelWidth = 280;
  const panelHeight = 18 + lines.length * lineHeight;

  ctx.fillStyle = "rgba(27, 31, 28, 0.72)";
  ctx.fillRect(panelX, panelY, panelWidth, panelHeight);
  ctx.strokeStyle = "rgba(255, 250, 241, 0.22)";
  ctx.lineWidth = 1;
  ctx.strokeRect(panelX + 0.5, panelY + 0.5, panelWidth - 1, panelHeight - 1);

  ctx.fillStyle = "#fffaf1";
  ctx.font = '13px "IBM Plex Sans", "Avenir Next", sans-serif';
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  lines.forEach((line, index) => {
    ctx.fillText(line, panelX + 12, panelY + 10 + index * lineHeight);
  });
}

function createShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const message = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(`WebGL shader compile failed: ${message}`);
  }
  return shader;
}

function createProgram(gl, vertexSource, fragmentSource) {
  const program = gl.createProgram();
  gl.attachShader(program, createShader(gl, gl.VERTEX_SHADER, vertexSource));
  gl.attachShader(program, createShader(gl, gl.FRAGMENT_SHADER, fragmentSource));
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const message = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(`WebGL program link failed: ${message}`);
  }
  return program;
}

function createTextureFromCanvas(gl, canvas, options = {}) {
  const pixelated = options.pixelated !== false;
  const texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, pixelated ? gl.NEAREST : gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, pixelated ? gl.NEAREST : gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas);
  return texture;
}

function buildPreviewSpriteAtlas(tileSize) {
  const spriteKeys = ["#", "B", "?", "o", "E", "P", "S", "G", "ACTOR"];
  const cols = 3;
  const rows = Math.ceil(spriteKeys.length / cols);
  const atlas = document.createElement("canvas");
  atlas.width = cols * tileSize;
  atlas.height = rows * tileSize;
  const ctx = atlas.getContext("2d");
  const lookup = {};

  spriteKeys.forEach((key, index) => {
    const col = index % cols;
    const row = Math.floor(index / cols);
    const x = col * tileSize;
    const y = row * tileSize;
    ctx.clearRect(x, y, tileSize, tileSize);
    ctx.save();
    ctx.translate(x, y);
    if (key === "ACTOR") {
      drawActor(
        ctx,
        {
          x: 0,
          y: 0,
          width: tileSize * 0.72,
          height: tileSize * 0.9,
        },
        0,
      );
    } else {
      drawTile(ctx, key, 0, 0, tileSize);
    }
    ctx.restore();
    lookup[key] = {
      u0: x / atlas.width,
      v0: y / atlas.height,
      u1: (x + tileSize) / atlas.width,
      v1: (y + tileSize) / atlas.height,
    };
  });

  return { atlas, lookup };
}

function buildPreviewBackgroundTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 256;
  const ctx = canvas.getContext("2d");
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#8cd4ff");
  gradient.addColorStop(0.68, "#dbf3ff");
  gradient.addColorStop(0.68, "#f0ddb7");
  gradient.addColorStop(1, "#e9ca8e");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < 18; i += 1) {
    const x = (i * 47) % canvas.width;
    const y = 20 + ((i * 23) % 96);
    ctx.fillStyle = "rgba(255,255,255,0.15)";
    ctx.beginPath();
    ctx.arc(x, y, 10 + (i % 3) * 4, 0, Math.PI * 2);
    ctx.arc(x + 12, y + 4, 8 + (i % 2) * 4, 0, Math.PI * 2);
    ctx.arc(x + 22, y, 10, 0, Math.PI * 2);
    ctx.fill();
  }
  return canvas;
}

function buildPreviewCloudTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 1024;
  canvas.height = 320;
  const ctx = canvas.getContext("2d");
  const clouds = [
    [90, 64, 48],
    [280, 92, 54],
    [520, 56, 44],
    [760, 84, 58],
    [920, 48, 36],
  ];
  clouds.forEach(([x, y, radius]) => {
    ctx.fillStyle = "rgba(255,255,255,0.78)";
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.arc(x + radius * 0.8, y + 10, radius * 0.8, 0, Math.PI * 2);
    ctx.arc(x + radius * 1.5, y - 6, radius * 0.72, 0, Math.PI * 2);
    ctx.fill();
  });
  return canvas;
}

function buildPreviewHillTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 1024;
  canvas.height = 320;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "rgba(96, 159, 110, 0.42)";
  ctx.beginPath();
  ctx.moveTo(0, 250);
  ctx.bezierCurveTo(80, 170, 180, 180, 280, 250);
  ctx.bezierCurveTo(360, 190, 470, 175, 560, 250);
  ctx.bezierCurveTo(660, 165, 785, 170, 910, 250);
  ctx.lineTo(1024, 320);
  ctx.lineTo(0, 320);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "rgba(54, 118, 69, 0.62)";
  ctx.beginPath();
  ctx.moveTo(0, 285);
  ctx.bezierCurveTo(110, 220, 210, 215, 320, 286);
  ctx.bezierCurveTo(420, 226, 530, 230, 670, 288);
  ctx.bezierCurveTo(780, 230, 905, 225, 1024, 292);
  ctx.lineTo(1024, 320);
  ctx.lineTo(0, 320);
  ctx.closePath();
  ctx.fill();
  return canvas;
}

function pushTexturedQuad(vertices, x, y, width, height, uv) {
  vertices.push(
    x, y, uv.u0, uv.v0,
    x + width, y, uv.u1, uv.v0,
    x, y + height, uv.u0, uv.v1,
    x, y + height, uv.u0, uv.v1,
    x + width, y, uv.u1, uv.v0,
    x + width, y + height, uv.u1, uv.v1,
  );
}

function pushParallaxTexture(vertices, x, width, height) {
  pushTexturedQuad(vertices, x, 0, width, height, { u0: 0, v0: 0, u1: 1, v1: 1 });
  if (x > 0) {
    pushTexturedQuad(vertices, x - width, 0, width, height, { u0: 0, v0: 0, u1: 1, v1: 1 });
  } else {
    pushTexturedQuad(vertices, x + width, 0, width, height, { u0: 0, v0: 0, u1: 1, v1: 1 });
  }
}

function initPreviewRenderer() {
  const sceneCanvas = document.getElementById("preview-canvas");
  const overlayCanvas = document.getElementById("preview-overlay");
  if (!sceneCanvas || !overlayCanvas) {
    return null;
  }

  const vertexSource = `
    attribute vec2 a_position;
    attribute vec2 a_texCoord;
    uniform vec2 u_resolution;
    varying vec2 v_texCoord;
    void main() {
      vec2 zeroToOne = a_position / u_resolution;
      vec2 clipSpace = zeroToOne * 2.0 - 1.0;
      gl_Position = vec4(clipSpace * vec2(1.0, -1.0), 0.0, 1.0);
      v_texCoord = a_texCoord;
    }
  `;
  const fragmentSource = `
    precision mediump float;
    varying vec2 v_texCoord;
    uniform sampler2D u_texture;
    void main() {
      gl_FragColor = texture2D(u_texture, v_texCoord);
    }
  `;

  try {
    const gl = sceneCanvas.getContext("webgl", {
      alpha: false,
      antialias: true,
      premultipliedAlpha: true,
    });
    if (!gl) {
      return {
        mode: "2d",
        sceneCanvas,
        overlayCanvas,
        overlayCtx: overlayCanvas.getContext("2d"),
      };
    }

    const program = createProgram(gl, vertexSource, fragmentSource);
    const positionLocation = gl.getAttribLocation(program, "a_position");
    const texCoordLocation = gl.getAttribLocation(program, "a_texCoord");
    const resolutionLocation = gl.getUniformLocation(program, "u_resolution");
    const textureLocation = gl.getUniformLocation(program, "u_texture");
    const buffer = gl.createBuffer();
    const { atlas, lookup } = buildPreviewSpriteAtlas(state.preview.tileSize);
    const atlasTexture = createTextureFromCanvas(gl, atlas);
    const backgroundTexture = createTextureFromCanvas(gl, buildPreviewBackgroundTexture(), { pixelated: false });
    const cloudTexture = createTextureFromCanvas(gl, buildPreviewCloudTexture(), { pixelated: false });
    const hillTexture = createTextureFromCanvas(gl, buildPreviewHillTexture(), { pixelated: false });
    const actorCanvas = document.createElement("canvas");
    actorCanvas.width = 64;
    actorCanvas.height = 64;
    const actorTexture = createTextureFromCanvas(gl, actorCanvas);

    gl.useProgram(program);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 16, 0);
    gl.enableVertexAttribArray(texCoordLocation);
    gl.vertexAttribPointer(texCoordLocation, 2, gl.FLOAT, false, 16, 8);
    gl.uniform2f(resolutionLocation, sceneCanvas.width, sceneCanvas.height);
    gl.uniform1i(textureLocation, 0);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    return {
      mode: "webgl",
      sceneCanvas,
      overlayCanvas,
      overlayCtx: overlayCanvas.getContext("2d"),
      gl,
      program,
      buffer,
      positionLocation,
      texCoordLocation,
      resolutionLocation,
      textureLocation,
      atlasTexture,
      backgroundTexture,
      cloudTexture,
      hillTexture,
      actorCanvas,
      actorTexture,
      spriteLookup: lookup,
    };
  } catch (error) {
    console.warn("Preview WebGL initialization failed, falling back to 2D canvas.", error);
    return {
      mode: "2d",
      sceneCanvas,
      overlayCanvas,
      overlayCtx: overlayCanvas.getContext("2d"),
    };
  }
}

function ensurePreviewRenderer() {
  if (!state.preview.renderer) {
    state.preview.renderer = initPreviewRenderer();
  }
  return state.preview.renderer;
}

function drawParallaxBackground2d(ctx, width, height) {
  drawSky(ctx, width, height);
  const clock = state.preview.renderClock;
  const camera = state.preview.cameraX;

  ctx.save();
  ctx.globalAlpha = 0.75;
  const cloudShift = -((camera * 0.18 + clock * 12) % (width + 180));
  for (let i = 0; i < 4; i += 1) {
    const x = cloudShift + i * 300;
    const y = 48 + (i % 2) * 24;
    ctx.fillStyle = "rgba(255,255,255,0.72)";
    ctx.beginPath();
    ctx.arc(x, y, 22, 0, Math.PI * 2);
    ctx.arc(x + 20, y + 6, 18, 0, Math.PI * 2);
    ctx.arc(x + 40, y, 22, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();

  const farShift = -((camera * 0.12) % (width + 240));
  ctx.fillStyle = "rgba(114, 179, 122, 0.42)";
  for (let i = -1; i < 3; i += 1) {
    const x = farShift + i * 420;
    ctx.beginPath();
    ctx.moveTo(x, height);
    ctx.quadraticCurveTo(x + 120, height - 95, x + 240, height);
    ctx.closePath();
    ctx.fill();
  }

  const nearShift = -((camera * 0.28) % (width + 240));
  ctx.fillStyle = "rgba(56, 122, 73, 0.54)";
  for (let i = -1; i < 3; i += 1) {
    const x = nearShift + i * 360;
    ctx.beginPath();
    ctx.moveTo(x, height);
    ctx.quadraticCurveTo(x + 90, height - 72, x + 180, height);
    ctx.closePath();
    ctx.fill();
  }
}

function drawPreviewScene2d(ctx, canvas, map) {
  drawParallaxBackground2d(ctx, canvas.width, canvas.height);

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

  if ((state.preview.mode === "playable" || state.preview.mode === "replay" || state.preview.mode === "physics") && state.preview.actor) {
    drawActor(ctx, state.preview.actor, state.preview.cameraX);
  } else {
    const markerX = 80;
    const markerY = canvas.height - tileSize * 2.9;
    drawActor(ctx, { x: markerX + state.preview.cameraX, y: markerY, width: tileSize * 0.72, height: tileSize * 0.9 }, state.preview.cameraX);
  }
}

function updateActorTexture(renderer, actor) {
  const ctx = renderer.actorCanvas.getContext("2d");
  const canvas = renderer.actorCanvas;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawActor(
    ctx,
    {
      x: 8,
      y: 4,
      width: 46,
      height: 56,
      vx: actor?.vx ?? 0,
    },
    0,
    {
      phase: state.preview.renderClock * 10 + (actor?.x ?? 0) * 0.02,
      velocity: actor?.vx ?? 0,
      disableBob: true,
    },
  );
  const { gl } = renderer;
  gl.bindTexture(gl.TEXTURE_2D, renderer.actorTexture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas);
}

function drawWebglBatch(renderer, texture, vertices) {
  if (!vertices.length) {
    return;
  }
  const { gl, buffer } = renderer;
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.DYNAMIC_DRAW);
  gl.drawArrays(gl.TRIANGLES, 0, vertices.length / 4);
}

function drawPreviewSceneWebgl(renderer, map) {
  const { gl, sceneCanvas, spriteLookup, atlasTexture, backgroundTexture, cloudTexture, hillTexture } = renderer;
  const tileSize = state.preview.tileSize;
  const startCol = Math.max(0, Math.floor(state.preview.cameraX / tileSize));
  const endCol = Math.min(map[0].length, startCol + Math.ceil(sceneCanvas.width / tileSize) + 2);

  gl.viewport(0, 0, sceneCanvas.width, sceneCanvas.height);
  gl.clearColor(0.54, 0.83, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
  gl.useProgram(renderer.program);
  gl.uniform2f(renderer.resolutionLocation, sceneCanvas.width, sceneCanvas.height);

  const bgVertices = [];
  pushTexturedQuad(bgVertices, 0, 0, sceneCanvas.width, sceneCanvas.height, { u0: 0, v0: 0, u1: 1, v1: 1 });
  drawWebglBatch(renderer, backgroundTexture, bgVertices);

  const cloudVertices = [];
  const cloudOffset = -((state.preview.cameraX * 0.18 + state.preview.renderClock * 12) % 1024);
  pushParallaxTexture(cloudVertices, cloudOffset, 1024, sceneCanvas.height);
  drawWebglBatch(renderer, cloudTexture, cloudVertices);

  const hillVertices = [];
  const hillOffset = -((state.preview.cameraX * 0.22) % 1024);
  pushParallaxTexture(hillVertices, hillOffset, 1024, sceneCanvas.height);
  drawWebglBatch(renderer, hillTexture, hillVertices);

  const tileVertices = [];
  for (let row = 0; row < map.length; row += 1) {
    for (let col = startCol; col < endCol; col += 1) {
      const tile = map[row][col];
      if (tile === "." || !spriteLookup[tile]) {
        continue;
      }
      const x = col * tileSize - state.preview.cameraX;
      const y = row * tileSize;
      pushTexturedQuad(tileVertices, x, y, tileSize, tileSize, spriteLookup[tile]);
    }
  }
  drawWebglBatch(renderer, atlasTexture, tileVertices);

  const actorVertices = [];
  if ((state.preview.mode === "playable" || state.preview.mode === "replay" || state.preview.mode === "physics") && state.preview.actor) {
    updateActorTexture(renderer, state.preview.actor);
    pushTexturedQuad(
      actorVertices,
      state.preview.actor.x - state.preview.cameraX,
      state.preview.actor.y,
      state.preview.actor.width,
      state.preview.actor.height,
      { u0: 0, v0: 0, u1: 1, v1: 1 },
    );
  } else {
    const markerX = 80;
    const markerY = sceneCanvas.height - tileSize * 2.9;
    updateActorTexture(renderer, { x: markerX + state.preview.cameraX, y: markerY, width: tileSize * 0.72, height: tileSize * 0.9, vx: state.preview.autoplaySpeed * 40 });
    pushTexturedQuad(actorVertices, markerX, markerY, tileSize * 0.72, tileSize * 0.9, { u0: 0, v0: 0, u1: 1, v1: 1 });
  }
  drawWebglBatch(renderer, renderer.actorTexture, actorVertices);
}

function drawPreview() {
  const renderer = ensurePreviewRenderer();
  const canvas = renderer?.sceneCanvas || document.getElementById("preview-canvas");
  const overlayCanvas = renderer?.overlayCanvas || document.getElementById("preview-overlay");
  const overlayCtx = renderer?.overlayCtx || overlayCanvas?.getContext("2d");
  const map = state.preview.map;
  if (!map) {
    if (renderer?.mode === "2d") {
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    } else if (renderer?.gl) {
      renderer.gl.viewport(0, 0, canvas.width, canvas.height);
      renderer.gl.clearColor(0, 0, 0, 0);
      renderer.gl.clear(renderer.gl.COLOR_BUFFER_BIT);
    }
    if (overlayCtx) {
      overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
    }
    return;
  }

  if (renderer?.mode === "webgl") {
    drawPreviewSceneWebgl(renderer, map);
  } else {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPreviewScene2d(ctx, canvas, map);
  }

  if (overlayCtx) {
    overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
    drawPreviewHud(overlayCtx, overlayCanvas);
  }
}

function animationStep(timestamp) {
  if (state.preview.lastTimestamp === null) {
    state.preview.lastTimestamp = timestamp;
  }
  const dt = Math.min(0.033, (timestamp - state.preview.lastTimestamp) / 1000);
  state.preview.lastTimestamp = timestamp;
  state.preview.renderClock += dt;

  if (state.preview.mode === "playable") {
    updatePlayable(dt);
  } else if (state.preview.mode === "physics") {
    updatePhysicsReplay(dt);
  } else if (state.preview.mode === "replay") {
    updateReplay(dt);
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
  rebuildReplayPath(caseData);
  buildLitePhysicsPlan();
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
  renderEvidence(caseData);

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

  document.getElementById("preview-replay").addEventListener("click", () => {
    setPreviewMode("replay");
  });

  document.getElementById("preview-physics").addEventListener("click", () => {
    setPreviewMode("physics");
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
  setPreviewMode("physics");
  state.litePhysicsPlans = window.LITE_PHYSICS_PLANS || null;

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
