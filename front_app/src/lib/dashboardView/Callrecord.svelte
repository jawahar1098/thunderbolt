<script>
  import { onMount, afterUpdate } from 'svelte';
  import Chart from 'chart.js/auto';
  import { basepath } from '$lib/config';

  export let number = '';
  export let fromdat ;
  export let todate;
  console.log(number,fromdat,todate)
  let chartValues;
  let totalCalls = 0;
  let data;
  let chartCanvas;
  let ctx;
  let chartInstance;
 

  let chartLabels = ['Incoming Calls', 'Outgoing Calls'];
  var Color1 = 'rgb(255, 99, 132)';
  var Color2 = 'rgb(54, 162, 235)';
  var Color3 = 'rgb(154, 162, 180)';

  onMount(() => {
    phone_dashboard(number);
  });

  async function phone_dashboard(number) {
    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "phone_dashboard");
    
    try {
      const response = await fetch(
        `${basepath()}/phone_dashboard`, 
        {
          method: "POST",
          body: profile_num,
        }
      );

      if (response.ok) {
        data = await response.json();
        chartValues = [data.incoming_calls.toString(), data.outgoing_calls.toString()];
        totalCalls = data.total_calls;
        createOrUpdateChart();
      } else {
        console.error("Failed to submit form", response);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  function createOrUpdateChart() {
    if (chartInstance) {
      chartInstance.destroy();
    }

    chartCanvas = document.getElementById('myChart');
    ctx = chartCanvas.getContext('2d');

    chartInstance = new Chart(ctx, {
      type: 'pie',
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

  $: {
    if (number) {
      phone_dashboard(number);
    }
  }

  afterUpdate(() => {
    createOrUpdateChart();
  });

</script>

<div class="chart-container">


<canvas bind:this={chartCanvas} id="myChart"></canvas>
<h2>Total calls - {totalCalls}</h2>
<h3 style="text-align: center;"><strong>Total Callcount</strong></h3>
</div>

<style>
.chart-container {
  width: 30vw;
  height: 30vh;
}
</style>
