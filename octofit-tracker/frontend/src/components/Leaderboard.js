import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://supreme-orbit-v95qgwwpgpv3w6vv-8000.app.github.dev/api/leaderboard/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Sort the leaderboard data by score in descending order
        const sortedData = [...data].sort((a, b) => b.score - a.score);
        setLeaderboard(sortedData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard data:', error);
        setError('Failed to load leaderboard. Please try again later.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container">
      <h2 className="page-header">Leaderboard</h2>
      {leaderboard.length === 0 ? (
        <div className="alert alert-info">No leaderboard data available.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-primary">
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">User</th>
                <th scope="col">Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={entry.id}>
                  <td>
                    {index < 3 ? (
                      <span className={`badge bg-${index === 0 ? 'warning' : index === 1 ? 'secondary' : 'danger'}`}>
                        {index + 1}
                      </span>
                    ) : (
                      index + 1
                    )}
                  </td>
                  <td>{entry.user.username || 'Unknown'}</td>
                  <td>
                    <strong>{entry.score}</strong>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;