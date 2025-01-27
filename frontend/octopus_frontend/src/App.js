import React from 'react';
import './App.css';
import NavBar from './components/NavBar.js';
import SearchBar from './components/SearchBar';

function App() {
  return (
    <div classname = "App">
      <NavBar />
      <h1>Octopus_AI</h1>
      <div className = "SearchSection">
        <SearchBar />
      </div>
    </div>
  );
}

export default App;
