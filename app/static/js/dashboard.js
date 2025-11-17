console.log("dashboard.js carregado!");

// Garante que o pai está logado
function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

// Carrega os heróis ao abrir a página
document.addEventListener("DOMContentLoaded", loadKids);

async function loadKids() {
  const parent_id = ensureLogged();
  const grid = document.getElementById("grid");

  grid.innerHTML = "<p class='text-center text-gray-500'>Carregando heróis...</p>";

  try {
    const res = await fetch(`/v1/kid?parent_id=${parent_id}`);
    if (!res.ok) throw new Error("Falha ao buscar heróis");

    const kids = await res.json();
    grid.innerHTML = "";

    if (!kids.length) {
      grid.innerHTML = "<p class='text-center text-gray-600'>Nenhum herói cadastrado ainda.</p>";
      return;
    }

    kids.forEach((kid) => {
      const card = document.createElement("div");
      card.className = "hero-card";

      card.innerHTML = `
        <img src="/static/assets/default-avatar.png" class="hero-avatar">

        <p class="hero-name">${kid.name}</p>
        <p class="hero-info">Lv. ${kid.level ?? 1}</p>
        <p class="hero-info">XP: ${kid.xp ?? 0}</p>
      `;

      // Card inteiro é clicável
      card.onclick = () => selectKid(kid.id, kid.name);

      grid.appendChild(card);
    });

  } catch (error) {
    console.error(error);
    grid.innerHTML = "<p class='text-center text-red-500'>Erro ao carregar heróis.</p>";
  }
}

// "Selecionar" → salva ID da criança e vai para tela do herói
function selectKid(id, name) {
  localStorage.setItem("kid_id", id);
  localStorage.setItem("kid_name", name);
  window.location.href = "/hero";
}

// Mostrar/ocultar formulário
function toggleForm() {
  const form = document.getElementById("formContainer");
  form.classList.toggle("hidden");
}

// Criar novo herói
async function addKid() {
  const parent_id = ensureLogged();

  const name = document.getElementById("name").value.trim();
  const age = parseInt(document.getElementById("age").value);

  if (!name || isNaN(age)) {
    alert("Preencha todos os campos.");
    return;
  }

  const payload = { name, age, parent_id };

  try {
    const res = await fetch("/v1/kid/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error();

    alert("Herói criado!");
    toggleForm();
    loadKids();

  } catch (err) {
    alert("Erro ao criar herói.");
  }
}
