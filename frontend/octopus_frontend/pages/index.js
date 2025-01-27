// filepath: /my-next-app/pages/index.js
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <nav>
        <div className="navbar-logo">LOGO</div>
        <div className="navbar-buttons">
          <button className="navbar-notes">My Notes</button>
          <button className="navbar-add">
            <Link href="/new">
              <a className="navbar-link">+</a>
            </Link>
          </button>
        </div>
      </nav>
      <div className="SearchSection">
        <img src="/path/to/logo.png" alt="Logo" className="search-logo" />
        <div className="search-container">
          <input type="text" placeholder="Search..." className="search-input" />
          <button className="search-button">Search My Notes</button>
        </div>
      </div>
    </div>
  );
}