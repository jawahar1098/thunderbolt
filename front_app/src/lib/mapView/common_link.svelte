<script>
	// @ts-nocheck
	import '../../gantt-default.css';
	import { onMount, getContext } from 'svelte';
	import Map from 'ol/Map';
	import View from 'ol/View';
	import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
	import { OSM, XYZ, Vector as VectorSource } from 'ol/source';
	import Feature from 'ol/Feature';
	import { Point, LineString } from 'ol/geom';
	import { Icon, Style, Stroke, Text, Fill } from 'ol/style';
	import { fromLonLat } from 'ol/proj';
	import Overlay from 'ol/Overlay';
	import {
		SvelteGantt,
		SvelteGanttDependencies,
		SvelteGanttTable,
		MomentSvelteGanttDateAdapter
	} from 'svelte-gantt';
	import { time } from '../../utils';
	import moment from 'moment';
    import { basepath } from '$lib/config';

	//variables for map
	let mapContainer;
	let map;
	let USER_NUMBERS;
	let lineLayer;
	let Date = '';
	let dates_of_suspect = [];
	let locationCount = {};
	let overlay;
	const colors = ['blue', 'green', 'orange', 'yellow'];

	//variables for gantt
	const currentStart = time('00:00');
	const currentEnd = time('24:00');

	let options2 = getContext('options');

	export const data = {
		rows: [],
		tasks: [],
		dependencies: []
	};
	let options = {
		dateAdapter: new MomentSvelteGanttDateAdapter(moment),
		rows: data.rows,
		tasks: data.tasks,
		dependencies: data.dependencies,

		columnOffset: 15,
		magnetOffset: 15,
		rowHeight: 52,
		rowPadding: 6,
		headers: [{ unit: 'hour', format: 'H:mm' }],
		fitWidth: true,
		minWidth: 1000,
		from: currentStart,
		to: currentEnd,
		tableHeaders: [{ title: 'Label', property: 'label', width: 140, type: 'tree' }],
		tableWidth: 240,
		ganttTableModules: [SvelteGanttTable],
		ganttBodyModules: [SvelteGanttDependencies]
	};
	let gantt;

	async function sendNumberToFlask(event) {
		locationCount = {};
		event.preventDefault();
		if (event.target.name === 'date') {
			Date = event.target.value;
		}

		const userNumbers = USER_NUMBERS.trim().split(',');

		if (userNumbers.length >= 0) {
			try {
				const response = await fetch(`${basepath()}/get_common_link`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ 'numbers': userNumbers, 'date': Date })
				});

				if (!response.ok) {
					throw new Error('Network response was not ok');
				} else {
					const data = await response.json();
					console.log(data);
					dates_of_suspect = data['common_dates'];
					if (data) {
						// Update the mapContainer height based on the selected date
						const mapContainerHeight = Date ? '65vh' : '65vh';
						mapContainer.style.height = mapContainerHeight;
					}
					data.rows = userNumbers.map((number, index) => ({
						id: index + 1,
						label: number,
						classes: `background-color: ${colors[index % colors.length]};`
					}));
					options.rows = data.rows;
					// Update the gantt with the new data
					gantt.$set(options);
					const tasks = [];

					userNumbers.forEach((number, index) => {
						const userData = data[number];
						if (userData && userData.length > 0) {
							userData.forEach((entry) => {
								const fromTime = time(entry.tower_time);
								const toTime = time(entry.tower_time).add(entry.tower_duration, 'minutes');

								tasks.push({
									id: tasks.length + 1,
									resourceId: index + 1,
									label: entry.tower_duration, // Use azimuth as label
									from: fromTime,
									to: toTime,
									classes: colors[index % colors.length],
									enableDragging: false
								});
							});
						}
					});

					// Update the gantt with the new tasks
					options.tasks = tasks;
					options.headers = [{ unit: 'hour', format: 'H:mm' }];
					if (Date) {
						options.headers.unshift({ unit: 'day', format: Date });
					}
					gantt.$set(options);
					lineLayer.getSource().clear();

					for (const number in data) {
						let numberIndex = 1;
						const tasks = [];
						data[number].forEach((item, index) => {
							const latitude = parseFloat(item.tower_latitude);
							const longitude = parseFloat(item.tower_longitude);
							const time = item.tower_time;
							const area = item.area_description;

							if (!isNaN(latitude) && !isNaN(longitude)) {
								const offset = index * 200000;
								const rotation = calculateRotation(latitude, longitude, number);

								const feature = new Feature({
									geometry: new Point(fromLonLat([longitude, latitude]))
								});

								feature.set('number', number);
								feature.set('latitude', latitude);
								feature.set('longitude', longitude);
								feature.set('area', area);
								feature.set('time', time);

								const textStyle =
									USER_NUMBERS.split(',').length === 1
										? new Text({
												text: numberIndex.toString(),
												offsetY: -30,
												fill: new Fill({
													color: '#000'
												}),
												font: 'bold 14px Arial'
										  })
										: null;

								feature.setStyle(
									new Style({
										image: new Icon({
											src: 'man.png',
											scale: 0.2,
											rotation: rotation,
											offset: [0, -15],
											color: getMarkerColor(number)
										}),
										text: textStyle
									})
								);

								// Add click event listener to each feature to show tooltip
								feature.on('click', (event) => {
									const coordinates = event.target.getGeometry().getCoordinates();
									const content = `User: ${number}<br>Latitude: ${latitude},Longitude: ${longitude}<br>Location: ${area}`;
									showTooltip(coordinates, content);
								});

								lineLayer.getSource().addFeature(feature);
								numberIndex++;
							}
						});
					}
				}
			} catch (error) {
				console.error('Error fetching user data:', error);
			}
		} else {
			alert('Please enter a valid user name.');
		}
	}

	onMount(() => {
		window.gantt = gantt = new SvelteGantt({
			target: document.getElementById('example-gantt'),
			props: options
		});
		// -------------------------------------------------------online map integration----------------------------------------------------------------------//
		// map = new Map({
		// 	target: mapContainer,
		// 	layers: [
		// 		new TileLayer({
		// 			source: new OSM({
		// 				attributions: []
		// 			})
		// 		})
		// 	],
		// 	view: new View({
		// 		center: [0, 0],
		// 		zoom: 2
		// 	})
		// });
		//-------------------------------------------------------offline map integration---------------------------------------------------------------------//
		map = new Map({
			target: mapContainer,
			layers: [
				new TileLayer({
					source: new XYZ({
						url: 'http://localhost:8082/tile/{z}/{x}/{y}.png'
					})
				})
			],
			view: new View({
				center: [0, 0],
				zoom: 2
			})
		});
		createTooltip();

		lineLayer = new VectorLayer({
			source: new VectorSource(),
			style: new Style({
				stroke: new Stroke({
					color: 'blue',
					width: 2
				})
			})
		});

		map.addLayer(lineLayer);
		map.on('click', (event) => {
			// Hide tooltip when map is clicked
			hideTooltip();

			map.forEachFeatureAtPixel(event.pixel, (feature) => {
				const coordinates = feature.getGeometry().getCoordinates();
				const content = `User: ${feature.get('number')}<br>Coordinates: ${feature.get(
					'latitude'
				)},${feature.get('longitude')}<br>Location: ${feature.get('area')}<br>Time: ${feature.get(
					'time'
				)}`;
				showTooltip(coordinates, content);
			});
		});
	});

	function getMarkerColor(number) {
		const index = USER_NUMBERS.split(',').indexOf(number);
		if (index !== -1) {
			return colors[index % colors.length];
		}
		return '#000000';
	}

	function createTooltip() {
		overlay = new Overlay({
			element: document.createElement('div'),
			positioning: 'bottom-center',
			offset: [0, -10],
			stopEvent: false
		});

		overlay.getElement().style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
		overlay.getElement().style.border = '1px solid #ccc';
		overlay.getElement().style.padding = '10px';
		overlay.getElement().style.borderRadius = '5px';
		overlay.getElement().style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
		overlay.getElement().style.fontSize = '14px';
		overlay.getElement().style.color = '#333';
		overlay.getElement().style.maxWidth = '300px';
		overlay.getElement().style.marginBottom = '2vh';

		map.addOverlay(overlay);
	}

	function showTooltip(coordinates, content) {
		overlay.setPosition(coordinates);
		overlay.getElement().innerHTML = content;
		overlay.getElement().style.display = 'block';
	}

	function hideTooltip() {
		overlay.getElement().style.display = 'none';
	}

	function calculateRotation(latitude, longitude, number) {
		const location = `${latitude}_${longitude}`;
		if (locationCount[location] && locationCount[location].numbers.includes(number)) {
			return 0;
		}
		if (locationCount[location]) {
			locationCount[location].count++;
			locationCount[location].numbers.push(number);
		} else {
			locationCount[location] = {
				count: 1,
				numbers: [number]
			};
		}
		const rotation = (locationCount[location].count - 1) * (30 * (Math.PI / 180));
		return rotation;
	}
