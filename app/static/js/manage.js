console.log("manage.js carregado!");

// Garante login
function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

/*
==========================================================
   ABRIR / FECHAR SEÇÕES (TOGGLE)
==========================================================
*/
function toggleSection(section) {
  const map = {
    heroes: "kidsSection",
    mission: "missionSection",
    reward: "rewardSection"
  };

  const selected = document.getElementById(map[section]);

  // Se já estiver aberta → fecha
  if (!selected.classList.contains("hidden")) {
    selected.classList.add("hidden");
    return;
  }

  // Fecha todas as outras
  Object.values(map).forEach(id => {
    document.getElementById(id).classList.add("hidden");
  });

  // Abre a escolhida
  selected.classList.remove("hidden");

  if (section === "heroes") loadKids();
}

/*
==========================================================
   CARREGAR HERÓIS
==========================================================
*/
async function loadKids() {
  const parent_id = ensureLogged();
  const list = document.getElementById("kidsList");

  list.innerHTML = `<p class="text-center text-gray-500">Carregando...</p>`;

  try {
    const res = await fetch(`/v1/kid?parent_id=${parent_id}`);
    const kids = await res.json();

    if (!kids.length) {
      list.innerHTML = `<p class="text-center text-gray-500">Nenhum herói cadastrado.</p>`;
      return;
    }

    list.innerHTML = "";

    kids.forEach(kid => {
      const card = document.createElement("div");
      card.className =
        "bg-bgkids border-2 border-sky rounded-xl p-4 mt-3 shadow";

      card.innerHTML = `
        <p class="text-xl text-sky font-bold">${kid.name}</p>
        <p class="text-gray-700">${kid.age} anos</p>

        <div class="flex gap-2 mt-3">
          <button class="bg-mint px-3 py-2 rounded-xl shadow text-white"
            onclick="editKid(${kid.id}, '${kid.name}', ${kid.age})">
            ✏ Editar
          </button>

          <button class="bg-pink px-3 py-2 rounded-xl shadow text-white"
            onclick="deleteKid(${kid.id})">
            🗑 Excluir
          </button>
        </div>
      `;

      list.appendChild(card);
    });
  } catch (error) {
    console.error(error);
    list.innerHTML = `<p class="text-center text-red-500">Erro ao carregar heróis.</p>`;
  }
}

/*
==========================================================
   EDITAR HERÓI (SEM PROMPT)
==========================================================
*/
function editKid(id, name, age) {
  const box = document.getElementById("editKidSection");

  // Preenche os inputs
  document.getElementById("editKidId").value = id;
  document.getElementById("editKidName").value = name;
  document.getElementById("editKidAge").value = age;

  // Abre a caixa de edição
  box.classList.remove("hidden");

  // Scroll até o formulário
  box.scrollIntoView({ behavior: "smooth", block: "center" });
}

/*
==========================================================
   SALVAR ALTERAÇÕES DO HERÓI
==========================================================
*/
async function updateKid() {
  const id = document.getElementById("editKidId").value;
  const name = document.getElementById("editKidName").value.trim();
  const age = parseInt(document.getElementById("editKidAge").value);

  if (!name || isNaN(age)) {
    alert("Preencha corretamente!");
    return;
  }

  try {
    const res = await fetch(`/v1/kid/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age })
    });

    if (res.ok) {
      alert("Herói atualizado!");
      document.getElementById("editKidSection").classList.add("hidden");
      loadKids();
    } else {
      alert("Erro ao atualizar.");
    }
  } catch (err) {
    alert("Erro de conexão.");
  }
}

/*
==========================================================
   EXCLUIR HERÓI
==========================================================
*/
async function deleteKid(id) {
  if (!confirm("Tem certeza que deseja excluir este herói?")) return;

  try {
    const res = await fetch(`/v1/kid/${id}`, { method: "DELETE" });
    if (res.ok) {
      alert("Herói excluído!");
      loadKids();
    } else {
      alert("Erro ao excluir herói.");
    }
  } catch {
    alert("Erro de conexão.");
  }
}

/*
==========================================================
   CRIAR MISSÃO
==========================================================
*/
async function createMission() {
  const parent_id = ensureLogged();

  const payload = {
    title: document.getElementById("missionTitle").value.trim(),
    description: document.getElementById("missionDescr").value.trim(),
    xp: parseInt(document.getElementById("missionXP").value),
    gold: parseInt(document.getElementById("missionGold").value),
    parent_id
  };

  if (!payload.title || isNaN(payload.xp) || isNaN(payload.gold)) {
    alert("Preencha todos os campos!");
    return;
  }

  const res = await fetch("/v1/missions/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert("Missão criada!");
    toggleSection("mission");
  } else {
    alert("Erro ao criar missão.");
  }
}

/*
==========================================================
   CRIAR RECOMPENSA
==========================================================
*/
async function createReward() {
  const parent_id = ensureLogged();

  const payload = {
    title: document.getElementById("rewardTitle").value.trim(),
    gold: parseInt(document.getElementById("rewardGold").value),
    parent_id
  };

  if (!payload.title || isNaN(payload.gold)) {
    alert("Preencha corretamente.");
    return;
  }

  const res = await fetch("/v1/rewards/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert("Recompensa criada!");
    toggleSection("reward");
  } else {
    alert("Erro ao criar recompensa.");
  }
}
