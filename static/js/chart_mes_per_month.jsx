let chartMesPerMonth;

function ChartMesPerMonth(props) {
    let memberNames = [];


    for (let member of props.members) {
        if (!props.selectedMemberIds[member['member_id']]) {
            continue;
        }
        let memberName = member['first_name'];
        memberNames.push(memberName);
    }

    const [months, setMonths] = React.useState([]);
    const [totalMes, setTotalMes] = React.useState([])

    React.useEffect(() => {
        fetch('/api/mes_per_month.json')
            .then((response) => response.json())
            .then((result) => {setMonths(result)});
    }, []);


    React.useEffect(() => {
        const chartContainer = document.getElementById('chart_mes_per_month');
        if (!chartContainer) {
            return;
        }
        chartMesPerMonth = new Chart(chartContainer, {
            type: 'line', data: {
                labels: months, datasets: [{
                    label: "Member " + memberNames, data: totalMes,
                }]
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
    }, [memberNames, totalMes, months]);

    return <canvas id="chart_mes_per_month"></canvas>;
}
