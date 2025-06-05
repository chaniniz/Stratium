import React, { useState } from 'react';
import axios from 'axios';
import PriceChart from './components/PriceChart.jsx';
import LoginForm from './components/LoginForm.jsx';
import StrategyList from "./components/StrategyList.jsx";
import Watchlist from './components/Watchlist.jsx';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [symbol, setSymbol] = useState('');
  const [prices, setPrices] = useState([]);

  const fetchPrices = async (sym) => {
    if (!sym) return;
    const res = await axios.get(`/prices/${sym}`);
    setPrices(res.data.prices);
  };

  const handleLogin = tok => {
    setToken(tok);
    localStorage.setItem('token', tok);
  };

  return (
    <div>
      <h1>Stratium Dashboard</h1>
      {!token ? (
        <LoginForm onLogin={handleLogin} />
      ) : (
        <>
          <Watchlist token={token} />
          <StrategyList token={token} />
          <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="종목코드" />
          <button onClick={() => fetchPrices(symbol)}>조회</button>
          <PriceChart data={prices} />
        </>
      )}
    </div>
  );
}
