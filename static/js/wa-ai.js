document.addEventListener("DOMContentLoaded", () => {

const btn = document.getElementById("waBtn");
const popup = document.getElementById("waSystem");
const typing = document.getElementById("waTyping");
const msgBox = document.getElementById("waMsg");
const sendBtn = document.getElementById("waSend");
const input = document.getElementById("waName");

const phone = "917908529153";

/* =========================
   STATE SYSTEM
   ========================= */
let step = 0;
let userData = {
    name: "",
    intent: "",
    budget: ""
};

/* =========================
   CONTEXT DETECTION
   ========================= */
function getContext() {
    const title = document.title;

    if (location.pathname.includes("services")) {
        return `Service: ${title}`;
    }
    if (location.pathname.includes("products")) {
        return `Product: ${title}`;
    }
    return "General Inquiry";
}

/* =========================
   MESSAGES FLOW
   ========================= */
function nextMessage() {
    step++;

    typing.style.display = "block";
    msgBox.classList.add("hidden");

    setTimeout(() => {
        typing.style.display = "none";
        msgBox.classList.remove("hidden");

        if (step === 1) {
            msgBox.innerText = "Hi 👋 What are you looking for?";
        }

        else if (step === 2) {
            userData.intent = input.value || "Not specified";
            input.value = "";
            msgBox.innerText = "Got it 👍 What is your budget range?";
        }

        else if (step === 3) {
            userData.budget = input.value || "Not specified";
            input.value = "";
            msgBox.innerText = "Great. Your name?";
        }

        else if (step === 4) {
            userData.name = input.value || "Customer";

            const finalMessage = `
Hi, I'm ${userData.name}.
${getContext()}
Requirement: ${userData.intent}
Budget: ${userData.budget}
            `;

            /* TRACK EVENT */
            console.log("WA Lead:", userData);

            /* OPEN WHATSAPP */
            const url = `https://wa.me/${phone}?text=${encodeURIComponent(finalMessage)}`;
            window.open(url, "_blank");

            popup.classList.remove("active");
        }

    }, 1000);
}

/* =========================
   BUTTON EVENTS
   ========================= */
btn.addEventListener("click", () => {
    popup.classList.toggle("active");

    if (step === 0) {
        setTimeout(() => nextMessage(), 500);
    }
});

sendBtn.addEventListener("click", () => {
    if (step < 4) nextMessage();
});

/* =========================
   SMART TRIGGER
   ========================= */
let triggered = false;

window.addEventListener("scroll", () => {
    if (!triggered && window.scrollY > 300) {
        popup.classList.add("active");
        nextMessage();
        triggered = true;
    }
});

/* =========================
   EXIT INTENT (DESKTOP)
   ========================= */
document.addEventListener("mouseleave", (e) => {
    if (e.clientY < 10 && !triggered) {
        popup.classList.add("active");
        nextMessage();
        triggered = true;
    }
});

});