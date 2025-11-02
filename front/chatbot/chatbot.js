document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("chatbot-placeholder");
  if (!container) return;

  // --- Cargar HTML del chatbot dinámicamente ---
  const scriptEl = document.currentScript || document.querySelector('script[src*="chatbot/chatbot.js"]');
  const chatbotHtmlUrl = new URL(scriptEl ? scriptEl.getAttribute("src") : "chatbot/chatbot.js", window.location.href);
  chatbotHtmlUrl.pathname = chatbotHtmlUrl.pathname.replace(/[^/]+$/, "chatbot.html");
  const response = await fetch(chatbotHtmlUrl.href);
  const html = await response.text();
  container.innerHTML = html;

  // --- Referencias ---
  const chatbot = document.getElementById("chatbot-container");
  const toggleBtn = document.getElementById("chatbot-toggle");
  const messages = document.getElementById("chatbot-messages");
  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const form = document.getElementById("chatbot-form");

console.log({
  chatbot,
  toggleBtn,
  messages,
  input,
  sendBtn,
  form
});

  // --- Evitar cualquier envío del formulario ---
  if (form) {
    form.addEventListener("submit", (e) => e.preventDefault());
  }

  // --- Mostrar/Ocultar chatbot ---
  window.toggleChatbot = function () {
    const visible = getComputedStyle(chatbot).display !== "none";
    chatbot.style.display = visible ? "none" : "flex";
    toggleBtn.style.display = visible ? "flex" : "none";
  };

  // --- Función para enviar mensajes ---
  async function sendMessage(e) {
    if (e) e.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);
    input.value = "";
    appendMessage("bot", "<em>Escribiendo...</em>");

    try {
      const res = await fetch("http://127.0.0.1:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: text })
      });

      if (!res.ok) throw new Error("Error de conexión con Flask");

      const data = await res.json();
      messages.lastChild.remove();
      appendMessage("bot", data.respuesta);
    } catch (err) {
      console.error("Error al conectar con la IA:", err);
      messages.lastChild.remove();
      appendMessage("bot", "⚠️ No se pudo conectar con el servidor Flask.");
    }
  }

  // --- Eventos ---
  if (sendBtn) {
    sendBtn.setAttribute("type", "button");
    sendBtn.addEventListener("click", sendMessage);
  }

  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault(); // Evita refresh
        sendMessage(e);
      }
    });
  }

  // --- Agregar mensaje al chat ---
  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerHTML = text;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  // --- Toggle chatbot ---
  toggleBtn.onclick = window.toggleChatbot;
});
