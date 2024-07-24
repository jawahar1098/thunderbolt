<script>
// @ts-nocheck

	import { onMount, onDestroy } from "svelte";
	import Map from "ol/Map";
	import View from "ol/View";
	import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
	import { XYZ, OSM, Vector as VectorSource } from "ol/source";
	import Feature from "ol/Feature";
	import { Point, Polygon } from "ol/geom";
	import { fromLonLat, toLonLat } from "ol/proj";
	import { Style, Stroke, Fill, Icon } from "ol/style";
	import { Draw, Modify, Select } from "ol/interaction";
	import {basepath} from '$lib/config'

	let mapContainer;
	let map;
	let vectorLayer;
	let circleLayer; // New vector layer for circles
	let drawInteraction;
	let modifyInteraction;
	let selectInteraction;
	let coordinates = [];
	let vectorSource = new VectorSource();
	let circleSource = new VectorSource();
	let towerKeys = [];
	let cellid = [];
	let cdrData = null;
	let selectedCdrData = null;
	let azimuth = [];
  
	onMount(() => {
		vectorLayer = new VectorLayer({
			source: vectorSource,
			style: new Style({
			stroke: new Stroke({
				color: "blue",
				width: 2,
			}),
			fill: new Fill({
				color: "rgba(0, 0, 255, 0.1)",
			}),
			}),
		});
  
		// Create a new vector layer for circles
		circleLayer = new VectorLayer({
			source: circleSource,
			style: new Style({
			stroke: new Stroke({
				color: "red",
				width: 2,
			}),
			fill: new Fill({
				color: "rgba(255, 0, 0, 0.1)",
			}),
			}),
		});
  
		// map = new Map({
		// 	target: mapContainer,
		// 	layers: [
		// 	new TileLayer({
		// 		source: new OSM({
		// 		attributions: [],
		// 		}),
		// 	}),
		// 	vectorLayer,
		// 	circleLayer, // Add the circle layer to the map
		// 	],
		// 	view: new View({
		// 	center: fromLonLat([0, 0]),
		// 	zoom: 2,
		// 	}),
		// });
				//-------------------------------------------------------offline map integration---------------------------------------------------------------------//
		map = new Map({
			target: mapContainer,
			layers: [
				new TileLayer({
					source: new XYZ({
						url: `http://0.0.0.0:8082/tile/{z}/{x}/{y}.png`
					}),
				}),
				vectorLayer,
				circleLayer,
			],
			view: new View({
				center: [0, 0],
				zoom: 2
			})
		});

  
		drawInteraction = new Draw({
			source: vectorSource,
			type: "Polygon",
			active: true, // Make sure the draw interaction is active initially
		});
  
		modifyInteraction = new Modify({ source: vectorSource });
	
		selectInteraction = new Select();
	
		// Event listener for the drawend event
		drawInteraction.on("drawend", (event) => {
			const feature = event.feature;
			const geometry = feature.getGeometry();
			const coordinatesArray = geometry.getCoordinates();
	
			// Convert coordinates to lon-lat format
			coordinates = coordinatesArray[0].map((coord) => {
			const lonLatCoordinate = toLonLat(coord);
			return {
				longitude: lonLatCoordinate[0],
				latitude: lonLatCoordinate[1],
			};
			});
			map.removeInteraction(drawInteraction);
		});
	
		// Add interactions to the map
		// map.addInteraction(drawInteraction);
		map.addInteraction(modifyInteraction);
		map.addInteraction(selectInteraction);
  
		// Event listener for the select interaction
		selectInteraction.on("select", (event) => {
			if (event.selected.length > 0) {
				const feature = event.selected[0];
				const coordinates = feature.getGeometry().getCoordinates();
				const azimuth = feature.get("azimuth");

				// Create a circle feature with a 120-degree span and add it to the circleSource
				const lonLat = [parseFloat(coordinates[0]), parseFloat(coordinates[1])];
				const circleCoords = calculateCircleCoordinates(lonLat, azimuth, 1000);
				// console.log(circleCoords);
				const circleFeature = new Feature({
					geometry: new Polygon([circleCoords]),
				});
				circleSource.clear();
				circleSource.addFeature(circleFeature);
				// console.log(circleFeature);
			}
		});
	});
  
	async function sendCoordinatesToFlask() {
		try {
			// Make sure coordinates are not empty before sending
			if (coordinates.length === 0) {
				alert("No coordinates to send.");
				return;
			}
  
			// Send the coordinates to the Flask backend
			const response = await fetch(`${basepath()}/tower_map_polygon`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(coordinates),
			});
	
			if (!response.ok) {
				throw new Error("Network response was not ok");
			} else if (coordinates.length > 0) {
				console.log("coordinates sent from Svelte to Flask");
			}
			const responseText = await response.text();
			const responseObj = JSON.parse(responseText);
			if (!responseObj.towers_in_polygon || !responseObj.cdr_in_towers) {
				console.error("Invalid response format:", responseObj);
				return;
			}
			vectorSource.clear();
			circleSource.clear(); 
	
			towerKeys = responseObj.towers_in_polygon.map((tower) => tower.tower_key);
			console.log("towerkeys", towerKeys);
			azimuth = responseObj.towers_in_polygon.map((tower) => tower.azimuth);
			console.log("azimuth:", azimuth);
			cellid = responseObj.towers_in_polygon.map((tower) => tower.celltowerid);
			console.log(cellid);
	
			createOrUpdateCircles(responseObj);
			const towerFeatures = responseObj.towers_in_polygon.map((tower) => {
				const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
				const feature = new Feature({
					geometry: new Point(fromLonLat(lonLat)),
					city: tower.tower_key,
					azimuth: tower.azimuth,
					coordinates: lonLat,
				});
		
				feature.setStyle(
						new Style({
						image: new Icon({
							src: "tower.png",
							scale: 0.05,
						}),
					})
				);
				// console.log(feature);
				vectorSource.addFeature(feature);
				return feature;
			});
	
			cdrData = responseObj.cdr_in_towers;
		} 
		catch (error) {
			console.error("Error sending coordinates:", error);
	    }
	}
  
	function showCdrData(cellid) {
	  	const selectedCdr = cdrData.find(
			(item) => item && item.cdr_data && item.cdr_data.first_cgid === cellid
	  	);
		console.log(selectedCdr);
		if (selectedCdr) {
			console.log(selectedCdr.cdr_data);
			selectedCdrData = selectedCdr.cdr_data;
		}
	}
  
	function clearMap() {
	  	vectorSource.clear();
		circleSource.clear();
		coordinates = [];

		cdrData = null;
		window.location.href = '/';

	}
	function reactivateDrawInteraction() {
		
		map.removeInteraction(drawInteraction);
			drawInteraction = new Draw({
			source: vectorSource,
			type: "Polygon",
		});
		map.addInteraction(drawInteraction);

		drawInteraction.setActive(true);
	}

	function calculateCircleCoordinates(center, azimuth, radius) {
		console.log(azimuth);
		let antennaAzimuth = (90 - azimuth) % 360;
		if (antennaAzimuth < 0) {
			antennaAzimuth += 360;
		}
		console.log(antennaAzimuth);

		const segments = 120; // Use 120 segments for a 120-degree span
		const startAngle = (antennaAzimuth - 60) * (Math.PI / 180); // Start angle shifted by -60 degrees
		const endAngle = (antennaAzimuth + 60) * (Math.PI / 180); // End angle shifted by +60 degrees

		const circleCoords = [];

		for (let i = 0; i <= segments; i++) {
			const angle = startAngle + (i / segments) * (endAngle - startAngle);

			const x = center[0] + radius * Math.cos(angle);
			const y = center[1] + radius * Math.sin(angle);
			circleCoords.push([x, y]);
		}
		// Connect the last point to the center to close the semicircle
		circleCoords.push(center);
		return circleCoords;
	}
	// Function to create or update circles
	function createOrUpdateCircles(responseObj) {
	  responseObj.towers_in_polygon.forEach((tower) => {
		const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
		const azimuth = parseFloat(tower.azimuth);
		const circleCoords = calculateCircleCoordinates(lonLat, azimuth, 1000);
		const circleFeature = new Feature({
		  	geometry: new Polygon([circleCoords]),
		});
		circleSource.addFeature(circleFeature);
	  });
	}
  </script>
  
  <main class="main">
	<div class="map">
		<div class="map-container" bind:this={mapContainer} />
		<div class="btn">
			<button on:click={sendCoordinatesToFlask}>Show</button>
			<button on:click={() => { clearMap(); reactivateDrawInteraction();}}>Clear</button>
		</div>
	</div>
	<div class="sidebar">
		<ul>
			{#each cellid as key}
				<li>
					{key}
					<button on:click={() => showCdrData(key)}>View</button>
				</li>
			{/each}
		</ul>
		<div>
			{#if selectedCdrData}
				<div class="cdr-data">
					<h2>CDR Data:</h2>
					<p>Source Number: {selectedCdrData.source_number}</p>
					<p>Call Type: {selectedCdrData.call_type}</p>
					<p>Timestamp: {selectedCdrData.timestamp}</p>
					<p>Destination Number: {selectedCdrData.destination_number}</p>
				</div>
			{/if}
	  	</div>
	</div>
</main>
  
<style>
	.main {
	  display: flex;
	  align-items: flex-start;
	}
  
	.map {
	  height: 500px;
	  width: 80%;
	}
  
	.map-container {
	height: 800px;
	  width: 100%;
	  /* cursor: pointer; */
	}
  
	button {
	  background-color: darkgreen;
	  color: aliceblue;
	  border-radius: 5px;
	  margin-top: 1rem;
	  text-align: center;
	  padding: 10px 34px;
	}
  
	button:hover {
	  background-color: rgb(8, 142, 8);
	}
  
	.btn {
	  display: flex;
	  justify-content: center;
	  align-items: center;
	  flex-wrap: nowrap;
	  gap: 8px;
	  border-radius: 20%;
	  text-align: center;
	}
  
	.sidebar {
	  padding: 1rem;
	  width: 30%;
	  border-left: 1px solid grey;
	  display: flex;
	  align-items: flex-start;
	  justify-content: space-between;
	  gap: 10px;
	}
  
	li {
	  border: 1px solid grey;
	  padding: 10px;
	  text-decoration: none;
	  list-style-type: none;
	  align-content: left;
	}
</style>
  