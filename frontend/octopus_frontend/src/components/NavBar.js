import React from 'react';
import './NavBar.css';

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">LOGO</div>
      <div className="navbar-buttons">
        <button className="navbar-notes">My Notes</button>
        <button className="navbar-add">+</button>
      </div>
    </nav>
  );
}

export default NavBar;