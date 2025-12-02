console.log("hero.js carregado!");

let currentKidId = null;
let currentParentId = null;

/* ================================
      TOGGLE SECTIONS
================================ */
function toggleSection(section) {
  const el = document.getElementById(section + "Section");

  if (el.classList.contains("hidden")) {
    document.getElementById("missionsSection").classList.add("hidden");
    document.getElementById("rewardsSection").classList.add("hidden");
    el.classList.remove("hidden");
  } else {
    el.classList.add("hidden");
  }
}

/* ================================
      CARREGAR INFO DO HERÓI
================================ */
async function loadKidStats() {
  if (!currentKidId) return;

  const res = await fetch(`/v1/kid/${currentKidId}`);
  if (!res.ok) {
    document.getElementById("kidStats").textContent = "Erro ao carregar herói.";
    return;
  }

  const kid = await res.json();

  // Atualizando o nome e as informações do herói
  document.getElementById("kidName").textContent = kid.name;
  document.getElementById("kidStats").textContent =
    `Nível ${kid.level} | XP: ${kid.xp} | Gold: ${kid.gold}`;

  // Atualizando o avatar do herói
  const avatarEl = document.getElementById("kidAvatar");
  if (avatarEl) {
    // Verifica o caminho do avatar
    const avatarPath = kid.avatar || "/static/assets/default-avatar.png";  // Caminho padrão
    console.log("Avatar carregado:", avatarPath); // Para depuração, veja o caminho no console
    avatarEl.src = avatarPath;  // Atualiza o src do avatar
  }
}

/* ==========================================
      PEGAR MISSÕES CONCLUÍDAS
========================================== */
async function getCompletedMissionIds() {
  const res = await fetch(`/v1/kid-missions/`);
  if (!res.ok) return [];

  const data = await res.json();

  return data
    .filter(km => km.kid_id == currentKidId && km.completed)
    .map(km => km.mission_id);
}

/* ==========================================
      PEGAR RECOMPENSAS COMPRADAS
========================================== */
async function getPurchasedRewardIds() {
  const res = await fetch(`/v1/kid-rewards/`);
  if (!res.ok) return [];

  const data = await res.json();

  return data
    .filter(kr => kr.kid_id == currentKidId && kr.purchased)
    .map(kr => kr.reward_id);
}

/* ================================
      CARREGAR MISSÕES
================================ */
async function loadMissions() {
  const missionsList = document.getElementById("missionsList");
  missionsList.innerHTML = "<p class='text-center text-gray-500'>Carregando missões...</p>";

  try {
    const res = await fetch(`/v1/missions/parent/${currentParentId}`);
    const missions = res.ok ? await res.json() : [];

    if (!missions.length) {
      missionsList.innerHTML = "<p class='text-center text-gray-500'>Nenhuma missão disponível.</p>";
      return;
    }

    const completedIds = await getCompletedMissionIds();
    const filtered = missions.filter(m => !completedIds.includes(m.id));

    if (!filtered.length) {
      missionsList.innerHTML = "<p class='text-center text-gray-500'>Nenhuma missão pendente 🎉</p>";
      return;
    }

    missionsList.innerHTML = filtered.map(m => `
      <div class="mission-card">
        <p class="text-lg font-bold text-sky">${m.title}</p>
        <p>${m.description || ""}</p>
        <p class="mt-1 text-gray-600">XP: ${m.xp} | Gold: ${m.gold}</p>

        <button class="mt-2 px-3 py-1 rounded-lg shadow bg-mint text-gray-800 text-sm w-full"
          onclick="completeMission(${m.id}, ${m.xp}, ${m.gold})">
          Concluir missão
        </button>
      </div>
    `).join("");

  } catch (e) {
    console.error(e);
    missionsList.innerHTML = "<p class='text-center text-red-500'>Erro ao carregar missões.</p>";
  }
}

/* ================================
      CARREGAR RECOMPENSAS
================================ */
async function loadRewards() {
  const rewardsList = document.getElementById("rewardsList");
  rewardsList.innerHTML = "<p class='text-center text-gray-500'>Carregando recompensas...</p>";

  try {
    const res = await fetch(`/v1/rewards?parent_id=${currentParentId}`);
    const rewards = res.ok ? await res.json() : [];

    if (!rewards.length) {
      rewardsList.innerHTML = "<p class='text-center text-gray-500'>Nenhuma recompensa disponível.</p>";
      return;
    }

    const purchasedIds = await getPurchasedRewardIds();
    const filtered = rewards.filter(r => !purchasedIds.includes(r.id));

    if (!filtered.length) {
      rewardsList.innerHTML = "<p class='text-center text-gray-500'>Nenhuma recompensa restante 🎁</p>";
      return;
    }

    rewardsList.innerHTML = filtered.map(r => `
      <div class="reward-card">
        <p class="text-lg font-bold text-pink">${r.title}</p>
        <p class="mt-1 text-gray-600">Custa ${r.gold} Gold</p>

        <button class="mt-2 px-3 py-1 rounded-lg shadow bg-lemon text-gray-900 text-sm w-full"
          onclick="redeemReward(${r.id}, ${r.gold})">
          Resgatar recompensa
        </button>
      </div>
    `).join("");

  } catch (e) {
    console.error(e);
    rewardsList.innerHTML = "<p class='text-center text-red-500'>Erro ao carregar recompensas.</p>";
  }
}

/* ================================
      CONCLUIR MISSÃO
================================ */
async function completeMission(missionId, xp, gold) {
  try {
    const res = await fetch("/v1/kid-missions/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        kid_id: Number(currentKidId),
        mission_id: missionId,
        completed: true
      })
    });

    if (!res.ok) {
      let msg = "Erro ao concluir missão.";
      const err = await res.json().catch(() => null);
      if (err?.detail) msg = err.detail;
      alert(msg);
      return;
    }

    await loadKidStats();
    await loadMissions();
    alert(`Missão concluída! +${xp} XP, +${gold} Gold para o herói.`);

  } catch (e) {
    console.error(e);
    alert("Erro de comunicação com o servidor ao concluir missão.");
  }
}

/* ================================
      RESGATAR RECOMPENSA
================================ */
async function redeemReward(rewardId, priceGold) {
  try {
    const res = await fetch("/v1/kid-rewards/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        kid_id: Number(currentKidId),
        reward_id: rewardId,
        purchased: true
      })
    });

    if (!res.ok) {
      let msg = "Erro ao resgatar recompensa.";
      const err = await res.json().catch(() => null);
      if (err?.detail) msg = err.detail;
      alert(msg);
      return;
    }

    await loadKidStats();
    await loadRewards();
    alert(`Recompensa resgatada! -${priceGold} Gold do herói.`);

  } catch (e) {
    console.error(e);
    alert("Erro ao resgatar recompensa.");
  }
}

/* ================================
         INICIAR PÁGINA
================================ */
async function loadKidPage() {
  currentKidId = localStorage.getItem("kid_id");
  currentParentId = localStorage.getItem("parent_id");

  if (!currentKidId || !currentParentId) {
    window.location.href = "/dashboard";
    return;
  }

  await loadKidStats();
  await loadMissions();
  await loadRewards();
}



window.onload = loadKidPage;
