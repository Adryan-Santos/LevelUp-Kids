console.log("hero.js carregado!");

/* ================================
      TOGGLE SECTIONS
================================ */
function toggleSection(section) {
    const el = document.getElementById(section + "Section");

    if (el.classList.contains("hidden")) {
        // Fecha tudo antes de abrir
        document.getElementById("missionsSection").classList.add("hidden");
        document.getElementById("rewardsSection").classList.add("hidden");

        el.classList.remove("hidden");
    } else {
        el.classList.add("hidden");
    }
}

/* ================================
         LOAD PAGE DATA
================================ */
async function loadKidPage() {

    const kid_id = localStorage.getItem("kid_id");
    const parent_id = localStorage.getItem("parent_id");

    if (!kid_id || !parent_id) {
        window.location.href = "/dashboard";
        return;
    }

    /* ----- INFO DO KID ----- */
    const kidRes = await fetch(`/v1/kid/${kid_id}`);
    const kid = await kidRes.json();

    document.getElementById("kidName").textContent = kid.name;
    document.getElementById("kidStats").textContent =
        `Nível ${kid.level} | XP: ${kid.xp} | Gold: ${kid.gold}`;


    /* ============ MISSÕES ============ */
    const missionsRes = await fetch(`/v1/missions/parent/${parent_id}`);
    const missions = missionsRes.ok ? await missionsRes.json() : [];

    const missionsList = document.getElementById("missionsList");

    if (!missions.length) {
        missionsList.innerHTML =
            "<p class='text-center text-gray-500'>Nenhuma missão disponível.</p>";
    } else {
        missionsList.innerHTML = missions.map(m => `
            <div class="mission-card">
              <p class="text-lg font-bold text-sky">${m.title}</p>
              <p>${m.description || ""}</p>
              <p class="mt-1 text-gray-600">XP: ${m.xp} | Gold: ${m.gold}</p>
            </div>
        `).join("");
    }

    /* ============ RECOMPENSAS ============ */
    const rewardsRes = await fetch(`/v1/rewards?parent_id=${parent_id}`);
    const rewards = rewardsRes.ok ? await rewardsRes.json() : [];

    const rewardsList = document.getElementById("rewardsList");

    if (!rewards.length) {
        rewardsList.innerHTML =
            "<p class='text-center text-gray-500'>Nenhuma recompensa disponível.</p>";
    } else {
        rewardsList.innerHTML = rewards.map(r => `
            <div class="reward-card">
              <p class="text-lg font-bold text-pink">${r.title}</p>
              <p class="mt-1 text-gray-600">Custa ${r.gold} Gold</p>
            </div>
        `).join("");
    }
}

window.onload = loadKidPage;
