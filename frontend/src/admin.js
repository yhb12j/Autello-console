import "./styles.css";
import { api } from "./api";

const form = document.getElementById("service-form");
const statusNode = document.getElementById("service-status");
const listNode = document.getElementById("service-list");

function setStatus(type, message) {
  statusNode.className = `status ${type}`;
  statusNode.textContent = message;
}

async function loadServices() {
  const items = await api("/admin-settings");
  listNode.innerHTML = "";

  if (!items.length) {
    listNode.innerHTML = "<p class='status'>Список услуг пуст.</p>";
    return;
  }

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "service-card";
    card.innerHTML = `
      <div>
        <strong>${item.services}</strong>
        <p class="status">${item.budget_range}</p>
      </div>
    `;
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Удалить";
    button.addEventListener("click", async () => {
      await api(`/admin-settings/${item.id}`, { method: "DELETE" });
      await loadServices();
    });
    card.append(button);
    listNode.append(card);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  try {
    await api("/admin-settings", {
      method: "POST",
      body: JSON.stringify({
        services: String(data.get("services") || "").trim(),
        budget_range: String(data.get("budget_range") || "").trim(),
      }),
    });
    form.reset();
    setStatus("ok", "Услуга сохранена.");
    await loadServices();
  } catch (error) {
    setStatus("err", error.message);
  }
});

loadServices().catch((error) => setStatus("err", error.message));
