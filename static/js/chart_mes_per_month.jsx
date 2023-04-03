let chartMesPerMonth;

function ChartMesPerMonth(props) {
    let memberNames = [];
    for (let member of props.selectedMembers) {
        let memberName = member['first_name'];
        memberNames.push(memberName);
    }

    const memberById = {};
    for (let member of props.selectedMembers) {
        memberById[member['member_id']] = member;
    }
    // console.log(memberById);

    const [memberMonthCounts, setMemberMonthCounts] = React.useState([]);
    // const [totalMes, setTotalMes] = React.useState([]);
    const selectedMemberIds = props.selectedMembers.map((m) => m['member_id']);

    React.useEffect(() => {
        if (selectedMemberIds.length > 0) {
            fetch('/api/mes_per_month.json?selectedIds=' + selectedMemberIds.join(',') + '&chat_id=' + props.chatId)
                .then((response) => response.json())
                .then((result) => {
                    setMemberMonthCounts(result);
                });
        }
        else {
            setMemberMonthCounts([])
        }
    }, [props.selectedMembers]);


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


        // E.g. {388268832: [{'cnt': 5, 'year': 2023, 'month': 3}]}
        const stats = new Map(Object.entries(memberMonthCounts));
        // console.log('start');

        const selectedStats = {};
        for (let [memberId, value] of stats) {
            if (memberById[memberId]) {
                selectedStats[memberId] = value;
            }
        }

        let datasets = [];

        for (let [memberId, value] of stats) {
            if (!memberById[memberId]) {
                continue;
            }

            const date = new Date(value[0]["year"], value[0]["month"]-1, 1)
            // E.g. {'January': 123}
            let data = {};
            for (let i in value) {
                let ym = value[i];

                for (;(date.getFullYear() < ym["year"] ||(date.getFullYear() === ym["year"] && date.getMonth() < ym["month"]));) {
                    let monName = MONTHS[date.getMonth()] + " " + date.getFullYear();
                    data[monName] = 0;
                    date.setMonth(date.getMonth() + 1)
                }

                let monName = MONTHS[ym["month"] - 1] + " " + ym["year"];
                data[monName] = ym['cnt'];
            }

            // console.log(data);
            datasets.push({
                label: "Member " + memberById[memberId]["first_name"],
                data: data
            });
        }
        // console.log(datasets);

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
                        suggestedMax: 30,
                    }
                },
            },
        },);

    }, [memberMonthCounts]);

    return <canvas id="chart_mes_per_month" width="400" height="300"></canvas>;
}
