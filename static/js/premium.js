/* ============================================================
   PREMIUM JS — Scroll Reveal + Stagger Animations
   Performance-safe: uses IntersectionObserver (no scroll events)
   Only animates transform + opacity (GPU-composited)
   ============================================================ */
(function () {
    "use strict";

    // Respect reduced motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var ROOT_MARGIN = "0px 0px -60px 0px";
    var THRESHOLD = 0.08;

    // Auto-add .premium-stagger to card grids
    var staggerSelectors = [
        ".services-grid",
        ".products-grid",
        ".why-grid",
        ".testimonials-grid",
        ".service-detail-process__grid",
        ".service-detail-related__grid"
    ];

    staggerSelectors.forEach(function (sel) {
        document.querySelectorAll(sel).forEach(function (el) {
            el.classList.add("premium-stagger");
        });
    });

    // Auto-add .premium-reveal to section headers and key blocks
    var revealSelectors = [
        ".section-header",
        ".products-header",
        ".services-group",
        ".about-layout",
        ".why-section .container",
        ".testimonials-section .container",
        ".get-started-card",
        ".service-detail-hero__inner",
        ".service-detail-content",
        ".service-detail-highlights__panel",
        ".service-detail-cta__panel",
        ".contact-grid",
        ".service-block"
    ];

    revealSelectors.forEach(function (sel) {
        document.querySelectorAll(sel).forEach(function (el) {
            el.classList.add("premium-reveal");
        });
    });

    // IntersectionObserver for .premium-reveal
    var revealObserver = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { rootMargin: ROOT_MARGIN, threshold: THRESHOLD }
    );

    document.querySelectorAll(".premium-reveal").forEach(function (el) {
        revealObserver.observe(el);
    });

    // IntersectionObserver for .premium-stagger
    var staggerObserver = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    staggerObserver.unobserve(entry.target);
                }
            });
        },
        { rootMargin: ROOT_MARGIN, threshold: THRESHOLD }
    );

    document.querySelectorAll(".premium-stagger").forEach(function (el) {
        staggerObserver.observe(el);
    });
})();
