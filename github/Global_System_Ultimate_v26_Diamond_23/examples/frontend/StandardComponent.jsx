import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Standard Component Template (v37.0)
 * Engine: Speckit v2.0
 */
const StandardComponent = ({ title, apiEndpoint }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(apiEndpoint);
        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [apiEndpoint]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="standard-component">
      <h1>{title}</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

StandardComponent.propTypes = {
  title: PropTypes.string.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
};

export default StandardComponent;
