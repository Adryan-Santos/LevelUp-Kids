function toggleSection(section) {
    const el = document.getElementById(section + "Section");
    el.style.display = el.style.display === "block" ? "none" : "block";
}

async function loadKidPage() {
    const kid_id = localStorage.getItem("kid_id");
    const parent_id = localStorage.getItem("parent_id");

    if (!kid_id || !parent_id) {
        window.location.href = "/dashboard";
        return;
    }

    /* ----- BUSCA DADOS DO KID ----- */
    const kidRes = await fetch(`/v1/kid/${kid_id}`);
    const kid = await kidRes.json();

    document.getElementById("kidName").textContent = kid.name;
    document.getElementById("kidStats").textContent =
        `Lvl ${kid.level} | XP: ${kid.xp} | Gold: ${kid.gold}`;

    /* ----- MISSÕES ----- */
    const missionsRes = await fetch(`/v1/missions/parent/${parent_id}`);
    let missions = missionsRes.ok ? await missionsRes.json() : [];

    const missionsBox = document.getElementById("missionsList");

    if (!missions.length) {
        missionsBox.innerHTML = "<p>Nenhuma missão disponível.</p>";
    } else {
        missionsBox.innerHTML = missions
            .map(m => `
                <div class="item">
                    <strong>${m.title}</strong><br>
                    ${m.description || ""}<br>
                    XP: ${m.xp} | Gold: ${m.gold}
                </div>
            `)
            .join("");
    }

    /* ----- RECOMPENSAS ----- */
    const rewardsRes = await fetch(`/v1/rewards?parent_id=${parent_id}`);
    let rewards = rewardsRes.ok ? await rewardsRes.json() : [];

    const rewardsBox = document.getElementById("rewardsList");

    if (!rewards.length) {
        rewardsBox.innerHTML = "<p>Nenhuma recompensa disponível.</p>";
    } else {
        rewardsBox.innerHTML = rewards
            .map(r => `
                <div class="item">
                    <strong>${r.title}</strong><br>
                    Custa ${r.gold} Gold
                </div>
            `)
            .join("");
    }
}

window.onload = loadKidPage;
