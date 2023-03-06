function MemberCard(props) {

    const [isSelected, setIsSelected] = React.useState(false);

    const handleClick = () => {
        setIsSelected(!isSelected);
    };

    return (
        <div className={`member-card ${isSelected ? 'selected' : ''}`} onClick={handleClick}>
            <p>{props.fname} {props.lname}</p>
            <p>Username: @{props.member_name}</p>
            <p>Total Messages: {props.total}</p>
        </div>
    );
}

function MemberList(props) {
    // React.useEffect(() => {
    //     fetch("/members.json")
    //         .then((response) => response.json())
    //         .then((data) => setMembers(data));
    // }, []);

    const MemberCards = [];
    for (const member of props.members) {
        MemberCards.push(
            <MemberCard
                key={member.member_id}
                fname={member.first_name}
                lname={member.last_name}
                member_name={member.member_name}
                total={member.total}
            />,
        );
    }

    return <div>{MemberCards}</div>
}

let testChart;
function MemberCollection(props) {

    const [members, setMembers] = React.useState([]);

    const [searchText, setSearchText] = React.useState('');

    React.useEffect(() => {
        fetch('/search.json?search-text=' + encodeURIComponent(searchText))
            .then((response) => response.json())
            .then((data) => {
                setMembers(data)
            });
    }, [searchText]);

    React.useEffect(() => {
        let member_name_array = [];
        let total_mes = [];

        for (let member of members) {
            let member_name = member['first_name'];
            let total = member['total'];
            member_name_array.push(member_name);
            total_mes.push(total);
        }


        if (testChart) {
            testChart.destroy();
            testChart = null;
        }

        testChart = new Chart(
            document.querySelector('#test-chart'),
            {
                type: 'bar',
                data: {
                    labels: member_name_array,
                    datasets: [
                        {data: total_mes}
                    ]
                },
                options: {
                    datasets: {
                        bar: {
                            backgroundColor: () => randomColor(),
                        },
                    },
                    scales: {
                        yAxes: [
                            {
                                ticks: {
                                    min: 0,
                                    max: 40,
                                },
                            },
                        ],
                    },
                },
            }
        );
    }, [members]);


    return (
        <React.Fragment>
            <div className="search-box">

                <form id="search-result" className="text-center">
                    <h5><label htmlFor="search-text">Search Memeber:</label></h5>
                    <input type="text"
                           id="search-text"
                           className="form-control"
                           placeholder="Search all"
                           value={searchText}
                           onChange={(e) => setSearchText(e.target.value)}
                    />
                </form>
            </div>
            <br/>
            <div className="card">
                <MemberList members={members}/>
            </div>
        </React.Fragment>
    );
}

ReactDOM.render(<MemberCollection/>, document.getElementById('members'));
