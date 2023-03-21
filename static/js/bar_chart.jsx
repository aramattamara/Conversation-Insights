let barChart;

function BarChart(props) {
    let memberNames = [];
    let total_mes = [];

    // let isNoneSelected = true;
    // for (let member of members) {
    //     if (selectedMemberIds[member['member_id']]) {
    //         isNoneSelected = false;
    //         break;
    //     }
    // }


    for (let member of props.selectedMembers) {
        let memberName = member['first_name'];
        let total = member['total'];
        memberNames.push(memberName);
        total_mes.push(total);
    }

    React.useEffect(() => {
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
                            text: 'Total'
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
                        x: {
                            border: {
                                color: 'red'
                            },
                        },
                        y: {
                            min: 0,
                            max: 300,
                            ticks: {
                                stepSize: 5,
                            },
                        },
                    },
                },
            },
        );
    }, [memberNames, total_mes]);

    return <canvas id="bar-chart"></canvas>;
}