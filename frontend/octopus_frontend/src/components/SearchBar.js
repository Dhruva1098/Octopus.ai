import React from 'react';
import './SearchBar.css';

function SearchBar() {
  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Search..."
        className="search-input"
      />
      <button className="search-button">Search My Notes</button>
    </div>
  );
}

export default SearchBar;