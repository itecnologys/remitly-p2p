/**
 * Abas "Visões" em transaction.html — agregado por LP e resumo global.
 */
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

  function intFmt(n) {
    var x = Number(n);
    if (Number.isNaN(x)) return "—";
    try {
      return x.toLocaleString("pt-BR");
    } catch (e) {
      return String(x);
    }
  }

  function loadLpAggregates() {
    var base = apiBase();
    var meta = document.getElementById("fluxus-lp-agg-meta");
    var tb = document.getElementById("fluxus-lp-agg-tbody");
    if (!base || !tb) return;
    if (meta) meta.textContent = "A carregar…";
    fetch(base + "/api/rematches/by_lp")
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        var rows = j.rows || [];
        tb.innerHTML = "";
        rows.forEach(function (r) {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td class=\"f12-medium\">" +
            (r.lp_id || "") +
            "</td><td class=\"f12-medium\">" +
            (r.lp_nome || "") +
            "</td><td class=\"f12-medium text-end\">" +
            intFmt(r.n_rem) +
            "</td><td class=\"f12-medium text-end\">" +
            brl(r.sum_gtv_brl) +
            "</td><td class=\"f12-medium text-end\">" +
            brl(r.sum_spread_brl) +
            "</td><td class=\"f12-medium text-end\">" +
            brl(r.sum_taxas_trilho_brl) +
            "</td><td class=\"f12-medium text-end\">" +
            brl(r.sum_lp_retorno_brl) +
            "</td>";
          tb.appendChild(tr);
        });
        if (meta) meta.textContent = rows.length + " LPs";
      })
      .catch(function () {
        if (meta) meta.textContent = "Erro ao carregar (servidor em 127.0.0.1:8787?)";
      });
  }

  function loadSummary() {
    var base = apiBase();
    if (!base) return;
    fetch(base + "/api/summary")
      .then(function (r) {
        return r.json();
      })
      .then(function (s) {
        var elN = document.getElementById("fluxus-sum-n");
        var elG = document.getElementById("fluxus-sum-gtv");
        var elP = document.getElementById("fluxus-sum-ptax");
        if (elN) elN.textContent = intFmt(s.rematches);
        if (elG) elG.textContent = brl(s.gtv_brl);
        if (elP) elP.textContent = s.ptax_usd_brl_mid_media != null ? String(s.ptax_usd_brl_mid_media) : "—";
      })
      .catch(function () {});
  }

  function loadDre() {
    var base = apiBase();
    if (!base) return;
    var btn = document.getElementById("fluxus-dre-refresh");
    if (btn) btn.textContent = "Calculando...";
    
    fetch(base + "/api/dre")
      .then(function (r) { return r.json(); })
      .then(function (d) {
        // Cards
        var elRev = document.getElementById("fluxus-dre-rev");
        var elTaxDir = document.getElementById("fluxus-dre-tax-dir");
        var elPay = document.getElementById("fluxus-dre-payroll");
        var elNet = document.getElementById("fluxus-dre-net");
        
        if (elRev) elRev.textContent = brl(d.revenue_gross);
        if (elTaxDir) elTaxDir.textContent = brl(d.taxes_direct);
        if (elPay) elPay.textContent = brl(d.opex_payroll);
        if (elNet) elNet.textContent = brl(d.net_income);
        
        // Table Rows
        document.getElementById("fluxus-dre-row-rev").textContent = brl(d.revenue_gross);
        document.getElementById("fluxus-dre-row-tax-dir").textContent = brl(d.taxes_direct);
        document.getElementById("fluxus-dre-row-payroll").textContent = brl(d.opex_payroll);
        document.getElementById("fluxus-dre-row-infra").textContent = brl(d.opex_infra);
        document.getElementById("fluxus-dre-row-ebitda").textContent = brl(d.ebitda);
        document.getElementById("fluxus-dre-row-tax-corp").textContent = brl(d.taxes_corporate);
        document.getElementById("fluxus-dre-row-net").textContent = brl(d.net_income);
        
        // Percentages
        var rev = d.revenue_gross || 1;
        document.getElementById("fluxus-dre-pct-payroll").textContent = ((d.opex_payroll / rev) * 100).toFixed(2) + "%";
        document.getElementById("fluxus-dre-pct-infra").textContent = ((d.opex_infra / rev) * 100).toFixed(2) + "%";
        document.getElementById("fluxus-dre-pct-ebitda").textContent = ((d.ebitda / rev) * 100).toFixed(2) + "%";
        document.getElementById("fluxus-dre-pct-net").textContent = ((d.net_income / rev) * 100).toFixed(2) + "%";
        
        if (btn) btn.textContent = "Atualizar DRE";
      })
      .catch(function () {
        if (btn) btn.textContent = "Erro na API";
      });
  }

  $(function () {
    var btnAgg = document.getElementById("fluxus-lp-agg-refresh");
    if (btnAgg) btnAgg.addEventListener("click", loadLpAggregates);
    
    var btnDre = document.getElementById("fluxus-dre-refresh");
    if (btnDre) btnDre.addEventListener("click", loadDre);

    $("#fluxus-tx-views .widget-menu-tab").on("click", "li", function () {
      var idx = $(this).index();
      if (idx === 1) loadLpAggregates();
      if (idx === 2) loadSummary();
      if (idx === 3) loadDre();
    });
  });
})();

