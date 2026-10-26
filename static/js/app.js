/**
 * ApexGuard — Intelligent Transaction Anomaly & AML Platform
 * Frontend Logic with Lucide Icons, Clean White Charts, and Real-Time AI Inference
 */

// Application State
const state = {
    token: localStorage.getItem('apex_jwt_token') || null,
    user: JSON.parse(localStorage.getItem('apex_user') || '{"username": "admin", "role": "admin", "full_name": "Chief Compliance Officer"}'),
    activeView: 'dashboard-view',
    page: 1,
    pageSize: 15,
    riskFilter: 'ALL',
    searchQuery: '',
    selectedTxId: null,
    charts: {}
};

// Refresh Lucide Icons Helper
function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
    }
}

// ==========================================
// Toast Notifications
// ==========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast`;

    let iconName = 'info';
    let iconColor = '#a1a1aa';
    if (type === 'success') {
        iconName = 'check-circle-2';
        iconColor = '#16a34a';
    } else if (type === 'error') {
        iconName = 'alert-triangle';
        iconColor = '#ef4444';
    }

    toast.innerHTML = `<i data-lucide="${iconName}" style="color: ${iconColor}; width: 16px; height: 16px;"></i> <span>${message}</span>`;
    container.appendChild(toast);
    refreshIcons();

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 250);
    }, 4000);
}

// Dynamic API Base URL supporting local development, Render backend, or Vercel proxy
const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? ''
    : (localStorage.getItem('apex_api_url') || window.APEXGUARD_API_URL || '');

// ==========================================
// API Client
// ==========================================
async function apiCall(endpoint, options = {}) {
    const headers = options.headers || {};
    if (state.token) {
        headers['Authorization'] = `Bearer ${state.token}`;
    }

    const fullUrl = (endpoint.startsWith('http') || !API_BASE_URL)
        ? endpoint
        : `${API_BASE_URL}${endpoint}`;

    try {
        const response = await fetch(fullUrl, { ...options, headers });
        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: 'Server Error' }));
            throw new Error(err.detail || 'Request failed');
        }
        return await response.json();
    } catch (error) {
        console.error(`API Error on ${fullUrl}:`, error);
        throw error;
    }
}

// ==========================================
// Navigation & View Controller
// ==========================================
function initNavigation() {
    const navButtons = document.querySelectorAll('#main-nav .nav-item');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetView = btn.getAttribute('data-view');
            switchView(targetView);
        });
    });

    document.getElementById('btn-quick-scan-top')?.addEventListener('click', () => {
        switchView('scanner-view');
    });

    document.getElementById('btn-export-summary')?.addEventListener('click', () => {
        showToast('Generated executive AML audit summary report', 'success');
    });
}

function switchView(viewId) {
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('#main-nav .nav-item').forEach(btn => btn.classList.remove('active'));

    const targetSection = document.getElementById(viewId);
    const targetBtn = document.querySelector(`#main-nav .nav-item[data-view="${viewId}"]`);

    if (targetSection) targetSection.classList.add('active');
    if (targetBtn) targetBtn.classList.add('active');
    state.activeView = viewId;

    if (viewId === 'dashboard-view') loadDashboardStats();
    if (viewId === 'investigation-view') loadTransactionsTable();
    if (viewId === 'compliance-view' || viewId === 'models-view') loadModelInfo();

    refreshIcons();
}

// ==========================================
// Executive Dashboard Analytics (Clean White Design)
// ==========================================
async function loadDashboardStats() {
    try {
        const stats = await apiCall('/api/stats');
        const kpis = stats.kpis;

        document.getElementById('kpi-total-tx').textContent = Number(kpis.total_transactions).toLocaleString();
        document.getElementById('kpi-fraud-tx').textContent = Number(kpis.total_fraud_detected).toLocaleString();
        document.getElementById('kpi-fraud-rate').textContent = `${kpis.fraud_rate_pct}% Flagged`;
        document.getElementById('kpi-prevented-usd').textContent = `$${(kpis.prevented_loss_usd / 1000000).toFixed(1)}M`;
        document.getElementById('kpi-accuracy').textContent = `${kpis.model_accuracy_pct}%`;

        renderDashboardCharts(stats);
    } catch (err) {
        console.warn('Dashboard stats fallback:', err);
    }
}

