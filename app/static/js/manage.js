/* ======= MISSÕES ======= */
async function createMission() {
  const parent_id = ensureLogged();

  const title = document.getElementById("missionTitle").value.trim();
  const description = document.getElementById("missionDescr").value.trim();
  const xp = parseInt(document.getElementById("missionXP").value);
  const gold = parseInt(document.getElementById("missionGold").value);

  if (!title || isNaN(xp) || isNaN(gold)) {
    alert("Preencha todos os campos corretamente!");
    return;
  }

  try {
    const res = await fetch("/v1/missions/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title,
        description: description,
        xp: xp,
        gold: gold,
        parent_id: parseInt(parent_id)
      })
    });

    if (res.ok) {
      alert("Missão criada com sucesso!");
      toggleSection("mission");
    } else {
      const error = await res.json();
      alert("Erro ao criar missão: " + (error.detail || "Verifique os campos."));
    }
  } catch (err) {
    console.error(err);
    alert("Falha na comunicação com o servidor.");
  }
}

/* ======= RECOMPENSAS ======= */
async function createReward() {
  const parent_id = ensureLogged();

  const title = document.getElementById("rewardTitle").value.trim();
  const gold = parseInt(document.getElementById("rewardGold").value);

  if (!title || isNaN(gold)) {
    alert("Preencha nome e valor em gold!");
    return;
  }

  try {
    const res = await fetch("/v1/rewards/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title,
        gold: gold,
        parent_id: parseInt(parent_id)
      })
    });

    if (res.ok) {
      alert("Recompensa criada com sucesso!");
      toggleSection("reward");
    } else {
      const error = await res.json();
      alert("Erro ao criar recompensa: " + (error.detail || "Verifique os campos."));
    }
  } catch (err) {
    console.error(err);
    alert("Falha na comunicação com o servidor.");
  }
}
