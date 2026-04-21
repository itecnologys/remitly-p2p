/**
 * FLUXUS — Premium Institutional Analytics Controller
 * Manages the high-fidelity data binding for the LP Dashboard.
 */

$(document).ready(function() {
    const API_BASE = ""; 
    let currentLpId = 'LP_043'; // Default Roberta

    // 1. Theme Configuration
    const initTheme = () => {
        const savedTheme = localStorage.getItem('fluxus-theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme === 'dark' ? 'dark-institutional' : 'light');
    };
    initTheme();

    $('#theme-institutional-toggle').on('click', function() {
        const current = document.body.getAttribute('data-theme');
        const next = current === 'dark-institutional' ? 'light' : 'dark-institutional';
        document.body.setAttribute('data-theme', next);
        localStorage.setItem('fluxus-theme', next === 'dark-institutional' ? 'dark' : 'light');
    });

    // 2. Fetch Initial Data
    fetch(`${API_BASE}/api/lps`)
        .then(res => res.json())
        .then(data => {
            const roberta = data.rows.find(r => r.lp_id === currentLpId);
            if (roberta) {
                $('#current-lp-id').text(`ID: ${currentLpId}`);
                loadDashboard(currentLpId);
            }
        });

    function loadDashboard(lpId) {
        currentLpId = lpId;
        
        // Parallel Data Fetching
        Promise.all([
            fetch(`${API_BASE}/api/lps/performance/${lpId}`).then(r => r.json()),
            fetch(`${API_BASE}/api/lps/activity/${lpId}?limit=10`).then(r => r.json()),
            fetch(`${API_BASE}/api/stress/rows?limit=10`).then(r => r.json()) // For Queue context
        ]).then(([perf, activity, queueData]) => {
            renderSummary(perf);
            renderQueue(lpId, queueData);
            renderActivity(activity.activity);
        });
    }

    function formatBRL(val) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
    }

    function renderSummary(data) {
        // Bento Box 1: Capital
        $('#val-lp-capital').text(formatBRL(data.current_capital));
        $('#val-lp-yield').text(formatBRL(data.total_yield || data.yearly.profit));

        // Bento Box 3: Fees & Margin (Simulated based on simulation rules)
        const totalProfit = data.daily.profit || 150.00;
        const gasCost = 12.50; // Standard simulated cost per loop
        const dockCost = 5.00; 
        const fluxusFee = totalProfit * 0.25;
        const netProfit = totalProfit - gasCost - dockCost - fluxusFee;

        $('#val-cost-dock').text(formatBRL(dockCost));
        $('#val-cost-gas').text(formatBRL(gasCost));
        $('#val-fluxus-fee').text(formatBRL(fluxusFee));
        $('#val-lp-net-profit').text(formatBRL(netProfit));

        // Tax Governance
        const giro = data.monthly_giro || 0;
        const limit = 35000;
        const pct = Math.min((giro / limit) * 100, 100).toFixed(0);
        
        $('#fiscal-giro-text').text(`Giro Mensal: ${formatBRL(giro)}`);
        $('#fiscal-giro-pct').text(`${pct}%`);
        $('#fiscal-giro-bar').css('width', `${pct}%`);
        
        const badge = $('#fiscal-status-badge');
        if (giro > limit) {
            badge.text('PROVISÃO IR ATIVA').css('background', 'var(--fluxus-danger)').css('color', 'white');
            $('#fiscal-giro-bar').css('background', 'var(--fluxus-danger)');
        } else {
            badge.text('ISENTO').css('background', 'var(--fluxus-success)').css('color', 'white');
            $('#fiscal-giro-bar').css('background', 'var(--fluxus-success)');
        }
    }

    function renderQueue(lpId, queueData) {
        const visualizer = $('#premium-queue-visualizer');
        visualizer.empty();

        // Simulate queue neighbors for the visual effect
        const randomNeighbors = ['LP_021', 'LP_088', 'LP_012', lpId, 'LP_099', 'LP_005', 'LP_077'];
        
        randomNeighbors.forEach(id => {
            const isActive = id === lpId;
            const label = isActive ? 'Roberta (EU)' : id;
            visualizer.append(`<div class="queue-node ${isActive ? 'active' : ''}">${label}</div>`);
        });

        if (queueData.rows && queueData.rows.length > 0) {
            $('#current-cycle-id').text(`Ciclo: RM-${queueData.rows[0].rematch_id}`);
        }
    }

    function renderActivity(activity) {
        const tbody = $('#lp-activity-tbody');
        tbody.empty();

        activity.forEach(item => {
            const isDebit = item.type === 'DEBIT';
            const colorClass = isDebit ? 'text-danger' : 'text-success';
            
            const tr = `
                <tr>
                    <td class="f11-regular text-muted">${item.date}</td>
                    <td class="f11-bold">#${Math.random().toString(36).substring(7).toUpperCase()}</td>
                    <td class="f12-medium">${item.label}</td>
                    <td>
                         ${item.queue_pos ? `<span class="data-pill bg-light">Fila #${item.queue_pos}</span>` : '--'}
                    </td>
                    <td class="text-end f12-bold">R$ ${Math.abs(item.amount).toLocaleString('pt-BR')}</td>
                    <td class="text-end f12-bold ${colorClass}">${isDebit ? '-' : '+'} R$ ${(Math.abs(item.amount) * 0.0108).toFixed(2)}</td>
                </tr>
            `;
            tbody.append(tr);
        });
    }
});
