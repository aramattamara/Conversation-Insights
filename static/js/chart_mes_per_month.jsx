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
        const m = new Map(Object.entries(memberMonthCounts));
        console.log('start');

        const datasets = [];
        for (let [key, value] of m) {
            let data = {
                'x': value.map((v) => v['cnt']),
                'y': value.map((v) => v['month']),
            };
            console.log(data);
            datasets.push({
                label: "Member " + key,
                data: data
            });
        }

        chartMesPerMonth = new Chart(chartContainer, {
            type: 'line', data: {
                // labels: memberMonthCounts,
                datasets: datasets,
            }, options: {
                responsive: true, tooltip: {
                    mode: 'index', intersect: false
                }, title: {
                    display: true, text: 'Chart by Months Vizualization'
                },

            }, datasets: {
                // bar: {
                //     color: () => randomColor(),
                // },
            }, scales: {
                y: {
                    min: 0, max: 50, ticks: {
                        stepSize: 5,
                    },
                },
            },
        },);
    }, [memberNames, memberMonthCounts]);

    return <canvas id="chart_mes_per_month"></canvas>;
}
