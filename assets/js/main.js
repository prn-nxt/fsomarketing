/* =====================================================================
   FSO — shared site behaviour
   nav drawer · sticky header · diagnostic modal · testimonial carousel
   · FAQ accordion · scroll reveal · contact form
   ===================================================================== */
(function () {
  "use strict";
  // Signal that the site JS is executing. CSS uses this to cancel the
  // reveal fail-safe: if this line never runs, content still appears.
  document.documentElement.classList.add("js-run");
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Sticky header state ---------- */
  var header = $(".site-header");
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 12) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav drawer ---------- */
  var burger = $(".hamburger");
  var navLinks = $(".nav-links");
  function closeNav() {
    if (!burger || !navLinks) return;
    burger.setAttribute("aria-expanded", "false");
    navLinks.classList.remove("open");
    document.body.style.overflow = "";
  }
  if (burger && navLinks) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      navLinks.classList.toggle("open", !open);
      document.body.style.overflow = !open ? "hidden" : "";
    });
    $$(".nav-links a").forEach(function (a) { a.addEventListener("click", closeNav); });
    window.addEventListener("resize", function () { if (window.innerWidth > 960) closeNav(); });
  }

  /* ---------- Scroll reveal ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- FAQ accordion ---------- */
  $$(".faq-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var open = q.getAttribute("aria-expanded") === "true";
      var ans = q.nextElementSibling;
      q.setAttribute("aria-expanded", String(!open));
      if (ans) ans.style.maxHeight = open ? "0px" : ans.scrollHeight + "px";
    });
  });

  /* ---------- Testimonial carousel ---------- */
  $$("[data-carousel]").forEach(function (car) {
    var track = $(".tcar-track", car);
    var slides = $$(".tcar-slide", car);
    var dotsWrap = $(".tcar-dots", car);
    var prev = $("[data-prev]", car);
    var next = $("[data-next]", car);
    var i = 0, timer = null;
    if (!track || !slides.length) return;

    var dots = slides.map(function (_, idx) {
      var b = document.createElement("button");
      b.className = "tcar-dot" + (idx === 0 ? " active" : "");
      b.type = "button";
      b.setAttribute("aria-label", "Go to testimonial " + (idx + 1));
      b.addEventListener("click", function () { go(idx); reset(); });
      if (dotsWrap) dotsWrap.appendChild(b);
      return b;
    });

    function go(n) {
      i = (n + slides.length) % slides.length;
      track.style.transform = "translateX(" + (-i * 100) + "%)";
      track.style.transition = "transform .5s cubic-bezier(.4,0,.2,1)";
      dots.forEach(function (d, idx) { d.classList.toggle("active", idx === i); });
    }
    function reset() { if (timer) { clearInterval(timer); start(); } }
    function start() { timer = setInterval(function () { go(i + 1); }, 6500); }

    if (prev) prev.addEventListener("click", function () { go(i - 1); reset(); });
    if (next) next.addEventListener("click", function () { go(i + 1); reset(); });
    track.style.display = "flex";
    slides.forEach(function (s) { s.style.flex = "0 0 100%"; });
    start();
    car.addEventListener("mouseenter", function () { if (timer) clearInterval(timer); });
    car.addEventListener("mouseleave", start);
  });

  /* ---------- Diagnostic modal ---------- */
  var overlay = $("#diagnostic-modal");
  var lastFocus = null;
  function openModal() {
    if (!overlay) { window.location.href = "diagnostic.html"; return; }
    lastFocus = document.activeElement;
    overlay.classList.add("open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    // Lazy-mount diagnostic widget on first open
    if (window.FSODiagnostic && !overlay.dataset.mounted) {
      window.FSODiagnostic.mount("#diagnostic-modal-root");
      overlay.dataset.mounted = "1";
    }
    var c = $(".modal-close", overlay);
    if (c) c.focus();
  }
  function closeModal() {
    if (!overlay) return;
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  $$("[data-open-diagnostic]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); openModal(); });
  });
  if (overlay) {
    $$("[data-close-modal]", overlay).forEach(function (b) { b.addEventListener("click", closeModal); });
    overlay.addEventListener("click", function (e) { if (e.target === overlay) closeModal(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && overlay.classList.contains("open")) closeModal(); });
  }
  window.FSOCloseModal = closeModal;

  /* ---------- Contact form ----------
     Set CONTACT_ENDPOINT to your Google Apps Script / Web3Forms / Formspree
     URL (the same one used for the diagnostic works too — it routes on the
     "source" field). Leave "" and the form just shows a success message.
     See LEAD-CAPTURE-SETUP.md. */
  var CONTACT_ENDPOINT = "https://script.google.com/macros/s/AKfycbwN8EKY2uHubHocz0yvzCIUV0wSlzmRts-HPke8rudqPodJWHm5YWihfoqvh0aG4WakNg/exec";

  $$("[data-mock-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = form.querySelector(".form-ok");
      var required = $$("[required]", form);
      var valid = true;
      required.forEach(function (f) {
        if (!f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value))) {
          valid = false; f.style.borderColor = "#E15748";
        } else { f.style.borderColor = ""; }
      });
      if (!valid) return;

      var submitBtn = form.querySelector('[type="submit"]');
      var data = { source: "fso-contact", submitted_at: new Date().toISOString(), page_url: location.href };
      $$("input, select, textarea", form).forEach(function (f) { if (f.name) data[f.name] = f.value.trim(); });

      var succeed = function () {
        form.reset();
        if (ok) { ok.style.display = "block"; ok.scrollIntoView({ behavior: "smooth", block: "center" }); }
        if (submitBtn) { submitBtn.disabled = false; }
      };

      if (CONTACT_ENDPOINT) {
        if (submitBtn) submitBtn.disabled = true;
        fetch(CONTACT_ENDPOINT, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data) })
          .then(succeed)
          .catch(function () { if (submitBtn) submitBtn.disabled = false; succeed(); });
      } else {
        if (window.console) console.log("FSO contact (no endpoint set):", data);
        succeed();
      }
    });
  });

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
