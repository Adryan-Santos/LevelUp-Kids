console.log("dashboard.js carregado!");

// garante que o pai está logado
function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

document.addEventListener("DOMContentLoaded", loadKids);

// carregar heróis
async function loadKids() {
  const parent_id = ensureLogged();
  const grid = document.getElementById("grid");

  grid.innerHTML = "<p class='text-center text-gray-500'>Carregando heróis...</p>";

  try {
    const res = await fetch(`/v1/kid?parent_id=${parent_id}`);
    if (!res.ok) throw new Error();

    const kids = await res.json();
    grid.innerHTML = "";

    if (!kids.length) {
      grid.innerHTML = "<p class='text-center text-gray-600'>Nenhum herói cadastrado.</p>";
      return;
    }

    kids.forEach(kid => {
      const avatar = localStorage.getItem(`kid_avatar_${kid.id}`) || "/static/assets/default-avatar.png";

      const card = document.createElement("div");
      card.className = "hero-card";

      card.innerHTML = `
        <img src="${avatar}" class="hero-avatar">

        <p class="hero-name">${kid.name}</p>
        <p class="hero-info">Lv. ${kid.level ?? 1}</p>
        <p class="hero-info">XP: ${kid.xp ?? 0}</p>
      `;

      card.onclick = () => selectKid(kid.id, kid.name);

      grid.appendChild(card);
    });

  } catch(err) {
    grid.innerHTML = "<p class='text-center text-red-500'>Erro ao carregar heróis.</p>";
  }
}

// selecionar herói
function selectKid(id, name) {
  localStorage.setItem("kid_id", id);
  localStorage.setItem("kid_name", name);

  const avatar = localStorage.getItem(`kid_avatar_${id}`);
  if (avatar) localStorage.setItem("kid_avatar", avatar);

  window.location.href = "/hero";
}

// abrir/fechar form
function toggleForm() {
  document.getElementById("formContainer").classList.toggle("hidden");
}

// selecionar avatar
function selectAvatar(el) {
  document.querySelectorAll(".avatar-option").forEach(img => {
    img.classList.remove("avatar-selected");
  });

  el.classList.add("avatar-selected");
  document.getElementById("selectedAvatar").value = el.src;
}

// criar herói
async function addKid() {
  const parent_id = ensureLogged();

  const name = document.getElementById("name").value.trim();
  const age = parseInt(document.getElementById("age").value);
  const avatar = document.getElementById("selectedAvatar").value;

  if (!name || isNaN(age) || !avatar) {
    alert("Preencha todos os campos e escolha um avatar.");
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

    const savedKid = await res.json();

    localStorage.setItem(`kid_avatar_${savedKid.id}`, avatar);

    alert("Herói criado!");
    toggleForm();
    loadKids();

  } catch(err) {
    alert("Erro ao criar herói.");
  }
}
