import React from 'react';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  maintainAspectRatio: false,
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
  },
};

function Chart({ orders }) {
  let dates = orders.map((x) => x.delivery_date)
  let dates_set = Array.from(new Set(dates))
  let dates_counts = dates_set.map((x) => dates.filter((y) => y===x).length)

  const data = {
    labels: dates_set,
    datasets: [
      {
        label: 'кол-во заказов',
        data: dates_counts,
        borderColor: '#5583F5',
        backgroundColor: 'white',
      }
    ],
  };
  console.log(data)

  return (
    <Line options={options} data={data} />
  )
}

export default Chart;
