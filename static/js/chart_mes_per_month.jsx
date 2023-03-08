let chartMesPerMonth;

function ChartMesPerMonth(props){
    React.useEffect(() => {
        fetch('/yjkyi.json?search-text')
            .then((response) => response.json())
            .then((data) => {
                setMessages(data)
            });
    }, [searchText]);





    chartMesPerMonth = new Chart(
        document.querySelector('#test-chart'),
        {
            type: 'bar',
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
                plugins: {
                    colorschemes: {
                        scheme: 'brewer'
                    },
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
        },
    );

    return <canvas id="test-chart"></canvas>;
}