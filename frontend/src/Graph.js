import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import graphElements from './graphElements';
import './GraphStyles.css'; 

const Graph = () => {
  // Define the layout for the graph
  const layout = {
    name: 'cose', // Compound Spring Embedder layout
    idealEdgeLength: 100,
    nodeOverlap: 20,
  };

  // Import styles from external CSS file
  const stylesheet = [
    {
      selector: 'node',
      style: 'node' // Class name from CSS file
    },
    {
      selector: 'edge',
      style: 'edge' // Class name from CSS file
    }
  ];

  // Event handlers for nodes and edges
  const handleNodeClick = (event) => {
    const node = event.target;
    alert(`Node clicked: ${node.id()}`);
  };

  const handleEdgeClick = (event) => {
    const edge = event.target;
    alert(`Edge clicked: ${edge.id()}`);
  };

  return (
    <CytoscapeComponent
      elements={CytoscapeComponent.normalizeElements(graphElements)}
      style={{ width: '100%', height: '600px' }}
      layout={layout}
      stylesheet={stylesheet}
      cy={(cy) => {
        cy.on('tap', 'node', handleNodeClick);
        cy.on('tap', 'edge', handleEdgeClick);
      }}
    />
  );
};

export default Graph;
