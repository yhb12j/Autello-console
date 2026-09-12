const startedAt = Date.now();
const buttonsClicked = [];
const hoverZones = new Set();

const visitsKey = "autello_return_count";
const currentVisits = Number(sessionStorage.getItem(visitsKey) || "0") + 1;
sessionStorage.setItem(visitsKey, String(currentVisits));

export function initMetrics() {
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-track], button, a, select");
    if (!target) {
      return;
    }
    const label = target.getAttribute("data-track") || target.textContent.trim().slice(0, 40);
    if (label) {
      buttonsClicked.push(label);
    }
  });

  document.querySelectorAll("[data-zone]").forEach((node) => {
    node.addEventListener("mouseenter", () => {
      hoverZones.add(node.getAttribute("data-zone"));
    });
  });
}

export function collectBehavior() {
  return {
    time_on_page_seconds: Math.round((Date.now() - startedAt) / 1000),
    buttons_clicked: buttonsClicked.slice(-30),
    hover_zones: Array.from(hoverZones),
    return_count: currentVisits,
    extra_payload: {
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      locale: navigator.language,
      user_agent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
      },
      landing_url: window.location.href,
      referrer: document.referrer,
    },
  };
}
