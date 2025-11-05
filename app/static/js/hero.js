window.onload = async function() {
  const kid_id = localStorage.getItem("kid_id");
  if (!kid_id) {
    alert("Erro: Herói não encontrado.");
    window.location.href = "/dashboard";
  }

  await loadHero(kid_id);
  await loadMissions(kid_id);
};

// Carregar informações do herói
async function loadHero(kid_id) {
  try {
    const res = await fetch(`/v1/kid/${kid_id}`);
    const data = await res.json();
    if (data) {
      document.getElementById("heroName").textContent = `Herói: ${data.name}`;
      document.getElementById("heroLevel").textContent = `Nível: ${data.level}`;
      document.getElementById("heroXP").textContent = `XP: ${data.xp}`;
      document.getElementById("heroGold").textContent = `Gold: ${data.gold}`;
    }
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar informações do herói.");
  }
}

// Carregar missões do herói
async function loadMissions(kid_id) {
  try {
    const res = await fetch(`/v1/kid/${kid_id}/missions`);
    const missions = await res.json();
    const missionList = document.getElementById("missionList");
    missionList.innerHTML = missions.map(mission => `
      <div class="item">
        <span>${mission.name} - ${mission.descr}</span>
        <button class="complete-btn" onclick="completeMission(${mission.id}, ${kid_id})">Concluir</button>
      </div>
    `).join('');
  } catch (error) {
    console.error(error);
    alert("Erro ao carregar missões.");
  }
}

// Marcar missão como concluída
async function completeMission(mission_id, kid_id) {
  try {
    const res = await fetch(`/v1/kid/${kid_id}/missions/${mission_id}/complete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (res.ok) {
      alert("Missão concluída! Aguardando aprovação do pai.");
      loadHero(kid_id);
      loadMissions(kid_id);
    } else {
      alert("Erro ao concluir missão.");
    }
  } catch (error) {
    console.error(error);
    alert("Falha na comunicação com o servidor.");
  }
}
