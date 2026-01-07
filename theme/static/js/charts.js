function initCharts() {
    console.log('initCharts called — redrawing with old beautiful style');

    document.querySelectorAll('canvas[id^="ratingChart"], #mapComparisonChart').forEach(canvas => {
        const chart = Chart.getChart(canvas);
        if (chart) chart.destroy();
    });

    const data1 = document.getElementById('rating-data-1');
    if (data1) {
        const json = JSON.parse(data1.textContent);
        const ctx = document.getElementById('ratingChart1');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: json.dates,
                    datasets: [{
                        label: `Рейтинг — ${json.team}`,
                        data: json.values,
                        borderColor: '#60a5fa',
                        backgroundColor: '#60a5fa33',
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: 0.8,
                            max: 1.3,
                            title: { display: true, text: 'Рейтинг (выше = лучше)', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        },
                        x: {
                            title: { display: true, text: 'Дата', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: '#e2e8f0' } },
                        tooltip: { backgroundColor: '#1e293b' }
                    }
                }
            });
        }
    }

    const data2 = document.getElementById('rating-data-2');
    if (data2) {
        const json = JSON.parse(data2.textContent);
        const ctx = document.getElementById('ratingChart2');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: json.dates,
                    datasets: [{
                        label: `Рейтинг — ${json.team}`,
                        data: json.values,
                        borderColor: '#fb923c',
                        backgroundColor: '#fb923c33',
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: 0.8,
                            max: 1.3,
                            title: { display: true, text: 'Рейтинг (выше = лучше)', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        },
                        x: {
                            title: { display: true, text: 'Дата', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: '#e2e8f0' } },
                        tooltip: { backgroundColor: '#1e293b' }
                    }
                }
            });
        }
    }

    const mapData = document.getElementById('map-data');
    if (mapData) {
        const json = JSON.parse(mapData.textContent);
        const ctx = document.getElementById('mapComparisonChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: json.labels,
                    datasets: [
                        {
                            label: json.team1,
                            data: json.team1data,
                            backgroundColor: 'rgba(74, 222, 128, 0.7)',
                            borderColor: '#4ade80',
                            borderWidth: 1
                        },
                        {
                            label: json.team2,
                            data: json.team2data,
                            backgroundColor: 'rgba(251, 146, 60, 0.7)',
                            borderColor: '#fb923c',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            max: 100,
                            title: { display: true, text: 'Винрейт (%)', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        },
                        y: {
                            title: { display: true, text: 'Карта', color: '#e2e8f0' },
                            ticks: { color: '#e2e8f0' },
                            grid: { color: '#334155' }
                        }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: '#e2e8f0' } },
                        tooltip: { backgroundColor: '#1e293b' }
                    }
                }
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded — initCharts');
    initCharts();
});

htmx.on('htmx:afterSwap', () => {
    console.log('HTMX swap detected — redrawing charts');
    setTimeout(initCharts, 0);
});