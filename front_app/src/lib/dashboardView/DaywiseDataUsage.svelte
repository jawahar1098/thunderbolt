<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import {basepath} from '$lib/config.js'
    export let number = '';
    export let fromdate;
    export let todate;
    
    let daywise_data_usage = [];
    let chart;
  
    onMount(() => {
      // Fetch the data initially without any specific filter
      fetchData();
    });


    
  
  

     function fetchData(month = null, year = null) {
       fetch(`${basepath()}/graph_view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'number': number, 'fromdate':fromdate, 'todate':todate, mode: 'DaywiseDataUsage' }), // Adjust the 'mode' value if needed
      })
      .then(response => response.json())
      .then(daywise_data_usage =>{
        console.log(daywise_data_usage)

        
        // Prepare data for Chart.js  
        const chartData = {
          labels: daywise_data_usage.map((item) => item.destination_ip),
          datasets: [
            {
              label: 'Uplink Usage',
              data: daywise_data_usage.map((item) => item.uplink_usage / 1048576 ),
              backgroundColor: 'rgba(75, 192, 192, 0.8)',
            },
            {
              label: 'Downlink Usage',
              data: daywise_data_usage.map((item) => item.downlink_usage / 1048576),
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
      
      const ctx = document.getElementById('daywisedatausage').getContext('2d');
      chart = new Chart(ctx, chartConfig);
    })
    }
    
    
    </script>
  
  <style>
    .chart-container {
      max-width: auto;
      margin: auto;
    }
  </style>
  
  <div class="chart-container">

    <h2 style="text-align: center;"><strong>DaywiseDataUsage</strong></h2>
    <canvas id="daywisedatausage" width="400" height="200"></canvas>
  </div>
  