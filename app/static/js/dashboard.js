function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

async function loadKids() {
  const parent_id = ensureLogged();
  const grid = document.getElementById("grid");
  grid.innerHTML = "<p>Carregando heróis...</p>";

  try {
    const res = await fetch(`/v1/kid?parent_id=${parent_id}`);
    if (!res.ok) throw new Error("Falha ao buscar heróis");
    const kids = await res.json();
    grid.innerHTML = "";

    if (!kids.length) {
      grid.innerHTML = "<p>Nenhum herói encontrado ainda.</p>";
      return;
    }

    kids.forEach((kid) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <img src="/static/img/avatar1.png" alt="Avatar" width="80" />
        <p>${kid.name}</p>
        <p>Lv. ${kid.level ?? 1}</p>
        <p>XP: ${kid.xp ?? 0}</p>
        <button class="btn" onclick="selectKid(${kid.id}, '${kid.name.replace(/'/g,"&#39;")}')">Selecionar</button>
      `;
      grid.appendChild(card);
    });
  } catch (e) {
    console.error(e);
    grid.innerHTML = "<p>Erro ao carregar heróis.</p>";
  }
}

async function addKid() {
  const parent_id = ensureLogged();
  const name = document.getElementById("name").value.trim();
  const age = parseInt(document.getElementById("age").value, 10);

  if (!name || Number.isNaN(age)) {
    alert("Preencha nome e idade corretamente!");
    return;
  }

  try {
    const res = await fetch("/v1/kid", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, parent_id: parseInt(parent_id, 10) }),
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      console.error("Erro:", data);
      const msg = data?.detail || data?.message || JSON.stringify(data) || "Erro desconhecido.";
      alert("Erro ao criar herói: " + msg);
      return;
    }

    alert("Novo herói criado com sucesso!");
    document.getElementById("name").value = "";
    document.getElementById("age").value = "";
    toggleForm();
    loadKids();
  } catch (e) {
    console.error(e);
    alert("Falha na comunicação com o servidor.");
  }
}

function selectKid(kid_id, kid_name) {
  localStorage.setItem("kid_id", kid_id);
  localStorage.setItem("kid_name", kid_name);
  window.location.href = "/hero";
}


function toggleForm() {
  const form = document.getElementById("formContainer");
  const btn = document.getElementById("toggleFormBtn");
  const showing = form.style.display === "block";
  form.style.display = showing ? "none" : "block";
  btn.style.display = showing ? "inline-block" : "none";
}

window.onload = loadKids;
