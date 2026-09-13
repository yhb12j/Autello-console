const TOKEN_KEY = "autello_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export async function api(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`/api${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return null;
  }

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail || `HTTP ${response.status}`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return payload;
}

export function parseBudgetRange(range) {
  const matches = String(range || "").match(/\d+(?:[.,]\d+)?/g) || [];
  const values = matches.map((item) => {
    const numeric = Number(item.replace(",", "."));
    if (String(range).toLowerCase().includes("кк") && numeric < 20) {
      return Math.round(numeric * 1_000_000);
    }
    if (/к\b|тыс/i.test(range) && numeric < 20_000) {
      return Math.round(numeric * 1000);
    }
    return Math.round(numeric);
  });

  if (values.length >= 2) {
    return { min: Math.min(values[0], values[1]), max: Math.max(values[0], values[1]) };
  }
  if (values.length === 1) {
    return { min: Math.round(values[0] * 0.6), max: values[0] };
  }
  return { min: 40000, max: 280000 };
}

export function formatMoney(value) {
  return new Intl.NumberFormat("ru-RU").format(value) + " ₽";
}