function renderDashboardCharts(stats) {
    // 1. Hourly Trend Chart
    const trendCtx = document.getElementById('trendChart')?.getContext('2d');
    if (trendCtx) {
        if (state.charts.trend) state.charts.trend.destroy();

        const labels = stats.hourly_trends.map(h => h.step);
        const totals = stats.hourly_trends.map(h => h.total);
        const frauds = stats.hourly_trends.map(h => h.fraud);

        state.charts.trend = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Normal Transactions',
                        data: totals,
                        borderColor: '#09090b',
                        backgroundColor: 'rgba(9, 9, 11, 0.04)',
                        fill: true,
                        tension: 0.35,
                        borderWidth: 2,
                        pointRadius: 2
                    },
                    {
                        label: 'Anomalies Intercepted',
                        data: frauds,
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.08)',
                        fill: true,
                        tension: 0.35,
                        borderWidth: 2,
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#52525b', boxWidth: 12, font: { size: 11, family: 'Plus Jakarta Sans' } }
                    }
                },
                scales: {
                    x: { grid: { color: '#f4f4f5' }, ticks: { color: '#71717a', font: { size: 10 } } },
                    y: { grid: { color: '#f4f4f5' }, ticks: { color: '#71717a', font: { size: 10 } } }
                }
            }
        });
    }

    // 2. Risk Donut Chart
    const riskCtx = document.getElementById('riskDonutChart')?.getContext('2d');
    if (riskCtx) {
        if (state.charts.riskDonut) state.charts.riskDonut.destroy();

        const rDist = stats.risk_distribution;
        state.charts.riskDonut = new Chart(riskCtx, {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'Low Risk', 'Medium Risk', 'Critical Fraud'],
                datasets: [{
                    data: [rDist.NORMAL || 0, rDist.LOW || 0, rDist.MEDIUM || 0, rDist.CRITICAL || 0],
                    backgroundColor: ['#16a34a', '#2563eb', '#d97706', '#dc2626'],
                    borderColor: '#ffffff',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#52525b', font: { size: 11 } } }
                },
                cutout: '72%'
            }
        });
    }

    // 3. AML Rules Trigger Chart
    const rulesCtx = document.getElementById('rulesChart')?.getContext('2d');
    if (rulesCtx) {
        if (state.charts.rules) state.charts.rules.destroy();

        const rData = stats.rule_triggers;
        const keys = Object.keys(rData).map(k => k.replace(/_/g, ' '));
        const vals = Object.values(rData);

        state.charts.rules = new Chart(rulesCtx, {
            type: 'bar',
            data: {
                labels: keys,
                datasets: [{
                    label: 'Violations Flagged',
                    data: vals,
                    backgroundColor: '#18181b',
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: '#f4f4f5' }, ticks: { color: '#71717a' } },
                    y: { grid: { display: false }, ticks: { color: '#27272a', font: { size: 10, weight: 600 } } }
                }
            }
        });
    }

    // 4. Volume by Type Chart
    const typeCtx = document.getElementById('typeChart')?.getContext('2d');
    if (typeCtx) {
        if (state.charts.type) state.charts.type.destroy();

        const tData = stats.type_breakdown;
        state.charts.type = new Chart(typeCtx, {
            type: 'bar',
            data: {
                labels: tData.map(t => t.type),
                datasets: [{
                    label: 'Transactions',
                    data: tData.map(t => t.count),
                    backgroundColor: '#3f3f46',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#52525b' } },
                    y: { grid: { color: '#f4f4f5' }, ticks: { color: '#71717a' } }
                }
            }
        });
    }
}

