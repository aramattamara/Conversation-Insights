let chartMesPerMonth;

function ChartMesPerMonth(props) {
    let memberNames = []
    let total_mes = []


    for (let member of props.members){

    }

    React.useEffect(() => {
        chartMesPerMonth = new Chart(
            document.querySelector('#chart-mes-per-month'),
            {
                type: 'line',
                data: {
                    labels: memberNames,
                    datasets: [
                        {
                            label: "Total Messages",
                            data: total_mes,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    title: {
                        display: true,
                        text: 'Chart Total Vizualization'
                    },

                },
                datasets: {
                    // bar: {
                    //     color: () => randomColor(),
                    // },
                },
                scales: {
                    y: {
                        min: 0,
                        max: 50,
                        ticks: {
                            stepSize: 5,
                        },
                    },
                },
            },
        );
    }, []);

    return <canvas id="chart_mes_per_month"></canvas>;
}
