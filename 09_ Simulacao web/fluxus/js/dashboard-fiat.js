(function () {
  "use strict";

  function apiBase() {
    if (window.FLUXUS_API_BASE !== undefined && window.FLUXUS_API_BASE !== null && window.FLUXUS_API_BASE !== "") {
      return String(window.FLUXUS_API_BASE).replace(/\/$/, "");
    }
    if (window.location.protocol === "file:") return "";
    return window.location.origin.replace(/\/$/, "");
  }

  function brl(n) {
    var x = Number(n);
    if (Number.isNaN(x)) return "—";
    try {
      return x.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
    } catch (e) {
      return "R$ " + x.toFixed(2);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var gtvEl = document.getElementById("fluxus-dash-gtv");
    if (!gtvEl) return;
    var sim = window.FLUXUS_SIM_DATA || {};
    if (sim.gtv_brl) gtvEl.textContent = brl(sim.gtv_brl);
    var base = apiBase();
    if (!base) return;
    fetch(base + "/api/summary")
      .then(function (r) {
        return r.json();
      })
      .then(function (s) {
        var p = document.getElementById("fluxus-dash-ptax");
        if (p && s.ptax_usd_brl_mid_media != null) {
          p.textContent = String(s.ptax_usd_brl_mid_media) + " (média)";
        }
      })
      .catch(function () {});
  });
})();
