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
  let mode = 'none';
  onMount(() => {
    fetchData();

  });
  
  
  async function fetchData() {
    const response = await fetch(`${basepath()}/graph_view`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "number":number, 'fromdate':fromdate, 'todate':todate, mode: 'toptenlocation', 'submode':mode }), 
    });
    cdrcallcount = await response.json();
    console.log(cdrcallcount)
    if (cdrcallcount.length > 0){

    
    const chartData = {
      labels: cdrcallcount.map((item) => item.state),
      datasets: [
        {
          label: 'state',
          data: cdrcallcount.map((item) => item.count),
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
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
            labelString: 'state', 
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
    
    const ctx = document.getElementById('toplocation').getContext('2d');
    chart = new Chart(ctx, chartConfig);
  }
}
  
function updatemode(mode){
  mode = mode
  console.log(mode)
  fetchData()
}
</script>

<div class="chart-container">
  
  <h3 style="text-align: center;"><strong>Total Callcount</strong></h3>
  {#if mode === "none"}
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={() => updatemode("all_data")}>All data</button>
  {:else}
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"  on:click={() => updatemode("none")}>Clear</button>
  {/if}
 
  
    <canvas id="toplocation" width="800" height="400"></canvas>
</div>

<style>
  .chart-container {
    height: 30vh;
  }
</style>
