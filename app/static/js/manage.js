function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

function toggleSection(section) {
  const ids = ["missionSection", "rewardSection", "kidsSection"];
  ids.forEach(id => document.getElementById(id).style.display = "none");
  const el = document.getElementById(section + "Section");
  if (el) el.style.display = el.style.display === "block" ? "none" : "block";
  if (section === "kids") loadKids();
}

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
    const res = await fetch("/v1/missions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        xp,
        gold,
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
    alert("Preencha o nome e o valor em gold!");
    return;
  }

  try {
    const res = await fetch("/v1/rewards", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        gold,
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

/* ======= HERÓIS ======= */
async function loadKids() {
  const parent_id = ensureLogged();
  const list = document.getElementById("kidsList");
  list.innerHTML = "<p>Carregando heróis...</p>";

  try {
    const res = await fetch(`/v1/kid?parent_id=${parent_id}`);
    if (!res.ok) throw new Error("Falha ao buscar heróis");
    const kids = await res.json();
    list.innerHTML = "";

    if (!kids.length) {
      list.innerHTML = "<p>Nenhum herói encontrado ainda.</p>";
      return;
    }

    kids.forEach(kid => {
      const div = document.createElement("div");
      div.className = "item";
      div.innerHTML = `
        <span>${kid.name} (${kid.age} anos)</span>
        <div>
          <button class="btn small" onclick="showEditKid(${kid.id}, '${kid.name}', ${kid.age})">✏️ Editar</button>
          <button class="btn small" onclick="deleteKid(${kid.id})">🗑️ Excluir</button>
        </div>
      `;
      list.appendChild(div);
    });
  } catch (e) {
    console.error(e);
    list.innerHTML = "<p>Erro ao carregar heróis.</p>";
  }
}

async function deleteKid(id) {
  if (!confirm("Tem certeza que deseja excluir este herói?")) return;
  try {
    const res = await fetch(`/v1/kid/${id}`, { method: "DELETE" });
    if (res.ok) {
      alert("Herói excluído com sucesso!");
      loadKids();
    } else alert("Erro ao excluir herói.");
  } catch (err) {
    console.error(err);
    alert("Erro ao excluir herói.");
  }
}

function showEditKid(id, name, age) {
  document.getElementById("editKidId").value = id;
  document.getElementById("editKidName").value = name;
  document.getElementById("editKidAge").value = age;
  document.getElementById("editKidSection").style.display = "block";
}

async function updateKid() {
  const id = document.getElementById("editKidId").value;
  const name = document.getElementById("editKidName").value.trim();
  const age = parseInt(document.getElementById("editKidAge").value);

  if (!name || isNaN(age)) {
    alert("Preencha nome e idade corretamente!");
    return;
  }

  try {
    const res = await fetch(`/v1/kid/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age })
    });

    if (res.ok) {
      alert("Herói atualizado com sucesso!");
      document.getElementById("editKidSection").style.display = "none";
      loadKids();
    } else {
      const error = await res.json();
      alert("Erro ao atualizar herói: " + (error.detail || "Verifique os campos."));
    }
  } catch (err) {
    console.error(err);
    alert("Falha na comunicação com o servidor.");
  }
}
