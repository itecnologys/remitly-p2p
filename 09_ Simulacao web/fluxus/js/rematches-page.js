/**
 * Rematches — dados do SQLite via server_sim.py (mesma origem que o Excel/CSV).
 * Abrir site em http://127.0.0.1:8787/ para API funcionar.
 */
(function () {
  "use strict";

  function apiBase() {
    if (window.FLUXUS_API_BASE !== undefined && window.FLUXUS_API_BASE !== null && window.FLUXUS_API_BASE !== "") {
      return String(window.FLUXUS_API_BASE).replace(/\/$/, "");
    }
    if (window.location.protocol === "file:") {
      return "";
    }
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

  var state = { page: 1, limit: 25, lp: "" };

  function fillLpFilter(rows) {
    var sel = document.getElementById("fluxus-lp-filter");
    if (!sel || sel.dataset.filled) return;
    rows.forEach(function (r) {
      var o = document.createElement("option");
      o.value = r.lp_id;
      o.textContent = r.lp_id + " — " + (r.nome_completo || "");
      sel.appendChild(o);
    });
    sel.dataset.filled = "1";
  }

  function loadLps() {
    var base = apiBase();
    if (!base) return Promise.resolve();
    return fetch(base + "/api/lps")
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        fillLpFilter(j.rows || []);
      })
      .catch(function () {});
  }

  function renderRows(rows) {
    var tb = document.getElementById("fluxus-rm-tbody");
    if (!tb) return;
    tb.innerHTML = "";
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td class=\"f12-medium\">" +
        (r.rematch_id || "") +
        "</td><td class=\"f12-medium\">" +
        (r.timestamp_remessa_iso || "") +
        "</td><td class=\"f12-medium\">" +
        (r.lp_nome || "") +
        "</td><td class=\"f12-medium text-end\">" +
        brl(r.inicio_pool_com_lucro_rolado_brl) +
        "</td><td class=\"f12-medium text-end\">" +
        brl(r.gtv_brl) +
        "</td><td class=\"f12-medium text-end\">" +
        brl(r.total_taxas_trilho_brl) +
        "</td><td class=\"f12-medium text-end\">" +
        brl(r.lp_spread_retorno_brl) +
        "</td><td class=\"f12-medium text-end\">" +
        brl(r.valor_final_rolagem_brl) +
        "</td><td><button type=\"button\" class=\"btn btn-sm btn-outline-primary fluxus-status-btn\" data-id=\"" +
        (r.rematch_id || "") +
        "\">Status</button></td>";
      tb.appendChild(tr);
    });
    document.querySelectorAll(".fluxus-status-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        openModal(btn.getAttribute("data-id"));
      });
    });
  }

  function renderPager(total, page, limit) {
    var ul = document.getElementById("fluxus-rm-pager");
    if (!ul) return;
    ul.innerHTML = "";
    var pages = Math.max(1, Math.ceil(total / limit));
    for (var p = 1; p <= Math.min(pages, 200); p++) {
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
          loadRematches();
        });
        li.appendChild(a);
        ul.appendChild(li);
      })(p);
    }
  }

  function loadRematches() {
    var base = apiBase();
    var meta = document.getElementById("fluxus-rm-meta");
    if (!base) {
      if (meta) {
        meta.textContent =
          "Abra esta página via servidor local (python server_sim.py em 127.0.0.1:8787) para carregar os 84k rematches.";
      }
      return;
    }
    var u =
      base +
      "/api/rematches?page=" +
      state.page +
      "&limit=" +
      state.limit +
      (state.lp ? "&lp_id=" + encodeURIComponent(state.lp) : "");
    fetch(u)
      .then(function (r) {
        return r.json();
      })
      .then(function (j) {
        if (meta) {
          meta.textContent =
            "Total de linhas: " +
            j.total +
            " — página " +
            j.page +
            " — indicadores por linha alinhados ao CSV oficial.";
        }
        renderRows(j.rows || []);
        renderPager(j.total || 0, j.page || 1, j.limit || state.limit);
      })
      .catch(function () {
        if (meta) meta.textContent = "Falha ao contactar API (servidor parado?).";
      });
  }

  function openModal(rid) {
    var base = apiBase();
    if (!base || !rid) return;
    fetch(base + "/api/rematch/" + encodeURIComponent(rid))
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        var body = document.getElementById("fluxusStatusModalBody");
        if (!body) return;
        var keys = Object.keys(d).sort();
        var html = "<p class=\"f14-regular\">" + (d.status_explicacao_pt || "") + "</p>";
        html += "<dl class=\"row mb-0 small\">";
        keys.forEach(function (k) {
          if (k.indexOf("status_explicacao") >= 0) return;
          var v = d[k];
          if (typeof v === "number") v = String(v);
          html += "<dt class=\"col-sm-4\">" + k + "</dt><dd class=\"col-sm-8 text-break\">" + (v == null ? "" : v) + "</dd>";
        });
        html += "</dl>";
        body.innerHTML = html;
        var title = document.getElementById("fluxusStatusModalLabel");
        if (title) title.textContent = "Trilho — " + rid;
        var el = document.getElementById("fluxusStatusModal");
        if (typeof bootstrap !== "undefined" && el) {
          var modal = new bootstrap.Modal(el);
          modal.show();
        } else if (el) {
          el.classList.add("show");
          el.style.display = "block";
        }
      })
      .catch(function () {});
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.getElementById("fluxus-rm-table")) return;
    loadLps().then(function () {
      loadRematches();
    });
    var rf = document.getElementById("fluxus-rm-refresh");
    if (rf) rf.addEventListener("click", function () {
      state.page = 1;
      loadRematches();
    });
    var sf = document.getElementById("fluxus-lp-filter");
    if (sf) {
      sf.addEventListener("change", function () {
        state.lp = sf.value;
        state.page = 1;
        loadRematches();
      });
    }
  });
})();
