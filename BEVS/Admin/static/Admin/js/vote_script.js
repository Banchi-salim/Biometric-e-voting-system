function updateVoteData(electionId) {
    fetch(`/vote-data/${electionId}/`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`Error fetching vote data for election ${electionId}`);
            }
        })
        .then(data => {
            const labels = Object.keys(data);
            const votes = Object.values(data);

            const ctx = document.getElementById(`voteChart-${electionId}`).getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Votes',
                        data: votes,
                        backgroundColor: ['#28a745', '#dc3545']
                    }]
                }
            });
        })
        .catch(error => {
            console.error(error);
            // You can add additional logic here, such as displaying an error message to the user
        });
}