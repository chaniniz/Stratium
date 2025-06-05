import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

export default function PriceChart({ data }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    if (!data.length) return;

    const chartData = {
      labels: data.map(d => d.date),
      datasets: [{ label: 'Close', data: data.map(d => d.close), borderColor: 'blue' }]
    };

    const chart = new Chart(canvasRef.current, {
      type: 'line',
      data: chartData,
    });

    return () => chart.destroy();
  }, [data]);

  return <canvas ref={canvasRef} />;
}
