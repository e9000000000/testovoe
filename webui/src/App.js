import { useState, useEffect } from 'react';
import './App.css';
import Total from './Total.js';
import Orders from './Orders.js';
import Chart from './Chart.js';

function App() {
  const [ orders, setOrders ] = useState([
    {
      id: 12,
      number: 13,
      cost_usd: 14,
      cost_rub: 122,
      delivery_date: "15-12-1999",
      outdated_notified: true,
      archived: true,
    },
    {
      id: 15,
      number: 322323,
      cost_usd: 11,
      cost_rub: 99,
      delivery_date: "15-12-2077",
      outdated_notified: false,
      archived: false,
    },
    {
      id: 314,
      number: 3223323,
      cost_usd: 111,
      cost_rub: 999,
      delivery_date: "15-12-2077",
      outdated_notified: false,
      archived: false,
    },
  ])

  useEffect(() => {
    fetch('http://core/api/')
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
