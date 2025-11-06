window.onload = async function () {
  const kid_id = localStorage.getItem("kid_id");
  if (!kid_id) {
    alert("Erro: Herói não encontrado.");
    window.location.href = "/dashboard";
    return;
  }

  await loadHero(kid_id);
  await loadMissions(kid_id);
};

// Carregar informações do herói
async function loadHero(kid_id) {
  try {
    const res = await fetch(`/v1/kid/${kid_id}`);
    if (!res.ok) throw new Error("Falha ao buscar herói");
    const data = await res.json();

    document.getElementById("heroName").textContent = `Herói: ${data.name}`;
    document.getElementById("heroLevel").textContent = `Nível: ${data.level}`;
    document.getElementById("heroXP").textContent = `XP: ${data.xp}`;
    document.getElementById("heroGold").textContent = `Gold: ${data.gold}`;
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar informações do herói.");
  }
}

// Carregar missões associadas ao herói
async function loadMissions(kid_id) {
  try {
    const res = await fetch(`/v1/kid-missions`);
    if (!res.ok) throw new Error("Erro ao buscar missões do herói.");
    const missions = await res.json();

    // Filtra apenas as missões do herói atual
    const filtered = missions.filter((m) => m.kid_id === parseInt(kid_id));

    const missionList = document.getElementById("missionList");
    if (!filtered.length) {
      missionList.innerHTML = "<p>Nenhuma missão registrada ainda.</p>";
      return;
    }

    missionList.innerHTML = filtered
      .map(
        (m) => `
      <div class="item">
        <span>Missão #${m.mission_id}</span>
        <button class="complete-btn" onclick="markMissionComplete(${m.id}, ${kid_id})">
          ✔ Concluída
        </button>
      </div>`
      )
      .join("");
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar missões.");
  }
}

// Marcar missão como concluída
async function markMissionComplete(kid_mission_id, kid_id) {
  try {
    const res = await fetch(`/v1/kid-missions/${kid_mission_id}`, {
      method: "DELETE",
    });

    if (res.ok) {
      alert("Missão marcada como concluída!");
      loadHero(kid_id);
      loadMissions(kid_id);
    } else {
      alert("Erro ao atualizar missão.");
    }
  } catch (error) {
    console.error(error);
    alert("Falha na comunicação com o servidor.");
  }
}
