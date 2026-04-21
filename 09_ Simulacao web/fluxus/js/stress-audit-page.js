/**
 * Visões do log de stress Power BI (DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv via fluxus_stress.db).
 */
(function () {
  "use strict";

  var chartMonthly = null;

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

  function setErr(msg) {
    var el = document.getElementById("fluxus-stress-err");
    if (el) el.textContent = msg || "";
  }

  function loadSummary() {
    var base = apiBase();
    if (!base) return;
    fetch(base + "/api/stress/summary")
      .then(function (r) {
        if (r.status === 503) throw new Error("missing_db");
        return r.json();
      })
      .then(function (s) {
        setErr("");
        var map = [
          ["fluxus-stress-kpi-rows", intFmt(s.n_rows)],
          ["fluxus-stress-kpi-gtv", brl(s.sum_gtv)],
          ["fluxus-stress-kpi-spread", brl(s.sum_spread)],
          ["fluxus-stress-kpi-lp", brl(s.sum_lp_profit)],
          ["fluxus-stress-kpi-fluxus-fee", brl(s.sum_fluxus_fee)],
          ["fluxus-stress-kpi-vasp", brl(s.sum_vasp_fee)],
          ["fluxus-stress-kpi-pool", brl(s.sum_pool)],
          ["fluxus-stress-kpi-opex", brl((Number(s.sum_dock) || 0) + (Number(s.sum_gas) || 0))],
          ["fluxus-stress-kpi-net-fluxus", brl(s.sum_net_fluxus_margin)],
        ];
        map.forEach(function (pair) {
          var el = document.getElementById(pair[0]);
          if (el) el.textContent = pair[1];
        });
      })
      .catch(function (e) {
        if (e && e.message === "missing_db") {
          setErr("Base stress ausente. Na raiz do repo: python 05_SCRIPTS/SCRIPT_BUILD_STRESS_AUDIT_DB.py");
        } else {
          setErr("Falha ao ler /api/stress/summary (servidor em 127.0.0.1:8787?)");
        }
      });
  }

  function renderMonthlyChart(rows) {
    var el = document.querySelector("#fluxus-stress-chart-monthly");
    if (!el || typeof ApexCharts === "undefined") return;
    var cats = rows.map(function (r) {
      return "Mês " + r.month;
    });
    var gtv = rows.map(function (r) {
      return Number(r.sum_gtv) || 0;
    });
    var margin = rows.map(function (r) {
      return Number(r.sum_net_fluxus_margin) || 0;
    });
    var isDark = document.body.getAttribute('data-theme') === 'dark-institutional';
    var opts = {
      chart: { 
        height: 350, 
        type: "area", 
        toolbar: { show: false }, 
        zoom: { enabled: false },
        foreColor: isDark ? '#94A3B8' : '#64748B',
        background: 'transparent'
      },
      colors: ["#10B981", "#94A3B8"], // Emerald Green and Slate
      dataLabels: { enabled: false },
      stroke: { curve: "smooth", width: 3 },
      series: [
        { name: "Global GTV (BRL)", data: gtv },
        { name: "Net Protocol Margin (BRL)", data: margin },
      ],
      xaxis: { 
        categories: cats, 
        axisBorder: { show: false },
        axisTicks: { show: false }
      },
      yaxis: { 
        labels: { formatter: function (v) { return brl(v); } } 
      },
      legend: { position: "top", horizontalAlign: 'right' },
      fill: {
        type: "gradient",
        gradient: { 
            shadeIntensity: 1, 
            opacityFrom: 0.4, 
            opacityTo: 0.1, 
            stops: [0, 90, 100] 
        },
      },
      grid: {
        borderColor: isDark ? '#1E293B' : '#E2E8F0',
        strokeDashArray: 4
      },
      tooltip: {
        theme: isDark ? 'dark' : 'light'
      }
    };
    if (chartMonthly) {
      chartMonthly.destroy();
      chartMonthly = null;
    }
    chartMonthly = new ApexCharts(el, opts);
    chartMonthly.render();
  }

  function loadByMonth() {
    var base = apiBase();
    var tb = document.getElementById("fluxus-stress-month-tbody");
    if (!base || !tb) return;
    fetch(base + "/api/stress/by_month")
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        var rows = j.rows || [];
        tb.innerHTML = "";
        rows.forEach(function (r) {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            r.month +
            "</td><td class=\"text-end\">" +
            intFmt(r.n_rows) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_gtv) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_spread) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_lp_profit) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_net_fluxus_margin) +
            "</td>";
          tb.appendChild(tr);
        });
        renderMonthlyChart(rows);
      })
      .catch(function () {});
  }

  function fillLpFilter(rows) {
    var sel = document.getElementById("fluxus-stress-rows-lp");
    if (!sel || sel.dataset.filled) return;
    rows.forEach(function (r) {
      var o = document.createElement("option");
      o.value = r.lp_id || "";
      o.textContent = r.lp_id || "";
      sel.appendChild(o);
    });
    sel.dataset.filled = "1";
  }

  function loadByLp() {
    var base = apiBase();
    var tb = document.getElementById("fluxus-stress-lp-tbody");
    if (!base || !tb) return;
    fetch(base + "/api/stress/by_lp")
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        var rows = j.rows || [];
        fillLpFilter(rows);
        tb.innerHTML = "";
        rows.forEach(function (r) {
          var tr = document.createElement("tr");
          tr.innerHTML =
            "<td>" +
            (r.lp_id || "") +
            "</td><td class=\"text-end\">" +
            intFmt(r.n_rows) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_gtv) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_spread) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_lp_profit) +
            "</td><td class=\"text-end\">" +
            brl(r.sum_net_fluxus_margin) +
            "</td>";
          tb.appendChild(tr);
        });
      })
      .catch(function () {});
  }

  var state = { page: 1, limit: 30, lp: "", month: "" };

  function renderRowsPager(total, page, limit) {
    var ul = document.getElementById("fluxus-stress-pager");
    if (!ul) return;
    ul.innerHTML = "";
    var pages = Math.max(1, Math.ceil(total / limit));
    for (var p = 1; p <= Math.min(pages, 80); p++) {
      (function (pg) {
        var li = document.createElement("li");
        li.className = "page-item" + (pg === page ? " active" : "");
        var a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";
        a.textContent = String(pg);
        a.addEventListener("click", function (ev) {
          ev.preventDefault();
          state.page = pg;
          loadRows();
        });
        li.appendChild(a);
        ul.appendChild(li);
      })(p);
    }
  }

  function loadRows() {
    var base = apiBase();
    var tb = document.getElementById("fluxus-stress-rows-tbody");
    var meta = document.getElementById("fluxus-stress-rows-meta");
    if (!base || !tb) return;
    var q =
      "?page=" +
      state.page +
      "&limit=" +
      state.limit +
      (state.lp ? "&lp_id=" + encodeURIComponent(state.lp) : "") +
      (state.month ? "&month=" + encodeURIComponent(state.month) : "");
    fetch(base + "/api/stress/rows" + q)
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        tb.innerHTML = "";
        (j.rows || []).forEach(function (r) {
          var tr = document.createElement("tr");
          tr.style.cursor = "pointer";
          tr.dataset.kyc = JSON.stringify(r);
          tr.innerHTML =
            "<td>" +
            r.id +
            "</td><td>" +
            r.month +
            "/" +
            r.day +
            "</td><td>" +
            (r.lp_id || "") +
            "</td><td>" +
            (r.cycle_num != null ? r.cycle_num : "") +
            "</td><td class=\"text-end\">" +
            brl(r.principal_capital) +
            "</td><td class=\"text-end\">" +
            brl(r.transaction_value) +
            "</td><td class=\"text-end\">" +
            brl(r.total_spread) +
            "</td><td class=\"text-end\">" +
            brl(r.lp_profit) +
            "</td><td class=\"text-end\">" +
            brl(r.net_fluxus_margin) +
            "</td>";
          
          tr.addEventListener("click", function() {
              openKycModal(JSON.parse(this.dataset.kyc));
          });
          tb.appendChild(tr);
        });
        if (meta) meta.textContent = "Total " + intFmt(j.total) + " linhas";
        renderRowsPager(j.total, j.page, j.limit);
      })
      .catch(function () {});
  }

  var AUDIT_DATA = {
    "rows": {
      "title": "Linhas (Rematches)",
      "formula": "COUNT(*) OVER stress_audit",
      "desc": "Quantidade total de transações únicas (matchings) auditadas no Ledger. Cada linha representa um ciclo de compra e recompra de liquidez."
    },
    "gtv": {
      "title": "GTV (Total Transacionado)",
      "formula": "SUM(transaction_value) BRL",
      "desc": "Volume Bruto Transacionado (Gross Transaction Volume). É o somatório de todo o capital principal movimentado pelos 100 LPs ao longo da série temporal."
    },
    "spread": {
      "title": "Protocol Spread",
      "formula": "Yield Optimization",
      "desc": "O diferencial competitivo da FLUXUS no mercado institucional. Utilizamos um algoritmo de precificação dinâmica que garante o equilíbrio entre liquidez imediata e rentabilidade sustentável para grandes volumes."
    },
    "lp": {
      "title": "LP Yield",
      "formula": "Direct Profit Share",
      "desc": "A rentabilidade direta entregue aos provedores de liquidez. Corresponde à captura de valor sobre o volume transacionado, garantindo um retorno competitivo sobre o capital provido na esteira."
    },
    "fluxus-fee": {
      "title": "FLUXUS Fees",
      "formula": "Protocol Orchestration",
      "desc": "Receita de orquestração da plataforma. Representa a captura da FLUXUS para manutenção do motor de matching e gestão do pipeline global de liquidez."
    },
    "vasp": {
      "title": "Network Costs",
      "formula": "Settlement Layer",
      "desc": "Custos de rede e manutenção associados aos provedores de infraestrutura responsáveis pela custódia e trilhos de liquidação."
    },
    "pool": {
      "title": "Liquidity Reserve",
      "formula": "Guaranteed Liquidity",
      "desc": "Reserva de segurança para liquidez instantânea. Garante a prontidão do sistema para remessas de alta prioridade e volume institucional."
    },
    "opex": {
      "title": "OPEX (Gas + Dock)",
      "formula": "SUM(dock_reload + blockchain_gas)",
      "desc": "Custos variáveis de manutenção do trilho. Inclui taxas de rede (Gas) e o custo financeiro de recarga dos silos de liquidez (Dock)."
    },
    "net-fluxus": {
      "title": "Margem Líquida Operacional",
      "formula": "Receita Fluxus - OPEX (Direct)",
      "desc": "<b>EBITDA Operacional da Transação.</b> Resultado líquido das operações antes da dedução de folha de pagamento administrativa e impostos corporativos."
    }
  };

  function openAuditModal(id) {
    var d = AUDIT_DATA[id];
    if (!d) return;
    document.getElementById("auditTitle").textContent = d.title;
    document.getElementById("auditFormula").textContent = d.formula;
    document.getElementById("auditDesc").innerHTML = d.desc;
    var modal = new bootstrap.Modal(document.getElementById('auditModal'));
    modal.show();
  }

  function openKycModal(r) {
    document.getElementById("kyc-rematch-id").textContent = "#" + r.id;
    document.getElementById("kyc-sender-name").textContent = r.sender_name || "—";
    document.getElementById("kyc-sender-country").textContent = r.sender_country || "—";
    document.getElementById("kyc-sender-id").textContent = r.sender_id || "—";
    document.getElementById("kyc-sender-bank").textContent = r.sender_bank || "—";
    document.getElementById("kyc-sender-address").textContent = r.sender_address || "—";
    document.getElementById("kyc-sender-card").textContent = (r.sender_card_bin || "000000") + "XXXXXX";
    
    document.getElementById("kyc-recipient-name").textContent = r.recipient_name || "—";
    document.getElementById("kyc-recipient-type").textContent = r.recipient_type || "—";
    document.getElementById("kyc-recipient-id").textContent = r.recipient_id || "—";
    document.getElementById("kyc-recipient-bank").textContent = r.recipient_bank || "—";
    document.getElementById("kyc-recipient-sector").textContent = r.recipient_sector || "—";
    
    document.getElementById("kyc-purpose").textContent = r.remittance_purpose || "Family Support";
    document.getElementById("kyc-status").textContent = r.kyc_status || "VERIFIED";
    document.getElementById("kyc-ptax").textContent = r.usd_brl_ptax_mid ? ("R$ " + Number(r.usd_brl_ptax_mid).toFixed(4)) : "—";
    
    var modal = new bootstrap.Modal(document.getElementById('kycModal'));
    modal.show();
  }

  $(function () {
    loadSummary();
    loadByMonth();
    loadByLp();
    loadRows();

    $("#fluxus-stress-views .widget-menu-tab").on("click", "li", function () {
      var idx = $(this).index();
      if (idx === 0) {
        loadSummary();
        loadByMonth();
      }
      if (idx === 1) loadByMonth();
      if (idx === 2) loadByLp();
      if (idx === 3) loadRows();
    });

    // Event listener para os cards de auditoria
    $(document).on("click", ".audit-card", function() {
      var id = $(this).data("kpi");
      openAuditModal(id);
    });

    var rf = document.getElementById("fluxus-stress-rows-refresh");
    if (rf) rf.addEventListener("click", loadRows);
    var sf = document.getElementById("fluxus-stress-rows-lp");
    if (sf) sf.addEventListener("change", function () {
      state.lp = sf.value || "";
      state.page = 1;
      loadRows();
    });
    var mf = document.getElementById("fluxus-stress-rows-month");
    if (mf) mf.addEventListener("change", function () {
      state.month = mf.value || "";
      state.page = 1;
      loadRows();
    });
  });
})();
