(function () {
    "use strict";

    var doc = document;
    var body = doc.body;
    var header = doc.querySelector("[data-header]");
    var navToggle = doc.querySelector("[data-nav-toggle]");
    var navMenu = doc.querySelector("[data-nav-menu]");
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function closeNav() {
        body.classList.remove("nav-open");
        if (navToggle) {
            navToggle.setAttribute("aria-expanded", "false");
        }
    }

    if (navToggle && navMenu) {
        navToggle.addEventListener("click", function () {
            var isOpen = body.classList.toggle("nav-open");
            navToggle.setAttribute("aria-expanded", String(isOpen));
        });

        navMenu.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", closeNav);
        });

        window.addEventListener("keydown", function (event) {
            if (event.key === "Escape") closeNav();
        });
    }

    function updateHeader() {
        if (!header) return;
        header.classList.toggle("is-scrolled", window.scrollY > 8);
    }

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    doc.querySelectorAll(".btn").forEach(function (button) {
        button.addEventListener("pointerdown", function () {
            button.classList.remove("is-pressed");
            void button.offsetWidth;
            button.classList.add("is-pressed");
        });
        button.addEventListener("animationend", function () {
            button.classList.remove("is-pressed");
        });
    });

    function initGsap() {
        if (reduceMotion || !window.gsap) return;

        var gsap = window.gsap;
        var ScrollTrigger = window.ScrollTrigger;
        doc.documentElement.classList.add("gsap-ready");

        if (ScrollTrigger) {
            gsap.registerPlugin(ScrollTrigger);
        }

        gsap.from(".js-hero-item", {
            y: 34,
            opacity: 0,
            duration: 0.9,
            ease: "power3.out",
            stagger: 0.12,
            clearProps: "transform,opacity"
        });

        gsap.from(".hero-panel", {
            y: 38,
            scale: 0.94,
            opacity: 0,
            duration: 1.05,
            ease: "power3.out",
            stagger: 0.12,
            delay: 0.16,
            clearProps: "transform,opacity"
        });

        if (!ScrollTrigger) return;

        doc.querySelectorAll(".js-section").forEach(function (section) {
            gsap.from(section, {
                scrollTrigger: {
                    trigger: section,
                    start: "top 82%",
                    once: true
                },
                y: 30,
                opacity: 0,
                duration: 0.78,
                ease: "power3.out",
                clearProps: "transform,opacity"
            });
        });

        doc.querySelectorAll(".js-grid").forEach(function (grid) {
            var items = grid.children;
            if (!items.length) return;
            gsap.from(items, {
                scrollTrigger: {
                    trigger: grid,
                    start: "top 84%",
                    once: true
                },
                y: 32,
                opacity: 0,
                duration: 0.72,
                ease: "power3.out",
                stagger: {
                    each: 0.07,
                    from: "start"
                },
                clearProps: "transform,opacity"
            });
        });

        doc.querySelectorAll(".js-split").forEach(function (split) {
            var children = split.children;
            if (!children.length) return;
            gsap.from(children, {
                scrollTrigger: {
                    trigger: split,
                    start: "top 80%",
                    once: true
                },
                x: function (index) {
                    return index % 2 === 0 ? -28 : 28;
                },
                opacity: 0,
                duration: 0.82,
                ease: "power3.out",
                stagger: 0.1,
                clearProps: "transform,opacity"
            });
        });

        doc.querySelectorAll(".js-cta").forEach(function (cta) {
            gsap.from(cta, {
                scrollTrigger: {
                    trigger: cta,
                    start: "top 84%",
                    once: true
                },
                y: 24,
                scale: 0.98,
                opacity: 0,
                duration: 0.82,
                ease: "power3.out",
                clearProps: "transform,opacity"
            });
        });
    }

    if (doc.readyState === "complete") {
        initGsap();
    } else {
        window.addEventListener("load", initGsap, { once: true });
    }
})();
