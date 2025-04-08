import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://supreme-orbit-v95qgwwpgpv3w6vv-8000.app.github.dev/api/teams/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setTeams(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError('Failed to load teams. Please try again later.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container">
      <h2 className="page-header">Teams</h2>
      {teams.length === 0 ? (
        <div className="alert alert-info">No teams found.</div>
      ) : (
        <div className="row">
          {teams.map(team => (
            <div className="col-md-6 col-lg-4 mb-4" key={team.id}>
              <div className="card h-100">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <h6 className="card-subtitle mb-3">Team Members</h6>
                  {team.members && team.members.length > 0 ? (
                    <ul className="list-group">
                      {team.members.map(member => (
                        <li className="list-group-item d-flex justify-content-between align-items-center" key={member.id}>
                          {member.username || 'Unknown'}
                          <span className="badge bg-primary rounded-pill">Active</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="card-text">No members in this team.</p>
                  )}
                </div>
                <div className="card-footer bg-white">
                  <button className="btn btn-outline-primary btn-sm">Join Team</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Teams;