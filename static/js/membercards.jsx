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

function MemberCollection(props) {

    const [members, setMembers] = React.useState([]);
    const [selectedMemberIds, setSelectedMemberIds] = React.useState({});
    const [searchText, setSearchText] = React.useState('');

    function toggleSetSelected(memberId) {
        let newSelectedMemberIds = {...selectedMemberIds};
        newSelectedMemberIds[memberId] = !newSelectedMemberIds[memberId];
        setSelectedMemberIds(newSelectedMemberIds);
    }

    React.useEffect(() => {
        fetch('/search.json?search-text=' + encodeURIComponent(searchText))
            .then((response) => response.json())
            .then((data) => {
                setMembers(data)
            });
    }, [searchText]);


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
                    <div className="cards-list">
                        {MemberCards}
                    </div>
                </div>

                <div className="col-lg-6">
                    <h2 className="text-center"> Data viz </h2>
                    <BarChart members={members} selectedMemberIds={selectedMemberIds}/>
                </div>
            </div>
        </React.Fragment>
    );
}

ReactDOM.render(<MemberCollection/>, document.getElementById('container'));
