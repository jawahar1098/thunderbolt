<script>
	import { onMount } from "svelte";
	import * as d3 from "d3";

    export let otherStates;

	function getRandomColor(state_name) {
      const letters = "0123456789ABCDEF";
      let color = "#";
      if (otherStates.indexOf(state_name) == -1) {
        return "#fff"
      }
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
	function drawIndiaMap() {
		const projection = d3.geoMercator().scale(850).center([85, 25]);
		const svg = d3
			.select("#india-map")
			.append("svg")
			.attr("width", 800)
			.attr("height", 600);

		d3.json("/states_india.geojson").then(function (india) {
			const path = d3.geoPath().projection(projection);
			svg.selectAll("path")
				.data(india.features)
				.enter()
				.append("path")
				.attr("d", path)
				.style("fill", (d) => getRandomColor(d.properties.st_nm))
				.attr("stroke", "black");
			svg.selectAll("text")
				.data(india.features)
				.enter()
				.append("text")
				.attr("text-anchor","middle")
				.style("font-size","12px")
				.attr("class", "state-label")
				.attr("transform", function (d) {
					const centroid = path.centroid(d);
					return "translate(" + centroid[0] + "," + centroid[1] + ")";
				})
				.attr("dy", ".35em") 
				.text(function (d) {
					return [d.properties.st_nm]; 
				});
		});
	}
	onMount(() => {
        drawIndiaMap()
    });
</script>

<div id="india-map" class="map" />

<style>
	.map {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 55vh; 
	}
	
</style>
