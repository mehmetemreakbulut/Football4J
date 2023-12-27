import React from 'react';
import { useNavigate } from 'react-router-dom';

const AnalyseQueries = () => {
  const navigate = useNavigate(); // Hook to get the navigate function

  return (
    <div className="half-page" onClick={() => navigate('/analyse')}>
      ANALYSE QUERIES
    </div>
  );
};

export default AnalyseQueries;
