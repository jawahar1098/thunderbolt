<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { basepath } from '$lib/config';

  export let number = '';
  export let mode;
  export let indata;
  export let outdata;

  let incoming_values;
  let chartValues = [];
  let chartLabels = [];
  let data;
  let chartCanvas;
  let ctx;
  let chartInstance;
  let fromdate = '';
  let todate = '';

  const Color1 = 'rgb(255, 99, 132)';
  const Color2 = 'rgb(54, 162, 235)';
  const Color3 = 'rgb(154, 162, 180)';

  onMount(() => {
    outcoming_calldata(number);
  });

  async function outcoming_calldata(number) {
    const profile_num = new FormData();
    profile_num.append('number', number);
    profile_num.append('mode', 'incoming_data');

    try {
      const response = await fetch(`${basepath()}/phone_dashboard`, {
        method: 'POST',
        body: profile_num,
      });

      if (response.ok) {
        data = await response.json();
        incoming_values = data;
        updateChartData();
        createOrUpdateChart();
      } else {
        console.error('Failed to submit form', response);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }

  function createOrUpdateChart() {
    if (chartInstance) {
      chartInstance.destroy();
    }

    chartCanvas = document.getElementById('incoming');
    ctx = chartCanvas.getContext('2d');

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartLabels,
        datasets: [
          {
            label: 'Call Record',
            backgroundColor: [Color1, Color2, Color3],
            borderColor: [Color1, Color2, Color3],
            data: chartValues,
          },
        ],
      },
    });
  }

  function updateChartData() {
    chartValues = [];
    chartLabels = [];

    const entries = Object.entries(incoming_values);
    entries.sort((a, b) => b[1] - a[1]);
    const sortedObject = Object.fromEntries(entries.slice(0, 10));
    const values = Object.values(sortedObject);

    values.forEach(value => {
      chartValues.push(value);
    });

    const keyvalues = Object.keys(sortedObject);

    keyvalues.forEach(keyvalues => {
      chartLabels.push(keyvalues);
    });
  }

  
</script>

<div class="chart-container">
  

  <canvas bind:this={chartCanvas} id="incoming"></canvas>
  <h2>For Top 10 incoming</h2>
  <h3>Top 10 incoming - {incoming_values}</h3>
</div>

<style>
  .chart-container {
    width: 80%;
    margin: 0 auto;
  }
</style>
