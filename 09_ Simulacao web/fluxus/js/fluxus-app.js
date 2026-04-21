/**
 * FLUXUS simulação web — i18n + dados fixos + logo marca.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "fluxus_lang";

  function getBundle() {
    return window.FLUXUS_I18N_BUNDLE || null;
  }

  function getSim() {
    return window.FLUXUS_SIM_DATA || {};
  }

  function getLang() {
    var b = getBundle();
    var def = (b && b.langOrder && b.langOrder[0]) || "pt-BR";
    try {
      var s = localStorage.getItem(STORAGE_KEY);
      if (s && b && b.i18n && b.i18n[s]) return s;
    } catch (e) {}
    return def;
  }

  function t(lang, key) {
    var b = getBundle();
    if (!b || !b.i18n) return key;
    var row = b.i18n[lang] || b.i18n.en || {};
    if (row[key]) return row[key];
    var en = b.i18n.en || {};
    return en[key] || key;
  }

  function applyI18n(lang) {
    var b = getBundle();
    if (!b) return;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (!key) return;
      el.textContent = t(lang, key);
    });
    var suf = t(lang, "page_title_suffix");
    if (suf) document.title = "FLUXUS — " + suf;
  }

  function formatBRL(n) {
    try {
      return n.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
        maximumFractionDigits: 2,
      });
    } catch (e) {
      return "R$ " + String(n);
    }
  }

  function formatInt(n) {
    try {
      return n.toLocaleString("pt-BR", { maximumFractionDigits: 0 });
    } catch (e) {
      return String(n);
    }
  }

  function applySimData() {
    var d = getSim();
    document.querySelectorAll("[data-fluxus]").forEach(function (el) {
      var k = el.getAttribute("data-fluxus");
      if (k === "gtv_brl") el.textContent = formatBRL(d.gtv_brl);
      else if (k === "rematches") el.textContent = formatInt(d.rematches);
      else if (k === "lps") el.textContent = formatInt(d.active_lps);
      else if (k === "orch_brl") el.textContent = formatBRL(d.orchestration_fee_brl);
      else if (k === "stability_brl") el.textContent = formatBRL(d.stability_pool_alloc_brl);
    });
  }

  function applyBrandLogo() {
    var logo = document.getElementById("logo_header");
    if (!logo) return;
    logo.src = "images/fluxus-cover.png";
    logo.alt = "FLUXUS";
    logo.style.objectFit = "cover";
    logo.style.maxHeight = "44px";
    logo.style.width = "auto";
    logo.style.borderRadius = "8px";
  }

  function injectLangSelector(lang) {
    var mount = document.getElementById("fluxus-lang-mount");
    if (!mount || !getBundle()) return;
    var b = getBundle();
    var wrap = document.createElement("div");
    wrap.className = "fluxus-lang-wrap d-flex align-items-center gap-2";
    var lab = document.createElement("span");
    lab.className = "f12-regular text-Gray d-none d-md-inline";
    lab.setAttribute("data-i18n", "lang_select");
    lab.textContent = t(lang, "lang_select");
    var sel = document.createElement("select");
    sel.className = "form-select form-select-sm";
    sel.style.maxWidth = "220px";
    (b.langOrder || []).forEach(function (code) {
      var o = document.createElement("option");
      o.value = code;
      o.textContent = (b.langNative && b.langNative[code]) || code;
      sel.appendChild(o);
    });
    sel.value = lang;
    sel.addEventListener("change", function () {
      try {
        localStorage.setItem(STORAGE_KEY, sel.value);
      } catch (e) {}
      applyI18n(sel.value);
      applySearchPlaceholder(sel.value);
      applySimData();
      lab.textContent = t(sel.value, "lang_select");
    });
    wrap.appendChild(lab);
    wrap.appendChild(sel);
    mount.appendChild(wrap);
  }

  function injectDisclaimer(lang) {
    var mount = document.getElementById("fluxus-disclaimer-mount");
    if (!mount) return;
    mount.innerHTML =
      '<div class="alert alert-secondary py-2 px-3 mb-0 f12-regular" role="status" data-i18n="disclaimer_long"></div>';
    applyI18n(lang);
  }

  function applySearchPlaceholder(lang) {
    var inp = document.querySelector(".header-dashboard input.show-search");
    if (inp) inp.setAttribute("placeholder", t(lang, "search_placeholder"));
  }

  function applyThemeToggle() {
    var btn = document.getElementById("theme-institutional-toggle");
    if (!btn) return;
    
    var saved = localStorage.getItem("fluxus-premium-theme") || "light";
    document.body.setAttribute("data-theme", saved === "dark" ? "dark-institutional" : "light");

    btn.addEventListener("click", function() {
      var current = document.body.getAttribute("data-theme");
      var next = (current === "dark-institutional") ? "light" : "dark-institutional";
      document.body.setAttribute("data-theme", next);
      localStorage.setItem("fluxus-premium-theme", next === "dark-institutional" ? "dark" : "light");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var lang = getLang();
    applyThemeToggle();
    applyBrandLogo();
    applyI18n(lang);
    applySearchPlaceholder(lang);
    applySimData();
    injectLangSelector(lang);
    injectDisclaimer(lang);
  });
})();
