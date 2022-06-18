import { useState, useEffect } from 'react';
import './App.css';
import Total from './Total.js';
import Orders from './Orders.js';
import Chart from './Chart.js';

function App() {
  const [ orders, setOrders ] = useState([])

  useEffect(() => {
    fetch('/api/')
      .then(response => response.json())
      .then(data => setOrders(data))
      .catch(err => alert(err))
  }, [])

  return (
    <div className="App">
      <div className="left">
        <Chart orders={orders} />
      </div>
      <div className="right">
        <Total orders={orders} />
        <Orders orders={orders} />
      </div>
    </div>
  );
}

export default App;
