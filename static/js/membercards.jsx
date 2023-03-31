function MemberCard(props) {

    // const [isSelected, setIsSelected] = React.useState(false);

    // const handleClick = () => {
    //     setIsSelected(!isSelected);
    // };

    return (
        <div className={`member-card ${props.selected ? 'selected' : ''}`}
             onClick={props.toggleSelected}>
            <p>{props.fname} {props.lname}</p>
            <p>Username: @{props.member_name}</p>
            <p>Total Messages: {props.total}</p>
        </div>
    );
}

function MemberCollection(props) {
    props['chat_id']
    const [members, setMembers] = React.useState([]);
    const [selectedMemberIds, setSelectedMemberIds] = React.useState({});

    React.useEffect(() => {
        fetch('/api/get_members.json?chat_id=' + props.chat_id)
            .then((response) => response.json())
            .then((result) => {
                setMembers(result)
            });
    }, []);

    function toggleSetSelected(memberId) {
        let newSelectedMemberIds = {...selectedMemberIds};
        newSelectedMemberIds[memberId] = !newSelectedMemberIds[memberId];
        setSelectedMemberIds(newSelectedMemberIds);
    }




    const MemberCards = [];
    for (const member of members) {
        MemberCards.push(
            <MemberCard
                key={member.member_id}
                selected={selectedMemberIds[member.member_id]}
                toggleSelected={() => toggleSetSelected(member.member_id)}
                fname={member.first_name}
                lname={member.last_name}
                member_name={member.member_name}
                total={member.total}
            />,
        );
    }

    if (MemberCards.length === 0) {
        MemberCards.push(
            <div key='0' className="not-found">
                No members found...
            </div>
        )
    }

    const selectedMembers = [];
    for (let member of members) {
        if (selectedMemberIds[member['member_id']]) {
            selectedMembers.push(member);
        }
    }

    function handleSortTotalMaxMin() {
        let sortedMemberCard = [...members].sort((a, b) => {
            return b.total - a.total;
        })
        setMembers(sortedMemberCard)
    }

    function handleSortTotalMinMax() {
        let sortedMemberCard = [...members].sort((a, b) => {
            return a.total - b.total;
        })
        setMembers(sortedMemberCard)
    }

    return (
        <React.Fragment>
            <div className="row">
                <div className="col-6" id="members">
                    <SearchMembers setMembers={setMembers}/>
                    <br/>
                    <div className="sort">
                        <button onClick={handleSortTotalMaxMin} id="sort-max-min">Total: Max to Min</button>
                        <button onClick={handleSortTotalMinMax} id="sort-min-max">Total: Min to Max</button>
                    </div>
                    <br/>
                    <div className="cards-list">
                        {MemberCards}
                    </div>
                </div>
                <div className="col-6">
                    <h2 className="text-center"> Data Vizualization </h2>
                    <BarChart selectedMembers={selectedMembers}/>
                    <ChartMesPerMonth selectedMembers={selectedMembers}/>
                </div>
            </div>
        </React.Fragment>
    );
}

const chat_id = document.getElementById("chat_id")
ReactDOM.render(<MemberCollection chat_id={chat_id}/>, document.getElementById('container'));
