<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { basepath } from '$lib/config';

  export let number = '';

  let outgoing_values;
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
    outgoing_calldata(number);
  });

  $: {
    if (number) {
      outgoing_calldata(number);
    }
  }

  async function outgoing_calldata(number) {
    const profile_num = new FormData();
    profile_num.append('number', number);
    profile_num.append('mode', 'outgoing_data');

    try {
      const response = await fetch(`${basepath()}/phone_dashboard`, {
        method: 'POST',
        body: profile_num,
      });

      if (response.ok) {
        data = await response.json();
        outgoing_values = data;
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

    chartCanvas = document.getElementById('outgoing'); 
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

    const entries = Object.entries(outgoing_values);
    entries.sort((a, b) => b[1] - a[1]);
    const sortedObject = Object.fromEntries(entries.slice(0, 10));
    const values = Object.values(sortedObject);

    values.forEach(value => {
      chartValues.push(value.toString());
    });

    const keyvalues = Object.keys(sortedObject);

    keyvalues.forEach(keyvalues => {
      chartLabels.push(keyvalues.toString());
    });
  }

  function filterData() {
    const fromdateInput = document.getElementById('fromdate');
    const todateInput = document.getElementById('todate');
    fromdate = fromdateInput.value;
    todate = todateInput.value;

  }
</script>

<div class="chart-container">
  <label for="fromdate">From Date:</label>
  <input type="date" id="fromdate" bind:value={fromdate} />

  <label for="todate">To Date:</label>
  <input type="date" id="todate" bind:value={todate} />

  <!-- Add the Submit button to trigger the data filtering -->
  <button style="border: 1px solid;" on:click={filterData}>Submit</button>

  <canvas bind:this={chartCanvas} id="outgoing"></canvas> 
  <h2>For Top 10 Outgoing</h2>
  <h3>Top 10 Outgoing - {outgoing_values}</h3>
</div>

<style>
  .chart-container {
    width: 30vw;
    height: 30vh;
  }
</style>
