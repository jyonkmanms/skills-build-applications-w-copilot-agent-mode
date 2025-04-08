import React from 'react';
import './App.css';
import ExampleComponent from './components/ExampleComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to OctoFit Tracker</h1>
        <p>Your fitness journey starts here!</p>
      </header>
      <main>
        <ExampleComponent />
      </main>
    </div>
  );
}

export default App;