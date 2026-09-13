const startedAt = Date.now();
const buttonsClicked = [];
const cursorPositions = [];
let lastCursor = { x: 0, y: 0 };

function labelFor(target) {
  return target.getAttribute("data-track") || target.textContent.trim().slice(0, 40);
}

export function startBehaviorMetrics() {
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-track], button, a, select");
    if (!target) {
      return;
    }
    const label = labelFor(target);
    if (label) {
      buttonsClicked.push(label);
    }
  });

  document.addEventListener("mousemove", (event) => {
    lastCursor = { x: event.clientX, y: event.clientY };
  });

  window.setInterval(async () => {
    cursorPositions.push({
      x: lastCursor.x,
      y: lastCursor.y,
      t: Math.round((Date.now() - startedAt) / 1000),
    });
    if (cursorPositions.length > 240) {
      cursorPositions.splice(0, cursorPositions.length - 240);
    }

    const payload = {
      application_id: 0,
      time_on_page: Math.round((Date.now() - startedAt) / 1000),
      buttons_clicked: buttonsClicked.slice(-40).join(", "),
      cursor_positions: JSON.stringify(cursorPositions.slice(-60)),
      return_frequency: 0,
    };

    try {
      await fetch("/api/behavior-metrics/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch (_error) {
      // Keep collecting even if a single tick fails.
    }
  }, 1000);
}
