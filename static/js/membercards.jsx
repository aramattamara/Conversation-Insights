function MemberCard(props) {
    return (
        <div className="member">
            <p>{props.fname} {props.lname}</p>
            <p>Username: @{props.member_name}</p>
            <p>Total Messages: {props.total}</p>
        </div>
    );
}

function MemberCollection() {

    const [members, setMembers] = React.useState([]);

    React.useEffect(() => {
        fetch("/members.json")
            .then((response) => response.json())
            .then((data) => setMembers(data));
    }, []);

    const MemberCards = [];
    for (const member of members) {
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

    function onMySubmit(evt) {
        evt.preventDefault()

        fetch('/search.json?search-text=' + encodeURIComponent(searchText))
            .then((response) => response.json())
            .then((data) => {
                setMembers(data)
            });
    }
    const [searchText, setSearchText] = React.useState('');

    return (
        <React.Fragment>
            <div className="search-box">
                <form onChange={onMySubmit} id="search-result" className="text-center">
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
                {MemberCards}
            </div>
        </React.Fragment>
    );
}

ReactDOM.render(<MemberCollection/>, document.getElementById('members'));
