function SearchMember(){
    const [searchText, setSearchText] = React.useState('');

    React.useEffect(() => {
        fetch('/search.json?search-text=' + encodeURIComponent(searchText))
            .then((response) => response.json())
            .then((data) => {
                setMembers(data)
            });
    }, [searchText]);

    return(
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
    )
}
