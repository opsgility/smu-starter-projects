/* ── Dungeon Quest — frontend game logic ──────────────────────────────────── */
"use strict";

// ── State ─────────────────────────────────────────────────────────────────────
let state = {
  room:         null,
  player:       null,
  combat:       null,
  dialogueWith: null,   // character_id if in dialogue mode
  mapLayout:    null,   // {room_id: {name, coords, exits}}
  visited:      [],     // [room_id, ...]
};

// ── DOM refs ──────────────────────────────────────────────────────────────────
const $log        = document.getElementById("log");
const $input      = document.getElementById("cmd-input");
const $roomBg     = document.getElementById("room-bg");
const $roomName   = document.getElementById("room-name-overlay");
const $exitsList  = document.getElementById("exits-list");
const $npcsRow    = document.getElementById("npcs-row");
const $enemiesRow = document.getElementById("enemies-row");
const $hpText     = document.getElementById("hp-text");
const $goldText   = document.getElementById("gold-text");
const $combatHud  = document.getElementById("combat-hud");
const $enemyPortrait = document.getElementById("enemy-portrait");
const $enemyName  = document.getElementById("enemy-name-text");
const $enemyHpBar = document.getElementById("enemy-hp-bar");
const $enemyHpText = document.getElementById("enemy-hp-text");
const $loading    = document.getElementById("loading-overlay");
const $gameOver   = document.getElementById("game-over-overlay");
const $minimap    = document.getElementById("minimap");
const $minimapBar = document.getElementById("minimap-bar");
const $minimapToggle = document.getElementById("minimap-toggle");
const $minimapCount  = document.getElementById("minimap-count");
const $speechToggleLabel = document.getElementById("speech-toggle-label");
const $speechToggle      = document.getElementById("speech-toggle");

// ── Speech narration state ────────────────────────────────────────────────────
let currentAudio = null;

