/* ============================================
   BIKE RENTAL ADMIN PANEL - JavaScript
   ============================================ */

// Global CSRF Cookie Helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    if (!cookieValue && name === 'csrftoken') {
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) cookieValue = csrfInput.value;
    }
    return cookieValue || '';
}
window.getCookie = getCookie;

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Sidebar Toggle ---------- */
    const sidebarToggler = document.querySelector('.sidebar-toggler');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const body = document.body;

    if (sidebarToggler) {
        sidebarToggler.addEventListener('click', function () {
            if (window.innerWidth >= 1200) {
                body.classList.toggle('sidebar-collapsed');
            } else {
                body.classList.toggle('sidebar-open');
                if (body.classList.contains('sidebar-open')) {
                    sidebarOverlay.classList.add('show');
                } else {
                    sidebarOverlay.classList.remove('show');
                }
            }
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function () {
            body.classList.remove('sidebar-open');
            sidebarOverlay.classList.remove('show');
        });
    }

    /* ---------- Sidebar Submenus ---------- */
    document.querySelectorAll('.sidebar-toggle-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const submenu = this.nextElementSibling;
            const isOpen = submenu.classList.contains('show');

            // Close all open submenus (optional accordion behavior)
            // document.querySelectorAll('.sidebar-submenu.show').forEach(s => s.classList.remove('show'));
            // document.querySelectorAll('.sidebar-toggle-btn').forEach(b => b.classList.add('collapsed'));

            if (isOpen) {
                submenu.classList.remove('show');
                this.classList.add('collapsed');
            } else {
                submenu.classList.add('show');
                this.classList.remove('collapsed');
            }
        });
    });

    /* ---------- Tab Navigation ---------- */
    document.querySelectorAll('.admin-tabs').forEach(function (tabContainer) {
        tabContainer.querySelectorAll('.tab-item').forEach(function (tab) {
            tab.addEventListener('click', function () {
                tabContainer.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
                this.classList.add('active');

                // Show corresponding tab content if exists
                const target = this.getAttribute('data-tab');
                if (target) {
                    const parent = tabContainer.parentElement;
                    parent.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                    const pane = parent.querySelector('#' + target);
                    if (pane) pane.classList.add('active');
                } else {
                    // If universal filter is registered on page, synchronize with it
                    if (typeof window.applyTableFilter === 'function') {
                        window.applyTableFilter();
                        return;
                    }

                    // Fallback filtering table rows by clicked tab keyword (e.g. All, Pending, Verified, etc.)
                    const filterAttr = this.getAttribute('data-filter');
                    let rawText = (filterAttr !== null ? filterAttr : (this.childNodes[0]?.textContent || this.textContent || '')).trim().toLowerCase();
                    if (rawText === 'active rentals' || rawText === 'active bookings') {
                        rawText = 'active';
                    }

                    const table = document.querySelector('.admin-table');
                    if (table) {
                        const rows = table.querySelectorAll('tbody tr');
                        let visible = 0;
                        rows.forEach(row => {
                            if (row.querySelector('td[colspan]')) return;
                            const rowText = row.textContent.toLowerCase();
                            const isAll = !rawText || rawText === 'all' || rawText.includes('all');
                            if (isAll || rowText.includes(rawText)) {
                                row.style.display = '';
                                visible++;
                            } else {
                                row.style.display = 'none';
                            }
                        });
                        const pageInfo = document.querySelector('.admin-pagination .page-info');
                        if (pageInfo) pageInfo.textContent = `Showing ${visible} entries`;
                    }
                }
            });
        });
    });

    /* ---------- Pagination ---------- */
    document.querySelectorAll('.admin-pagination .page-link-item').forEach(function (link) {
        if (!link.classList.contains('disabled') && !link.hasAttribute('href')) {
            link.addEventListener('click', function () {
                const pagination = this.closest('.admin-pagination');
                pagination.querySelectorAll('.page-link-item').forEach(l => l.classList.remove('active'));
                if (!this.querySelector('i')) {
                    this.classList.add('active');
                }
            });
        }
    });

    /* ---------- Delete / Action Confirmation Modal ---------- */
    const confirmModal = document.getElementById('confirmActionModal');
    if (confirmModal) {
        confirmModal.addEventListener('show.bs.modal', function (event) {
            let trigger = event.relatedTarget;
            if (trigger && !trigger.hasAttribute('data-api-url') && !trigger.hasAttribute('data-url')) {
                const parentBtn = trigger.closest('[data-bs-toggle="modal"]') || trigger.closest('button') || trigger.closest('a');
                if (parentBtn) trigger = parentBtn;
            }
            if (trigger) {
                const action = (trigger.getAttribute('data-action') || 'delete').trim();
                const item = trigger.getAttribute('data-item') || 'this item';
                const titleEl = this.querySelector('.modal-title');
                const bodyEl = this.querySelector('.modal-body p');
                const confirmBtn = this.querySelector('#confirmModalActionBtn') || this.querySelector('.btn-confirm-action');

                const actions = {
                    'delete': { title: 'Confirm Delete', msg: 'Are you sure you want to delete ' + item + '? This action cannot be undone.', btn: 'Delete', cls: 'btn-danger' },
                    'block': { title: 'Block Customer', msg: 'Are you sure you want to block ' + item + '? They will not be able to make bookings.', btn: 'Block', cls: 'btn-warning' },
                    'unblock': { title: 'Unblock Customer', msg: 'Are you sure you want to unblock ' + item + '?', btn: 'Unblock', cls: 'btn-success' },
                    'approve': { title: 'Approve KYC', msg: 'Are you sure you want to approve KYC for ' + item + '?', btn: 'Approve', cls: 'btn-success' },
                    'reject': { title: 'Reject KYC', msg: 'Are you sure you want to reject KYC for ' + item + '? They will need to re-submit documents.', btn: 'Reject', cls: 'btn-danger' },
                    'cancel': { title: 'Cancel Booking', msg: 'Are you sure you want to cancel booking ' + item + '? This action cannot be undone.', btn: 'Cancel Booking', cls: 'btn-danger' },
                    'confirm': { title: 'Confirm Action', msg: 'Are you sure you want to confirm ' + item + '?', btn: 'Confirm', cls: 'btn-primary' },
                    'maintenance': { title: 'Mark for Maintenance', msg: 'Mark vehicle ' + item + ' for maintenance? It will be unavailable for bookings.', btn: 'Mark Maintenance', cls: 'btn-warning' },
                    'status': { title: 'Change Status', msg: 'Change status of ' + item + '?', btn: 'Update', cls: 'btn-primary' },
                    'update status to Pickup': { title: 'Set Status to Pickup', msg: 'Change status of ' + item + ' to Pickup (Self Pickup fulfillment)? Vehicle will be marked as Rented.', btn: 'Set Status: Pickup', cls: 'btn-info text-white' },
                    'update status to Drop Off': { title: 'Set Status to Drop Off', msg: 'Change status of ' + item + ' to Drop Off (Doorstep fulfillment)? Vehicle will be marked as Rented.', btn: 'Set Status: Drop Off', cls: 'btn-primary' },
                    'pickup': { title: 'Set Status to Pickup', msg: 'Change status of ' + item + ' to Pickup (Self Pickup)?', btn: 'Set Status: Pickup', cls: 'btn-info text-white' },
                    'drop off': { title: 'Set Status to Drop Off', msg: 'Change status of ' + item + ' to Drop Off (Doorstep)?', btn: 'Set Status: Drop Off', cls: 'btn-primary' }
                };

                confirmModal._currentTrigger = trigger;
                const config = actions[action] || actions['confirm'];
                if (titleEl) titleEl.textContent = config.title;
                if (bodyEl) bodyEl.textContent = config.msg;
                if (confirmBtn) {
                    confirmBtn.textContent = config.btn;
                    confirmBtn.className = 'btn btn-confirm-action ' + config.cls;
                }
            }
        });

        // Handle confirm button click with real API integration
        const confirmBtn = confirmModal.querySelector('#confirmModalActionBtn') || confirmModal.querySelector('.btn-confirm-action');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', async function () {
                const trigger = confirmModal._currentTrigger;
                const apiUrl = trigger ? (trigger.getAttribute('data-api-url') || trigger.getAttribute('data-url')) : null;
                let apiMethod = trigger ? (trigger.getAttribute('data-api-method') || 'POST') : 'POST';
                if (trigger && trigger.getAttribute('data-action') === 'delete' && !trigger.getAttribute('data-api-method')) {
                    apiMethod = 'DELETE';
                }
                const apiPayloadStr = trigger ? trigger.getAttribute('data-api-payload') : null;

                if (apiUrl) {
                    const originalText = confirmBtn.innerHTML;
                    confirmBtn.disabled = true;
                    confirmBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Processing...';
                    try {
                        let payload = {};
                        if (apiPayloadStr) {
                            try { payload = JSON.parse(apiPayloadStr); } catch (e) { }
                        }
                        const res = await fetch(apiUrl, {
                            method: apiMethod,
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': (typeof getCookie === 'function' ? getCookie('csrftoken') : '') || ''
                            },
                            body: apiMethod !== 'GET' ? JSON.stringify(payload) : null
                        });
                        const data = await res.json();
                        if (res.ok && data.success !== false) {
                            showToast(data.message || 'Action executed successfully!', 'success');
                            setTimeout(() => window.location.reload(), 600);
                        } else {
                            showToast(data.error || data.message || 'Action failed!', 'danger');
                            confirmBtn.disabled = false;
                            confirmBtn.innerHTML = originalText;
                        }
                    } catch (err) {
                        showToast('Network request failed: ' + err.message, 'danger');
                        confirmBtn.disabled = false;
                        confirmBtn.innerHTML = originalText;
                    }
                } else {
                    showToast('Action completed successfully!', 'success');
                }

                const modal = bootstrap.Modal.getInstance(confirmModal);
                if (modal) modal.hide();
            });
        }
    }

    /* ---------- Toast Notification ---------- */
    window.showToast = function (message, type) {
        type = type || 'info';
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) return;

        const icons = {
            'success': 'bi-check-circle-fill',
            'danger': 'bi-exclamation-circle-fill',
            'warning': 'bi-exclamation-triangle-fill',
            'info': 'bi-info-circle-fill'
        };

        const toastId = 'toast-' + Date.now();
        const html = '<div id="' + toastId + '" class="toast align-items-center border-0 text-bg-' + type + '" role="alert">' +
            '<div class="d-flex">' +
            '<div class="toast-body"><i class="bi ' + (icons[type] || icons['info']) + ' me-2"></i>' + message + '</div>' +
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>' +
            '</div></div>';

        toastContainer.insertAdjacentHTML('beforeend', html);
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();

        toastEl.addEventListener('hidden.bs.toast', function () {
            toastEl.remove();
        });
    };

    /* ---------- Action Buttons (Dummy) ---------- */
    document.querySelectorAll('[data-action-btn]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const action = this.getAttribute('data-action-btn');
            showToast('Action "' + action + '" executed successfully!', 'success');
        });
    });

    /* ---------- Form Submit (Removed Dummy Interceptor) ---------- */
    /* ---------- Export Buttons (File Download) ---------- */
    document.querySelectorAll('[data-export]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const format = this.getAttribute('data-export');
            
            if (format === 'pdf') {
                showToast('Preparing PDF report...', 'info');
                
                const element = document.getElementById('reportsDashboardExportArea') || document.querySelector('.admin-content') || document.body;
                
                // Temporarily convert chart canvases to <img> elements so html2canvas doesn't fail on blank/tainted canvas clones
                const canvases = element.querySelectorAll('canvas');
                const restorations = [];
                
                canvases.forEach(function (canvas) {
                    try {
                        const dataUrl = canvas.toDataURL('image/png');
                        if (dataUrl && dataUrl.length > 50) {
                            const img = document.createElement('img');
                            img.src = dataUrl;
                            img.style.width = '100%';
                            img.style.height = canvas.offsetHeight ? (canvas.offsetHeight + 'px') : 'auto';
                            img.style.display = 'block';
                            img.className = 'temp-pdf-export-img';
                            canvas.parentNode.insertBefore(img, canvas);
                            canvas.style.display = 'none';
                            restorations.push({ canvas: canvas, img: img });
                        }
                    } catch (err) {
                        console.warn('Canvas conversion note:', err);
                    }
                });

                function cleanup() {
                    restorations.forEach(function (r) {
                        r.canvas.style.display = '';
                        if (r.img && r.img.parentNode) {
                            r.img.parentNode.removeChild(r.img);
                        }
                    });
                }

                if (typeof html2pdf !== 'undefined') {
                    const opt = {
                        margin:       [8, 8, 8, 8],
                        filename:     'Monthly_Business_Report.pdf',
                        image:        { type: 'jpeg', quality: 0.95 },
                        html2canvas:  { 
                            scale: 1.5, 
                            useCORS: false,
                            logging: false,
                            scrollX: 0,
                            scrollY: 0
                        },
                        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'landscape' }
                    };
                    
                    html2pdf().set(opt).from(element).save().then(function () {
                        cleanup();
                        showToast('PDF downloaded successfully!', 'success');
                    }).catch(function (err) {
                        console.error('html2pdf encountered an error, falling back to print dialog:', err);
                        cleanup();
                        showToast('Opening print dialog for PDF export...', 'info');
                        window.print();
                    });
                } else {
                    cleanup();
                    showToast('Opening print dialog for PDF export...', 'info');
                    window.print();
                }
            } else {
                showToast('Downloading ' + format.toUpperCase() + ' report...', 'info');
                // Direct download trigger
                window.location.href = `/api/reports/export/?format=${format}`;
            }
        });
    });

    /* ---------- Print Invoice ---------- */
    document.querySelectorAll('.btn-print').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            window.print();
        });
    });

    /* ---------- Select All Checkbox ---------- */
    document.querySelectorAll('.select-all-check').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const table = this.closest('table');
            if (table) {
                table.querySelectorAll('.row-check').forEach(function (cb) {
                    cb.checked = checkbox.checked;
                });
            }
        });
    });

    /* ---------- Universal Table Filter ---------- */
    initUniversalTableFilter();

    /* ---------- Universal Edit & Delete Actions ---------- */
    initUniversalActions();

    /* ---------- Chart.js Initialization (Dashboard) ---------- */
    initDashboardCharts();

    /* ---------- Sidebar active state ---------- */
    highlightActiveSidebarLink();
});