</script>

<main class="main">
	<form class="header">
		<input type="text" bind:value={USER_NUMBERS} />
		<select name="date" bind:value={Date} on:change={sendNumberToFlask}>
			<option value="" disabled>Date</option>
			{#each dates_of_suspect as date}
				<option value={date}>{date}</option>
			{/each}
		</select>
		<button on:click={sendNumberToFlask}>Show</button>
	</form>

	<div class="container">
		<div id="example-gantt" />
	</div>
	<div class="map-container" bind:this={mapContainer} />
</main>

<style>
	#example-gantt {
		flex-grow: 1;
		overflow: auto;
	}


	.container {
		display: flex;
		overflow: auto;
		flex: 1;
		max-width: 100%;
	}
	.map-container {
		height: 68.5vh;
		width: 100%;
	}
	.header {
		height: 8vh;
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 10px;
	}
	input {
		height: 4vh;
		width: 35vw;
		border-radius: 4px;
		border: 2px solid rgb(51, 7, 121);
		align-content: center;
		font-size: large;
	}
	select {
		height: 4vh;
		width: 10vw;
		border: 2px solid rgb(51, 7, 121);
		background-color: rgb(51, 7, 121);
		border-radius: 4px;
		color: white;
	}
	button {
		height: 4vh;
		width: 10vw;
		border-radius: 4px;
		border: 2px solid rgb(51, 7, 121);
		background-color: rgb(51, 7, 121);
		color: white;
		font-size: large;
	}
	button:hover {
		background-color: rgba(51, 7, 121, 0.644);
		color: black;
	}
</style>
