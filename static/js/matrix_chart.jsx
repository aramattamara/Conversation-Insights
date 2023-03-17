let matrixChart;

function MatrixChart(props) {
    const config = {
        type: 'matrix',
        data: data,
        options: options
    };


    const options = {
        aspectRatio: 5,
        plugins: {
            legend: false,
            tooltip: {
                displayColors: false,
                callbacks: {
                    title() {
                        return '';
                    },
                    label(context) {
                        const v = context.dataset.data[context.dataIndex];
                        return ['d: ' + v.d, 'v: ' + v.v.toFixed(2)];
                    }
                }
            },
        },
        scales: scales,
        layout: {
            padding: {
                top: 10
            }
        }
    };


    const data = {
        datasets: [{
            label: 'My Matrix',
            data: generateData(),
            backgroundColor(c) {
                const value = c.dataset.data[c.dataIndex].v;
                const alpha = (10 + value) / 60;
                return helpers.color('green').alpha(alpha).rgbString();
            },
            borderColor(c) {
                const value = c.dataset.data[c.dataIndex].v;
                const alpha = (10 + value) / 60;
                return helpers.color('green').alpha(alpha).darken(0.3).rgbString();
            },
            borderWidth: 1,
            hoverBackgroundColor: 'yellow',
            hoverBorderColor: 'yellowgreen',
            width(c) {
                const a = c.chart.chartArea || {};
                return (a.right - a.left) / 53 - 1;
            },
            height(c) {
                const a = c.chart.chartArea || {};
                return (a.bottom - a.top) / 7 - 1;
            }
        }]
    };


    const scales = {
        y: {
            type: 'time',
            offset: true,
            time: {
                unit: 'day',
                round: 'day',
                isoWeekday: 1,
                parser: 'i',
                displayFormats: {
                    day: 'iiiiii'
                }
            },
            reverse: true,
            position: 'right',
            ticks: {
                maxRotation: 0,
                autoSkip: true,
                padding: 1,
                font: {
                    size: 9
                }
            },
            grid: {
                display: false,
                drawBorder: false,
                tickLength: 0
            }
        },
        x: {
            type: 'time',
            position: 'bottom',
            offset: true,
            time: {
                unit: 'week',
                round: 'week',
                isoWeekday: 1,
                displayFormats: {
                    week: 'MMM dd'
                }
            },
            ticks: {
                maxRotation: 0,
                autoSkip: true,
                font: {
                    size: 9
                }
            },
            grid: {
                display: false,
                drawBorder: false,
                tickLength: 0,
            }
        }
    };

    return <canvas id="matrix-chart"></canvas>
}