/* ---------- Dashboard Charts ---------- */
function initDashboardCharts() {
    // Booking Trends
    const bookingCtx = document.getElementById('bookingTrendsChart');
    if (bookingCtx && typeof Chart !== 'undefined') {
        const monthlyData = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            values: [320, 380, 420, 510, 580, 620, 710, 780, 850, 720, 680, 740]
        };
        const weeklyData = {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            values: [160, 195, 215, 150]
        };

        const bookingChart = new Chart(bookingCtx, {
            type: 'line',
            data: {
                labels: monthlyData.labels,
                datasets: [{
                    label: 'Bookings',
                    data: monthlyData.values,
                    borderColor: '#FF6B00',
                    backgroundColor: 'rgba(255, 107, 0, 0.08)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#FF6B00',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: chartOptions('Bookings')
        });

        const btnMonthly = document.getElementById('btnBookingMonthly');
        const btnWeekly = document.getElementById('btnBookingWeekly');
        if (btnMonthly && btnWeekly) {
            btnMonthly.addEventListener('click', function() {
                btnMonthly.classList.add('active');
                btnWeekly.classList.remove('active');
                bookingChart.data.labels = monthlyData.labels;
                bookingChart.data.datasets[0].data = monthlyData.values;
                bookingChart.update();
            });
            btnWeekly.addEventListener('click', function() {
                btnWeekly.classList.add('active');
                btnMonthly.classList.remove('active');
                bookingChart.data.labels = weeklyData.labels;
                bookingChart.data.datasets[0].data = weeklyData.values;
                bookingChart.update();
            });
        }
    }

    // Revenue Trends
    const revenueCtx = document.getElementById('revenueTrendsChart');
    if (revenueCtx && typeof Chart !== 'undefined') {
        new Chart(revenueCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue (₹)',
                    data: [185000, 210000, 245000, 298000, 345000, 380000, 425000, 465000, 510000, 420000, 395000, 440000],
                    backgroundColor: 'rgba(0, 43, 91, 0.85)',
                    borderRadius: 6,
                    borderSkipped: false,
                    barThickness: 24
                }]
            },
            options: chartOptions('Revenue')
        });
    }

    // Vehicle Utilization
    const utilizationCtx = document.getElementById('vehicleUtilizationChart');
    if (utilizationCtx && typeof Chart !== 'undefined') {
        new Chart(utilizationCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Bikes',
                    data: [72, 68, 75, 78, 85, 92, 88],
                    borderColor: '#002B5B',
                    backgroundColor: 'rgba(0, 43, 91, 0.05)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                }, {
                    label: 'Scooters',
                    data: [65, 72, 68, 74, 80, 88, 82],
                    borderColor: '#FF6B00',
                    backgroundColor: 'rgba(255, 107, 0, 0.05)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                }, {
                    label: 'EV',
                    data: [45, 52, 48, 56, 62, 70, 65],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.05)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                }]
            },
            options: chartOptions('Utilization %')
        });
    }

    // Booking Status Distribution
    const statusCtx = document.getElementById('bookingStatusChart');
    if (statusCtx && typeof Chart !== 'undefined') {
        const p = parseInt(statusCtx.dataset.pending, 10) || 0;
        const c = parseInt(statusCtx.dataset.confirmed, 10) || 0;
        const a = parseInt(statusCtx.dataset.active, 10) || 0;
        const comp = parseInt(statusCtx.dataset.completed, 10) || 0;
        const can = parseInt(statusCtx.dataset.cancelled, 10) || 0;
        const hasStatusData = (p + c + a + comp + can) > 0;
        const statusData = hasStatusData ? [p, c, a, comp, can] : [15, 22, 28, 45, 8];

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Confirmed', 'Active', 'Completed', 'Cancelled'],
                datasets: [{
                    data: statusData,
                    backgroundColor: ['#F59E0B', '#3B82F6', '#10B981', '#002B5B', '#EF4444'],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 16,
                            font: { size: 12, family: 'Inter' }
                        }
                    }
                }
            }
        });
    }

    // Vehicle Type Distribution
    const typeCtx = document.getElementById('vehicleTypeChart');
    if (typeCtx && typeof Chart !== 'undefined') {
        const b = parseInt(typeCtx.dataset.bike, 10) || 0;
        const s = parseInt(typeCtx.dataset.scooter, 10) || 0;
        const e = parseInt(typeCtx.dataset.ev, 10) || 0;
        const hasTypeData = (b + s + e) > 0;
        const typeData = hasTypeData ? [b, s, e] : [210, 186, 90];

        new Chart(typeCtx, {
            type: 'doughnut',
            data: {
                labels: ['Bike', 'Scooter', 'EV'],
                datasets: [{
                    data: typeData,
                    backgroundColor: ['#002B5B', '#FF6B00', '#10B981'],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 16,
                            font: { size: 12, family: 'Inter' }
                        }
                    }
                }
            }
        });
    }

    // Reports page charts
    const reportRevenueCtx = document.getElementById('reportRevenueChart');
    if (reportRevenueCtx && typeof Chart !== 'undefined') {
        new Chart(reportRevenueCtx, {
            type: 'line',
            data: {
                labels: window.reportChartLabels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue (₹)',
                    data: window.reportRevenueData || [185000, 210000, 245000, 298000, 345000, 380000, 425000, 465000, 510000, 420000, 395000, 440000],
                    borderColor: '#FF6B00',
                    backgroundColor: 'rgba(255, 107, 0, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4
                }]
            },
            options: chartOptions('Revenue')
        });
    }

    const reportBookingCtx = document.getElementById('reportBookingChart');
    if (reportBookingCtx && typeof Chart !== 'undefined') {
        new Chart(reportBookingCtx, {
            type: 'bar',
            data: {
                labels: window.reportChartLabels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Completed',
                    data: window.reportBookingCompleted || [280, 310, 350, 420, 480, 520, 590, 640, 700, 600, 560, 610],
                    backgroundColor: '#002B5B',
                    borderRadius: 4,
                    barThickness: 14
                }, {
                    label: 'Cancelled',
                    data: window.reportBookingCancelled || [40, 35, 45, 50, 55, 42, 48, 52, 58, 45, 40, 46],
                    backgroundColor: '#EF4444',
                    borderRadius: 4,
                    barThickness: 14
                }]
            },
            options: chartOptions('Bookings')
        });
    }
}

