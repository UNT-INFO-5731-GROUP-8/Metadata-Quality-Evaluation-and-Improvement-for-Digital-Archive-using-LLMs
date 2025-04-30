// Tab Management
function openTab(evt, tabName) {
    const tabcontents = document.getElementsByClassName("tabcontent");
    const tablinks = document.getElementsByClassName("tablink");
    
    // Hide all tab content
    Array.from(tabcontents).forEach(tab => tab.style.display = "none");
    
    // Remove active class from all tabs
    Array.from(tablinks).forEach(link => link.classList.remove("active"));
    
    // Show selected tab and mark button as active
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
}

// Common UI Functions
function showLoader(context) {
    context.querySelector('.loader').classList.remove('hidden');
}

function hideLoader(context) {
    context.querySelector('.loader').classList.add('hidden');
}

function showError(context, message) {
    const errorDiv = context.querySelector('.error-message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function clearError(context) {
    context.querySelector('.error-message').classList.add('hidden');
}

// Generation Form Handler - Updated
document.getElementById('generateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const resultsDiv = document.getElementById('generateResults');
    const formData = new FormData(form);
    
    showLoader(resultsDiv);
    clearError(resultsDiv);
    
    try {
        const response = await axios.post('/generate', formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
        
        // Clear previous results
        resultsDiv.querySelector('.result-table').innerHTML = '';
        
        // Display batch information
        const batchInfo = document.createElement('div');
        batchInfo.className = 'batch-info';
        batchInfo.innerHTML = `
            <div class="batch-card">
                <h3>Generation Complete</h3>
                <div class="batch-details">
                    <div class="detail-item">
                        <span class="detail-label">Batch ID:</span>
                        <span class="detail-value">${response.data.batch_id}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Documents Processed:</span>
                        <span class="detail-value">${response.data.stats.processed}</span>
                    </div>
                </div>
            </div>
        `;
        
        resultsDiv.querySelector('.result-table').appendChild(batchInfo);
        resultsDiv.querySelector('.result-table').classList.remove('hidden');
        
    } catch (error) {
        showError(resultsDiv, `Generation failed: ${error.response?.data?.detail || error.message}`);
    } finally {
        hideLoader(resultsDiv);
    }
});

// // Validation Form Handler
// document.getElementById('validateForm').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const form = e.target;
//     const resultsDiv = document.getElementById('validateResults');
//     const formData = new FormData(form);
    
//     showLoader(resultsDiv);
//     clearError(resultsDiv);
    
//     try {
//         const response = await axios.post('/validate', formData, {
//             headers: {'Content-Type': 'multipart/form-data'}
//         });
//         console.log("Response : ", response)
//         // Update overall score
//         document.getElementById('overallScore').textContent = 
//             response.data.overall.toFixed(1);
        
//         // Prepare chart data
//         const scores = response.data.scores;
//         console.log("Scores : ",scores)
//         const metrics = Object.keys(scores[0]);
//         console.log("Everything done")

//         const dataset = {
//             label: 'Validation Scores',
//             data: metrics.map(metric => 
//                 scores.reduce((acc, curr) => acc + curr[metric], 0) / scores.length
//             ),
//             backgroundColor: 'rgba(54, 162, 235, 0.2)',
//             borderColor: 'rgba(54, 162, 235, 1)'
//         };
//         console.log("Everything done")
        
//         // Render/Update chart
//         const ctx = document.getElementById('scoreChart').getContext('2d');
//         if(window.scoreChart) window.scoreChart.destroy();
        
//         window.scoreChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: metrics.map(m => m.replace(/_/g, ' ').toUpperCase()),
//                 datasets: [dataset]
//             },
//             options: {
//                 responsive: true,
//                 scales: {
//                     y: {
//                         beginAtZero: true,
//                         max: 10
//                     }
//                 }
//             }
//         });
//         console.log("Everything done")
//         // Show results section
//         resultsDiv.querySelector('.chart-container').classList.remove('hidden');
//         resultsDiv.querySelector('.score-summary').classList.remove('hidden');
        
//     } catch (error) {
//         showError(resultsDiv, `Validation failed: ${error.response?.data?.detail || error.message}`);
//     } finally {
//         hideLoader(resultsDiv);
//     }
// });

document.getElementById('validateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const resultsDiv = document.getElementById('validateResults');
    const formData = new FormData(form);
    
    showLoader(resultsDiv);
    clearError(resultsDiv);
    
    try {
        const response = await axios.post('/validate', formData);
        const scores = transformScores(response.data.scores);
        const overall = response.data.overall;

        const metrics = Object.keys(scores[0]).filter(k => k !== 'overall_score');
        
        const barDataset = {
            label: 'Average Scores',
            data: metrics.map(metric => {
                const values = scores.map(s => s[metric]);
                return average(values);
            }),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)'
        };

        document.getElementById('overallScore').textContent = overall.toFixed(1);
        renderCharts(metrics, barDataset, overall);

        
        resultsDiv.querySelector('.chart-container').classList.remove('hidden');
        resultsDiv.querySelector('.score-summary').classList.remove('hidden');
        
    } catch (error) {
        showError(resultsDiv, `Validation failed: ${error.message}`);
    } finally {
        hideLoader(resultsDiv);
    }
});

