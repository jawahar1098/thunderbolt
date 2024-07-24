<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { basepath } from '$lib/config';
  export let number ;
  export let fromdate;
  export let todate;
  let dataUsage = [];
  let chart;

  onMount(() => {
    // Fetch the data initially without any specific filter
    fetchData();
  });



  async function fetchData() {
    const response = await fetch(`${basepath()}/graph_view`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'number': number, 'fromdate':fromdate, 'todate':todate, mode: 'DataUsage' }),
    });
    dataUsage = await response.json();
    console.log(dataUsage,"------")
    // Prepare data for Chart.js
    const chartData = {
      labels: dataUsage.map((item) => item.destination_ip),
      datasets: [
        {
          label: 'Uplink Usage',
          data: dataUsage.map((item) => item.usage_data[0].uplink_usage / 1048576),
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
        },
        {
          label: 'Downlink Usage',
          data: dataUsage.map((item) => item.usage_data[0].downlink_usage / 1048576),
          backgroundColor: 'rgba(255, 99, 132, 0.8)',
        },
      ],
    };

    // Chart.js configuration
    const chartConfig = {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Destination IP',
            },
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Usage (MB)',
            },
            stacked: true, // Enable stacked bars
          },
        },
      },
    };

    if (chart) {
      chart.destroy(); // Destroy the existing chart instance before updating
    }

    const ctx = document.getElementById('datausagedata').getContext('2d');
    chart = new Chart(ctx, chartConfig);
  }

  // Fetch data on initial mount
  onMount(()=>{

    fetchData();
  });

  
  
</script>

<div class="chart-container">
 
  <h3 style="text-align: center;"><strong>Data Usage</strong></h3>
  <canvas id="datausagedata" width="400" height="200"></canvas>

</div>

<style>
  .chart-container {
    max-width: auto;
    margin: auto;
  }
</style>
