// AreaDetail.js
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import TableComponent from './TableComponent';


const AreaDetail = ({ details }) => {
  const { queryId } = useParams();
  console.log('queryId', queryId);
  const detail = details.find(item => item.queryId.toString() === queryId);
  console.log('detail');

  if (!detail) {
    return <p>Detail not found!</p>;
  }

  return (
    <div className="area-detail">
       <Link to="/" style={{
        display: 'inline-block',
        margin: '10px 0',
        padding: '10px 20px',
        backgroundColor: '#000000',
        color: '#ffffff',
        textDecoration: 'none',
        borderRadius: '5px',
        textAlign: 'center',
        transition: 'background-color 0.2s',
      }}>
        Home
      </Link>
      <h1>{detail.title}</h1>
      <p>{detail.description}</p>

      {queryId === "18" && (
        <img src="https://i.imgur.com/MjeXNNq.gif"/>
      )}

      <TableComponent tableData={detail.table} />
    </div>
  );
};

export default AreaDetail;
