const $ = (sel) => document.querySelector(sel);
const api = (path) => `${window.API_BASE_URL}${path}`;

async function safeFetch(input, init) {
  const r = await fetch(input, init);
  let data = null;
  try { data = await r.json(); } catch {}
  if (!r.ok) {
    const msg = data?.detail || r.statusText || "Erro desconhecido";
    throw new Error(msg);
  }
  return data;
}

async function ping() {
  try {
    const data = await safeFetch(api("/health"));
    $("#status").textContent = `Conectado (${data.model})`;
  } catch (e) {
    $("#status").textContent = "API offline";
  }
}

async function classifyText() {
  const text = $("#emailText").value.trim();
  if (!text) return alert("Cole um texto primeiro 🙂");

  setBusy(true, "Classificando…");
  try {
    const data = await safeFetch(api("/process"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    showResult(data);
  } catch (e) {
    alert("Falha ao classificar: " + e.message);
  } finally {
    setBusy(false);
  }
}

async function uploadFile() {
  const file = $("#fileInput").files[0];
  if (!file) return alert("Selecione um arquivo.");

  const form = new FormData();
  form.append("file", file);

  setBusy(true, "Processando arquivo…");
  try {
    const data = await safeFetch(api("/upload"), { method: "POST", body: form });
    showResult(data);
  } catch (e) {
    alert("Falha no upload: " + e.message);
  } finally {
    setBusy(false);
  }
}

function showResult({ categoria, score, resposta }) {
  $("#categoria").textContent = categoria ?? "-";
  $("#score").textContent = score != null ? (score * 100).toFixed(1) + "%" : "-";
  $("#resposta").textContent = resposta ?? "-";
  $("#result").classList.remove("hidden");
}

function setBusy(busy, text = "Processando…") {
  $("#btnProcess").disabled = busy;
  $("#btnUpload").disabled = busy;
  $("#status").textContent = busy ? text : "Pronto";
}

$("#btnProcess").addEventListener("click", classifyText);
$("#btnUpload").addEventListener("click", uploadFile);
window.addEventListener("load", ping);