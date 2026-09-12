import "./styles.css";
import { api, formatMoney, parseBudgetRange } from "./api";
import { collectBehavior, initMetrics } from "./metrics";

const form = document.getElementById("lead-form");
const statusNode = document.getElementById("form-status");
const productSelect = document.getElementById("product");
const budgetInput = document.getElementById("budget");
const budgetLabel = document.getElementById("budget-label");

let services = [];

function setStatus(type, message) {
  statusNode.className = `status ${type}`;
  statusNode.textContent = message;
}

function applyBudgetRange(range) {
  const parsed = parseBudgetRange(range);
  budgetInput.min = String(parsed.min);
  budgetInput.max = String(parsed.max);
  budgetInput.step = "5000";
  const mid = Math.round((parsed.min + parsed.max) / 2);
  budgetInput.value = String(mid);
  budgetInput.disabled = false;
  budgetLabel.textContent = formatMoney(mid);
}

async function loadServices() {
  try {
    services = await api("/admin-settings");
    productSelect.innerHTML = "";

    if (!services.length) {
      const empty = document.createElement("option");
      empty.value = "";
      empty.disabled = true;
      empty.selected = true;
      empty.textContent = "Услуги пока не добавлены";
      productSelect.append(empty);
      return;
    }

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.disabled = true;
    placeholder.selected = true;
    placeholder.textContent = "Выберите услугу";
    productSelect.append(placeholder);

    services.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.services;
      option.textContent = `${item.services} · ${item.budget_range}`;
      option.dataset.range = item.budget_range;
      productSelect.append(option);
    });
  } catch (error) {
    productSelect.innerHTML = "";
    const failed = document.createElement("option");
    failed.value = "";
    failed.disabled = true;
    failed.selected = true;
    failed.textContent = "Не удалось загрузить услуги";
    productSelect.append(failed);
    setStatus("err", error.message);
  }
}

productSelect.addEventListener("change", () => {
  const selected = services.find((item) => item.services === productSelect.value);
  if (selected) {
    applyBudgetRange(selected.budget_range);
  }
});

budgetInput.addEventListener("input", () => {
  budgetLabel.textContent = formatMoney(Number(budgetInput.value));
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("", "Отправляем заявку…");

  const data = new FormData(form);
  const payload = {
    first_name: String(data.get("first_name") || "").trim(),
    last_name: String(data.get("last_name") || "").trim(),
    patronymic: String(data.get("patronymic") || "").trim(),
    phone: String(data.get("phone") || "").trim(),
    email: String(data.get("email") || "").trim(),
    business_info: String(data.get("business_info") || "").trim(),
    business_niche: String(data.get("business_niche") || "").trim(),
    company_size: String(data.get("company_size") || "").trim(),
    business_size: String(data.get("business_size") || "").trim(),
    role: String(data.get("role") || "").trim(),
    task_volume: String(data.get("task_volume") || "").trim(),
    need_volume: String(data.get("need_volume") || "").trim(),
    deadline: String(data.get("deadline") || "").trim(),
    task_type: String(data.get("task_type") || "").trim(),
    product: String(data.get("product") || "").trim(),
    budget: String(data.get("budget") || "").trim(),
    contact_method: String(data.get("contact_method") || "").trim(),
    convenient_time: String(data.get("convenient_time") || "").trim(),
    comment: String(data.get("comment") || "").trim(),
    behavior: collectBehavior(),
  };

  try {
    await api("/applications", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setStatus("ok", "Заявка отправлена! Мы свяжемся с вами в ближайшее время.");
    form.reset();
    budgetInput.disabled = true;
    budgetLabel.textContent = "Выберите услугу";
    await loadServices();
  } catch (error) {
    setStatus("err", error.message);
  }
});

initMetrics();
loadServices();
