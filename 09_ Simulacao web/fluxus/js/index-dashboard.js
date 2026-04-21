/**
 * Dashboard index.html — macros DRE/stress, oscilação PTAX, cartões Forex (séries),
 * listas compra/recompra por LP (04_PROCESS).
 */
(function () {
  "use strict";

  var charts = { c1: null, c2: null, c3: null, c4: null, deep: null, twoline: null };

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

  function fmt4(n) {
    var x = Number(n);
    if (Number.isNaN(x)) return "—";
    return x.toFixed(4);
  }

  function synthSeries(mids, anchor, scale) {
    var out = [];
    var v = anchor;
    out.push(v);
    for (var i = 1; i < mids.length; i++) {
      var dr = (mids[i] - mids[i - 1]) / (mids[i - 1] || 1);
      v = v * (1 + dr * scale);
      out.push(Math.round(v * 1e5) / 1e5);
    }
    if (mids.length === 0) return [];
    if (mids.length === 1) return [anchor];
    return out;
  }

  function sparkOpts(categories, series, name, color) {
    return {
      chart: { type: "area", height: 110, sparkline: { enabled: true }, animations: { enabled: false } },
      stroke: { width: 2, curve: "smooth" },
      fill: { type: "gradient", gradient: { shadeIntensity: 0.8, opacityFrom: 0.35, opacityTo: 0.05 } },
      colors: [color],
      series: [{ name: name, data: series }],
      xaxis: { categories: categories },
      tooltip: { enabled: true, x: { show: false } },
    };
  }

  function destroyChart(k) {
    if (charts[k]) {
      try {
        charts[k].destroy();
      } catch (e) {}
      charts[k] = null;
    }
  }

  function renderMacro(summary, stress, fx) {
    var gtv = document.getElementById("fluxus-dash-gtv");
    if (gtv) gtv.textContent = brl(summary.gtv_brl);
    var elN = document.getElementById("fluxus-dash-rematches");
    if (elN) elN.textContent = String(summary.rematches || "—");
    var elLp = document.getElementById("fluxus-dash-lps");
    if (elLp) elLp.textContent = String(summary.lp_distinct != null ? summary.lp_distinct : "—");
    var p = document.getElementById("fluxus-dash-ptax");
    if (p && summary.ptax_usd_brl_mid_media != null) {
      p.textContent = String(summary.ptax_usd_brl_mid_media) + " (média)";
    }
    var amp = document.getElementById("fluxus-dash-amplitude");
    if (amp && fx) amp.textContent = fx.amplitude_pct != null ? fmt4(fx.amplitude_pct) + " %" : "—";
    var sg = document.getElementById("fluxus-dash-sigma");
    if (sg && fx) sg.textContent = fx.ptax_sigma != null ? String(fx.ptax_sigma) : "—";
    var st = document.getElementById("fluxus-dash-stress-gtv");
    if (st) {
      if (stress && stress.sum_gtv != null) st.textContent = brl(stress.sum_gtv);
      else st.textContent = "—";
    }
    var osc = document.getElementById("fluxus-fx-oscillation");
    if (osc && fx) {
      osc.innerHTML =
        "<strong>Oscilação PTAX (período DRE)</strong> — observações: " +
        (fx.n_observacoes || "—") +
        "; mínimo " +
        fmt4(fx.ptax_min) +
        "; máximo " +
        fmt4(fx.ptax_max) +
        "; média " +
        fmt4(fx.ptax_avg) +
        "; desvio padrão " +
        (fx.ptax_sigma != null ? fx.ptax_sigma : "—") +
        "; amplitude relativa (máx−mín)/média: " +
        (fx.amplitude_pct != null ? fmt4(fx.amplitude_pct) : "—") +
        " %. Cruz EUR/USD/GBP/JPY nos cartões inferiores é <em>sintético</em> derivado da variação diária USD/BRL (ver nota no cartão).";
    }
  }

  function setCard(idx, label, head, sub, mids, synth, color) {
    var lb = document.getElementById("fluxus-fx-card-" + idx + "-label");
    var hd = document.getElementById("fluxus-fx-card-" + idx + "-head");
    var sb = document.getElementById("fluxus-fx-card-" + idx + "-sub");
    if (lb) lb.textContent = label;
    if (hd) hd.textContent = head;
    if (sb) sb.textContent = sub;
    var el = document.querySelector("#small-chart-" + idx);
    if (!el || typeof ApexCharts === "undefined") return;
    var cats = mids.map(function (_, i) {
      return String(i + 1);
    });
    var data = synth ? synth : mids;
    destroyChart("c" + idx);
    charts["c" + idx] = new ApexCharts(el, sparkOpts(cats, data, label, color));
    charts["c" + idx].render();
  }

  function renderFxCards(dailyRows, fx) {
    var mids = dailyRows.map(function (r) {
      return r.mid;
    });
    if (mids.length === 0) return;
    var lo = Math.min.apply(null, mids);
    var hi = Math.max.apply(null, mids);
    var vol = hi - lo;
    var isDark = document.body.getAttribute('data-theme') === 'dark-institutional';
    setCard(
      1,
      "USD/BRL (PTAX BCB)",
      fmt4(fx.ptax_avg),
      "Δ período " + fmt4(vol) + " (" + (fx.amplitude_pct != null ? fmt4(fx.amplitude_pct) + "% amp." : "") + ")",
      mids,
      mids,
      "#10B981"
    );
    var eur = synthSeries(mids, 1.087, 0.45);
    var eurVol = Math.max.apply(null, eur) - Math.min.apply(null, eur);
    setCard(2, "EUR/USD *", fmt4(eur[eur.length - 1]), "Δ sintético " + fmt4(eurVol), mids, eur, "#64748B");
    var gbp = synthSeries(mids, 1.267, 0.38);
    var gbpVol = Math.max.apply(null, gbp) - Math.min.apply(null, gbp);
    setCard(3, "GBP/USD *", fmt4(gbp[gbp.length - 1]), "Δ sintético " + fmt4(gbpVol), mids, gbp, "#10B981");
    var jpy = synthSeries(mids, 149.5, 0.62);
    var jpyVol = Math.max.apply(null, jpy) - Math.min.apply(null, jpy);
    setCard(4, "USD/JPY *", fmt4(jpy[jpy.length - 1]), "Δ sintético " + fmt4(jpyVol), mids, jpy, "#34D399");
  }

  function renderDeepChart(dailyRows) {
    var el = document.getElementById("fluxus-ptax-deep-chart");
    if (!el || typeof ApexCharts === "undefined") return;
    var cats = dailyRows.map(function (r) {
      return r.d;
    });
    var mids = dailyRows.map(function (r) {
      return r.mid;
    });
    var ma = [];
    for (var i = 0; i < mids.length; i++) {
      var a = mids[Math.max(0, i - 2)];
      var b = mids[i];
      var c2 = mids[Math.min(mids.length - 1, i + 2)];
      ma.push(Math.round(((a + b + c2) / 3) * 1e4) / 1e4);
    }
    var isDark = document.body.getAttribute('data-theme') === 'dark-institutional';
    destroyChart("deep");
    charts.deep = new ApexCharts(el, {
      chart: { 
        type: "area", 
        height: 320, 
        toolbar: { show: false }, 
        zoom: { enabled: true },
        foreColor: isDark ? '#94A3B8' : '#64748B',
        background: 'transparent'
      },
      dataLabels: { enabled: false },
      stroke: { curve: "smooth", width: [3, 2] },
      colors: ["#10B981", "#64748B"],
      series: [
        { name: "PTAX médio/dia", data: mids },
        { name: "Média móvel (3d)", data: ma },
      ],
      xaxis: { 
        categories: cats, 
        labels: { rotate: -45, style: { fontSize: "10px" } },
        axisBorder: { show: false },
        axisTicks: { show: false }
      },
      yaxis: { labels: { formatter: function (v) {
        return fmt4(v);
      } } },
      legend: { position: "top" },
      fill: { type: "gradient", gradient: { opacityFrom: 0.35, opacityTo: 0.05 } },
      grid: {
        borderColor: isDark ? '#1E293B' : '#E2E8F0',
        strokeDashArray: 4
      },
      tooltip: { theme: isDark ? 'dark' : 'light' }
    });
    charts.deep.render();
  }

  function renderTwoline(dailyRows) {
    var el = document.getElementById("line-chart-twoline");
    if (!el || typeof ApexCharts === "undefined") return;
    var cats = dailyRows.map(function (r) {
      return r.d;
    });
    var mids = dailyRows.map(function (r) {
      return r.mid;
    });
    destroyChart("twoline");
    charts.twoline = new ApexCharts(el, {
      chart: { type: "line", height: 280, toolbar: { show: false } },
      stroke: { width: [3, 2], curve: "smooth" },
      colors: ["#FFFFFF", "#C0FAA0"],
      series: [
        { name: "USD/BRL PTAX", data: mids },
        { name: "Envelope ±0,15%", data: mids.map(function (m) {
          return Math.round(m * 1.0015 * 1e4) / 1e4;
        }) },
      ],
      xaxis: { categories: cats, labels: { style: { colors: "#E0E0E0" } } },
      yaxis: { labels: { style: { colors: "#E0E0E0" }, formatter: function (v) {
        return fmt4(v);
      } } },
      legend: { labels: { colors: "#F8F8F8" } },
      grid: { borderColor: "rgba(255,255,255,0.1)" },
    });
    charts.twoline.render();
  }

  function fillMatchTables(rows) {
    var tbC = document.getElementById("fluxus-match-compra-body");
    var tbR = document.getElementById("fluxus-match-recompra-body");
    if (!tbC || !tbR) return;
    tbC.innerHTML = "";
    tbR.innerHTML = "";
    rows.forEach(function (r) {
      var trc = document.createElement("tr");
      trc.innerHTML =
        "<td class=\"f14-regular\">" +
        (r.lp_id || "") +
        "</td><td class=\"f14-regular\">" +
        (r.rematch_id || "") +
        "</td><td class=\"f14-regular\">" +
        (r.timestamp_remessa_iso || "") +
        "</td><td class=\"f14-regular text-end\">" +
        brl(r.compra_brl) +
        "</td>";
      tbC.appendChild(trc);
      var trr = document.createElement("tr");
      trr.innerHTML =
        "<td class=\"f14-regular\">" +
        (r.lp_id || "") +
        "</td><td class=\"f14-regular\">" +
        (r.rematch_recompra || "") +
        "</td><td class=\"f14-regular\">" +
        (r.ts_recompra || "") +
        "</td><td class=\"f14-regular text-end\">" +
        brl(r.recompra_brl) +
        "</td>";
      tbR.appendChild(trr);
    });
  }

  function jget(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    });
  }

  function jgetNull(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) return null;
      return r.json();
    });
  }

  $(function () {
    var base = apiBase();
    if (!base) return;
    Promise.all([
      jget(base + "/api/summary"),
      jget(base + "/api/fx/ptax_stats"),
      jget(base + "/api/fx/ptax_daily"),
      jget(base + "/api/index/lp_match_pairs?limit=36"),
      jgetNull(base + "/api/stress/summary"),
    ])
      .then(function (parts) {
        var summary = parts[0];
        var fx = parts[1];
        var daily = parts[2];
        var pairs = parts[3];
        var stress = parts[4] && !parts[4].error ? parts[4] : null;
        renderMacro(summary, stress, fx);
        var rows = (daily && daily.rows) || [];
        renderFxCards(rows, fx);
        renderDeepChart(rows);
        renderTwoline(rows);
        fillMatchTables((pairs && pairs.rows) || []);
      })
      .catch(function () {});
  });
})();

