/* ── Pages Unwritten — frontend novel logic ───────────────────────────────── */
"use strict";

// ── State ─────────────────────────────────────────────────────────────────────
let state = {
  genre:     null,    // {id, name, subtitle, icon}
  scene:     null,    // {narration, speaker, choices, image_url, scene_no, ...}
  busy:      false,   // true while a fetch is in flight
};

// ── DOM refs ──────────────────────────────────────────────────────────────────
const $sceneBg        = document.getElementById("scene-bg");
const $titleScreen    = document.getElementById("title-screen");
const $storyScreen    = document.getElementById("story-screen");
const $genreGrid      = document.getElementById("genre-grid");
const $genrePill      = document.getElementById("genre-pill");
const $scenePill      = document.getElementById("scene-pill");
const $speakerLine    = document.getElementById("speaker-line");
const $narration      = document.getElementById("narration");
const $page           = document.getElementById("page");
const $choices        = document.getElementById("choices");
const $loading        = document.getElementById("loading-overlay");
const $loadingText    = document.getElementById("loading-text");
const $endingOverlay  = document.getElementById("ending-overlay");

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", showTitleScreen);

document.getElementById("btn-restart").addEventListener("click", async () => {
  await api("api/restart", {});
  showTitleScreen();
});

document.getElementById("btn-new-story").addEventListener("click", async () => {
  $endingOverlay.classList.add("hidden");
  await api("api/restart", {});
  showTitleScreen();
});


// ── Title screen ──────────────────────────────────────────────────────────────
async function showTitleScreen() {
  state = { genre: null, scene: null, busy: false };
  $titleScreen.classList.remove("hidden");
  $storyScreen.classList.add("hidden");
  $genrePill.classList.add("hidden");
  $scenePill.classList.add("hidden");
  $endingOverlay.classList.add("hidden");
  setBackground(null);

  // Render the genre cards
  const data = await fetch("api/genres").then(r => r.json());
  $genreGrid.innerHTML = "";
  data.genres.forEach(g => {
    const card = document.createElement("button");
    card.className = "genre-card";
    card.dataset.genre = g.id;
    card.innerHTML = `
      <div class="genre-card-icon">${g.icon}</div>
      <div class="genre-card-name">${g.name}</div>
      <div class="genre-card-sub">${g.subtitle}</div>
    `;
    card.addEventListener("click", () => beginStory(g.id));
    $genreGrid.appendChild(card);
  });
}


// ── Begin story ───────────────────────────────────────────────────────────────
async function beginStory(genreId) {
  if (state.busy) return;
  setLoading(true, "The storyteller draws breath…");
  try {
    const data = await api("api/begin", { genre: genreId });
    state.genre = data.genre;
    enterStoryScreen();
    renderScene(data);
  } catch (e) {
    console.error(e);
    alert("Could not start the story. Is the server running?");
  }
  setLoading(false);
}


// ── Make a choice ─────────────────────────────────────────────────────────────
async function makeChoice(choiceIndex) {
  if (state.busy) return;
  setLoading(true, "Turning the page…");
  try {
    const data = await api("api/choice", { choice_index: choiceIndex });
    renderScene(data);
  } catch (e) {
    console.error(e);
    alert("The story stumbled. Try again.");
  }
  setLoading(false);
}


// ── Screen transitions ────────────────────────────────────────────────────────
function enterStoryScreen() {
  $titleScreen.classList.add("hidden");
  $storyScreen.classList.remove("hidden");

  if (state.genre) {
    $genrePill.textContent = `${state.genre.icon}  ${state.genre.name}`;
    $genrePill.classList.remove("hidden");
    setBackground(state.genre.id);
  }
  $scenePill.classList.remove("hidden");
}


function setBackground(genreId, imageUrl) {
  // Reset classes
  $sceneBg.className = "";
  $sceneBg.style.backgroundImage = "";

  if (imageUrl) {
    $sceneBg.style.backgroundImage = `url("${imageUrl}")`;
    return;
  }
  if (genreId) {
    $sceneBg.classList.add(`genre-${genreId}`);
  }
}


// ── Render a scene ────────────────────────────────────────────────────────────
function renderScene(scene) {
  state.scene = scene;

  // Background — image if we have one, otherwise the genre gradient.
  setBackground(scene.genre_id || (state.genre && state.genre.id), scene.image_url);

  // Speaker / scene meta
  const speaker = scene.speaker || "Narrator";
  $speakerLine.textContent = speaker.toUpperCase();
  $scenePill.textContent   = `Scene ${scene.scene_no}`;

  // Narration — replay the page-flip animation by re-attaching the node.
  $page.style.animation = "none";
  void $page.offsetHeight; // force reflow
  $page.style.animation = "";
  $narration.textContent = scene.narration || "";

  // Choices
  $choices.innerHTML = "";
  const choices = scene.choices || [];
  if (choices.length === 0) {
    if (scene.is_ending) {
      showEnding();
    }
    return;
  }
  choices.forEach((text, i) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.innerHTML = `
      <span class="choice-marker">${romanize(i + 1)}</span>
      <span class="choice-text">${escapeHtml(text)}</span>
    `;
    btn.addEventListener("click", () => makeChoice(i));
    $choices.appendChild(btn);
  });
}


function showEnding() {
  $endingOverlay.classList.remove("hidden");
}


// ── Helpers ───────────────────────────────────────────────────────────────────
async function api(path, body) {
  state.busy = true;
  try {
    const res  = await fetch(path, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Request failed (${res.status})`);
    }
    return await res.json();
  } finally {
    state.busy = false;
  }
}


function setLoading(on, message) {
  if (on) {
    if (message) document.getElementById("loading-text").textContent = message;
    $loading.classList.remove("hidden");
  } else {
    $loading.classList.add("hidden");
  }
}


function romanize(n) {
  const map = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];
  return map[n] || String(n);
}


function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
