let chartMesPerMonth;

function ChartMesPerMonth(props) {
    let memberNames = [];


    // for (let member of props.members) {
    //     if (!props.selectedMemberIds[member['member_id']]) {
    //         continue;
    //     }
    //     let memberName = member['first_name'];
    //     memberNames.push(memberName);
    // }

    const [memberMonthCounts, setMemberMonthCounts] = React.useState([]);
    // const [totalMes, setTotalMes] = React.useState([])

    React.useEffect(() => {
        fetch('/api/mes_per_month.json')
            .then((response) => response.json())
            .then((result) => {
                setMemberMonthCounts(result);
            });
    }, []);


    React.useEffect(() => {
        const chartContainer = document.getElementById('chart_mes_per_month');
        if (!chartContainer) {
            return;
        }
        if (chartMesPerMonth) {
            chartMesPerMonth.destroy();
            chartMesPerMonth = null;
        }
        // const months = [];
        // for (a in memberMonthCounts) {
        //     months.push(a['month'].toString());
        // }
        // const months = memberMonthCounts.map((a) => a['month']);

        // E.g. {388268832: [{'cnt': 5, 'month': 3}]}
        const member = new Map(Object.entries(memberMonthCounts));
        console.log('start');


        let datasets = [];
        for (let [key, value] of member) {

            let data = {};
            for (let i in value) {
                let mm = value[i];
                let monName = MONTHS[mm['month'] - 1];
                data[monName] = mm['cnt'];
            }

            // console.log(data);
            datasets.push({
                label: "Member " + key,
                data: data
            });
        }
        console.log(datasets);

        // datasets = [{
        //     label: "Member 123",
        //     data: {
        //         'July': 10,
        //         'August': 20,
        //     }
        // }]

        chartMesPerMonth = new Chart(chartContainer, {
            type: 'line',
            data: {
                datasets: datasets,
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    title: {
                        display: true,
                        text: 'By Month'
                    },
                    colorschemes: {
                        scheme: 'brewer.Paired12'
                    },
                },
                scales: {
                    x: {
                        grid: {
                            tickColor: 'red'
                        },
                        ticks: {
                            color: 'blue',
                        }
                    },
                    y: {
                        suggestedMin: 0,
                        suggestedMax: 100,
                    }
                },
            },
        },);

    }, [memberNames, memberMonthCounts]);

    return <canvas id="chart_mes_per_month" width="400" height="300"></canvas>;
}
