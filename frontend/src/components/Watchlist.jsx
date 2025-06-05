import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Watchlist({ token }) {
  const [symbol, setSymbol] = useState('');
  const [list, setList] = useState([]);

  const headers = { Authorization: `Bearer ${token}` };

  const load = async () => {
    const res = await axios.get('/watchlist', { headers });
    setList(res.data);
  };

  const add = async () => {
    if (!symbol) return;
    await axios.post('/watchlist', { symbol }, { headers });
    setSymbol('');
    load();
  };

  const remove = async (s) => {
    await axios.delete(`/watchlist/${s}`, { headers });
    load();
  };

  useEffect(() => {
    if (token) load();
  }, [token]);

  return (
    <div>
      <h2>관심 종목</h2>
      <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="종목코드" />
      <button onClick={add}>추가</button>
      <ul>
        {list.map(s => (
          <li key={s}>{s} <button onClick={() => remove(s)}>삭제</button></li>
        ))}
      </ul>
    </div>
  );
}
