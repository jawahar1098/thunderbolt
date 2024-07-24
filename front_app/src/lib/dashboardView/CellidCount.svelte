<script>
  // Import required modules
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let number; 
  export let fromdate ;
  export let todate ;
  let chart;

  onMount(() => {
   
    fetchData();
  });

   
  function fetchData() {
    
    fetch(`http://${window.location.hostname}:5005/graph_view`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number: number, fromdate, todate, mode: 'CellidCount' }),
    })
    .then(response => response.json())
    .then(data =>{
      updateChart(data)
    })
  
  }

  function updateChart(data) {
    if (chart) {
      
      chart.data.labels = data.map(item => item.cell_id);
      chart.data.datasets[0].data = data.map(item => item.count);
      chart.update();
    } else {
      
      const ctx = document.getElementById('cellidchart').getContext('2d');
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(item => item.cell_id),
          datasets: [
            {
              label: 'Count',
              data: data.map(item => item.count),
              fill: false,
              borderColor: 'rgba(75, 192, 192, 1)',
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
  }

  
</script>

<div class="chart-container">
  <h3>Cell id Chart</h3>

 
  <canvas id="cellidchart" width="400" height="170"></canvas>
</div>

<style>
  .chart-container {
    max-width: auto;
    margin: auto;
  }
</style>
