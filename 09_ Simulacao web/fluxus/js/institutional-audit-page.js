/**
 * FLUXUS — Institutional Profitability Analysis (JS Engine)
 * Handles multidimensional filtering and hierarchical DRE rendering.
 */
(function () {
    "use strict";

    let chartWaterfall = null;
    let state = {
        month: "",
        region: "",
        sector: "",
        lp: ""
    };

    function brl(n) {
        let x = Number(n);
        if (isNaN(x)) return "R$ 0,00";
        return x.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
    }

    function pct(n) {
        let x = Number(n);
        if (isNaN(x)) return "0.00%";
        return x.toFixed(2) + "%";
    }

    async function loadFilters() {
        try {
            const r = await fetch("/api/stress/filters");
            const data = await r.json();
            
            const selRegion = document.getElementById("filter-region");
            const selSector = document.getElementById("filter-sector");
            const selLp = document.getElementById("filter-lp");

            data.regions.forEach(v => selRegion.add(new Option(v, v)));
            data.sectors.forEach(v => selSector.add(new Option(v, v)));
            data.lps.forEach(v => selLp.add(new Option(v, v)));
        } catch (e) {
            console.error("Failed to load filters", e);
        }
    }

    async function loadDRE() {
        const query = new URLSearchParams(state).toString();
        try {
            const r = await fetch(`/api/institutional/dre?${query}`);
            const d = await r.json();
            renderDRE(d);
            renderWaterfall(d);
            updateKPIs(d);
        } catch (e) {
            console.error("Failed to load DRE", e);
        }
    }

    function renderDRE(d) {
        const tbody = document.getElementById("dre-body");
        tbody.innerHTML = "";

        const rows = [
            { type: "main", label: "RECEITA BRUTA (SPREAD CAPTURADO)", val: d.revenue.total, pct: (d.revenue.total/d.gtv*100) },
            { type: "sub", label: "Yield de Orquestração Protocolar", val: d.revenue.orchestration_fee, pct: (d.revenue.orchestration_fee/d.gtv*100), indent: 1 },
            
            { type: "main", label: "(-) CUSTO DE TRANSACIONAL (COGS)", val: -d.cogs.total, pct: (-d.cogs.total/d.gtv*100) },
            { type: "sub", label: "LP Profit Share (Yield Gerado)", val: -d.cogs.lp_share, pct: (-d.cogs.lp_share/d.gtv*100), indent: 1 },
            { type: "sub", label: "Taxas de Rede Settlement (VASP)", val: -d.cogs.network_vasp, pct: (-d.cogs.network_vasp/d.gtv*100), indent: 1 },
            
            { type: "total", label: "(=) MARGEM BRUTA", val: d.gross_margin, pct: (d.gross_margin/d.gtv*100) },
            
            { type: "main", label: "(-) DESPESAS OPERACIONAIS (OPEX)", val: -d.opex.total, pct: (-d.opex.total/d.gtv*100) },
            { type: "sub", label: "Blockchain Gas (Settlement Layer)", val: -d.opex.blockchain_gas, pct: (-d.opex.blockchain_gas/d.gtv*100), indent: 1 },
            { type: "sub", label: "Dock Reloads (Liquidity Maintenance)", val: -d.opex.liquidity_dock, pct: (-d.opex.liquidity_dock/d.gtv*100), indent: 1 },
            { type: "sub", label: "Compliance & AML Outsourcing (5bps)", val: -d.opex.compliance_aml, pct: (-d.opex.compliance_aml/d.gtv*100), indent: 1 },
            { type: "sub", label: "Payroll Est. (Admin & Core Team)", val: -d.opex.payroll_est, pct: (-d.opex.payroll_est/d.gtv*100), indent: 1 },
            { type: "sub", label: "Infra & SaaS (Cloud/Office)", val: -d.opex.infra_est, pct: (-d.opex.infra_est/d.gtv*100), indent: 1 },
            
            { type: "total", label: "(=) EBITDA OPERACIONAL SIMULADO", val: d.ebitda, pct: (d.ebitda/d.gtv*100) },
            
            { type: "main", label: "(-) IMPOSTO DE RENDA (EST. PRESUMIDO)", val: -d.taxes, pct: (-d.taxes/d.gtv*100) },
            { type: "total", label: "(=) LUCRO LÍQUIDO DA OPERAÇÃO", val: d.net_income, pct: (d.net_income/d.gtv*100) }
        ];

        rows.forEach(r => {
            const tr = document.createElement("tr");
            tr.className = `dre-row dre-row-${r.type}`;
            
            const colorClass = r.val < 0 ? "text-danger" : (r.type === "total" ? "text-success" : "");
            const indentClass = r.indent ? `dre-indent-${r.indent}` : "";

            tr.innerHTML = `
                <td class="dre-cell dre-label-cell ${indentClass}">
                    ${r.indent ? "" : "<div class='dre-expander'></div>"}
                    ${r.label}
                </td>
                <td class="dre-cell dre-value ${colorClass}">${brl(Math.abs(r.val))}</td>
                <td class="dre-cell dre-pct">${pct(Math.abs(r.pct))}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderWaterfall(d) {
        const el = document.getElementById("chart-waterfall");
        if (!el) return;
        const options = {
            series: [{
                data: [
                    { x: 'Revenue', y: Math.round(d.revenue.total) },
                    { x: 'COGS', y: Math.round(-d.cogs.total) },
                    { x: 'Margin', y: Math.round(d.gross_margin) },
                    { x: 'OPEX', y: Math.round(-d.opex.total) },
                    { x: 'Taxes', y: Math.round(-d.taxes) },
                    { x: 'Net', y: Math.round(d.net_income) }
                ]
            }],
            chart: { 
                type: 'bar', 
                height: 350, 
                toolbar: { show: false }, 
                background: 'transparent',
                foreColor: '#94A3B8'
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '60%',
                    colors: {
                        ranges: [
                            { from: -1000000000, to: 0, color: '#EF4444' },
                            { from: 1, to: 1000000000, color: '#10B981' }
                        ]
                    }
                }
            },
            dataLabels: { 
                enabled: true, 
                formatter: function(val) { return (val / 1e6).toFixed(1) + 'M'; },
                style: { fontSize: '10px', colors: ['#fff'] } 
            },
            theme: { mode: 'dark' },
            xaxis: { axisBorder: { show: false }, axisTicks: { show: false } },
            yaxis: { show: false },
            grid: { borderColor: '#334155', strokeDashArray: 4 }
        };

        if (chartWaterfall) chartWaterfall.destroy();
        chartWaterfall = new ApexCharts(el, options);
        chartWaterfall.render();
    }

    function updateKPIs(d) {
        document.getElementById("kpi-gtv").textContent = brl(d.gtv);
        document.getElementById("kpi-take-rate").textContent = d.metrics.take_rate_bps.toFixed(2) + " bps";
        
        const statusEl = document.getElementById("kpi-status");
        if (d.net_income > 0) {
            statusEl.textContent = "HEALTHY";
            statusEl.className = "data-pill text-success";
        } else {
            statusEl.textContent = "CRITICAL";
            statusEl.className = "data-pill text-danger";
        }
    }

    // Event Listeners
    document.getElementById("apply-filters").addEventListener("click", () => {
        state.month = document.getElementById("filter-month").value;
        state.region = document.getElementById("filter-region").value;
        state.sector = document.getElementById("filter-sector").value;
        state.lp = document.getElementById("filter-lp").value;
        loadDRE();
    });

    document.getElementById("reset-filters").addEventListener("click", () => {
        document.getElementById("filter-month").value = "";
        document.getElementById("filter-region").value = "";
        document.getElementById("filter-sector").value = "";
        document.getElementById("filter-lp").value = "";
        state = { month: "", region: "", sector: "", lp: "" };
        loadDRE();
    });

    $(function () {
        loadFilters();
        loadDRE();
    });

})();
