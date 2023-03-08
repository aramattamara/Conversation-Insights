let barChart;

function BarChart(props){
    let memberNames = [];
    let total_mes = [];

    // let isNoneSelected = true;
    // for (let member of members) {
    //     if (selectedMemberIds[member['member_id']]) {
    //         isNoneSelected = false;
    //         break;
    //     }
    // }

    for (let member of props.members) {
        if (!props.selectedMemberIds[member['member_id']]) {
            continue;
        }
        let memberName = member['first_name'];
        let total = member['total'];
        memberNames.push(memberName);
        total_mes.push(total);
    }


    if (barChart) {
        barChart.destroy();
        barChart = null;
    }

    barChart = new Chart(
        document.querySelector('#bar-chart'),
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
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    title: {
                        display: true,
                        text: 'Chart Total Vizualization'
                    },
                    colorschemes: {
                        scheme: 'brewer.Paired12'
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

    return <canvas id="bar-chart"></canvas>;
}