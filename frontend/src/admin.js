import "./styles.css";
import { api, setToken } from "./api";

const authScreen = document.getElementById("auth-screen");
const consoleScreen = document.getElementById("console");
const authForm = document.getElementById("auth-form");
const registerBtn = document.getElementById("register-btn");
const authStatus = document.getElementById("auth-status");
const adminLoginLabel = document.getElementById("admin-login-label");
const servicesBody = document.getElementById("services-body");
const serviceForm = document.getElementById("service-form");
const serviceStatus = document.getElementById("service-status");
const leadsBody = document.getElementById("leads-body");
const leadModal = document.getElementById("lead-modal");
const leadDetails = document.getElementById("lead-details");
const statsModal = document.getElementById("stats-modal");
const statsSummary = document.getElementById("stats-summary");
const heatmap = document.getElementById("heatmap");

function setAuthStatus(type, message) {
  authStatus.className = `status ${type}`;
  authStatus.textContent = message;
}

function showConsole(login) {
  authScreen.hidden = true;
  consoleScreen.hidden = false;
  adminLoginLabel.textContent = login;
}

function showAuth() {
  setToken("");
  authScreen.hidden = false;
  consoleScreen.hidden = true;
}

async function refreshAuthGate() {
  const check = await api("/auth/check");
  registerBtn.hidden = Boolean(check.exists);
}

async function bootstrap() {
  try {
    await refreshAuthGate();
    const me = await api("/auth/me");
    showConsole(me.login);
    await Promise.all([loadServices(), loadLeads()]);
  } catch (_error) {
    showAuth();
  }
}

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(authForm);
  const payload = {
    login: String(data.get("login") || "").trim(),
    password: String(data.get("password") || ""),
  };
  try {
    const token = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setToken(token.access_token);
    const me = await api("/auth/me");
    showConsole(me.login);
    await Promise.all([loadServices(), loadLeads()]);
  } catch (error) {
    setAuthStatus("err", error.message);
  }
});

registerBtn.addEventListener("click", async () => {
  const data = new FormData(authForm);
  try {
    await api("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        login: String(data.get("login") || "").trim(),
        password: String(data.get("password") || ""),
      }),
    });
    registerBtn.hidden = true;
    setAuthStatus("ok", "Кабинет создан. Теперь войдите.");
  } catch (error) {
    setAuthStatus("err", error.message);
  }
});

document.getElementById("logout-btn").addEventListener("click", showAuth);

async function loadServices() {
  const items = await api("/admin-settings");
  servicesBody.innerHTML = "";
  items.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.id}</td>
      <td><input data-field="services" value="${item.services}"></td>
      <td><input data-field="budget_range" value="${item.budget_range}"></td>
      <td>${String(item.updated_at).slice(0, 19).replace("T", " ")}</td>
      <td class="tools"></td>
    `;
    const tools = row.querySelector(".tools");
    const save = document.createElement("button");
    save.type = "button";
    save.className = "ghost";
    save.textContent = "Сохранить";
    save.addEventListener("click", async () => {
      const services = row.querySelector('[data-field="services"]').value.trim();
      const budgetRange = row.querySelector('[data-field="budget_range"]').value.trim();
      await api(`/admin-settings/${item.id}`, {
        method: "PUT",
        body: JSON.stringify({ services, budget_range: budgetRange }),
      });
      serviceStatus.className = "status ok";
      serviceStatus.textContent = "Услуга обновлена.";
      await loadServices();
    });
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "ghost";
    remove.textContent = "Удалить";
    remove.addEventListener("click", async () => {
      await api(`/admin-settings/${item.id}`, { method: "DELETE" });
      await loadServices();
    });
    tools.append(save, remove);
    servicesBody.append(row);
  });
}

serviceForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(serviceForm);
  await api("/admin-settings", {
    method: "POST",
    body: JSON.stringify({
      services: String(data.get("services") || "").trim(),
      budget_range: String(data.get("budget_range") || "").trim(),
    }),
  });
  serviceForm.reset();
  await loadServices();
});

function temperatureClass(value) {
  return `chip ${value}`;
}

async function loadLeads() {
  const items = await api("/applications/queue");
  leadsBody.innerHTML = "";
  items.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><span class="${temperatureClass(item.temperature)}">${item.temperature_label} · ${item.score}</span></td>
      <td>${item.last_name} ${item.first_name}</td>
      <td>${item.product}</td>
      <td>${item.budget}</td>
      <td>${item.department}</td>
      <td>${item.need_manager ? "Нужен" : "Не требуется"}</td>
      <td></td>
    `;
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Просмотр";
    button.addEventListener("click", () => openLead(item));
    row.lastElementChild.append(button);
    leadsBody.append(row);
  });
}

function openLead(item) {
  leadDetails.innerHTML = `
    <p class="eyebrow">${item.temperature_label}</p>
    <h2>${item.last_name} ${item.first_name} ${item.patronymic}</h2>
    <p>${item.analysis}</p>
    <div class="stats-grid">
      <article><small>Телефон</small><strong>${item.phone}</strong></article>
      <article><small>Email</small><strong>${item.email}</strong></article>
      <article><small>Услуга</small><strong>${item.product}</strong></article>
      <article><small>Бюджет</small><strong>${item.budget}</strong></article>
      <article><small>Срок</small><strong>${item.deadline}</strong></article>
      <article><small>Роль</small><strong>${item.role}</strong></article>
      <article><small>Компания</small><strong>${item.company_size}</strong></article>
      <article><small>Отдел</small><strong>${item.department}</strong></article>
    </div>
    <p>${item.comment || "Комментарий не указан."}</p>
  `;
  leadModal.hidden = false;
}

document.getElementById("stats-btn").addEventListener("click", async () => {
  const summary = await api("/behavior-metrics/summary");
  statsSummary.innerHTML = `
    <article><small>День, среднее / макс.</small><strong>${Math.round(summary.avg_day)} / ${summary.max_day} с</strong></article>
    <article><small>Неделя, среднее / макс.</small><strong>${Math.round(summary.avg_week)} / ${summary.max_week} с</strong></article>
    <article><small>Месяц, среднее / макс.</small><strong>${Math.round(summary.avg_month)} / ${summary.max_month} с</strong></article>
  `;
  drawHeatmap(summary.cursor_samples || []);
  statsModal.hidden = false;
});

function drawHeatmap(samples) {
  const ctx = heatmap.getContext("2d");
  ctx.clearRect(0, 0, heatmap.width, heatmap.height);
  ctx.fillStyle = "#f7f1e6";
  ctx.fillRect(0, 0, heatmap.width, heatmap.height);

  const points = [];
  samples.forEach((sample) => {
    try {
      const parsed = JSON.parse(sample);
      if (Array.isArray(parsed)) {
        parsed.forEach((point) => points.push(point));
      }
    } catch (_error) {
      // Ignore malformed ticks.
    }
  });

  points.forEach((point) => {
    const x = Math.min(heatmap.width, Math.max(0, Number(point.x) || 0));
    const y = Math.min(heatmap.height, Math.max(0, Number(point.y) || 0));
    const gradient = ctx.createRadialGradient(x, y, 2, x, y, 28);
    gradient.addColorStop(0, "rgba(196, 162, 101, 0.55)");
    gradient.addColorStop(1, "rgba(196, 162, 101, 0)");
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, 28, 0, Math.PI * 2);
    ctx.fill();
  });
}

document.querySelectorAll("[data-close]").forEach((button) => {
  button.addEventListener("click", () => {
    document.getElementById(button.getAttribute("data-close")).hidden = true;
  });
});

bootstrap();
