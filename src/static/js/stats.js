document.addEventListener("DOMContentLoaded", function () {
    const rawDataElement = document.getElementById("stats-data");
    if (!rawDataElement) return;

    const statsData = JSON.parse(rawDataElement.textContent);

    // Monthly Trend Chart: Purchases vs. Sales
    const ctxMonthly = document.getElementById("monthlyPurchasesChart");
    if (ctxMonthly) {
        new Chart(ctxMonthly, {
            type: "line",
            data: {
                labels: statsData.months && statsData.months.length ? statsData.months : ["Sin datos"],
                datasets: [
                    {
                        label: "Ingresos (Ventas)",
                        data: statsData.salesTotals && statsData.salesTotals.length ? statsData.salesTotals : [0],
                        borderColor: "#2e7d32",
                        backgroundColor: "rgba(46, 125, 50, 0.1)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: "Inversión (Compras)",
                        data: statsData.purchaseTotals && statsData.purchaseTotals.length ? statsData.purchaseTotals : [0],
                        borderColor: "#1976d2",
                        backgroundColor: "rgba(25, 118, 210, 0.1)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "top" }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) { return "$" + value; }
                        }
                    }
                }
            }
        });
    }

    //  Donut Chart: Top 5 Best-Selling Products
    const ctxTopSold = document.getElementById("topSoldProductsChart");
    if (ctxTopSold) {
        new Chart(ctxTopSold, {
            type: "doughnut",
            data: {
                labels: statsData.soldProdNames && statsData.soldProdNames.length ? statsData.soldProdNames : ["Sin datos"],
                datasets: [{
                    data: statsData.soldProdQtys && statsData.soldProdQtys.length ? statsData.soldProdQtys : [0],
                    backgroundColor: ["#2e7d32", "#66bb6a", "#81c784", "#a5d6a7", "#c8e6c9"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    //  Donut Chart: Top 5 Most Purchased Products
    const ctxTopProducts = document.getElementById("topProductsChart");
    if (ctxTopProducts) {
        new Chart(ctxTopProducts, {
            type: "doughnut",
            data: {
                labels: statsData.prodNames && statsData.prodNames.length ? statsData.prodNames : ["Sin datos"],
                datasets: [{
                    data: statsData.prodQtys && statsData.prodQtys.length ? statsData.prodQtys : [0],
                    backgroundColor: ["#1976d2", "#42a5f5", "#64b5f6", "#90caf9", "#bbdefb"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    // Horizontal Bar Chart: Top 5 Suppliers
    const ctxSuppliers = document.getElementById("topSuppliersChart");
    if (ctxSuppliers) {
        const hasSuppliers = statsData.supplierNames && statsData.supplierNames.length > 0;
        new Chart(ctxSuppliers, {
            type: "bar",
            data: {
                labels: hasSuppliers ? statsData.supplierNames : ["Sin datos"],
                datasets: [{
                    label: "Inversión",
                    data: hasSuppliers ? statsData.supplierTotals : [0],
                    backgroundColor: "#1565c0",
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) { return "$" + value; }
                        }
                    },
                    y: {
                        ticks: {
                            autoSkip: false,
                            font: { weight: "bold" }
                        }
                    }
                }
            }
        });
    }

    // 5. Horizontal Bar Chart: Top 5 Customers
    const ctxClients = document.getElementById("topClientsChart");
    if (ctxClients) {
        const hasClients = statsData.clientNames && statsData.clientNames.length > 0;
        new Chart(ctxClients, {
            type: "bar",
            data: {
                labels: hasClients ? statsData.clientNames : ["Sin datos"],
                datasets: [{
                    label: "Ingresos",
                    data: hasClients ? statsData.clientTotals : [0],
                    backgroundColor: "#2e7d32",
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) { return "$" + value; }
                        }
                    },
                    y: {
                        ticks: {
                            autoSkip: false,
                            font: { weight: "bold" }
                        }
                    }
                }
            }
        });
    }
});