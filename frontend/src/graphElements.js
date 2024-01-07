// graphElements.js
const graphElements = [
    // Nodes for clubs
    { data: { id: 'club1', label: 'Club 1' } },
    { data: { id: 'club2', label: 'Club 2' } },
    // Nodes for players
    { data: { id: 'player1', label: 'Player 1' } },
    { data: { id: 'player2', label: 'Player 2' } },
    // Node for a game
    { data: { id: 'game1', label: 'Game 1' } },
    // Edges for relationships
    { data: { id: 'edge1', source: 'player1', target: 'club1', label: 'Plays for' } },
    { data: { id: 'edge2', source: 'player2', target: 'club2', label: 'Plays for' } },
    { data: { id: 'edge3', source: 'club1', target: 'game1', label: 'Participated in' } },
    { data: { id: 'edge4', source: 'club2', target: 'game1', label: 'Participated in' } },
  ];
  
  export default graphElements;
  