// TwentyAreas.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const TwentyAreas = ({ titles }) => {
  const navigate = useNavigate(); // Hook to get the navigate function
  const handleClick = (index) => {
    navigate(`/query/${index}`);
  };

  return (
    <div className="twenty-areas-container">
      {titles.map((title, index) => (
        <div
          key={title}
          className="area"
          onClick={() => handleClick(index)}
        >
          {title}
        </div>
      ))}
    </div>
  );
};

export default TwentyAreas;
