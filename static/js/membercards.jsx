function MemberCard(props) {

    // const [isSelected, setIsSelected] = React.useState(false);

    // const handleClick = () => {
    //     setIsSelected(!isSelected);
    // };

    return (
        <div className={`card member-card ${props.selected ? 'selected' : ''}`}
             onClick={props.toggleSelected}>
            <p>{props.fname} {props.lname}</p>
            <p>Username: @{props.member_name}</p>
            <p>Total Messages: {props.total}</p>
        </div>
    );
}

function MemberCollection() {

    const [members, setMembers] = React.useState([]);
    const [selectedMemberIds, setSelectedMemberIds] = React.useState({});

    React.useEffect(() => {
        fetch('/api/get_members.json')
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

    return (
        <React.Fragment>
            <div className="row">
                <div className="col-lg-6" id="members">
                        <SearchMembers setMembers={setMembers}/>
                    <br/>
                    <div className="cards-list">
                        {MemberCards}
                    </div>
                </div>
                <div className="col-lg-6">
                    <h2 className="text-center"> Data viz </h2>
                    <BarChart members={members} selectedMemberIds={selectedMemberIds}/>
                    <ChartMesPerMonth members={members} selectMemberIds={selectedMemberIds}/>
                </div>
            </div>
        </React.Fragment>
    );
}

ReactDOM.render(<MemberCollection/>, document.getElementById('container'));
