// TableComponent.js
import React from 'react';

const TableComponent = ({ tableData }) => {
  if (!tableData) {
    return <p>No data provided.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          {tableData.columns.map((header, index) => (
            <th key={index}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {tableData.rows.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TableComponent;
