  <script>
    import { onMount, afterUpdate } from 'svelte';
    import Chart from 'chart.js/auto';
    import { basepath } from '$lib/config';

    export let number = '';
    export let fromdate ;
    export let todate ;
    
    let chart;

    onMount(() => {
      fetchData();
    });


    
     function fetchData() {
      fetch(`${basepath()}/graph_view`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 'number': number, 'formdate':fromdate, 'todate':todate, 'mode': 'ImeiCount' }),
      })
      .then(response =>response.json())
      .then(data=>{

        updateChart(data)
      })
    }

    function updateChart(data) {
      const ctx = document.getElementById('imeichart').getContext('2d');
      if (chart) {
        // If the chart instance already exists, destroy it first
        chart.destroy();
      }
      chart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: data.map(item => item.imei),
          datasets: [
            {
              label: 'Count',
              data: data.map(item => item.count),
              backgroundColor: [
                // Define different colors for the pie chart sections
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#3ebf9b', '#6c757d', '#d9534f', '#4d83ff'
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true, // Make the chart responsive
        },
      });
    }
  </script>

<div class="chart-container">
  
  <h3 style="text-align: center;"><strong> IMEI Count</strong></h3>
  <canvas id="imeichart"></canvas>
</div>

<style>
  .chart-container {
    width: 100mm;
    height: 100mm;
  }
</style>

