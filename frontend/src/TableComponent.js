// TableComponent.js
import React, {useState} from 'react';
import './table.css';

const TableComponent = ({ tableData }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });

  const sortedData = React.useMemo(() => {
    let sortableItems = [...tableData];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [tableData, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  if (!tableData || tableData.length === 0) {
    return <p>No data provided.</p>;
  }

  // Extract column headers from the keys of the first object
  const columns = Object.keys(tableData[0]);

  return (
    <table>
      <thead>
        <tr>
          {columns.map((header) => (
            <th
            key={header}
            onClick={() => requestSort(header)}
            className={sortConfig.key === header ? sortConfig.direction : ''}
          >
            {header}
          </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {columns.map((column, columnIndex) => (
              <td key={columnIndex}>{row[column]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TableComponent;