// ==========================================
// Live Transaction Scanner & Gauge
// ==========================================
function initScanner() {
    initRiskGauge(0.02);

    // Presets
    document.getElementById('preset-normal')?.addEventListener('click', () => {
        setScannerInputs('PAYMENT', 45.00, 'C1829472', 3500.00, 3455.00, 'M9827461', 12000.00, 12045.00);
    });

    document.getElementById('preset-drain')?.addEventListener('click', () => {
        setScannerInputs('CASH_OUT', 120000.00, 'C9283741', 120000.00, 0.00, 'C8472910', 5000.00, 125000.00);
    });

    document.getElementById('preset-smurfing')?.addEventListener('click', () => {
        setScannerInputs('TRANSFER', 9850.00, 'C4729184', 25000.00, 15150.00, 'C7482910', 0.00, 9850.00);
    });

    document.getElementById('preset-large')?.addEventListener('click', () => {
        setScannerInputs('TRANSFER', 450000.00, 'C5829102', 800000.00, 350000.00, 'C9182741', 0.00, 450000.00);
    });

    // Form Submission
    document.getElementById('scanner-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            step: 1,
            type: document.getElementById('inp-type').value,
            amount: parseFloat(document.getElementById('inp-amount').value),
            nameOrig: document.getElementById('inp-orig').value,
            oldbalanceOrg: parseFloat(document.getElementById('inp-oldbalance-org').value),
            newbalanceOrig: parseFloat(document.getElementById('inp-newbalance-orig').value),
            nameDest: document.getElementById('inp-dest').value,
            oldbalanceDest: parseFloat(document.getElementById('inp-oldbalance-dest').value),
            newbalanceDest: parseFloat(document.getElementById('inp-newbalance-dest').value)
        };

        const btn = document.getElementById('btn-run-scanner');
        btn.innerHTML = `<i data-lucide="loader-2" class="animate-spin" style="width: 15px; height: 15px;"></i> Evaluating Risk...`;
        btn.disabled = true;
        refreshIcons();

        try {
            const res = await apiCall('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            updateScannerUI(res);
            showToast(`Evaluated ${res.transaction_id}: ${res.evaluation.risk_level}`, res.evaluation.is_fraud ? 'error' : 'success');
        } catch (err) {
            showToast(err.message, 'error');
        } finally {
            btn.innerHTML = `<i data-lucide="sparkles" style="width: 15px; height: 15px;"></i> Evaluate Transaction Risk`;
            btn.disabled = false;
            refreshIcons();
        }
    });
}

function setScannerInputs(type, amt, orig, oldO, newO, dest, oldD, newD) {
    document.getElementById('inp-type').value = type;
    document.getElementById('inp-amount').value = amt.toFixed(2);
    document.getElementById('inp-orig').value = orig;
    document.getElementById('inp-oldbalance-org').value = oldO.toFixed(2);
    document.getElementById('inp-newbalance-orig').value = newO.toFixed(2);
    document.getElementById('inp-dest').value = dest;
    document.getElementById('inp-oldbalance-dest').value = oldD.toFixed(2);
    document.getElementById('inp-newbalance-dest').value = newD.toFixed(2);
}

function initRiskGauge(val = 0.0) {
    const ctx = document.getElementById('riskGaugeChart')?.getContext('2d');
    if (!ctx) return;

    if (state.charts.gauge) state.charts.gauge.destroy();

    const percentage = Math.round(val * 100);
    const color = val >= 0.7 ? '#dc2626' : (val >= 0.4 ? '#d97706' : '#16a34a');

    state.charts.gauge = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [color, '#f4f4f5'],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: -90,
            cutout: '80%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { tooltip: { enabled: false } }
        }
    });
}

function updateScannerUI(data) {
    const ev = data.evaluation;
    initRiskGauge(ev.risk_score);

    const badge = document.getElementById('res-badge');
    badge.className = `badge badge-${ev.risk_level.toLowerCase()}`;
    badge.textContent = `${ev.risk_level} RISK (${Math.round(ev.risk_score * 100)}%)`;

    document.getElementById('res-composite-score').textContent = ev.risk_score.toFixed(2);
    document.getElementById('res-ml-score').textContent = ev.ml_score.toFixed(2);
    document.getElementById('res-rule-score').textContent = ev.rule_score.toFixed(2);

    const chipsContainer = document.getElementById('res-rule-chips');
    chipsContainer.innerHTML = '';
    if (ev.triggered_rules && ev.triggered_rules.length > 0) {
        ev.triggered_rules.forEach(rule => {
            const chip = document.createElement('span');
            chip.className = 'violation-tag';
            chip.textContent = rule.replace(/_/g, ' ');
            chipsContainer.appendChild(chip);
        });
    } else {
        chipsContainer.innerHTML = '<span class="badge badge-normal">All AML Rule Checks Clear</span>';
    }

    document.getElementById('res-explanation').textContent = ev.explanation;
    document.getElementById('res-proc-time').innerHTML = `<i data-lucide="clock" style="width: 12px; height: 12px;"></i> Latency: ${data.processing_time_ms}ms | Stored in SQLite as ${data.transaction_id}`;
    refreshIcons();
}

