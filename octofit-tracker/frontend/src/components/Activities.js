import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://supreme-orbit-v95qgwwpgpv3w6vv-8000.app.github.dev/api/activity/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setActivities(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
        setError('Failed to load activities. Please try again later.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container">
      <h2 className="page-header">Activities</h2>
      {activities.length === 0 ? (
        <div className="alert alert-info">No activities found.</div>
      ) : (
        <div className="row">
          {activities.map(activity => (
            <div className="col-md-6 col-lg-4 mb-4" key={activity.id}>
              <div className="card h-100">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{activity.activity_type}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">
                    <strong>Duration:</strong> {activity.duration}
                  </p>
                  <p className="card-text">
                    <strong>User:</strong> {activity.user.username || 'Unknown'}
                  </p>
                </div>
                <div className="card-footer bg-white">
                  <button className="btn btn-outline-primary btn-sm">View Details</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Activities;