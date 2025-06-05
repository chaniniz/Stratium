import React, { useState } from 'react';
import axios from 'axios';
import PriceChart from './components/PriceChart.jsx';

export default function App() {
  const [symbol, setSymbol] = useState('');
  const [prices, setPrices] = useState([]);

  const fetchPrices = async () => {
    if (!symbol) return;
    const res = await axios.get(`/prices/${symbol}`);
    setPrices(res.data.prices);
  };

  return (
    <div>
      <h1>Stratium Dashboard</h1>
      <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="종목코드" />
      <button onClick={fetchPrices}>조회</button>
      <PriceChart data={prices} />
    </div>
  );
}
