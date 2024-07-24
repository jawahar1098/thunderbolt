<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
 import {basepath} from '$lib/config'
  export let number;
  export let fromdate;
  export let todate;
  console.log(fromdate,todate)
  let cdrcallcount = [];
  let chart;
 
  onMount(() => {
    fetchData();

  });
  
  
  async function fetchData() {
    const response = await fetch(`${basepath()}/graph_view`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "number":number, 'fromdate':fromdate, 'todate':todate, mode: 'CdrCount' }), 
    });
    cdrcallcount = await response.json();
    console.log(cdrcallcount)
    if (cdrcallcount.length > 0){

    
    const chartData = {
      labels: cdrcallcount.map((item) => item.destination_number),
      datasets: [
        {
          label: 'call in',
          data: cdrcallcount.map((item) => item.call_in_count),
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
        },
        {
          label: 'call out',
          data: cdrcallcount.map((item) => item.call_out_count),
          backgroundColor: 'rgba(255, 99, 132, 0.8)',
        },
      ],
    };
  
    

const chartConfig = {
  type: 'bar',
  data: chartData,
  options: {
    responsive: true,
    scales: {
      xAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Destination Number', 
          },
        },
      ],
      yAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Count', 
          },
          stacked: true, 
        },
      ],
    },
  },
};

    
    if (chart) {
      chart.destroy(); // Destroy the existing chart instance before updating
    }
    
    const ctx = document.getElementById('cdrcallcount').getContext('2d');
    chart = new Chart(ctx, chartConfig);
  }
}
  
  
</script>

<div class="chart-container">
  
  <h3 style="text-align: center;"><strong>Total Callcount</strong></h3>
  <canvas id="cdrcallcount" width="800" height="400"></canvas>
</div>

<style>
  .chart-container {
    height: 30vh;
  }
</style>
