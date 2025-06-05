import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function StrategyList({ token }) {
  const [strategies, setStrategies] = useState([]);
  const [symbol, setSymbol] = useState('');
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  useEffect(() => {
    axios.get('/strategies').then(res => setStrategies(res.data));
  }, []);

  const execute = async (name) => {
    if (!symbol) return;
    await axios.post(`/strategy/${name}/execute`, null, { params: { symbol }, headers });
    alert('실행 완료');
  };

  return (
    <div>
      <h2>전략 목록</h2>
      <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="종목코드" />
      <ul>
        {strategies.map(s => (
          <li key={s.name}>
            <strong>{s.name}</strong> - {s.description}
            {token && <button onClick={() => execute(s.name)}>실행</button>}
          </li>
        ))}
      </ul>
    </div>
  );
}
