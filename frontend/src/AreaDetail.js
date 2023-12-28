// AreaDetail.js
import React from 'react';
import { useParams } from 'react-router-dom';
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
      <h1>{detail.title}</h1>
      <p>{detail.description}</p>
      <TableComponent tableData={detail.table} />
    </div>
  );
};

export default AreaDetail;
