// Get current tab URL
async function getCurrentTabUrl() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab.url;
}

// Show loader using animated dots (CSS-based)
function showLoader(message) {
  const status = document.getElementById("status");
  status.innerHTML = `
    <div class="loader-bar-container">
      <span class="loading-text">${message}<span class="dots"><span>.</span><span>.</span><span>.</span></span></span>
      <div class="loader-bar">
        <div class="bar"></div>
      </div>
    </div>
  `;
}

// Hide loader and show final status
function hideLoader(message) {
  const status = document.getElementById("status");
  status.textContent = message;
}

// Scrape content from the current tab's URL
async function scrapeWebsite(url) {
  showLoader("Scraping in progress");

  const summaryBtn = document.getElementById("summaryBtn");
  const qaBtn = document.getElementById("qaBtn");
  const questionInput = document.getElementById("questionInput");

  summaryBtn.disabled = true;
  qaBtn.disabled = true;
  questionInput.disabled = true;

  try {
    const res = await fetch("http://localhost:5000/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const result = await res.json();

    if (res.ok) {
      console.log("[EXTENSION] Scraping done:", result);
      hideLoader("Scraping completed!");
      summaryBtn.disabled = false;
      qaBtn.disabled = false;
      questionInput.disabled = false;
    } else {
      hideLoader("Scraping failed.");
      console.error("[EXTENSION] Scrape error:", result.error);
    }
  } catch (error) {
    console.error("[EXTENSION] Fetch error:", error);
    hideLoader("Error during scraping.");
  }
}

// DOM ready
document.addEventListener("DOMContentLoaded", async () => {
  const url = await getCurrentTabUrl();
  console.log("[EXTENSION] Current URL:", url);
  scrapeWebsite(url);

  // Summary button handler
  document.getElementById("summaryBtn").addEventListener("click", async () => {
    showLoader("Generating summary");

    try {
      const res = await fetch("http://localhost:5000/summary");
      const data = await res.json();
      document.getElementById("output").textContent = data.summary || data.error;
      hideLoader("Summary ready!");
    } catch (e) {
      console.error("[EXTENSION] Summary error:", e);
      hideLoader("Error during summary.");
    }
  });

  // QA button handler
  document.getElementById("qaBtn").addEventListener("click", async () => {
    const question = document.getElementById("questionInput").value;
    if (!question) return alert("Enter your question");

    showLoader("Finding answer");

    try {
      const res = await fetch(`http://localhost:5000/qa?question=${encodeURIComponent(question)}`);
      const data = await res.json();
      document.getElementById("output").textContent = data.answer || data.error;
      hideLoader("Answer ready!");
    } catch (e) {
      console.error("[EXTENSION] QA error:", e);
      hideLoader("Error during QA.");
    }
  });

  // Reset History button handler (UPDATED)
  document.getElementById("resetHistoryBtn").addEventListener("click", async () => {
    document.getElementById("output").textContent = "";
    document.getElementById("questionInput").value = "";

    document.getElementById("summaryBtn").disabled = true;
    document.getElementById("qaBtn").disabled = true;
    document.getElementById("questionInput").disabled = true;

    showLoader("Resetting history...");

    try {
      const resetRes = await fetch("http://localhost:5000/reset", {
        method: "POST",
      });

      const resetResult = await resetRes.json();
      console.log("[EXTENSION] Reset response:", resetResult);

      const url = await getCurrentTabUrl();
      scrapeWebsite(url);
    } catch (error) {
      console.error("[EXTENSION] Reset error:", error);
      hideLoader("Error during reset.");
    }
  });

  // Theme toggle handler
  const toggle = document.getElementById("themeToggle");
  const label = document.getElementById("themeLabel");
  const body = document.body;

  const savedTheme = localStorage.getItem("theme") || "day";
  body.classList.add(savedTheme);
  toggle.checked = savedTheme === "night";
  label.textContent = savedTheme.charAt(0).toUpperCase() + savedTheme.slice(1);

  toggle.addEventListener("change", () => {
    const theme = toggle.checked ? "night" : "day";
    body.classList.remove("day", "night");
    body.classList.add(theme);
    localStorage.setItem("theme", theme);
    label.textContent = theme.charAt(0).toUpperCase() + theme.slice(1);
  });
});
