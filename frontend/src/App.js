import React from 'react';
import './App.css';
import AnalyseQueries from './AnalyseQueries';
import PlayWithData from './PlayWithData';
import TwentyAreas from './TwentyAreas';
import AreaDetail from './AreaDetail';
import titles from './titles';
import details from './details';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (

    <Router>
      <Routes> {/* Use Routes instead of Switch */}
        <Route path="/" element={
          <div className="App">
            <div className="landing">
              <AnalyseQueries />
              <PlayWithData />
            </div>
          </div>} />

        <Route path="/analyse" element={<TwentyAreas titles={titles} />} /> 
        <Route path="/query/:queryId" element={<AreaDetail details={details} />} />

      </Routes>
    </Router>
    
  );
}

export default App;