// ==========================================
// Batch CSV Auditor
// ==========================================
function initBatchAuditor() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('batch-file-input');

    document.getElementById('btn-browse-trigger')?.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropzone?.addEventListener('click', () => fileInput.click());

    dropzone?.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone?.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

    dropzone?.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            uploadBatchCSV(e.dataTransfer.files[0]);
        }
    });

    fileInput?.addEventListener('change', () => {
        if (fileInput.files.length) {
            uploadBatchCSV(fileInput.files[0]);
        }
    });

    document.getElementById('btn-use-sample-csv')?.addEventListener('click', () => {
        showToast('Generating benchmark PaySim transaction file...', 'info');
        const sampleCSV = `step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest\n1,PAYMENT,42.50,C1029384,2000,1957.5,M928374,5000,5042.5\n1,TRANSFER,9850.00,C2039485,30000,20150,C8472910,0,9850\n1,CASH_OUT,145000.00,C3049586,145000,0,C9283741,2000,147000\n2,PAYMENT,12.00,C4059687,500,488,M102938,1000,1012\n2,TRANSFER,250000.00,C5069788,250000,0,C8492019,0,250000`;
        const blob = new Blob([sampleCSV], { type: 'text/csv' });
        const testFile = new File([blob], 'benchmark_transactions.csv', { type: 'text/csv' });
        uploadBatchCSV(testFile);
    });

    document.getElementById('btn-export-batch-csv')?.addEventListener('click', exportFlaggedBatchCSV);
}

let lastBatchAnomalies = [];

async function uploadBatchCSV(file) {
    const progressBox = document.getElementById('batch-progress-box');
    const progressBar = document.getElementById('batch-progress-fill');
    const progressPercent = document.getElementById('batch-progress-percent');
    const resultsWrapper = document.getElementById('batch-results-wrapper');

    progressBox.style.display = 'block';
    resultsWrapper.style.display = 'none';

    let p = 15;
    const interval = setInterval(() => {
        p = Math.min(p + 15, 85);
        progressBar.style.width = `${p}%`;
        progressPercent.textContent = `${p}%`;
    }, 120);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await apiCall('/api/predict/batch', {
            method: 'POST',
            body: formData
        });

        clearInterval(interval);
        progressBar.style.width = '100%';
        progressPercent.textContent = '100%';

        setTimeout(() => {
            progressBox.style.display = 'none';
            displayBatchResults(res);
            showToast(`Processed ${res.total_processed} transactions: Flagged ${res.total_anomalies_detected} anomalies!`, 'success');
        }, 200);
    } catch (err) {
        clearInterval(interval);
        progressBox.style.display = 'none';
        showToast(err.message, 'error');
    }
}