if ($speechToggle) {
  $speechToggle.addEventListener("change", () => {
    $speechToggleLabel.classList.toggle("is-on", $speechToggle.checked);
    if (!$speechToggle.checked && currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }
  });
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", startGame);

document.getElementById("btn-send").addEventListener("click", handleInput);
document.getElementById("btn-restart").addEventListener("click", startGame);
document.getElementById("btn-new-game").addEventListener("click", () => {
  $gameOver.classList.add("hidden");
  startGame();
});

$input.addEventListener("keydown", e => {
  if (e.key === "Enter") handleInput();
});

document.querySelectorAll(".combat-btn").forEach(btn => {
  btn.addEventListener("click", () => combatAction(btn.dataset.action));
});

$minimapToggle.addEventListener("click", () => {
  $minimapBar.classList.toggle("collapsed");
});

// ── Game start ────────────────────────────────────────────────────────────────
async function startGame() {
  clearLog();
  setLoading(true);
  state.dialogueWith = null;
  try {
    const data = await api("api/start", {});
    applyUpdate(data);
    appendLog(data.narrative, "narrator");
  } catch (e) {
    appendLog("Could not connect to the dungeon server. Is app.py running?", "system");
  }
  setLoading(false);
  $input.focus();
}

// ── Input handling ────────────────────────────────────────────────────────────
async function handleInput() {
  const raw = $input.value.trim();
  if (!raw) return;
  $input.value = "";

  appendLog(`> ${raw}`, "player");

  // If in dialogue mode, send straight to talk endpoint
  if (state.dialogueWith) {
    if (raw.toLowerCase() === "bye" || raw.toLowerCase() === "leave") {
      state.dialogueWith = null;
      appendLog("You end the conversation.", "system");
      return;
    }
    await doTalk(state.dialogueWith, raw);
    return;
  }

  // If in combat, direct player input to action
  if (state.combat) {
    const action = parseCombatInput(raw);
    if (action) { await combatAction(action); return; }
  }

  // Otherwise, check for a few client-side quick commands first
  const lower = raw.toLowerCase();

  // Movement: handled deterministically, no LLM round-trip needed
  const moveMatch = lower.match(/^(?:go|move|head|walk)\s+(north|south|east|west|n|s|e|w)$/);
  if (moveMatch) {
    const dirMap = { n: "north", s: "south", e: "east", w: "west" };
    const dir = dirMap[moveMatch[1]] ?? moveMatch[1];
    await moveDir(dir);
    return;
  }
  if (["north", "south", "east", "west", "n", "s", "e", "w"].includes(lower)) {
    const dirMap = { n: "north", s: "south", e: "east", w: "west" };
    await moveDir(dirMap[lower] ?? lower);
    return;
  }

  if (lower === "help") {
    appendLog(
      "Commands:\n" +
      "  go [north / south / east / west] — move to another room\n" +
      "  look                             — describe your surroundings\n" +
      "  talk to [name]                   — speak with a character\n" +
      "  fight [enemy name]               — begin combat\n" +
      "  inventory                        — check your items\n" +
      "  help                             — show this list",
      "system"
    );
    return;
  }

  if (lower === "inventory") {
    if (state.player) {
      const items = state.player.inventory.length
        ? state.player.inventory.join(", ")
        : "nothing";
      appendLog(`You are carrying: ${items}.\nGold: ${state.player.gold} coins.`, "system");
    }
    return;
  }

  // Handle "talk to [name]" locally to set dialogue mode
  const talkMatch = lower.match(/^talk(?:\s+to)?\s+(.+)$/);
  if (talkMatch) {
    const target = talkMatch[1].trim();
    const charId = findCharacter(target);
    if (charId) {
      state.dialogueWith = charId;
      const char = state.room.characters.find(c => c.id === charId);
      appendLog(`You approach ${char.name}. (Type 'bye' to end the conversation.)`, "system");
      await doTalk(charId, "Hello");
      return;
    } else {
      appendLog(`There is no one here called "${target}".`, "system");
      return;
    }
  }

  // Handle "fight [enemy]" locally to start combat
  const fightMatch = lower.match(/^(?:fight|attack|engage)\s+(.+)$/);
  if (fightMatch) {
    const target   = fightMatch[1].trim();
    const enemyId  = findEnemy(target);
    if (enemyId) {
      await startCombat(enemyId);
      return;
    } else {
      appendLog(`There is no enemy called "${target}" here.`, "system");
      return;
    }
  }

  // Everything else → game master
  setLoading(true);
  try {
    const data = await api("api/action", { input: raw });
    applyUpdate(data);
    appendLog(data.narrative, "narrator");
  } catch (e) {
    appendLog("The dungeon master is silent. (Check your server logs.)", "system");
  }
  setLoading(false);
}

// ── Movement ──────────────────────────────────────────────────────────────────
async function moveDir(direction) {
  setLoading(true);
  try {
    const data = await api("api/move", { direction });
    applyUpdate(data);
    appendLog(data.narrative, "narrator");
  } catch (e) {
    appendLog(`You can't move ${direction} right now.`, "system");
  }
  setLoading(false);
}

// ── Dialogue ──────────────────────────────────────────────────────────────────
async function doTalk(characterId, message) {
  setLoading(true);
  try {
    const data = await api("api/talk", { character_id: characterId, message });
    const char = state.room?.characters.find(c => c.id === characterId);
    const name = char?.name ?? characterId;
    appendDialogue(name, data.reply, characterId);
  } catch (e) {
    appendLog("No response. (Check your server logs.)", "system");
  }
  setLoading(false);
}

// ── Combat ────────────────────────────────────────────────────────────────────
async function startCombat(enemyId) {
  setLoading(true);
  try {
    const data = await api("api/combat/start", { enemy_id: enemyId });
    state.combat = data.combat;
    updateCombatHud(data.enemy, data.combat.enemy_hp);
    $combatHud.classList.remove("hidden");
    appendLog(data.narrative, "combat");
    updatePlayerStats(data.player);
  } catch (e) {
    appendLog("Could not start combat.", "system");
  }
  setLoading(false);
}

async function combatAction(action) {
  if (!state.combat) return;
  setLoading(true);
  try {
    const data = await api("api/combat/action", { action });
    appendLog(data.narrative, "combat");
    updatePlayerStats(data.player);

    if (data.combat) {
      state.combat = data.combat;
      const enemy = state.room?.enemies.find(e => e.id === data.combat.enemy_id);
      if (enemy) updateCombatHud(enemy, data.combat.enemy_hp);
    }

    if (data.enemy_defeated) {
      state.combat = null;
      $combatHud.classList.add("hidden");
      // refresh room state
      const roomData = data.room_data;
      if (roomData) applyRoomData(roomData);
    }

    if (data.game_over) {
      state.combat = null;
      $combatHud.classList.add("hidden");
      $gameOver.classList.remove("hidden");
    }
  } catch (e) {
    appendLog("Combat error. (Check your server logs.)", "system");
  }
  setLoading(false);
}

function parseCombatInput(raw) {
  const l = raw.toLowerCase();
  if (l === "attack" || l === "a" || l.startsWith("attack")) return "attack";
  if (l === "defend" || l === "d" || l.startsWith("defend")) return "defend";
  if (l === "flee"   || l === "f" || l.startsWith("flee"))   return "flee";
  return null;
}

// ── State application ─────────────────────────────────────────────────────────
function applyUpdate(data) {
  if (data.map_layout) state.mapLayout = data.map_layout;
  if (data.player)     updatePlayerStats(data.player);
  if (data.room_data)  applyRoomData(data.room_data);
  if (data.combat !== undefined) {
    state.combat = data.combat;
    if (!data.combat) $combatHud.classList.add("hidden");
  }
  renderMinimap();
}

function applyRoomData(roomData) {
  if (state.room && state.room.id !== roomData.id) {
    state.dialogueWith = null;
  }
  state.room = roomData;
  if (Array.isArray(roomData.visited)) state.visited = roomData.visited;

  // Background image
  const newSrc = `static/assets/backgrounds/${roomData.background}`;
  if (!$roomBg.src.endsWith(roomData.background)) {
    $roomBg.classList.add("loading");
    $roomBg.onload = () => $roomBg.classList.remove("loading");
    $roomBg.src = newSrc;
  }
  $roomName.textContent = roomData.name;

  // Exits
  $exitsList.innerHTML = "";
  for (const [dir, dest] of Object.entries(roomData.exits)) {
    const badge = document.createElement("span");
    badge.className = "exit-badge";
    badge.textContent = dir;
    badge.title = `Go ${dir}`;
    badge.addEventListener("click", () => {
      appendLog(`> go ${dir}`, "player");
      moveDir(dir);
    });
    $exitsList.appendChild(badge);
  }

  // NPCs
  $npcsRow.innerHTML = "";
  for (const char of roomData.characters) {
    $npcsRow.appendChild(makeEntityCard(char, false));
  }

  // Enemies
  $enemiesRow.innerHTML = "";
  for (const enemy of roomData.enemies) {
    $enemiesRow.appendChild(makeEntityCard(enemy, true));
  }
}

function makeEntityCard(entity, isEnemy) {
  const card  = document.createElement("div");
  card.className = isEnemy ? "entity-card enemy-card" : "entity-card";
  card.title     = isEnemy ? `Fight ${entity.name}` : `Talk to ${entity.name}`;

  const img  = document.createElement("img");
  img.className  = "entity-sprite";
  img.src        = `static/assets/characters/${entity.sprite}`;
  img.alt        = entity.name;

  const label = document.createElement("div");
  label.className = "entity-label";
  label.textContent = entity.name;

  card.appendChild(img);
  card.appendChild(label);

  card.addEventListener("click", () => {
    if (isEnemy) {
      state.dialogueWith = null;
      $input.value = `fight ${entity.name}`;
    } else {
      $input.value = `talk to ${entity.name}`;
    }
    handleInput();
  });

  return card;
}

function updatePlayerStats(player) {
  state.player = player;
  const hp    = player.hp;
  const maxHp = player.max_hp;
  $hpText.textContent = `${hp} / ${maxHp}`;
  $hpText.className = hp > maxHp * 0.6 ? "hp-high"
                    : hp > maxHp * 0.3 ? "hp-mid"
                    : "hp-low";
  $goldText.textContent = player.gold;
}

function updateCombatHud(enemy, currentHp) {
  const maxHp = enemy.max_hp ?? enemy.hp ?? currentHp;
  $enemyPortrait.src    = `static/assets/characters/${enemy.sprite}`;
  $enemyPortrait.alt    = enemy.name;
  $enemyName.textContent = enemy.name;
  const pct = Math.max(0, Math.round((currentHp / maxHp) * 100));
  $enemyHpBar.style.width = `${pct}%`;
  $enemyHpText.textContent = `${currentHp} / ${maxHp} HP`;
}

// ── Find entity helpers ───────────────────────────────────────────────────────
function findCharacter(query) {
  if (!state.room?.characters) return null;
  const q = query.toLowerCase();
  return state.room.characters.find(c =>
    c.name.toLowerCase().includes(q) || c.id.toLowerCase().includes(q)
  )?.id ?? null;
}

function findEnemy(query) {
  if (!state.room?.enemies) return null;
  const q = query.toLowerCase();
  return state.room.enemies.find(e =>
    e.name.toLowerCase().includes(q) || e.id.toLowerCase().includes(q)
  )?.id ?? null;
}

// ── Minimap ───────────────────────────────────────────────────────────────────
function renderMinimap() {
  if (!state.mapLayout) return;

  const layout  = state.mapLayout;
  const visited = new Set(state.visited || []);
  const current = state.room?.id;

  // Rooms visible = visited + adjacent to any visited room
  const visible = new Set(visited);
  for (const rid of visited) {
    const r = layout[rid];
    if (!r) continue;
    for (const dest of Object.values(r.exits || {})) {
      if (layout[dest]) visible.add(dest);
    }
  }

  const CELL = 22, PAD = 6, NODE = 14;
  let maxX = 0, maxY = 0;
  for (const r of Object.values(layout)) {
    if (r.coords[0] > maxX) maxX = r.coords[0];
    if (r.coords[1] > maxY) maxY = r.coords[1];
  }
  const W = (maxX + 1) * CELL + PAD * 2;
  const H = (maxY + 1) * CELL + PAD * 2;

  const cx = (x) => PAD + x * CELL + CELL / 2;
  const cy = (y) => PAD + y * CELL + CELL / 2;

  // Collect unique edges between visible rooms
  const edges = new Map(); // key → {a, b, known}
  for (const [rid, r] of Object.entries(layout)) {
    if (!visible.has(rid)) continue;
    for (const dest of Object.values(r.exits || {})) {
      if (!visible.has(dest)) continue;
      const key = [rid, dest].sort().join("|");
      if (!edges.has(key)) {
        const bothVisited = visited.has(rid) && visited.has(dest);
        edges.set(key, { a: rid, b: dest, known: !bothVisited });
      }
    }
  }

  let svg = `<svg viewBox="0 0 ${W} ${H}" class="minimap-svg" xmlns="http://www.w3.org/2000/svg">`;
  // Edges first (so nodes draw on top)
  for (const { a, b, known } of edges.values()) {
    const [ax, ay] = layout[a].coords;
    const [bx, by] = layout[b].coords;
    svg += `<line x1="${cx(ax)}" y1="${cy(ay)}" x2="${cx(bx)}" y2="${cy(by)}" class="mm-edge${known ? " known" : ""}"/>`;
  }
  // Nodes
  for (const rid of visible) {
    const r = layout[rid];
    if (!r) continue;
    const [x, y] = r.coords;
    const cls = rid === current ? "current"
              : visited.has(rid) ? "visited"
              : "known";
    svg += `<rect x="${cx(x) - NODE / 2}" y="${cy(y) - NODE / 2}" width="${NODE}" height="${NODE}" rx="2" class="mm-node ${cls}"><title>${r.name}${visited.has(rid) ? "" : " (unexplored)"}</title></rect>`;
  }
  svg += `</svg>`;

  $minimap.innerHTML = svg;
  const total = Object.keys(layout).length;
  $minimapCount.textContent = `${visited.size} / ${total}`;
}

// ── Log helpers ───────────────────────────────────────────────────────────────
function appendLog(text, type = "narrator") {
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.textContent = text;
  $log.appendChild(entry);
  entry.scrollIntoView({ behavior: "smooth", block: "end" });

  // Voice narration (Exercise 4) — narrator and combat lines use the GM voice.
  if (type === "narrator" || type === "combat") {
    playNarration(text, "");
  }
}

function appendDialogue(speakerName, text, speakerId = "") {
  const entry = document.createElement("div");
  entry.className = "log-entry dialogue";
  const nameEl = document.createElement("span");
  nameEl.className = "speaker-name";
  nameEl.textContent = speakerName;
  entry.appendChild(nameEl);
  entry.appendChild(document.createTextNode(text));
  $log.appendChild(entry);
  entry.scrollIntoView({ behavior: "smooth", block: "end" });

  // Voice narration (Exercise 4) — character/enemy lines use that speaker's voice.
  playNarration(text, speakerId);
}

// ── Voice narration ───────────────────────────────────────────────────────────
// Calls /api/speech for each log line. Until Exercise 4 is wired up, the
// backend returns {"audio_url": null} and this is a quiet no-op.
async function playNarration(text, speaker) {
  if (!$speechToggle || !$speechToggle.checked) return;
  if (!text) return;
  try {
    if (currentAudio) { currentAudio.pause(); currentAudio = null; }
    const res = await fetch("api/speech", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ text, speaker }),
    });
    if (!res.ok) return;
    const { audio_url } = await res.json();
    if (!audio_url) return;
    currentAudio = new Audio(audio_url);
    currentAudio.play().catch(() => { /* autoplay blocked; ignore */ });
  } catch (e) {
    console.warn("speech narration failed", e);
  }
}

function clearLog() { $log.innerHTML = ""; }

// ── API helper ────────────────────────────────────────────────────────────────
async function api(path, body) {
  const res = await fetch(path, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error ?? res.statusText);
  }
  return res.json();
}

// ── Loading state ─────────────────────────────────────────────────────────────
function setLoading(on) {
  $loading.classList.toggle("hidden", !on);
  $input.disabled    = on;
  document.getElementById("btn-send").disabled = on;
}
