document.addEventListener("DOMContentLoaded", () => {

const btn = document.getElementById("waBtn");
const popup = document.getElementById("waSystem");
const typing = document.getElementById("waTyping");
const msgBox = document.getElementById("waMsg");
const sendBtn = document.getElementById("waSend");
const input = document.getElementById("waName");

const phone = "917908529153";

/* ===== CONTEXT DETECTION ===== */
function getContextMessage() {
    const title = document.title;

    if (location.pathname.includes("services")) {
        return `I'm interested in your service: ${title}`;
    }
    if (location.pathname.includes("products")) {
        return `I want details about: ${title}`;
    }
    return "I want to discuss a project";
}

/* ===== OPEN POPUP ===== */
btn.addEventListener("click", () => {
    popup.classList.toggle("active");
});

/* ===== AUTO TRIGGER ===== */
setTimeout(() => {
    popup.classList.add("active");
}, 2500);

/* ===== TYPING EFFECT ===== */
setTimeout(() => {
    typing.style.display = "none";
    msgBox.classList.remove("hidden");
    msgBox.innerText = "Hi 👋 How can we help you today?";
}, 1500);

/* ===== SEND ===== */
sendBtn.addEventListener("click", () => {
    let name = input.value.trim();
    let msg = getContextMessage();

    if (name) msg = `Hi, I'm ${name}. ${msg}`;

    const url = `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
    window.open(url, "_blank");
});

});