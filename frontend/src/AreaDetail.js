// AreaDetail.js
import React from 'react';
import { useParams } from 'react-router-dom';
import TableComponent from './TableComponent';

const AreaDetail = ({ data }) => {
  const { queryId } = useParams();
  const detail = data.find(item => item.queryId === queryId);

  return (
    <div className="area-detail">
      <h1>{detail.title}</h1>
      <p>{detail.description}</p>
      <TableComponent tableData={detail.table} />
    </div>
  );
};

export default AreaDetail;
