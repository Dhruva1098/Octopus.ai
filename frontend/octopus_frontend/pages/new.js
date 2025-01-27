// filepath: /my-next-app/pages/new.js
import { useState } from 'react';

export default function CreateNotePage() {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const handleSave = () => {
    // Implement save logic here
    console.log('Title:', title, 'Body:', body);
  };

  return (
    <div className="create-note-container">
      <nav className="navbar">
        <input
          type="text"
          className="navbar-title"
          value={title}
          placeholder="Note Title"
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="navbar-notes" onClick={handleSave}>Save</button>
      </nav>
      <textarea
        className="note-body"
        placeholder="Type your note here..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
    </div>
  );
}