function displayBatchResults(res) {
    document.getElementById('batch-results-wrapper').style.display = 'block';
    document.getElementById('batch-total').textContent = res.total_processed;
    document.getElementById('batch-anomalies').textContent = res.total_anomalies_detected;
    document.getElementById('batch-rate').textContent = `${res.anomaly_rate_percent}%`;
    document.getElementById('batch-prevented').textContent = `$${Number(res.fraud_volume_prevented_usd).toLocaleString()}`;

    lastBatchAnomalies = res.preview_flagged_transactions || [];
    const tbody = document.getElementById('batch-preview-tbody');
    tbody.innerHTML = '';

    lastBatchAnomalies.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${row.id}</strong></td>
            <td><span class="badge" style="background: #f4f4f5; color: #18181b;">${row.type}</span></td>
            <td><strong>$${Number(row.amount).toLocaleString(undefined, {minimumFractionDigits: 2})}</strong></td>
            <td>${row.nameOrig}</td>
            <td>${row.nameDest}</td>
            <td><span class="badge badge-${row.risk_level.toLowerCase()}">${row.risk_level}</span></td>
            <td>${row.risk_score.toFixed(2)}</td>
            <td><span style="font-size: 0.78rem; font-weight: 600; color: #dc2626;">${row.triggered_rules.join(', ') || 'XGBoost ML Outlier'}</span></td>
        `;
        tbody.appendChild(tr);
    });
    refreshIcons();
}

function exportFlaggedBatchCSV() {
    if (!lastBatchAnomalies || lastBatchAnomalies.length === 0) {
        showToast('No flagged transactions to export.', 'info');
        return;
    }

    const headers = ['ID', 'Type', 'Amount', 'Sender', 'Beneficiary', 'Risk Level', 'Risk Score', 'Violations', 'Explanation'];
    const rows = lastBatchAnomalies.map(r => [
        r.id,
        r.type,
        r.amount,
        r.nameOrig,
        r.nameDest,
        r.risk_level,
        r.risk_score,
        `"${r.triggered_rules.join(';')}"`,
        `"${r.explanation.replace(/"/g, '""')}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `ApexGuard_AML_Audit_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    showToast('Downloaded AML Audit Report CSV', 'success');
}

// ==========================================
// Investigation Hub & Case Management
// ==========================================
function initInvestigationHub() {
    document.getElementById('btn-refresh-table')?.addEventListener('click', () => loadTransactionsTable());

    let searchTimeout;
    document.getElementById('tbl-search-input')?.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            state.searchQuery = e.target.value.trim();
            state.page = 1;
            loadTransactionsTable();
        }, 250);
    });

    document.querySelectorAll('#risk-filter-pills .preset-chip').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#risk-filter-pills .preset-chip').forEach(b => {
                b.style.background = '#ffffff';
                b.style.color = 'var(--ink-secondary)';
            });
            btn.style.background = '#09090b';
            btn.style.color = '#ffffff';
            state.riskFilter = btn.getAttribute('data-filter');
            state.page = 1;
            loadTransactionsTable();
        });
    });

    document.getElementById('btn-page-prev')?.addEventListener('click', () => {
        if (state.page > 1) {
            state.page--;
            loadTransactionsTable();
        }
    });

    document.getElementById('btn-page-next')?.addEventListener('click', () => {
        state.page++;
        loadTransactionsTable();
    });

    document.getElementById('modal-close-btn')?.addEventListener('click', () => {
        document.getElementById('tx-modal').classList.remove('show');
    });

    document.getElementById('btn-modal-confirm-fraud')?.addEventListener('click', () => handleReviewAction('CONFIRMED_FRAUD'));
    document.getElementById('btn-modal-clear-normal')?.addEventListener('click', () => handleReviewAction('CLEARED_NORMAL'));
}

async function loadTransactionsTable() {
    const tbody = document.getElementById('investigation-tbody');
    tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 25px; color: var(--ink-muted);">Loading transactions ledger...</td></tr>';

    try {
        let url = `/api/transactions?page=${state.page}&page_size=${state.pageSize}`;
        if (state.riskFilter !== 'ALL') url += `&risk_level=${state.riskFilter}`;
        if (state.searchQuery) url += `&search=${encodeURIComponent(state.searchQuery)}`;

        const data = await apiCall(url);
        tbody.innerHTML = '';

        if (data.items.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 30px; color: var(--ink-muted);">No records found matching filters.</td></tr>';
            return;
        }

        data.items.forEach(tx => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${tx.id}</strong></td>
                <td><span class="badge" style="background: #f4f4f5; color: #18181b;">${tx.type}</span></td>
                <td><strong>$${Number(tx.amount).toLocaleString(undefined, {minimumFractionDigits: 2})}</strong></td>
                <td><span style="font-family: monospace; font-size: 0.8rem; background: #f4f4f5; padding: 2px 6px; border-radius: 4px;">${tx.nameOrig}</span></td>
                <td><span style="font-family: monospace; font-size: 0.8rem; background: #f4f4f5; padding: 2px 6px; border-radius: 4px;">${tx.nameDest}</span></td>
                <td>${tx.risk_score.toFixed(2)}</td>
                <td><span class="badge badge-${tx.risk_level.toLowerCase()}">${tx.risk_level}</span></td>
                <td><span class="badge" style="background: #ffffff; border: 1px solid #e4e4e7; color: #3f3f46;">${tx.status.replace(/_/g, ' ')}</span></td>
                <td style="font-size: 0.78rem; color: var(--ink-muted);">${tx.created_at ? tx.created_at.replace('T', ' ').slice(0, 19) : 'N/A'}</td>
            `;
            tr.addEventListener('click', () => openTransactionModal(tx.id));
            tbody.appendChild(tr);
        });

        const start = (data.page - 1) * data.page_size + 1;
        const end = Math.min(data.page * data.page_size, data.total_records);
        document.getElementById('pagination-info').textContent = `Showing ${start} to ${end} of ${data.total_records} records`;
        document.getElementById('btn-page-prev').disabled = data.page <= 1;
        document.getElementById('btn-page-next').disabled = data.page >= data.total_pages;

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="9" style="color: #dc2626; text-align: center; padding: 20px;">Failed to load transactions: ${err.message}</td></tr>`;
    }
    refreshIcons();
}

async function openTransactionModal(txnId) {
    state.selectedTxId = txnId;
    try {
        const data = await apiCall(`/api/transactions/${txnId}`);
        const tx = data.transaction;

        document.getElementById('modal-tx-id').textContent = `Case Audit: ${tx.id}`;
        document.getElementById('modal-tx-time').textContent = tx.created_at ? tx.created_at.replace('T', ' ') : 'N/A';
        document.getElementById('modal-amount').textContent = `$${Number(tx.amount).toLocaleString(undefined, {minimumFractionDigits: 2})}`;

        const rBadge = document.getElementById('modal-risk-badge');
        rBadge.className = `badge badge-${tx.risk_level.toLowerCase()}`;
        rBadge.textContent = `${tx.risk_level} (Score: ${tx.risk_score.toFixed(2)})`;

        document.getElementById('modal-status-badge').textContent = tx.status.replace(/_/g, ' ');

        document.getElementById('modal-orig-acc').textContent = tx.nameOrig;
        document.getElementById('modal-orig-bal').textContent = `$${tx.oldbalanceOrg.toLocaleString()} → $${tx.newbalanceOrig.toLocaleString()}`;

        document.getElementById('modal-dest-acc').textContent = tx.nameDest;
        document.getElementById('modal-dest-bal').textContent = `$${tx.oldbalanceDest.toLocaleString()} → $${tx.newbalanceDest.toLocaleString()}`;

        document.getElementById('modal-explanation').textContent = tx.explanation || 'Normal transaction flow.';

        document.getElementById('tx-modal').classList.add('show');
        refreshIcons();
    } catch (err) {
        showToast('Failed to load transaction details.', 'error');
    }
}

async function handleReviewAction(newStatus) {
    if (!state.selectedTxId) return;

    try {
        await apiCall(`/api/transactions/${state.selectedTxId}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: newStatus,
                notes: `Audited and verified by ${state.user.full_name || state.user.username}.`
            })
        });

        document.getElementById('tx-modal').classList.remove('show');
        showToast(`Transaction ${state.selectedTxId} marked as ${newStatus.replace(/_/g, ' ')}`, 'success');
        loadTransactionsTable();
        loadDashboardStats();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// ==========================================
