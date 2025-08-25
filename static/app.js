const titleEl = document.getElementById("title");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const genBtn = document.getElementById("generateBtn");
const clearBtn = document.getElementById("clearBtn");

function renderContent(data) {
  resultEl.innerHTML = "";
  if (!data || !data.content) return;

  // Markdown parsing logic for the generated content, updated for the new UI styles
  const html = data.content
    .replace(/\*\*(.*?)\*\*/g, "<h2 class='text-xl font-semibold mt-6 mb-2 text-indigo-800'>$1</h2>")
    .replace(/\n- (.*?)/g, "<li class='text-gray-700'>$1</li>")
    .replace(/\n\d+\.\s(.*?)/g, "<li class='text-gray-700'>$1</li>")
    .replace(/\n/g, "<br/>");

  resultEl.innerHTML = `
    <div class="bg-white shadow-lg rounded-3xl p-6 prose max-w-none text-gray-800">
      <div class="prose max-w-none">
        ${html}
      </div>
    </div>
  `;
}

async function generate() {
  const title = titleEl.value.trim();
  if (!title) {
    statusEl.textContent = "Please enter a course title.";
    return;
  }
  genBtn.disabled = true;
  statusEl.textContent = "Generating...";
  statusEl.classList.add("status-pulsing");
  resultEl.innerHTML = "";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    const data = await res.json();
    if (!res.ok) {
      statusEl.textContent = data.error || "Server error.";
      return;
    }
    renderContent(data);
    statusEl.textContent = "Done.";
  } catch (err) {
    statusEl.textContent = "Network error: " + err.message;
  } finally {
    genBtn.disabled = false;
    statusEl.classList.remove("status-pulsing");
  }
}

genBtn.addEventListener("click", generate);
clearBtn.addEventListener("click", () => {
  titleEl.value = "";
  statusEl.textContent = "";
  resultEl.innerHTML = "";
});