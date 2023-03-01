function UserCard(props) {
    return (
        <div className="user">
            <p>{props.fname} {props.lname}</p>
            <p>Username: {props.username}</p>
        </div>
    );
}

function UserCollection() {
    const [users, setUsers] = React.useState([]);

    React.useEffect(() => {
        fetch("/users.json")
            .then((response) => response.json())
            .then((data) => setUsers(data));
    }, []);

    const userCards = [];
    for (const user of users) {
        userCards.push(
            <UserCard
                key={user.user_id}
                fname={user.first_name}
                lname={user.last_name}
                username={user.username}
            />,
        );
    }


    return (
        <div className="card">
            {userCards}
        </div>
    );
}


ReactDOM.render(<UserCollection/>, document.getElementById('container'));
