import React from 'react';
import { useNavigate } from 'react-router-dom';

const PlayWithData = () => {
  const navigate = useNavigate(); // Hook to get the navigate function

  return (
    <div className="half-page" onClick={() => navigate('/play')}>
      PLAY WITH DATA
    </div>
  );
};

export default PlayWithData;
