<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
  
    export let number;
    export let fromdate;
    export let todate ;
    
    let nightwise_data_usage = [];
    let chart;

  onMount(()=>{
    fetchData()
  })

    function fetchData() {
      fetch(`http://${window.location.hostname}:5005/graph_view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'number': number, 'fromdate':fromdate, 'todate':todate, 'mode': 'NightwiseDataUsage' }), 
      })
      .then(response => response.json())
      .then(nightwise_data_usage => {

      
      console.log(nightwise_data_usage)
  
      const chartData = {
        labels: nightwise_data_usage.map((item) => item.destination_ip),
        datasets: [
          {
            label: 'Uplink Usage',
            data: nightwise_data_usage.map((item) => item.uplink_usage / 1048576 ),
            backgroundColor: 'rgba(75, 192, 192, 0.8)',
          },
          {
            label: 'Downlink Usage',
            data: nightwise_data_usage.map((item) => item.downlink_usage / 1048576),
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
              stacked: true, 
            },
          },
        },
      };
  
      if (chart) {
        chart.destroy();
      }
  
      const ctx = document.getElementById('nightwisedata').getContext('2d');
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
    
    <h2 style="text-align: center;"><strong>NightwiseDataUsage</strong></h2>
    <canvas id="nightwisedata" width="400" height="200"></canvas>
  </div>
   