// Helper functions
function transformScores(scoresObject) {
    const entries = {};
    
    // First create entry objects for each index
    Object.entries(scoresObject).forEach(([metric, values]) => {
        Object.entries(values).forEach(([index, score]) => {
            if (!entries[index]) entries[index] = {};
            entries[index][metric] = score;
        });
    });
    
    // Convert to array and sort by index
    return Object.values(entries)
        .sort((a, b) => Object.keys(a)[0] - Object.keys(b)[0]);
}

function average(arr) {
    const valid = arr.filter(Number.isFinite);
    return valid.length ? valid.reduce((a, b) => a + b, 0) / valid.length : 0;
}
// function safeChartUpdate(ctx, config) {
//     // Destroy existing chart properly
//     if (window.scoreChart) {
//         try {
//             if (typeof window.scoreChart.destroy === 'function') {
//                 window.scoreChart.destroy();
//             }
//         } catch (e) {
//             console.warn('Error destroying previous chart:', e);
//         }
//         window.scoreChart = null;
//     }

//     // Create new chart instance
//     try {
//         window.scoreChart = new Chart(ctx, config);
//     } catch (e) {
//         console.error('Chart creation failed:', e);
//         window.scoreChart = null;
//     }
// }

// // Usage in renderChart:
// function renderChart(labels, dataset) {
//     const ctx = document.getElementById('scoreChart').getContext('2d');
//     safeChartUpdate(ctx, {
//         type: 'bar',
//         data: {
//             labels: labels.map(l => l
//                 .replace(/_/g, ' ')
//                 .replace(/_score/g, '')
//                 .toUpperCase()),
//             datasets: [dataset]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     max: 10,
//                     ticks: {
//                         callback: v => `${v}/10`
//                     }
//                 }
//             }
//         }
//     });
// }

// function renderCharts(metrics, barDataset, overallScore) {
//     const barCtx = document.getElementById('scoreChart').getContext('2d');
//     const pieCtx = document.getElementById('pieChart').getContext('2d');
    
//     // Destroy existing charts
//     safeChartUpdate(barCtx, 'bar', {
//         labels: metrics.map(l => l
//             .replace(/_/g, ' ')
//             .replace(/_score/g, '')
//             .toUpperCase()),
//         datasets: [barDataset]
//     });
    
//     renderPieChart(pieCtx, overallScore);
// }
// Updated safeChartUpdate function
function safeChartUpdate(chartVar, ctx, chartType, config) {
    try {
        // Destroy existing chart if it exists
        if (chartVar && typeof chartVar.destroy === 'function') {
            chartVar.destroy();
        }
    } catch (e) {
        console.warn('Error destroying chart:', e);
    }

    // Create new chart instance
    try {
        return new Chart(ctx, {
            type: chartType,
            ...config
        });
    } catch (e) {
        console.error('Chart creation failed:', e);
        return null;
    }
}

// Updated renderCharts function
function renderCharts(metrics, barDataset, overallScore) {
    const barCtx = document.getElementById('scoreChart').getContext('2d');
    const pieCtx = document.getElementById('pieChart').getContext('2d');

    // Update bar chart
    window.scoreChart = safeChartUpdate(
        window.scoreChart,
        barCtx,
        'bar',
        {
            data: {
                labels: metrics.map(l => l
                    .replace(/_/g, ' ')
                    .replace(/_score/g, '')
                    .toUpperCase()),
                datasets: [{
                    ...barDataset,
                    borderRadius: 8,
                    borderWidth: 0,
                    backgroundColor: createGradient(barCtx),
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2,
                            callback: v => `${v}/10`
                        }
                    }
                }
            }
        }
    );

    // Update pie chart
    window.pieChart = safeChartUpdate(
        window.pieChart,
        pieCtx,
        'pie',
        {
            data: {
                labels: ['Achieved Score', 'Remaining'],
                datasets: [{
                    data: [overallScore, 10 - overallScore],
                    backgroundColor: ['#36a2eb', '#e0e0e0']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    );
}

// Initialize chart variables at the start
window.scoreChart = null;
window.pieChart = null;

// Gradient helper function
function createGradient(ctx) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, '#36a2eb');
    gradient.addColorStop(1, '#3b83f6');
    return gradient;
}

function renderPieChart(ctx, score) {
    if(window.pieChart && typeof window.pieChart.destroy === 'function') {
        window.pieChart.destroy();
    }
    
    const remaining = 10 - score;
    
    window.pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Achieved Score', 'Remaining'],
            datasets: [{
                data: [score, remaining],
                backgroundColor: ['#36a2eb', '#ff6384'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw.toFixed(1)}/10`;
                        }
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// function safeChartUpdate(ctx, chartType, config) {
//     // Destroy existing chart
//     const chartVar = chartType === 'bar' ? window.scoreChart : window.pieChart;
//     if (chartVar && typeof chartVar.destroy === 'function') {
//         chartVar.destroy();
//     }

//     // Create new chart
//     if(chartType === 'bar') {
//         window.scoreChart = new Chart(ctx, {
//             type: chartType,
//             data: config,
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 scales: {
//                     y: {
//                         beginAtZero: true,
//                         max: 10,
//                         ticks: {
//                             callback: v => `${v}/10`
//                         }
//                     }
//                 }
//             }
//         });
//     }
// }