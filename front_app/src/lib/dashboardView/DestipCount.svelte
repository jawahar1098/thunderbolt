<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
import { basepath } from '$lib/config';
  export let number = '';
  export let fromdate;
  export let todate;
  let chart;
  let data = []; // Initialize with an empty array

  function updateChart() {
  const ctx = document.getElementById('destipchart').getContext('2d');

  if (chart) {
    chart.destroy(); // Destroy the previous chart instance to prevent duplicates
  }

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item._id.destination_ip),
      datasets: [
        {
          label: 'Count',
          data: data.map(item => item.count),
          fill: true,
          borderColor: 'rgba(125, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}


  async function filterData() {
    try {
      const response = await fetch(`${basepath()}/graph_view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          number: number,
          fromdate: fromdate,
          todate: todate,
          mode: 'IPCount',
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      data = await response.json();
      console.log(data)
      updateChart();
    } catch (error) {
      console.error('Error fetching filtered data:', error);
      data = []; // Handle the error by resetting the data array
      updateChart();
    }
  }
onMount(()=>{
  filterData()
})
</script>

<div class="chart-container">
  
  <h3 style="text-align: center;"><strong>Destination IP Count</strong></h3>
  <canvas id="destipchart" width="800" height="400"></canvas>
</div>

<style>
  .chart-container {
    max-width: auto;
    margin: auto;
  }
</style>
