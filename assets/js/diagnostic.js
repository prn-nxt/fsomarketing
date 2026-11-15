/* =====================================================================
   FSO DIAGNOSTIC ,  reusable widget (with lead capture + score email)

   Flow:  intro → 15 questions → [capture name + email] → score result
   The capture step is where every completion becomes a lead: the answers,
   the computed score and the dimension breakdown are POSTed to your
   endpoint, which (a) records the lead for you and (b) emails the score
   to the respondent. See LEAD-CAPTURE-SETUP.md for wiring it to your inbox.

   CONFIGURE the three lines in FSO_CONFIG below.
   ===================================================================== */
window.FSODiagnostic = (function () {
  "use strict";

  /* ------------------------------------------------------------------ *
   *  CONFIG, set these three, then the diagnostic captures + emails.  *
   * ------------------------------------------------------------------ */
  var FSO_CONFIG = {
    // Where leads are sent. This ONE URL both records the lead for you and
    // emails the score to the respondent. Paste your Google Apps Script Web
    // App URL (recommended) or a Web3Forms/Formspree endpoint here.
    // Leave "" while testing, the score still shows, but nothing is sent.
    submitEndpoint: "https://script.google.com/macros/s/AKfycbwN8EKY2uHubHocz0yvzCIUV0wSlzmRts-HPke8rudqPodJWHm5YWihfoqvh0aG4WakNg/exec",

    // Ask for name + email BEFORE revealing the score (captures every
    // completion). Set to false to show the score first, then ask.
    gateResults: true,

    bookingUrl: "contact.html",              // your Calendly / booking link
    portalUrl:  "https://app.fsoworld.com"
  };
  /* ------------------------------------------------------------------ */

  var LOGO = '<img class="logo-mark" src="assets/img/fso-mark-blue.png" alt="FSO" width="231" height="96" decoding="async">';

  var DIMENSIONS = {
    cash:    { name: "Cash Flow Clarity",             remedy: "a disciplined cash-allocation system that shows your true cash position and protects it",
               advice: "Split cash into deliberate buckets, operations, tax, growth, owner, and run a rolling 13-week forecast so you always know your true position." },
    profit:  { name: "Profitability Insight",         remedy: "daily / weekly profitability tracking so margins are real, not year-end guesses",
               advice: "Track profit at the product, order or job level and review margins weekly, pricing off current replacement cost so margins stay real." },
    mis:     { name: "MIS & Decision Data",           remedy: "a fast month-close and a decision-ready dashboard of the numbers that matter",
               advice: "Close each month within 7 days and drive decisions off a live dashboard of the few numbers that matter, not gut, memory or the bank balance." },
    wc:      { name: "Working Capital & Receivables", remedy: "a working-capital and collections discipline that frees up trapped cash",
               advice: "Manage receivable days to a target, chase collections actively, and track your working-capital cycle to release trapped cash." },
    capital: { name: "Capital Structure & Funding",   remedy: "a deliberate capital structure and a clear view of your cost of capital",
               advice: "Build a deliberate mix of debt, equity and own funds matched to the business, and know your cost of capital so you can see if returns beat it." },
    growth:  { name: "Planning, Controls & Growth",   remedy: "budgeting, internal controls and capex-readiness so you can grow without guessing",
               advice: "Run the year against a budget with monthly variance tracking, add controls to catch leakage early, and stay capex-ready for opportunities." }
  };

  // A dimension at or above this % is treated as "already strong" → we say
  // "This is a good score" instead of showing an improvement tip. 76 is the certification line.
  var GOOD_DIM = 76;

  var QUESTIONS = [
    { d: "cash", q: "Right now, do you know exactly how much cash your business has across all accounts?", a: ["No, I'd have to ask someone or check later", "Roughly, within a broad range", "Yes, I check it every few days", "Yes, to the rupee, any moment"] },
    { d: "cash", q: "How is your business cash organised?", a: ["One account, everything flows in and out together", "Mostly one pool, some money set aside informally", "Separate pots for tax, operations and growth", "Deliberate buckets I manage by rule (ops, statutory, growth, owner)"] },
    { d: "cash", q: "Can you see your cash position 4 to 13 weeks ahead?", a: ["No, cash surprises hit me regularly", "I can guess for the next week or two", "I have a rough monthly view", "Yes, a rolling 13-week forecast I actually use"] },
    { d: "profit", q: "Do you know your true profit on each product, order or job?", a: ["No, only the overall profit at year-end", "I estimate margins by feel", "I know it for major lines, not all", "Yes, product / order-level profit is visible to me"] },
    { d: "profit", q: "How often do you actually look at profitability?", a: ["Once a year, when the audit is done", "Quarterly, roughly", "Monthly", "Daily or weekly, it drives my decisions"] },
    { d: "profit", q: "When you price and cost your work, what do you base it on?", a: ["Old purchase price / whatever the books show", "A rough markup on last-known cost", "Recent cost, updated occasionally", "Current replacement cost, so margins stay real"] },
    { d: "mis", q: "After a month closes, how soon do you get reliable numbers?", a: ["45+ days, or only at year-end", "Around 30 days", "Within 15 days", "Within 7 days, consistently"] },
    { d: "mis", q: "What do you mainly rely on to make big decisions?", a: ["Gut and memory", "Bank balance and a few reports", "A monthly MIS pack", "A live dashboard of the numbers that matter"] },
    { d: "wc", q: "How well do you manage what customers owe you?", a: ["I don't track collection days", "I know we're stretched, but don't measure it", "I track receivable days and chase them", "I manage receivable days to a target, deliberately"] },
    { d: "wc", q: "Do you know your working-capital cycle in days?", a: ["I'm not sure what that means for us", "I know it's tight, but not the number", "I know the number roughly", "Yes, I track it and actively shorten it"] },
    { d: "capital", q: "Your current mix of loans, equity and own funds is…", a: ["Whatever was available when I needed money", "Mostly reactive, with some planning", "A reasonably deliberate structure", "A deliberate structure matched to the business"] },
    { d: "capital", q: "Do you know your cost of capital, and whether your returns beat it?", a: ["No", "I know my interest rates only", "I have a rough sense of both", "Yes, I know it and measure returns against it"] },
    { d: "growth", q: "Do you run the year against a budget?", a: ["No budget", "A loose target in my head", "A budget, reviewed occasionally", "A budget with monthly variance tracking"] },
    { d: "growth", q: "If money were leaking, wastage, leakage or fraud, would you catch it?", a: ["Probably not until it's large", "Eventually, by chance", "Likely, we have some checks", "Yes, controls / internal audit would flag it early"] },
    { d: "growth", q: "If a strong growth or capex opportunity came tomorrow, could you evaluate and fund it with confidence?", a: ["No, I'd be guessing", "I could try, but shakily", "Mostly yes, with some scramble", "Yes, I know my numbers, capacity and funding options"] }
  ];

  var BANDS = [
    { min: 0,  max: 40,  name: "Financially Blind", color: "#E15748", verdict: "Right now, key decisions are made without reliable numbers.", sub: "Because so little is measured today, the first few disciplines tend to release cash and clarity quickly." },
    { min: 41, max: 60,  name: "Reactive",          color: "#E39A2B", verdict: "Money is managed after the event, not ahead of it.", sub: "You feel the problems after they land. A few core systems would move you from firefighting to foresight." },
    { min: 61, max: 75,  name: "Developing",        color: "#3E8FD8", verdict: "Solid foundations, with clear gaps still to close.", sub: "You are close. A full FSO Assessment would show exactly what stands between you and the line at 76." },
    { min: 76, max: 100, name: "Certification ready", color: "#18AE80", verdict: "On this indicative check, you are at or above the line of 76.", sub: "A full FSO Assessment, on evidence, is the next step. Clear the line there and you may apply for Certification." }
  ];

  // Reusable capture-form fields (name + email required; mobile/company optional)
  function captureFields(btnLabel) {
    return '' +
      '<div class="field"><label>Name</label><input data-f="name" type="text" autocomplete="name" placeholder="Your name" required></div>' +
      '<div class="field"><label>Work email</label><input data-f="email" type="email" autocomplete="email" placeholder="you@company.com" required></div>' +
      '<div class="grid2">' +
        '<div class="field"><label>Mobile <span class="opt">(optional)</span></label><input data-f="mobile" type="tel" autocomplete="tel" inputmode="tel" placeholder="+91 …"></div>' +
        '<div class="field"><label>Company <span class="opt">(optional)</span></label><input data-f="company" type="text" autocomplete="organization" placeholder="Company name"></div>' +
      '</div>' +
      '<div class="err" data-err></div>' +
      '<button class="btn btn-primary btn-block" data-submit>' + btnLabel + ' <span class="ar">→</span></button>';
  }

  function resultSvg() {
    return '<div class="gauge-wrap">' +
      '<svg class="gauge" viewBox="0 0 400 214" role="img" aria-label="Your financial smartness score">' +
        '<g fill="none" stroke-width="18" stroke-linecap="round">' +
          '<path d="M40 180 A160 160 0 0 1 66.9 91.0" stroke="#E15748"/>' +
          '<path d="M74.5 79.9 A160 160 0 0 1 143.0 34.2" stroke="#E39A2B"/>' +
          '<path d="M155.5 29.6 A160 160 0 0 1 244.5 29.6" stroke="#3E8FD8"/>' +
          '<path d="M257.0 34.2 A160 160 0 0 1 325.5 79.9" stroke="#18AE80"/>' +
          '<path d="M333.1 91.0 A160 160 0 0 1 360 180" stroke="#0A38C0"/>' +
        '</g>' +
        '<g class="needle" data-needle>' +
          '<line x1="200" y1="180" x2="200" y2="58" stroke="#0B1B3F" stroke-width="3.5" stroke-linecap="round"/>' +
          '<circle cx="200" cy="180" r="9" fill="#0B1B3F"/><circle cx="200" cy="180" r="4" fill="#fff"/>' +
        '</g>' +
        '<text class="score-num" data-scorenum x="200" y="176" text-anchor="middle">0</text>' +
        '<text class="score-of" x="200" y="200" text-anchor="middle">OUT OF 100</text>' +
      '</svg></div>';
  }

  function tmpl() {
    return '' +
    '<div class="fsod-inner">' +
      '<div class="fsod-brand">' + LOGO + '<span class="fsod-kick">Diagnostic</span></div>' +

      '<section data-view="intro">' +
        '<p class="eyebrow">A six minute financial reality check</p>' +
        '<h2>How financially smart is <em>your company?</em></h2>' +
        '<p class="d-lede">Fifteen questions. One private score, emailed straight to you. See where your business is in control of its numbers, and where the gaps are, before the full FSO Assessment.</p>' +
        '<div class="meta-row">' +
          '<div class="meta"><span class="n">15</span><span class="l">Questions</span></div>' +
          '<div class="meta"><span class="n">~6</span><span class="l">Minutes</span></div>' +
          '<div class="meta"><span class="n">100</span><span class="l">Point score</span></div>' +
        '</div>' +
        '<button class="btn btn-primary btn-block" data-start>Start the diagnostic <span class="ar">→</span></button>' +
      '</section>' +

      '<section data-view="quiz" class="hidden" aria-live="polite">' +
        '<div class="progress-meta"><span class="dim" data-dimlabel>Cash Flow Clarity</span><span data-counter>1 / 15</span></div>' +
        '<div class="progress-track"><div class="progress-fill" data-progress></div></div>' +
        '<div class="qwrap" data-qwrap></div>' +
        '<div class="navrow"><button class="back" data-back disabled>← Back</button><span class="hint">Tap an answer to continue</span></div>' +
      '</section>' +

      // GATE, where the lead is captured and the score email is triggered
      '<section data-view="gate" class="hidden">' +
        '<div class="gate-badge" data-gateband><span class="swatch"></span><span>Your score is ready</span></div>' +
        '<h2>Where should we send your <em>FSO Score?</em></h2>' +
        '<p class="d-lede">Add your details to reveal your score now, we\'ll also email you the full breakdown: your result on every dimension and exactly where you\'re losing points.</p>' +
        '<div class="capture" data-capture-slot></div>' +
        '<p class="fineprint">We\'ll only use this to send your report and, if you want it, a short conversation about closing the gaps. No spam, ever.</p>' +
      '</section>' +

      '<section data-view="result" class="hidden">' +
        resultSvg() +
        '<div style="text-align:center;"><span class="band-tag" data-bandtag><span class="swatch"></span><span data-bandname>Developing</span></span></div>' +
        '<p class="verdict" data-verdict></p><p class="verdict-sub" data-verdictsub></p>' +
        '<div class="emailed hidden" data-emailed><span class="check-sm">✓</span><span data-emailedtext></span></div>' +
        '<div class="gap-note"><div class="k">Your biggest gap</div><p data-gaptext></p></div>' +
        '<div class="breakdown"><h3>Where you stand, dimension by dimension</h3><div data-dimbars></div></div>' +
        // shown only when gateResults=false (score-first mode): capture appears here
        '<div class="capture hidden" data-postcapture>' +
          '<h2>Email me my full FSO report</h2>' +
          '<p class="sub">Your score against every dimension, and exactly where you\'re losing points.</p>' +
          '<div data-capture-slot-post></div>' +
          '<p class="fineprint">No spam, just your report and, if you want it, a short conversation about closing the gaps.</p>' +
        '</div>' +
        '<div class="result-cta" data-resultcta>' +
          '<a class="btn btn-primary btn-block" data-book href="#">Book a Discovery Call <span class="ar">→</span></a>' +
        '</div>' +
        '<div class="d-foot"><span>Built on the <b>FSO 2.0 standard</b></span><button class="back" data-restart style="color:var(--muted-2);">↻ Retake</button></div>' +
      '</section>' +
    '</div>';
  }

  function mount(target) {
    var root = typeof target === "string" ? document.querySelector(target) : target;
    if (!root) return;
    root.className = "fsod";
    root.innerHTML = tmpl();

    var answers = new Array(QUESTIONS.length).fill(null);
    var current = 0;
    var payload = null;             // {score, band, dims, weakest}
    var q = function (sel) { return root.querySelector(sel); };
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var gated = FSO_CONFIG.gateResults !== false;

    var views = {
      intro:  q('[data-view="intro"]'),
      quiz:   q('[data-view="quiz"]'),
      gate:   q('[data-view="gate"]'),
      result: q('[data-view="result"]')
    };
    function show(name) { Object.keys(views).forEach(function (k) { views[k].classList.toggle("hidden", k !== name); }); }

    // Inject the capture form into the active slot and wire it
    if (gated) {
      q("[data-capture-slot]").innerHTML = captureFields("Reveal my FSO Score");
    } else {
      q("[data-capture-slot-post]").innerHTML = captureFields("Email me my report");
    }

    q("[data-start]").addEventListener("click", function () { show("quiz"); render(); });
    q("[data-back]").addEventListener("click", function () { if (current > 0) { current--; render(); } });
    q("[data-restart]").addEventListener("click", function () {
      answers.fill(null); current = 0; payload = null;
      q("[data-emailed]").classList.add("hidden");
      // clear the capture fields and any error so a retake starts clean
      Array.prototype.forEach.call(root.querySelectorAll("[data-f]"), function (el) { el.value = ""; });
      var err = root.querySelector("[data-err]"); if (err) err.textContent = "";
      show("intro");
      root.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    });

    function render() {
      var item = QUESTIONS[current];
      q("[data-dimlabel]").textContent = DIMENSIONS[item.d].name;
      q("[data-counter]").textContent = (current + 1) + " / " + QUESTIONS.length;
      q("[data-progress]").style.width = (current / QUESTIONS.length * 100) + "%";
      q("[data-back]").disabled = current === 0;
      var wrap = q("[data-qwrap]"); wrap.innerHTML = "";
      var num = document.createElement("div"); num.className = "qnum"; num.textContent = String(current + 1).padStart(2, "0");
      var qt = document.createElement("p"); qt.className = "qtext"; qt.textContent = item.q;
      var opts = document.createElement("div"); opts.className = "options";
      item.a.forEach(function (text, i) {
        var b = document.createElement("button");
        b.className = "opt" + (answers[current] === i ? " sel" : ""); b.type = "button";
        b.innerHTML = '<span class="mark"></span><span>' + text + '</span>';
        b.addEventListener("click", function () { choose(i); });
        opts.appendChild(b);
      });
      wrap.appendChild(num); wrap.appendChild(qt); wrap.appendChild(opts);
    }

    function choose(i) {
      answers[current] = i; render();
      setTimeout(function () {
        if (current < QUESTIONS.length - 1) { current++; render(); } else { finish(); }
      }, 190);
    }

    function computeScore() {
      var raw = answers.reduce(function (s, v) { return s + (v == null ? 0 : v); }, 0);
      var score = Math.round(raw / (QUESTIONS.length * 3) * 100);
      var agg = {}; Object.keys(DIMENSIONS).forEach(function (k) { agg[k] = { got: 0, max: 0 }; });
      QUESTIONS.forEach(function (qn, idx) { agg[qn.d].max += 3; agg[qn.d].got += (answers[idx] == null ? 0 : answers[idx]); });
      var dims = Object.keys(DIMENSIONS).map(function (k) {
        var misses = [];
        QUESTIONS.forEach(function (qn, idx) {
          if (qn.d !== k) return;
          var ai = answers[idx];
          if (ai == null || ai < 3) {
            misses.push({ q: qn.q, your: (ai == null ? "Not answered" : qn.a[ai]), best: qn.a[qn.a.length - 1] });
          }
        });
        return { key: k, name: DIMENSIONS[k].name, remedy: DIMENSIONS[k].remedy, advice: DIMENSIONS[k].advice, pct: Math.round(agg[k].got / agg[k].max * 100), misses: misses };
      });
      return { score: score, dims: dims };
    }
    function bandFor(s) { return BANDS.find(function (b) { return s >= b.min && s <= b.max; }) || BANDS[0]; }
    function barColor(p) { if (p <= 40) return "#E15748"; if (p <= 60) return "#E39A2B"; if (p <= 75) return "#3E8FD8"; if (p <= 90) return "#18AE80"; return "#0A38C0"; }
    function animateNumber(el, from, to, dur) {
      if (dur <= 0) { el.textContent = to; return; }
      var start = performance.now();
      (function step(now) {
        var p = Math.min(1, (now - start) / dur), eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(from + (to - from) * eased);
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
    }

    // Q15 done → compute, then either gate (capture first) or show result
    function finish() {
      var res = computeScore(), band = bandFor(res.score);
      var weakest = res.dims.slice().sort(function (a, b) { return a.pct - b.pct; })[0];
      payload = { score: res.score, band: band.name, dims: res.dims, weakest: weakest };
      if (gated) {
        var gb = q("[data-gateband]"); if (gb) gb.style.color = band.color;
        show("gate");
        root.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      } else {
        showResult();
        q("[data-postcapture]").classList.remove("hidden");
      }
    }

    function showResult() {
      show("result");
      q("[data-progress]").style.width = "100%";
      var res = { score: payload.score, dims: payload.dims };
      var band = bandFor(res.score), weakest = payload.weakest;

      var angle = (res.score / 100) * 180 - 90;
      var needle = q("[data-needle]");
      needle.style.transform = "rotate(-90deg)";
      requestAnimationFrame(function () {
        setTimeout(function () {
          needle.style.transform = "rotate(" + angle + "deg)";
          animateNumber(q("[data-scorenum]"), 0, res.score, reduce ? 0 : 1050);
        }, 120);
      });

      var tag = q("[data-bandtag]"); tag.style.color = band.color;
      q("[data-bandname]").textContent = band.name;
      q("[data-verdict]").textContent = band.verdict;
      q("[data-verdictsub]").textContent = band.sub;
      q("[data-book]").href = FSO_CONFIG.bookingUrl || "#";

      q("[data-gaptext]").innerHTML = "Your weakest area is <b>" + weakest.name + "</b> (" + weakest.pct +
        "%), often where the most value is at stake.";

      var box = q("[data-dimbars]"); box.innerHTML = "";
      res.dims.forEach(function (dm) {
        var row = document.createElement("div"); row.className = "dimrow";
        var flag = dm.key === weakest.key ? '<span class="flag">Biggest gap</span>' : '';
        var good = dm.pct >= GOOD_DIM;
        var status = good
          ? '<div class="dimadvice good" style="margin:7px 0 2px;font-size:13px;line-height:1.5;color:#18AE80;font-weight:600;">✓ This is a good score.</div>'
          : '';
        var miss = '';
        if (!good && dm.misses && dm.misses.length) {
          miss = '<div style="margin:8px 0 2px;padding:11px 13px;background:#FBFCFE;border:1px solid #EEF2FA;border-radius:9px;">' +
            '<div style="font-size:10px;letter-spacing:.5px;text-transform:uppercase;color:#8792A8;font-weight:700;margin-bottom:7px;">Where you missed</div>' +
            dm.misses.map(function (m) {
              return '<div style="font-size:13px;line-height:1.5;color:#44536E;margin:0 0 9px;">&#8226; ' + m.q +
                '<br><span style="color:#B04A3D;">Your answer:</span> ' + m.your +
                '<br><span style="color:#18AE80;">Best answer:</span> ' + m.best + '</div>';
            }).join('') + '</div>';
        }
        row.innerHTML = '<div class="dimhead"><span class="dimname">' + dm.name + flag + '</span><span class="dimpct">' + dm.pct + '%</span></div><div class="bar"><span></span></div>' + status + miss;
        box.appendChild(row);
        var fill = row.querySelector(".bar span");
        fill.style.background = barColor(dm.pct);
        requestAnimationFrame(function () { setTimeout(function () { fill.style.width = dm.pct + "%"; }, 260); });
      });
    }

    // Submit handler (works for both gate and post-capture forms)
    root.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("[data-submit]") : null;
      if (!btn) return;
      e.preventDefault();
      submitLead(btn);
    });

    function submitLead(btn) {
      var scope = btn.closest("[data-capture-slot], [data-capture-slot-post]") || root;
      var get = function (f) { var el = scope.querySelector('[data-f="' + f + '"]'); return el ? el.value.trim() : ""; };
      var name = get("name"), email = get("email"), mobile = get("mobile"), company = get("company");
      var err = scope.querySelector("[data-err]");
      if (!name) { if (err) err.textContent = "Please add your name."; return; }
      if (!/^\S+@\S+\.\S+$/.test(email)) { if (err) err.textContent = "Please enter a valid email so we can send your score."; return; }
      if (err) err.textContent = "";

      // Full lead: everything your backend needs to record the lead AND
      // build the score email for the respondent.
      var lead = {
        source: "fso-diagnostic",
        name: name, email: email, mobile: mobile, company: company,
        score: payload.score,
        band: payload.band,
        weakest: payload.weakest ? payload.weakest.name : "",
        weakest_pct: payload.weakest ? payload.weakest.pct : "",
        dimensions: (payload.dims || []).map(function (d) { return { name: d.name, pct: d.pct, advice: d.advice, misses: d.misses }; }),
        // Full question-by-question record of what the respondent selected, for the FSO team report.
        responses: QUESTIONS.map(function (qn, idx) {
          var ai = answers[idx];
          return {
            dim: DIMENSIONS[qn.d].name,
            q: qn.q,
            your: (ai == null ? "Not answered" : qn.a[ai]),
            best: qn.a[qn.a.length - 1],
            ok: (ai === qn.a.length - 1)
          };
        }),
        // flat, email-friendly summary line
        summary: (payload.dims || []).map(function (d) { return d.name + ": " + d.pct + "%"; }).join(" · "),
        page_url: (window.location && window.location.href) || "",
        submitted_at: new Date().toISOString()
      };

      var done = function (ok) {
        if (gated) {
          showResult();
          if (FSO_CONFIG.submitEndpoint && ok) {
            var e2 = q("[data-emailed]");
            q("[data-emailedtext]").textContent = "Your full FSO report is on its way to " + email + ".";
            e2.classList.remove("hidden");
          }
          root.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
        } else {
          q("[data-postcapture]").classList.add("hidden");
          var e3 = q("[data-emailed]");
          q("[data-emailedtext]").textContent = FSO_CONFIG.submitEndpoint && ok
            ? "Your full FSO report is on its way to " + email + "."
            : "Thanks, we've noted your details.";
          e3.classList.remove("hidden");
        }
      };

      if (FSO_CONFIG.submitEndpoint) {
        btn.disabled = true; btn.classList.add("is-loading");
        // text/plain avoids a CORS preflight, so a Google Apps Script Web App
        // (recommended) accepts it directly. Web3Forms/Formspree also accept it.
        fetch(FSO_CONFIG.submitEndpoint, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          body: JSON.stringify(lead)
        }).then(function () { done(true); })
          .catch(function () {
            // Never trap the user: still show their score, note email may be delayed.
            btn.disabled = false; btn.classList.remove("is-loading");
            if (err) err.textContent = "";
            done(false);
          });
      } else {
        if (window.console) console.log("FSO lead (no endpoint set):", lead);
        done(false);
      }
    }
  }

  return { mount: mount, config: FSO_CONFIG };
})();

/* Auto-mount on standalone diagnostic page */
document.addEventListener("DOMContentLoaded", function () {
  var el = document.getElementById("diagnostic-page-root");
  if (el) window.FSODiagnostic.mount(el);
});
