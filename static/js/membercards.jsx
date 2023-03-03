import React from "react";

function MemberCard(props) {
    return (
        <div className="member">
            <p>{props.fname} {props.lname}</p>
            <p>Username: @{props.username}</p>
            <p>Total Messages: {props.total}</p>
        </div>
    );
}

function MemberCollection() {
    const [members, setMembers] = React.useState([]);

    React.useEffect(() => {
        fetch("/members.json")
            .then((response) => response.json())
            .then((data) => setUsers(data));
    }, []);

    const MemberCards = [];
    for (const member of members) {
        MemberCards.push(
            <MemberCard
                key={user.user_id}
                fname={user.first_name}
                lname={user.last_name}
                username={user.username}
                total={user.total}
            />,
        );
    }

    function onMySubmit(evt) {
        evt.preventDefault()

        React.useEffect(() => {
            fetch('/search.json')
                .then((response) => response.json())
                .then((data) => {
                    setMembers(data)
                })
        }, []);
    }

    return (
        <React.Fragment>
            <!-- MEMBER SEARCH FORM -->
            <div className="search-box">
                <form onSubmit={onMySubmit} id="search-result" className="text-center">
                    <h5><label htmlFor="search-text">Search Memeber:</label></h5>
                    <input type="text" name="search-text" id="search-text" className="form-control"
                           placeholder="Search all"/>
                </form>
            </div>
            <br/>
                <div className="card">
                    {MemberCards}
                </div>

        </React.Fragment>
);
}

ReactDOM.render(<UserCollection/>, document.getElementById('members'));
