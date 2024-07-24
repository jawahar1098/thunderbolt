<script>
	// @ts-nocheck
	
	
		import { onMount, onDestroy } from "svelte";
		import Map from "ol/Map";
		import View from "ol/View";
		import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
		import { OSM, Vector as VectorSource } from "ol/source";
		import Feature from "ol/Feature";
		import { Point, Polygon } from "ol/geom";
		import { fromLonLat, toLonLat,transform } from "ol/proj";
		import { Style, Stroke, Fill, Icon } from "ol/style";
		import { Draw, Modify, Select } from "ol/interaction";
		  import { basepath } from "$lib/config";
		  import Overlay from 'ol/Overlay';
		  import { writable } from 'svelte/store';
		import * as XLSX from 'xlsx';
	
		export const bookmarkedTowers = writable([]);
	
	
	  
	  
	
	  
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
		let fileupload = null;
		let showlatlong;
	  
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
	  
			map = new Map({
				target: mapContainer,
				layers: [
				new TileLayer({
					source: new OSM({
					attributions: [],
					}),
				}),
				vectorLayer,
				circleLayer, // Add the circle layer to the map
				],
				view: new View({
				center: fromLonLat([0, 0]),
				zoom: 2,
				}),
			});
	
			map.on('singleclick', function(event) {
				map.forEachFeatureAtPixel(event.pixel, function(feature) {
					if (feature.get('city')) {
						const cellId = feature.get('celltowerid'); 
						if (cellId !== undefined) {
							console.log('celltowerid:', cellId);
							selectedCdrData = cellId; 
						}
					}
				});
			});

			map.on('pointermove', function (event) {
				if (event.dragging) {
					return;
				}
				const coordinate = map.getEventCoordinate(event.originalEvent);
				const lonLat = coordinate ? transform(coordinate, 'EPSG:3857', 'EPSG:4326') : null;
				// console.log(lonLat);
				showlatlong = lonLat
				});
	
			map.on('click', function(evt) {
				const feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
					return feature;
				});
	
				if (feature && feature.get('type') === 'tower') {
					const cellId = feature.get('cellId');
					document.getElementById('cellIdDisplay').innerText = 'celltowerid: ' + cellId;
				}
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
			map.addInteraction(drawInteraction);
			map.addInteraction(modifyInteraction);
			map.addInteraction(selectInteraction);
		
		// map.addInteraction(selectInteraction);
	
	  
			// Event listener for the select interaction
			selectInteraction.on("select", (event) => {
		  // console.log(alert("asdfasdfasdf"))
				if (event.selected.length > 0) {
					const feature = event.selected[0];
					const coordinates = feature.getGeometry().getCoordinates();
					const azimuth = feature.get("azimuth");
			// console.log(alert("mitha oru loosu"));
	
					// Create a circle feature with a 120-degree span and add it to the circleSource
					const lonLat = [parseFloat(coordinates[0]), parseFloat(coordinates[1])];
					const circleCoords = calculateCircleCoordinates(lonLat, azimuth, 1000);
					// console.log(circleCoords);
					const circleFeature = new Feature({
						geometry: new Polygon([circleCoords]),
					});
					circleSource.clear();
					circleSource.addFeature(circleFeature);
				}
			});
	
			const unsubscribe = bookmarkedTowers.subscribe(value => {
				console.log("Updated bookmarkedTowers:", value);
			});
	
			onDestroy(() => {
				unsubscribe();
			});
		});
	 
		function bookmarkTower(towerKey) {
			var tower = vectorSource.getFeatures().find(feature => feature.get('city') === towerKey);
			if (tower) {
				bookmarkedTowers.update(currentTowers => {
					const newTower = {
						key: tower.get('city'),
						name: tower.get('name'),
						coordinates: tower.get('coordinates'),
					};
	
					console.log('Bookmarking tower:', newTower);
	
					return [...currentTowers, newTower];
				});
			} else {
				console.log('Tower not found:', towerKey);
			}
		}
	
		function createBookmarkButton(node, towerKey) {
			const button = document.createElement('button');
			button.className = 'bookmark-btn';
			button.textContent = 'Bookmark';
			button.addEventListener('click', () => bookmarkTower(towerKey));
			node.appendChild(button);
	
			return {
				destroy() {
				}
			};
		}
	
	  
		async function sendCoordinatesToFlask() {
			try {
				// Make sure coordinates are not empty before sending
				if (coordinates.length === 0) {
					alert("No coordinates to send.");
					return;
				}
		  console.log(coordinates)
		  
				// Send the coordinates to the Flask backend
				const response = await fetch(`${basepath()}/tower`, {
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
				console.log(responseObj)
				if (!responseObj.towers_in_polygon ) {
					console.error("Invalid response format:", responseObj);
					return;
				}
				vectorSource.clear();
				circleSource.clear(); 
	
				const providerTower = {
					airtel: [], jio: [], vodafone:[], cellone:[]
				};
	
				responseObj.towers_in_polygon.forEach((tower) => {
					const provider = tower.provider;
					console.log(provider)
					
					if (provider === 'AIRTEL') {
						console.log()
						ploatmaps(tower,"airtel.png")
						// const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
						// const feature = new Feature({
						// 	geometry: new Point(fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])),
						// 	city: tower.tower_key,
						// 	azimuth: tower.azimuth,
						// 	coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
						// 	name: tower.name,
						// 	type: 'tower',
						// 	cellId: tower.tower_key,
						// });
					
						// 	feature.setStyle(
						// 			new Style({
						// 			image: new Icon({
						// 				src: "airtel.png",
						// 				scale: 0.1,
						// 			}),
									
						// 	})
						// 	);
						// 	console.log(feature);
						// 	vectorSource.addFeature(feature);
	
						// 	var element = document.createElement('div');
						// 	element.innerHTML = `${tower.areadescription}, Lat: ${tower.lat}, Long: ${tower.long}`;
	
						// 	element.className = 'tower-label';
						// 	element.style.fontSize = '8px';
						// 	element.style.fontWeight = 'bold'; 
	
						// 	const bookmarkImage = document.createElement('img');
						// 	bookmarkImage.src = "bookmark.jpeg"
						// 	bookmarkImage.className = 'bookmark-img';
						// 	bookmarkImage.textContent = 'Bookmark';
						// 	bookmarkImage.addEventListener('click', () => bookmarkTower(tower.tower_key));
						// 	element.appendChild(bookmarkImage);
							
						// 	var overlay = new Overlay({
						// 		element: element,
						// 		positioning: 'bottom-center',
						// 		stopEvent: false,
						// 		offset: [0, -50]
								
						// 	});
							
						// 	overlay.setPosition(fromLonLat(lonLat));
						// 	map.addOverlay(overlay);
						// 	return feature;
					}else if (provider === 'CELLONE') {
						console.log()
						ploatmaps(tower,"cellone.png")

						// const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
						// const feature = new Feature({
						// 	geometry: new Point(fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])),
						// 	city: tower.tower_key,
						// 	azimuth: tower.azimuth,
						// 	coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
						// 	name: tower.areadescription,
						// });
					
						// 	feature.setStyle(
						// 			new Style({
						// 			image: new Icon({
						// 				src: "cellone.png",
						// 				scale: 0.1,
						// 			}),
									
						// 	})
						// 	);
						// 	console.log(feature);
						// 	vectorSource.addFeature(feature);
	
						// 	var element = document.createElement('div');
						// 	element.innerHTML = `${tower.areadescription}, Lat: ${tower.lat}, Long: ${tower.long}`;
	
						// 	element.className = 'tower-label';
						// 	element.style.fontSize = '8px';
						// 	element.style.fontWeight = 'bold'; 
	
						// 	const bookmarkButton = document.createElement('button');
						// 	bookmarkButton.className = 'bookmark-btn';
						// 	bookmarkButton.textContent = 'Bookmark';
						// 	bookmarkButton.addEventListener('click', () => bookmarkTower(tower.tower_key));
						// 	element.appendChild(bookmarkButton);
							
						// 	var overlay = new Overlay({
						// 		element: element,
						// 		positioning: 'bottom-center',
						// 		stopEvent: false,
						// 		offset: [0, -50]
								
						// 	});
							
						// 	overlay.setPosition(fromLonLat(lonLat));
						// 	map.addOverlay(overlay);
						// 	return feature;
					}else if (provider === 'JIO') {
						console.log()
						ploatmaps(tower,"jio.png")

						// const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
						// const feature = new Feature({
						// 	geometry: new Point(fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])),
						// 	city: tower.tower_key,
						// 	azimuth: tower.azimuth,
						// 	coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
						// 	name: tower.areadescription,
						// });
					
						// 	feature.setStyle(
						// 			new Style({
						// 			image: new Icon({
						// 				src: "jio.png",
						// 				scale: 0.1,
						// 			}),
									
						// 	})
						// 	);
						// 	console.log(feature);
						// 	vectorSource.addFeature(feature);
	
						// 	var element = document.createElement('div');
						// 	element.innerHTML = `${tower.areadescription}, Lat: ${tower.lat}, Long: ${tower.long}`;
	
						// 	element.className = 'tower-label';
						// 	element.style.fontSize = '8px';
						// 	element.style.fontWeight = 'bold'; 
	
						// 	const bookmarkButton = document.createElement('button');
						// 	bookmarkButton.className = 'bookmark-btn';
						// 	bookmarkButton.textContent = 'Bookmark';
						// 	bookmarkButton.addEventListener('click', () => bookmarkTower(tower.tower_key));
						// 	element.appendChild(bookmarkButton);
							
						// 	var overlay = new Overlay({
						// 		element: element,
						// 		positioning: 'bottom-center',
						// 		stopEvent: false,
						// 		offset: [0, -50]
								
						// 	});
							
						// 	overlay.setPosition(fromLonLat(lonLat));
						// 	map.addOverlay(overlay);
						// 	return feature;
					}else if (provider === 'VODAFONE') {
						console.log()
						ploatmaps(tower,"vodo.png")

						// const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
						// const feature = new Feature({
						// 	geometry: new Point(fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])),
						// 	city: tower.tower_key,
						// 	azimuth: tower.azimuth,
						// 	coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
						// 	name: tower.areadescription,
						// });
					
						// 	feature.setStyle(
						// 			new Style({
						// 			image: new Icon({
						// 				src: "voda.png",
						// 				scale: 0.1,
						// 			}),
									
						// 	})
						// 	);
						// 	console.log(feature);
						// 	vectorSource.addFeature(feature);
	
						// 	var element = document.createElement('div');
						// 	element.innerHTML = `${tower.areadescription}, Lat: ${tower.lat}, Long: ${tower.long}`;
	
						// 	element.className = 'tower-label';
						// 	element.style.fontSize = '8px';
						// 	element.style.fontWeight = 'bold'; 
	
						// 	const bookmarkButton = document.createElement('button');
						// 	bookmarkButton.className = 'bookmark-btn';
						// 	bookmarkButton.textContent = 'Bookmark';
						// 	bookmarkButton.addEventListener('click', () => bookmarkTower(tower.tower_key));
						// 	element.appendChild(bookmarkButton);
							
						// 	var overlay = new Overlay({
						// 		element: element,
						// 		positioning: 'bottom-center',
						// 		stopEvent: false,
						// 		offset: [0, -50]
								
						// 	});
							
						// 	overlay.setPosition(fromLonLat(lonLat));
						// 	map.addOverlay(overlay);
						// 	return feature;
					}
					
				});
		
				towerKeys = responseObj.towers_in_polygon.map((tower) => tower.tower_key);
				// console.log("towerkeys", towerKeys);
				azimuth = responseObj.towers_in_polygon.map((tower) => tower.azimuth);
				// console.log("azimuth:", azimuth);
				cellid = responseObj.towers_in_polygon.map((tower) => tower.celltowerid);
				// console.log(cellid);
		
				createOrUpdateCircles(responseObj);
		
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
			// console.log(azimuth);
			let antennaAzimuth = (90 - azimuth) % 360;
			if (antennaAzimuth < 0) {
				antennaAzimuth += 360;
			}
			// console.log(antennaAzimuth);
	
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
	
		let records = [];
		let file;
		let columnNames = [];
	
	
		function handlefileupload(event) {
			file = event.target.files[0];
			// console.log(file);
			const reader = new FileReader();
	
			reader.onload = () => {
				const arrayBuffer = reader.result;
				const workbook = XLSX.read(arrayBuffer, { type: 'array' });
	
				const sheetName = workbook.SheetNames[0];
				const sheet = workbook.Sheets[sheetName];
	
				const range = XLSX.utils.decode_range(sheet['!ref']);
	
				// Extract column names
				for (let col = range.s.c; col <= range.e.c; col++) {
				const cellAddress = XLSX.utils.encode_cell({ r: range.s.r, c: col });
				const cell = sheet[cellAddress];
				if (cell && cell.t === 's') {
					// If the cell type is a string, use the string value
					columnNames.push(cell.v.trim());
				} else {
					// Otherwise, use the cell address as the column name
					columnNames.push(cellAddress);
				}
				}
	
				for (let row = range.s.r + 1; row <= range.e.r; row++) {
					const rowData = {};
					for (let col = range.s.c; col <= range.e.c; col++) {
					const columnName = columnNames[col];
					const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
					const cell = sheet[cellAddress];
					if (cell) {
					// Use utils.format_cell to preserve formatting
					const formattedValue = XLSX.utils.format_cell(cell);
					rowData[columnName] = formattedValue.trim();
					} else {
					// If the cell is empty, assign an empty string
					rowData[columnName] = '';
					}
				}
					records.push(rowData);
				}
				console.log(records)
				records.forEach(items => {
					ploatmaps(items,"tower.png")
				})
				
				}
				reader.readAsArrayBuffer(file);
				
		}
	
	
		function ploatmaps(tower,image){
			console.log(tower,"-----")
			const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
				const feature = new Feature({
					geometry: new Point(fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])),
					city: tower.tower_key,
					azimuth: tower.azimuth,
					coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
					name: tower.areadescription,
				});
			
					feature.setStyle(
							new Style({
							image: new Icon({
								src: image,
								scale: 0.1,
							}),
							
					})
					);
					console.log(feature);
					vectorSource.addFeature(feature);
	
					var element = document.createElement('div');
					element.innerHTML = `${tower.areadescription}</br>${tower.lat},${tower.long}`;
	
					element.className = 'tower-label';
					element.style.fontSize = '8px';
					element.style.fontWeight = 'bold';
					element.style.display = 'flex';
					element.style.flexDirection = 'column';
					element.style.alignItems = 'flex-start';
					element.style.border = '1px solid';
					element.style.padding = '5px';          
	
					const bookmarkImage = document.createElement('img');
					bookmarkImage.src = "bookmark.png"
					bookmarkImage.className = 'bookmark-img';
					bookmarkImage.style.width = '25px';
					bookmarkImage.style.height = '25px';
					bookmarkImage.textContent = 'Bookmark';
					bookmarkImage.addEventListener('click', () => bookmarkTower(tower.tower_key));
					element.appendChild(bookmarkImage);
	
					var overlay = new Overlay({
					element: element,
					positioning: 'bottom-center',
					stopEvent: false,
					offset: [0, -50]
					
				});
				
				overlay.setPosition(fromLonLat(lonLat));
				map.addOverlay(overlay);
				return feature;
	
	}
	
	</script>
	  
	<main class="main">
		<div class="map">
			<div class="map-container" bind:this={mapContainer} />
	
			<div class="text-red-600">
				{showlatlong}
			</div>
		<div class="btn">
				<button on:click={sendCoordinatesToFlask}>Show</button>
				<button on:click={() => { clearMap(); reactivateDrawInteraction();}}>Clear</button>
			</div>
		</div>
		<!-- <div class="sidebar">
			<ul>
				{#each cellid as key}
					<li>
						{key}
						<button on:click={() => showcellid(key)}>View</button>
					</li>
				{/each}
			</ul>
	
		</div> -->
		<div class="flex items-center">
			<input type="file" name="uploadFile" accept=".csv,.xlsx,.xls" id="fileupload" multiple required class="mt-1 p-2 border rounded-md" on:change={handlefileupload}>
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
		height: 650px;
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
		.ol-popup {
			position: absolute;
			background-color: white;
			box-shadow: 0 1px 4px rgba(0,0,0,0.2);
			padding: 15px;
			border-radius: 10px;
			border: 1px solid #cccccc;
			bottom: 12px;
			left: -50px;
			min-width: 280px;
			display: none;
		}
		.bookmark-btn {
			margin-top: 5px;
			padding: 2px 5px;
			font-size: 8px;
			cursor: pointer;
		}
		.bookmarked-towers {
			margin-top: 20px;
		}
	
		.bookmarked-towers h3 {
			margin-bottom: 10px;
		}
	
		.bookmarked-towers ul {
			list-style-type: none;
			padding: 0;
		}
	
		.bookmarked-towers li {
			margin-bottom: 5px;
		}
	</style>
	  



	

