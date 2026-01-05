function initRatingChart(canvasId, dates, values, teamName, color = '#60a5fa') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: `Рейтинг - ${teamName}`,
                data: values,
                borderColor: color,
                backgroundColor: color + '33',
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
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

function initMapComparisonChart(labels, team1Data, team2Data, team1Name, team2Name) {
    const ctx = document.getElementById('mapComparisonChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: team1Name,
                    data: team1Data,
                    backgroundColor: 'rgba(74, 222, 128, 0.7)',
                    borderColor: '#4ade80',
                    borderWidth: 1
                },
                {
                    label: team2Name,
                    data: team2Data,
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