function chartOptions(label) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                align: 'end',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 16,
                    font: { size: 12, family: 'Inter' }
                }
            },
            tooltip: {
                backgroundColor: '#1E293B',
                titleFont: { size: 12, family: 'Inter' },
                bodyFont: { size: 12, family: 'Inter' },
                padding: 12,
                cornerRadius: 8,
                displayColors: true
            }
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { font: { size: 11, family: 'Inter' }, color: '#64748B' }
            },
            y: {
                grid: { color: 'rgba(226, 232, 240, 0.6)', drawBorder: false },
                ticks: { font: { size: 11, family: 'Inter' }, color: '#64748B' },
                beginAtZero: true
            }
        }
    };
}

/* ---------- Highlight Active Sidebar Link ---------- */
function highlightActiveSidebarLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-link').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && currentPath === href) {
            link.classList.add('active');
            // Expand parent submenu if needed
            const submenu = link.closest('.sidebar-submenu');
            if (submenu) {
                submenu.classList.add('show');
                const toggleBtn = submenu.previousElementSibling;
                if (toggleBtn) toggleBtn.classList.remove('collapsed');
            }
        }
    });
}

/* ========================================================
   UNIVERSAL TABLE FILTER & LIVE SEARCH
   ======================================================== */
function initUniversalTableFilter() {
    const filterBars = document.querySelectorAll('.filter-bar');
    if (!filterBars.length) return;

    filterBars.forEach(function (bar) {
        const table = document.querySelector('.admin-table');
        if (!table) return;

        const searchInput = bar.querySelector('.filter-search input, input[type="text"]');
        const selects = bar.querySelectorAll('select');
        const dateInputs = bar.querySelectorAll('input[type="date"]');

        const urlParams = new URLSearchParams(window.location.search);
        if (searchInput && urlParams.get('search')) {
            searchInput.value = urlParams.get('search');
        }
        const statusParam = urlParams.get('status');
        if (statusParam) {
            const tabs = document.querySelectorAll('.admin-tabs .tab-item');
            tabs.forEach(t => {
                const f = (t.getAttribute('data-filter') || t.childNodes[0]?.textContent || '').trim().toLowerCase();
                if (f === statusParam.toLowerCase() || (statusParam.toLowerCase() === 'active' && f.includes('active'))) {
                    tabs.forEach(x => x.classList.remove('active'));
                    t.classList.add('active');
                }
            });
        }

        function applyFilter() {
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            const activeSelects = Array.from(selects).map(s => s.value.toLowerCase().trim()).filter(v => v && !v.includes('all'));

            // Check active tab filter
            const activeTab = document.querySelector('.admin-tabs .tab-item.active');
            let tabFilter = '';
            if (activeTab && !activeTab.getAttribute('data-tab')) {
                const fAttr = activeTab.getAttribute('data-filter');
                tabFilter = (fAttr !== null ? fAttr : (activeTab.childNodes[0]?.textContent || activeTab.textContent || '')).trim().toLowerCase();
                if (tabFilter === 'active rentals' || tabFilter === 'active bookings') {
                    tabFilter = 'active';
                }
                if (tabFilter === 'all' || tabFilter.includes('all')) {
                    tabFilter = '';
                }
            }

            const rows = table.querySelectorAll('tbody tr');
            let visibleCount = 0;

            rows.forEach(function (row) {
                if (row.querySelector('td[colspan]')) return;

                const text = row.textContent.toLowerCase();
                let matchesSearch = !query || text.includes(query);
                let matchesTab = !tabFilter || text.includes(tabFilter);
                let matchesSelects = true;

                for (let val of activeSelects) {
                    if (val && !text.includes(val)) {
                        matchesSelects = false;
                        break;
                    }
                }

                if (matchesSearch && matchesTab && matchesSelects) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            const pageInfo = document.querySelector('.admin-pagination .page-info');
            if (pageInfo) {
                pageInfo.textContent = `Showing ${visibleCount} entries`;
            }
        }
        window.applyTableFilter = applyFilter;

        if (searchInput) {
            searchInput.addEventListener('input', applyFilter);
            searchInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    applyFilter();
                }
            });
        }

        selects.forEach(function (sel) {
            sel.addEventListener('change', applyFilter);
        });

        dateInputs.forEach(function (d) {
            d.addEventListener('change', applyFilter);
        });

        if (searchInput && searchInput.value) {
            applyFilter();
        }
    });
}

