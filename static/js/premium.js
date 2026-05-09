const nav = document.querySelector("[data-nav]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const mobileMenu = document.querySelector("[data-mobile-menu]");
const cursorLight = document.querySelector(".cursor-light");

const setNavState = () => {
  nav?.classList.toggle("is-scrolled", window.scrollY > 24);
};

setNavState();
window.addEventListener("scroll", setNavState, { passive: true });

menuToggle?.addEventListener("click", () => {
  const isOpen = menuToggle.classList.toggle("is-open");
  mobileMenu?.classList.toggle("is-open", isOpen);
  document.body.classList.toggle("menu-open", isOpen);
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  mobileMenu?.setAttribute("aria-hidden", String(!isOpen));
});

mobileMenu?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuToggle?.classList.remove("is-open");
    mobileMenu.classList.remove("is-open");
    document.body.classList.remove("menu-open");
    menuToggle?.setAttribute("aria-expanded", "false");
    mobileMenu.setAttribute("aria-hidden", "true");
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });

document.querySelectorAll(".reveal").forEach((element, index) => {
  element.style.transitionDelay = `${Math.min(index % 5, 4) * 80}ms`;
  revealObserver.observe(element);
});

const countObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const element = entry.target;
    const target = Number(element.dataset.count || 0);
    const duration = 1400;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.round(target * eased);
      if (progress < 1) requestAnimationFrame(tick);
    };

    requestAnimationFrame(tick);
    countObserver.unobserve(element);
  });
}, { threshold: 0.4 });

document.querySelectorAll("[data-count]").forEach((element) => countObserver.observe(element));

document.querySelectorAll(".magnetic").forEach((button) => {
  button.addEventListener("mousemove", (event) => {
    const rect = button.getBoundingClientRect();
    const x = event.clientX - rect.left - rect.width / 2;
    const y = event.clientY - rect.top - rect.height / 2;
    button.style.transform = `translate(${x * 0.12}px, ${y * 0.18}px)`;
  });
  button.addEventListener("mouseleave", () => {
    button.style.transform = "";
  });
});

window.addEventListener("mousemove", (event) => {
  if (!cursorLight) return;
  cursorLight.style.left = `${event.clientX}px`;
  cursorLight.style.top = `${event.clientY}px`;
}, { passive: true });

const parallaxHero = document.querySelector("[data-parallax] .hero-media img");
window.addEventListener("scroll", () => {
  if (!parallaxHero) return;
  parallaxHero.style.transform = `translateY(${window.scrollY * 0.08}px) scale(1.08)`;
}, { passive: true });

document.querySelectorAll("[data-tabs]").forEach((tabs) => {
  const buttons = [...tabs.querySelectorAll("[data-tab-button]")];
  const panels = [...tabs.querySelectorAll("[data-tab-panel]")];

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.tabButton;
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      panels.forEach((panel) => panel.classList.toggle("is-active", panel.dataset.tabPanel === target));
    });
  });
});
