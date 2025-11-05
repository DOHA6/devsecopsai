import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// VULNERABILITY: Hardcoded API key
const API_KEY = 'sk-1234567890abcdef';
const API_BASE_URL = 'http://localhost:8080/api';

function App() {
  const [username, setUsername] = useState('');
  const [users, setUsers] = useState([]);
  const [filename, setFilename] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [host, setHost] = useState('');
  const [pingResult, setPingResult] = useState('');

  // VULNERABILITY: No input validation - XSS risk
  const searchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users?username=${username}`);
      setUsers(response.data);
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  // VULNERABILITY: Dangerous file read - Path traversal
  const readFile = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/file?filename=${filename}`);
      setFileContent(response.data);
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  // VULNERABILITY: Command injection risk
  const pingHost = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/ping?host=${host}`);
      setPingResult(response.data);
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  // VULNERABILITY: Using eval() - code injection risk
  const calculateExpression = (expr) => {
    try {
      // eslint-disable-next-line no-eval
      const result = eval(expr);
      return result;
    } catch (error) {
      return 'Invalid expression';
    }
  };

  // VULNERABILITY: Storing sensitive data in localStorage
  const saveCredentials = () => {
    localStorage.setItem('apiKey', API_KEY);
    localStorage.setItem('username', username);
    alert('Credentials saved!');
  };

  // VULNERABILITY: dangerouslySetInnerHTML - XSS risk
  const renderHTML = (html) => {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vulnerable DevSecOps Demo App</h1>
        <p className="warning">⚠️ This app contains intentional security vulnerabilities for testing purposes</p>
      </header>

      <main className="container">
        <section className="feature-section">
          <h2>User Search (SQL Injection Test)</h2>
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <button onClick={searchUsers}>Search</button>
          </div>
          <div className="results">
            {users.map((user, idx) => (
              <div key={idx} className="user-card">
                <p><strong>ID:</strong> {user.id}</p>
                <p><strong>Username:</strong> {user.username}</p>
                <p><strong>Email:</strong> {user.email}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="feature-section">
          <h2>File Reader (Path Traversal Test)</h2>
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter filename"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
            />
            <button onClick={readFile}>Read File</button>
          </div>
          <pre className="code-block">{fileContent}</pre>
        </section>

        <section className="feature-section">
          <h2>Ping Utility (Command Injection Test)</h2>
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter host"
              value={host}
              onChange={(e) => setHost(e.target.value)}
            />
            <button onClick={pingHost}>Ping</button>
          </div>
          <pre className="code-block">{pingResult}</pre>
        </section>

        <section className="feature-section">
          <h2>Calculator (eval() Test)</h2>
          <p>Result: {calculateExpression('2 + 2')}</p>
          <button onClick={saveCredentials}>Save Credentials</button>
        </section>
      </main>

      <footer>
        <p>Built for DevSecOps AI Pipeline Demo | API Key: {API_KEY}</p>
      </footer>
    </div>
  );
}

export default App;