/* ========================================================
   UNIVERSAL EDIT MODAL & FORM BUILDER
   ======================================================== */
window.openEditModal = async function(type, id, triggerBtn) {
    const modalEl = document.getElementById('adminEditModal');
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);
    const titleEl = document.getElementById('editModalTitle');
    const bodyEl = document.getElementById('editModalBody');
    const formEl = document.getElementById('adminEditForm');

    titleEl.textContent = `Edit ${type.charAt(0).toUpperCase() + type.slice(1)} #${id}`;
    bodyEl.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">Loading ${type} details...</p>
        </div>
    `;
    modal.show();

    let endpoint = `/api/${type}s/${id}/`;
    if (type === 'kyc') endpoint = `/api/kyc/${id}/`;
    if (type === 'support' || type === 'ticket') endpoint = `/api/support/tickets/${id}/`;
    if (type === 'faq') endpoint = `/api/support/faqs/${id}/`;
    if (type === 'maintenance') endpoint = `/api/maintenance/${id}/`;
    if (type === 'offer') endpoint = `/api/offers/${id}/`;
    if (type === 'location') endpoint = `/api/locations/${id}/`;
    if (type === 'franchise') endpoint = `/api/franchises/${id}/`;
    if (type === 'vehicle') endpoint = `/api/vehicles/${id}/`;
    if (type === 'booking') endpoint = `/api/bookings/${id}/`;
    if (type === 'customer') endpoint = `/api/customers/${id}/`;
    if (type === 'vendor') endpoint = `/api/vendors/${id}/`;
    if (type === 'vehicle-category') endpoint = `/api/vehicle-categories/${id}/`;
    if (type === 'insurance') endpoint = `/api/insurance/${id}/`;
    if (type === 'delivery-zone') endpoint = `/api/delivery-zones/${id}/`;
    if (type === 'franchise-owner') endpoint = `/api/franchise-owners/${id}/`;

    try {
        const res = await fetch(endpoint);
        if (!res.ok) {
            let errMsg = 'Failed to load details (' + res.status + ')';
            try {
                const errData = await res.json();
                if (errData && (errData.error || errData.message)) errMsg = errData.error || errData.message;
            } catch (_) {}
            bodyEl.innerHTML = `<div class="alert alert-danger">${errMsg}</div>`;
            return;
        }
        const data = await res.json();
        
        let item = data[type] || data.record || data.booking || data.vehicle || data.vendor || data.customer || data.franchise || data.location || data.offer || data.ticket || data.category || data.results || data;
        if (data.success === false && !item) {
            bodyEl.innerHTML = `<div class="alert alert-danger">Failed to load details: ${data.error || 'Not found'}</div>`;
            return;
        }

        renderEditFields(type, id, item, bodyEl);

        formEl.onsubmit = async function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('btnSaveEdit');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Saving...';

            const formData = new FormData(formEl);
            const payload = {};
            formData.forEach((val, key) => {
                if (val === 'true') payload[key] = true;
                else if (val === 'false') payload[key] = false;
                else payload[key] = val;
            });

            try {
                const saveRes = await fetch(endpoint, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') || ''
                    },
                    body: JSON.stringify(payload)
                });
                const saveJson = await saveRes.json();
                if (saveRes.ok && saveJson.success !== false) {
                    showToast(`${type.charAt(0).toUpperCase() + type.slice(1)} updated successfully!`, 'success');
                    
                    // Immediately update row in table DOM if present
                    try {
                        const rows = Array.from(document.querySelectorAll('.admin-table tbody tr'));
                        const row = rows.find(r => r.textContent.includes(id));
                        if (row) {
                            if (payload.kyc_status) {
                                const kycBadges = row.querySelectorAll('.status-badge');
                                kycBadges.forEach(badge => {
                                    const txt = badge.textContent.trim().toLowerCase();
                                    if (['pending', 'verified', 'rejected'].includes(txt)) {
                                        badge.className = `status-badge badge-${payload.kyc_status}`;
                                        badge.textContent = payload.kyc_status.charAt(0).toUpperCase() + payload.kyc_status.slice(1);
                                    }
                                });
                            }
                            if (typeof payload.is_active !== 'undefined') {
                                const statusBadges = row.querySelectorAll('.status-badge');
                                statusBadges.forEach(badge => {
                                    const txt = badge.textContent.trim().toLowerCase();
                                    if (['active', 'blocked'].includes(txt)) {
                                        const isAct = payload.is_active === true || payload.is_active === 'true';
                                        badge.className = `status-badge badge-${isAct ? 'active' : 'blocked'}`;
                                        badge.textContent = isAct ? 'Active' : 'Blocked';
                                    }
                                });
                            }
                        }
                    } catch (e) { }

                    modal.hide();
                    setTimeout(() => window.location.reload(), 700);
                } else {
                    showToast(saveJson.error || saveJson.message || 'Update failed', 'danger');
                }
            } catch (err) {
                showToast('Save error: ' + err.message, 'danger');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-check2"></i> Save Changes';
            }
        };

    } catch (err) {
        bodyEl.innerHTML = `<div class="alert alert-danger">Network error: ${err.message}</div>`;
    }
};

function renderEditFields(type, id, item, container) {
    let html = '<div class="row g-3">';

    if (type === 'customer' || type === 'vendor') {
        html += `
            <div class="col-md-6">
                <label class="form-label font-weight-bold">Full Name</label>
                <input type="text" name="full_name" class="form-control" value="${item.full_name || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Phone Number</label>
                <input type="text" name="phone" class="form-control" value="${item.phone || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Email Address</label>
                <input type="email" name="email" class="form-control" value="${item.email || ''}" required>
            </div>
            ${type === 'vendor' ? `
            <div class="col-md-6">
                <label class="form-label font-weight-bold">Business Name</label>
                <input type="text" name="business_name" class="form-control" value="${item.business_name || item.company_name || ''}" placeholder="e.g. SpeedWheels Rentals">
            </div>
            <div class="col-md-6">
                <label class="form-label">GST Number <span class="text-muted" style="font-weight:normal;">(Optional)</span></label>
                <input type="text" name="gst_no" class="form-control" value="${item.gst_no || ''}" placeholder="e.g. 20AAACA1234A1Z5">
            </div>
            ` : ''}
            <div class="col-md-6">
                <label class="form-label">Account Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active ? 'selected' : ''}>Active</option>
                    <option value="false" ${!item.is_active ? 'selected' : ''}>Blocked / Inactive</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">KYC Status</label>
                <select name="kyc_status" class="form-select">
                    <option value="pending" ${(item.kyc_status || '').toLowerCase() === 'pending' ? 'selected' : ''}>Pending</option>
                    <option value="verified" ${(item.kyc_status || '').toLowerCase() === 'verified' ? 'selected' : ''}>Verified</option>
                    <option value="rejected" ${(item.kyc_status || '').toLowerCase() === 'rejected' ? 'selected' : ''}>Rejected</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">City</label>
                <input type="text" name="city" class="form-control" value="${item.city || 'Ranchi'}">
            </div>
            <div class="col-12">
                <label class="form-label">Address</label>
                <textarea name="address" class="form-control" rows="2">${item.address || ''}</textarea>
            </div>
            ${type === 'vendor' ? `
            <div class="col-12 mt-3">
                <h6 class="border-bottom pb-2 mb-2 text-primary"><i class="bi bi-file-earmark-person me-1"></i> Identity & Licence Documents</h6>
            </div>
            <div class="col-md-6">
                <label class="form-label">PAN Card Number</label>
                <input type="text" name="pan_number" class="form-control" value="${item.pan_number || ''}" placeholder="e.g. ABCDE1234F">
            </div>
            <div class="col-md-6">
                <label class="form-label">PAN Card Image URL / Path</label>
                <input type="text" name="pan_card_image" class="form-control" value="${item.pan_card_image || ''}" placeholder="https://... or /static/...">
            </div>
            <div class="col-md-6">
                <label class="form-label">Aadhaar Card Number</label>
                <input type="text" name="aadhaar_number" class="form-control" value="${item.aadhaar_number || ''}" placeholder="12-digit Aadhaar">
            </div>
            <div class="col-md-6">
                <label class="form-label">Aadhaar Front Image URL</label>
                <input type="text" name="aadhaar_front_image" class="form-control" value="${item.aadhaar_front_image || ''}" placeholder="https://... or /static/...">
            </div>
            <div class="col-md-6">
                <label class="form-label">Aadhaar Back Image URL</label>
                <input type="text" name="aadhaar_back_image" class="form-control" value="${item.aadhaar_back_image || ''}" placeholder="https://... or /static/...">
            </div>
            <div class="col-md-6">
                <label class="form-label">Driving Licence Number</label>
                <input type="text" name="licence_number" class="form-control" value="${item.licence_number || ''}" placeholder="e.g. JH01-2022-0045812">
            </div>
            <div class="col-md-6">
                <label class="form-label">Licence Image URL</label>
                <input type="text" name="licence_front_image" class="form-control" value="${item.licence_front_image || ''}" placeholder="https://... or /static/...">
            </div>
            <div class="col-md-6">
                <label class="form-label">Vendor Image URL / Path</label>
                <input type="text" name="profile_image" class="form-control" value="${item.profile_image || ''}" placeholder="https://... or /static/...">
            </div>
            ` : ''}
        `;
    } else if (type === 'faq') {
        html += `
            <div class="col-12">
                <label class="form-label font-weight-bold">Question</label>
                <input type="text" name="question" class="form-control" value="${item.question || ''}" required>
            </div>
            <div class="col-12">
                <label class="form-label">Answer</label>
                <textarea name="answer" class="form-control" rows="4" required>${item.answer || ''}</textarea>
            </div>
            <div class="col-md-6">
                <label class="form-label">Category</label>
                <input type="text" name="category" class="form-control" value="${item.category || 'General'}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active !== false ? 'selected' : ''}>Active</option>
                    <option value="false" ${item.is_active === false ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    } else if (type === 'vehicle-category') {
        html += `
            <div class="col-12">
                <label class="form-label font-weight-bold">Category Name</label>
                <input type="text" name="name" class="form-control" value="${item.name || ''}" required>
            </div>
            <div class="col-12">
                <label class="form-label">Description</label>
                <textarea name="description" class="form-control" rows="2">${item.description || ''}</textarea>
            </div>
            <div class="col-md-6">
                <label class="form-label">Base Daily Rate (₹)</label>
                <input type="number" name="base_daily_rate" class="form-control" value="${item.base_daily_rate || 400}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active !== false ? 'selected' : ''}>Active</option>
                    <option value="false" ${item.is_active === false ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    
    } else if (type === 'inspection') {
        html += `
            <div class="col-12"><label class="form-label">Inspector Name</label><input type="text" name="inspector_name" class="form-control" value="${item.inspector_name || ''}" required></div>
            <div class="col-12">
                <label class="form-label">Condition</label>
                <select name="condition" class="form-select">
                    <option value="Excellent" ${item.condition === 'Excellent' ? 'selected' : ''}>Excellent</option>
                    <option value="Good" ${item.condition === 'Good' ? 'selected' : ''}>Good</option>
                    <option value="Fair" ${item.condition === 'Fair' ? 'selected' : ''}>Fair</option>
                    <option value="Poor" ${item.condition === 'Poor' ? 'selected' : ''}>Poor</option>
                </select>
            </div>
            <div class="col-12"><label class="form-label">Notes</label><textarea name="notes" class="form-control" rows="2">${item.notes || ''}</textarea></div>
        `;
    } else if (type === 'insurance') {
        html += `
            <div class="col-md-6"><label class="form-label">Provider</label><input type="text" name="provider" class="form-control" value="${item.provider || ''}" required></div>
            <div class="col-md-6"><label class="form-label">Policy Number</label><input type="text" name="policy_number" class="form-control" value="${item.policy_number || ''}"></div>
            <div class="col-md-6"><label class="form-label">Coverage Type</label><input type="text" name="coverage_type" class="form-control" value="${item.coverage_type || ''}"></div>
            <div class="col-md-6"><label class="form-label">Premium (₹)</label><input type="number" step="0.01" name="premium_amount" class="form-control" value="${item.premium_amount || ''}"></div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="Active" ${item.status === 'Active' ? 'selected' : ''}>Active</option>
                    <option value="Expired" ${item.status === 'Expired' ? 'selected' : ''}>Expired</option>
                    <option value="Cancelled" ${item.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
            </div>
        `;
    } else if (type === 'franchise') {
        html += `
            <div class="col-12"><label class="form-label">Franchise Name</label><input type="text" name="name" class="form-control" value="${item.name || ''}" required></div>
            <div class="col-12"><label class="form-label">City</label><input type="text" name="city" class="form-control" value="${item.city || ''}"></div>
        `;

    } else if (type === 'vehicle') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Brand</label>
                <input type="text" name="brand" class="form-control" value="${item.brand || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Model</label>
                <input type="text" name="model" class="form-control" value="${item.model || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Rental Price (Per Day ₹)</label>
                <input type="number" name="rental_price_per_day" class="form-control" value="${item.rental_price_per_day || 450}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Availability Status</label>
                <select name="availability_status" class="form-select">
                    <option value="Available" ${item.availability_status === 'Available' ? 'selected' : ''}>Available</option>
                    <option value="Rented" ${item.availability_status === 'Rented' ? 'selected' : ''}>Rented</option>
                    <option value="Reserved" ${item.availability_status === 'Reserved' ? 'selected' : ''}>Reserved</option>
                    <option value="Maintenance" ${item.availability_status === 'Maintenance' ? 'selected' : ''}>Maintenance</option>
                    <option value="Inactive" ${item.availability_status === 'Inactive' ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Odometer Reading (KM)</label>
                <input type="number" name="odometer_reading" class="form-control" value="${item.odometer_reading || 0}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Fuel / Battery Level (%)</label>
                <input type="number" name="fuel_or_battery_level" class="form-control" value="${item.fuel_or_battery_level || 100}">
            </div>
        `;
    } else if (type === 'franchise-owner') {
        html += `
            <div class="col-12"><label class="form-label">Full Name</label><input type="text" name="full_name" class="form-control" value="${item.full_name || ''}" required></div>
            <div class="col-md-6"><label class="form-label">Email</label><input type="email" name="email" class="form-control" value="${item.email || ''}" required></div>
            <div class="col-md-6"><label class="form-label">Phone</label><input type="text" name="phone" class="form-control" value="${item.phone || ''}" required></div>
            <div class="col-12">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="active" ${item.status === 'active' ? 'selected' : ''}>Active</option>
                    <option value="inactive" ${item.status === 'inactive' ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    } else if (type === 'booking') {
        const curDeliv = item.delivery_type || 'Self Pickup';
        const isDoor = String(curDeliv).toLowerCase().includes('door');
        html += `
            <div class="col-md-6">
                <label class="form-label font-weight-bold">Delivery Type</label>
                <select name="delivery_type" id="bookingEditDeliveryType" class="form-select" onchange="window.onBookingDeliveryTypeChange(this.value)">
                    <option value="Self Pickup" ${!isDoor ? 'selected' : ''}>Self Pickup</option>
                    <option value="Doorstep" ${isDoor ? 'selected' : ''}>Doorstep</option>
                </select>
                <small class="text-muted">Customer preference: Self Pickup or Doorstep</small>
            </div>
            <div class="col-md-6">
                <label class="form-label font-weight-bold">Booking Status</label>
                <select name="status" id="bookingEditStatus" class="form-select">
                    <option value="Confirmed" ${item.status === 'Confirmed' ? 'selected' : ''}>Confirmed</option>
                    <option value="Pickup" ${item.status === 'Pickup' ? 'selected' : ''}>Pickup (Self Pickup fulfillment)</option>
                    <option value="Drop Off" ${item.status === 'Drop Off' ? 'selected' : ''}>Drop Off (Doorstep fulfillment)</option>
                    <option value="Active" ${item.status === 'Active' ? 'selected' : ''}>Active</option>
                    <option value="Completed" ${item.status === 'Completed' ? 'selected' : ''}>Completed</option>
                    <option value="Pending" ${item.status === 'Pending' ? 'selected' : ''}>Pending</option>
                    <option value="Cancelled" ${item.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
                <small class="text-muted" id="bookingStatusHint">${isDoor ? 'Doorstep chosen: Vendor/Admin changes status to <b>Drop Off</b>' : 'Self Pickup chosen: Vendor/Admin changes status to <b>Pickup</b>'}</small>
            </div>
            <div class="col-md-6">
                <label class="form-label">Payment Status</label>
                <select name="payment_status" class="form-select">
                    <option value="Paid" ${item.payment_status === 'Paid' ? 'selected' : ''}>Paid</option>
                    <option value="Pending" ${item.payment_status === 'Pending' ? 'selected' : ''}>Pending</option>
                    <option value="Refunded" ${item.payment_status === 'Refunded' ? 'selected' : ''}>Refunded</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Pickup & Drop Fulfillment Status</label>
                <select name="pickup_drop_status" class="form-select">
                    <option value="Scheduled" ${item.pickup_drop_status === 'Scheduled' ? 'selected' : ''}>Scheduled</option>
                    <option value="Ready" ${item.pickup_drop_status === 'Ready' ? 'selected' : ''}>Ready</option>
                    <option value="Out for Delivery" ${item.pickup_drop_status === 'Out for Delivery' ? 'selected' : ''}>Out for Delivery</option>
                    <option value="Picked Up" ${item.pickup_drop_status === 'Picked Up' ? 'selected' : ''}>Picked Up</option>
                    <option value="Dropped Off" ${item.pickup_drop_status === 'Dropped Off' ? 'selected' : ''}>Dropped Off</option>
                    <option value="Return Pending" ${item.pickup_drop_status === 'Return Pending' ? 'selected' : ''}>Return Pending</option>
                    <option value="Returned" ${item.pickup_drop_status === 'Returned' ? 'selected' : ''}>Returned</option>
                </select>
            </div>
        `;
    } else if (type === 'franchise') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Franchise Name</label>
                <input type="text" name="name" class="form-control" value="${item.name || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Owner Name</label>
                <input type="text" name="owner_name" class="form-control" value="${item.owner_name || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Phone</label>
                <input type="text" name="phone" class="form-control" value="${item.phone || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label">City</label>
                <input type="text" name="city" class="form-control" value="${item.city || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Commission Rate (%)</label>
                <input type="number" step="0.1" name="commission_rate" class="form-control" value="${item.commission_rate || 15}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="active" ${item.status === 'active' ? 'selected' : ''}>Active</option>
                    <option value="pending" ${item.status === 'pending' ? 'selected' : ''}>Pending</option>
                    <option value="inactive" ${item.status === 'inactive' ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    } else if (type === 'location') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Location Name</label>
                <input type="text" name="name" class="form-control" value="${item.name || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">City</label>
                <input type="text" name="city" class="form-control" value="${item.city || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Total Parking Capacity</label>
                <input type="number" name="total_capacity" class="form-control" value="${item.total_capacity || 40}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active ? 'selected' : ''}>Active</option>
                    <option value="false" ${!item.is_active ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
            <div class="col-12">
                <label class="form-label">Address</label>
                <textarea name="address" class="form-control" rows="2">${item.address || ''}</textarea>
            </div>
        `;
    } else if (type === 'delivery-zone') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Zone Name</label>
                <input type="text" name="name" class="form-control" value="${item.name || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Radius (km)</label>
                <input type="number" step="0.1" name="radius_km" class="form-control" value="${item.radius_km || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Delivery Charge</label>
                <input type="number" step="0.01" name="delivery_charge" class="form-control" value="${item.delivery_charge || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Min Booking Amount</label>
                <input type="number" step="0.01" name="min_booking_amount" class="form-control" value="${item.min_booking_amount || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Est. Delivery Time</label>
                <input type="text" name="estimated_delivery_time" class="form-control" value="${item.estimated_delivery_time || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active !== false ? 'selected' : ''}>Active</option>
                    <option value="false" ${item.is_active === false ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    } else if (type === 'maintenance') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Maintenance Type</label>
                <select name="maintenance_type" class="form-select">
                    <option value="Routine Service" ${item.maintenance_type === 'Routine Service' ? 'selected' : ''}>Routine Service</option>
                    <option value="Repair" ${item.maintenance_type === 'Repair' ? 'selected' : ''}>Repair</option>
                    <option value="Inspection" ${item.maintenance_type === 'Inspection' ? 'selected' : ''}>Inspection</option>
                    <option value="Tyre Replacement" ${item.maintenance_type === 'Tyre Replacement' ? 'selected' : ''}>Tyre Replacement</option>
                    <option value="Battery Check" ${item.maintenance_type === 'Battery Check' ? 'selected' : ''}>Battery Check</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="Scheduled" ${item.status === 'Scheduled' ? 'selected' : ''}>Scheduled</option>
                    <option value="In Progress" ${item.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="Completed" ${item.status === 'Completed' ? 'selected' : ''}>Completed</option>
                    <option value="Cancelled" ${item.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Service Center</label>
                <input type="text" name="service_center" class="form-control" value="${item.service_center || 'Main Hub'}">
            </div>
            <div class="col-md-6">
                <label class="form-label">Cost (₹)</label>
                <input type="number" name="cost" class="form-control" value="${item.cost || 0}">
            </div>
            <div class="col-12">
                <label class="form-label">Description / Remarks</label>
                <textarea name="description" class="form-control" rows="2">${item.description || ''}</textarea>
            </div>
        `;
    } else if (type === 'rental-plan') {
        html += `
            <div class="col-12"><label class="form-label">Plan Name</label><input type="text" name="name" class="form-control" value="${item.name || ''}" required></div>
            <div class="col-md-6">
                <label class="form-label">Duration Type</label>
                <select name="duration_type" class="form-select">
                    <option value="Hourly" ${item.duration_type === 'Hourly' ? 'selected' : ''}>Hourly</option>
                    <option value="Daily" ${item.duration_type === 'Daily' ? 'selected' : ''}>Daily</option>
                    <option value="Weekly" ${item.duration_type === 'Weekly' ? 'selected' : ''}>Weekly</option>
                    <option value="Monthly" ${item.duration_type === 'Monthly' ? 'selected' : ''}>Monthly</option>
                </select>
            </div>
            <div class="col-md-6"><label class="form-label">Price (₹)</label><input type="number" step="0.01" name="base_price" class="form-control" value="${item.base_price || ''}" required></div>
            <div class="col-md-6"><label class="form-label">Extra Charge (₹/km)</label><input type="number" step="0.01" name="extra_km_charge" class="form-control" value="${item.extra_km_charge || ''}"></div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active ? 'selected' : ''}>Active</option>
                    <option value="false" ${item.is_active === false ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
        `;
    } else if (type === 'offer') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Title</label>
                <input type="text" name="title" class="form-control" value="${item.title || ''}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Discount Type</label>
                <select name="discount_type" class="form-select">
                    <option value="percentage" ${item.discount_type === 'percentage' ? 'selected' : ''}>Percentage (%)</option>
                    <option value="flat" ${item.discount_type === 'flat' ? 'selected' : ''}>Flat (₹)</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Discount Value</label>
                <input type="number" name="discount_value" class="form-control" value="${item.discount_value || 10}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="is_active" class="form-select">
                    <option value="true" ${item.is_active ? 'selected' : ''}>Active</option>
                    <option value="false" ${!item.is_active ? 'selected' : ''}>Inactive / Expired</option>
                </select>
            </div>
        `;
    } else if (type === 'support' || type === 'ticket') {
        html += `
            <div class="col-md-6">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="Open" ${item.status === 'Open' ? 'selected' : ''}>Open</option>
                    <option value="In Progress" ${item.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="Resolved" ${item.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                    <option value="Closed" ${item.status === 'Closed' ? 'selected' : ''}>Closed</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label">Priority</label>
                <select name="priority" class="form-select">
                    <option value="Low" ${item.priority === 'Low' ? 'selected' : ''}>Low</option>
                    <option value="Medium" ${item.priority === 'Medium' ? 'selected' : ''}>Medium</option>
                    <option value="High" ${item.priority === 'High' ? 'selected' : ''}>High</option>
                    <option value="Urgent" ${item.priority === 'Urgent' ? 'selected' : ''}>Urgent</option>
                </select>
            </div>
            <div class="col-12">
                <label class="form-label">Assigned Agent</label>
                <input type="text" name="assigned_agent" class="form-control" value="${item.assigned_agent || 'Support Team'}">
            </div>
        `;
    } else {
        html += `
            <div class="col-12">
                <label class="form-label">Status</label>
                <input type="text" name="status" class="form-control" value="${item.status || ''}">
            </div>
        `;
    }

    html += '</div>';
    container.innerHTML = html;
}

function initUniversalActions() {
    document.querySelectorAll('.admin-table tbody tr').forEach(function (row) {
        const editBtn = row.querySelector('.btn-sm-action[title="Edit"], button[title="Edit"]');
        if (editBtn && !editBtn.getAttribute('onclick')) {
            editBtn.addEventListener('click', function (e) {
                e.preventDefault();
                const viewLink = row.querySelector('a[href*="/"]');
                if (viewLink) {
                    const href = viewLink.getAttribute('href');
                    const parts = href.split('/').filter(p => p);
                    if (parts.length >= 2) {
                        let entityType = parts[0];
                        if (entityType.endsWith('s')) entityType = entityType.slice(0, -1);
                        const entityId = parts[1];
                        window.openEditModal(entityType, entityId, this);
                    }
                }
            });
        }
    });
}

window.onBookingDeliveryTypeChange = function(val) {
    const hint = document.getElementById('bookingStatusHint');
    const statusSelect = document.getElementById('bookingEditStatus');
    if (!hint) return;
    if (val === 'Doorstep') {
        hint.innerHTML = 'Doorstep chosen: Vendor/Admin changes status to <b>Drop Off</b>';
        if (statusSelect && (statusSelect.value === 'Pickup' || statusSelect.value === 'Confirmed')) {
            statusSelect.value = 'Drop Off';
        }
    } else {
        hint.innerHTML = 'Self Pickup chosen: Vendor/Admin changes status to <b>Pickup</b>';
        if (statusSelect && (statusSelect.value === 'Drop Off' || statusSelect.value === 'Confirmed')) {
            statusSelect.value = 'Pickup';
        }
    }
};

