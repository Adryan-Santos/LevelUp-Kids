async function loadMissions() {
  const parent_id = localStorage.getItem("parent_id");
  const res = await fetch(`/v1/mission?parent_id=${parent_id}`);
  const data = await res.json();
  const div = document.getElementById("missionsList");
  if (!data.length) {
    div.innerHTML = "<p>Nenhuma missão disponível!</p>";
    return;
  }
  div.innerHTML = data.map(m => `
    <div class="item">
      <span>${m.name} (+${m.xp_reward}XP / ${m.gold_reward}G)</span>
      <button class="btn small" onclick="completeMission('${m.name}')">Completar</button>
    </div>
  `).join('');
}
function completeMission(name) {
  alert(`Missão "${name}" completada! +XP +Gold`);
}
window.onload = loadMissions;