// AI Models & Colab Center
// ==========================================
async function loadModelInfo() {
    try {
        const info = await apiCall('/api/model/info');
        renderFeatureImportanceChart(info.feature_importance);
    } catch (err) {
        console.warn('Model info load error:', err);
    }
}

function renderFeatureImportanceChart(features) {
    const ctx = document.getElementById('featuresChart')?.getContext('2d');
    if (!ctx) return;

    if (state.charts.features) state.charts.features.destroy();

    const labels = features.map(f => f.feature);
    const dataVals = features.map(f => f.importance);

    state.charts.features = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Relative Importance Score',
                data: dataVals,
                backgroundColor: '#18181b',
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: '#f4f4f5' }, ticks: { color: '#71717a' } },
                y: { grid: { display: false }, ticks: { color: '#27272a', font: { size: 11, weight: 600 } } }
            }
        }
    });
}

function initComplianceHub() {
    const sarModal = document.getElementById('sar-modal');
    const openSarBtn = document.getElementById('btn-open-sar-modal');
    const closeSarBtn = document.getElementById('sar-modal-close-btn');

    openSarBtn?.addEventListener('click', () => {
        const now = new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
        const draftTime = document.getElementById('sar-draft-time');
        if (draftTime) draftTime.textContent = now;
        sarModal?.classList.add('show');
        refreshIcons();
    });

    closeSarBtn?.addEventListener('click', () => {
        sarModal?.classList.remove('show');
    });

    document.getElementById('btn-copy-sar-json')?.addEventListener('click', () => {
        const sarText = `FINCEN / FATF FORM SAR-01\nFILING ENTITY: ApexGuard Autonomous Sentinel Rail (Node: 01)\nSUBJECT: C19283748 -> M91827364\nAMOUNT: $145,000.00 (CASH_OUT)\nSCORE: 0.992 (CRITICAL)\nNARRATIVE: Instantaneous 100% account drainage violating FATF Recommendation 10 & 20. Immediate asset freeze and law enforcement referral.`;
        navigator.clipboard.writeText(sarText);
        showToast('Copied Official SAR Draft to clipboard!', 'success');
    });

    document.getElementById('btn-export-sar-pdf')?.addEventListener('click', () => {
        const sarData = {
            regulatory_form: "SAR-01",
            jurisdiction: "FATF-FinCEN-BSA",
            filing_node: "ApexGuard-Sentinel-Prod-01",
            timestamp: new Date().toISOString(),
            account_origin: "C19283748",
            account_dest: "M91827364",
            amount: 145000.0,
            anomaly_score: 0.992,
            rules_violated: ["FATF_R10_RAPID_DRAINAGE", "FATF_R20_SAR_TRIGGER", "XGBOOST_CONFIRMED"],
            status: "AUTO_FILED"
        };
        const blob = new Blob([JSON.stringify(sarData, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `FATF_SAR_C19283748_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('Exported Official SAR JSON ledger record', 'success');
    });

    document.getElementById('cfg-policy-action')?.addEventListener('change', (e) => {
        showToast(`Regulatory enforcement policy updated to: ${e.target.value}`, 'info');
    });
}

// ==========================================
// Authentication Modal & State
// ==========================================
function initAuth() {
    const authBtn = document.getElementById('auth-btn');
    const authModal = document.getElementById('auth-modal');
    const authClose = document.getElementById('auth-close-btn');

    authBtn?.addEventListener('click', () => {
        authModal.classList.add('show');
        refreshIcons();
    });
    authClose?.addEventListener('click', () => authModal.classList.remove('show'));

    document.getElementById('btn-fill-admin')?.addEventListener('click', () => {
        document.getElementById('auth-username').value = 'admin';
        document.getElementById('auth-password').value = 'Admin@123';
    });

    document.getElementById('btn-fill-analyst')?.addEventListener('click', () => {
        document.getElementById('auth-username').value = 'analyst';
        document.getElementById('auth-password').value = 'Analyst@123';
    });

    document.getElementById('login-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('auth-username').value;
        const password = document.getElementById('auth-password').value;

        try {
            const res = await apiCall('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            state.token = res.access_token;
            state.user = res.user;
            localStorage.setItem('apex_jwt_token', res.access_token);
            localStorage.setItem('apex_user', JSON.stringify(res.user));

            updateUserBadge(res.user);
            authModal.classList.remove('show');
            showToast(`Logged in as ${res.user.full_name || res.user.username}`, 'success');
        } catch (err) {
            showToast(err.message, 'error');
        }
    });

    updateUserBadge(state.user);
}

function updateUserBadge(user) {
    if (!user) return;
    document.getElementById('nav-username').textContent = user.username === 'admin' ? 'Sarah (CCO)' : 'Alex (Analyst)';
    const avatarImg = document.getElementById('nav-avatar-img');
    if (avatarImg) {
        avatarImg.src = user.username === 'admin' ? '/static/assets/admin_avatar.svg' : '/static/assets/analyst_avatar.svg';
    }
}

// ==========================================
// App Entrypoint
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initAuth();
    initScanner();
    initBatchAuditor();
    initInvestigationHub();
    initComplianceHub();

    loadDashboardStats();
    refreshIcons();
});
