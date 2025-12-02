console.log("dashboard.js carregado!");

// garante que o pai está logado
function ensureLogged() {
  const parent_id = localStorage.getItem("parent_id");
  if (!parent_id) window.location.href = "/login";
  return parent_id;
}

document.addEventListener("DOMContentLoaded", () => {
  loadKids();
  // não temos carregamento dinâmico de avatares aqui — avatares estão no HTML
});

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
      // usa o avatar vindo do backend, se houver; senão tenta localStorage; senão default
      const avatar = kid.avatar || localStorage.getItem(`kid_avatar_${kid.id}`) || "/static/assets/default-avatar.png";

      const card = document.createElement("div");
      card.className = "hero-card";

      card.innerHTML = `
        <img src="${avatar}" class="hero-avatar">
        <p class="hero-name">${kid.name}</p>
        <p class="hero-info">Lv. ${kid.level ?? 1}</p>
        <p class="hero-info">XP: ${kid.xp ?? 0}</p>
      `;

      // passa avatar também (para garantir persistência no localStorage quando necessário)
      card.onclick = () => selectKid(kid.id, kid.name, avatar);

      grid.appendChild(card);
    });

  } catch(err) {
    console.error("loadKids error:", err);
    grid.innerHTML = "<p class='text-center text-red-500'>Erro ao carregar heróis.</p>";
  }
}

// selecionar herói
function selectKid(id, name, avatar) {
  localStorage.setItem("kid_id", id);
  localStorage.setItem("kid_name", name);

  // Se backend forneceu avatar, use; senão, se já houver no localStorage copie pra chave padrão
  if (avatar) {
    localStorage.setItem("kid_avatar", avatar);
    // também armazena por id para fallback em loadKids anterior
    localStorage.setItem(`kid_avatar_${id}`, avatar);
  } else {
    const fallback = localStorage.getItem(`kid_avatar_${id}`);
    if (fallback) localStorage.setItem("kid_avatar", fallback);
  }

  window.location.href = "/hero";
}

// abrir/fechar form
function toggleForm() {
  document.getElementById("formContainer").classList.toggle("hidden");
}

/* ============================================================
      SELETOR DE AVATAR — VERSÃO MESCLADA (visual + path relativo)
=============================================================== */
function selectAvatar(el) {
  try {
    // remove seleção anterior
    document.querySelectorAll(".avatar-option").forEach(img => {
      img.classList.remove("avatar-selected");
    });

    // marca novo selecionado
    el.classList.add("avatar-selected");

    // pega src do atributo (mais confiável) e transforma em relativo
    const srcAttr = el.getAttribute("src") || el.src || "";
    const origin = window.location.origin;
    const relative = srcAttr.startsWith(origin) ? srcAttr.replace(origin, "") : srcAttr;

    // salva no input hidden (valor enviado ao backend)
    const hidden = document.getElementById("selectedAvatar");
    if (hidden) hidden.value = relative;

    console.log("Avatar selecionado:", relative);

    return relative;
  } catch (e) {
    console.error("selectAvatar error:", e);
  }
}

// criar herói
async function addKid() {
  const parent_id = ensureLogged();

  const name = document.getElementById("name").value.trim();
  const age = parseInt(document.getElementById("age").value);
  const avatar = (document.getElementById("selectedAvatar") || {}).value;

  console.log("ENVIANDO AVATAR:", avatar);

  if (!name || isNaN(age) || !avatar) {
    alert("Preencha todos os campos e selecione o avatar.");
    return;
  }

  const payload = { name, age, parent_id, avatar };

  try {
    const res = await fetch("/v1/kid/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const text = await res.text();
      console.error("POST /v1/kid/ error:", res.status, text);
      throw new Error("Erro ao salvar herói");
    }

    const savedKid = await res.json();

    // salva avatar por id no localStorage para compatibilidade retroativa
    if (savedKid?.id && avatar) {
      localStorage.setItem(`kid_avatar_${savedKid.id}`, avatar);
    }

    alert("Herói criado!");
    toggleForm();
    loadKids();

  } catch(err) {
    console.error("addKid error:", err);
    alert("Erro ao criar herói.");
  }
}
