<script>
    import { onMount, onDestroy } from "svelte";
    import Map from "ol/Map";
    import View from "ol/View";
    import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
    import { OSM, Vector as VectorSource } from "ol/source";
    import { transform } from "ol/proj";
    import Feature from "ol/Feature";
    import { Point, Circle, Polygon} from "ol/geom";
    import { fromLonLat } from "ol/proj";
    import { Style, Stroke, Fill, Icon } from "ol/style";
    import { Draw, Modify, Select } from "ol/interaction";
    import {basepath} from '$lib/config'

    let mapContainer;
    let map;
    let vectorLayer;
    let circleLayer;
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
    let circleCenter = [];
    let radius = 0;

    // Function to calculate a point on a circle given its center and radius
    function calculatePointOnCircle(center, radius) {
        const lon1 = center[0];
        const lat1 = center[1];
        const angleInRadians = Math.random() * 2 * Math.PI; // Generate a random angle
        const lon2 = lon1 + (radius / (111.32 * 1000)) * Math.cos(angleInRadians);
        const lat2 = lat1 + (radius / (111.32 * 1000)) * Math.sin(angleInRadians);

        return [lon2, lat2];
    }

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
                circleLayer,
            ],
            view: new View({
                center: transform([0, 0], "EPSG:4326", "EPSG:3857"),
                zoom: 2,
            }),
        });

        drawInteraction = new Draw({
            source: vectorSource,
            type: "Circle",
			active: true,
        });

        modifyInteraction = new Modify({ source: vectorSource });
        selectInteraction = new Select();

        map.addInteraction(drawInteraction);
        map.addInteraction(modifyInteraction);
        map.addInteraction(selectInteraction);

        drawInteraction.on("drawstart", (event) => {
            coordinates = [];
        });

        drawInteraction.on("drawend", (event) => {
            const feature = event.feature;
            const geometry = feature.getGeometry();
            circleCenter = transform(geometry.getCenter(), "EPSG:3857", "EPSG:4326");
            radius = geometry.getRadius();
            const circlePoint = calculatePointOnCircle(circleCenter, radius);
            console.log("Circle Center:", circleCenter);
            console.log("Circle Radius:", radius);
            console.log("Point on the Circle:", circlePoint);
            getTowersInCircle();
			map.removeInteraction(drawInteraction);
        });
selectInteraction.on("select", (event) => {
    if (event.selected.length > 0) {
        const feature = event.selected[0];
        const coordinates = feature.getGeometry().getCoordinates();
        const azimuth = feature.get("azimuth");

        // Create a semicircle feature and add it to the circleSource
        const lonLat = [parseFloat(coordinates[0]), parseFloat(coordinates[1])];
        const circleCoords = calculateSemicircleCoordinates(lonLat, azimuth, 1000);
        const semicircleFeature = new Feature({
            geometry: new Polygon([circleCoords]),
        });
        circleSource.clear();
        circleSource.addFeature(semicircleFeature);
        console.log(semicircleFeature);
    }
});
    });

    async function getTowersInCircle() {
        try {
            if (circleCenter.length === 0 || radius === 0) {
                alert("No circle drawn.");
                return;
            }

            const response = await fetch(`${basepath()}/tower_map_circle`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ circleCenter, radius }),
            });

            const responseObj = await response.json();

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
                            src: "tower.png", // Make sure this path is correct
                            scale: 0.05,
                        }),
                    })
                );

                vectorSource.addFeature(feature);
                return feature;
            });

            cdrData = responseObj.cdr_in_towers;
        } catch (error) {
            console.error("Error:", error);
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
		window.location.href = '';

	}

// Function to calculate a semicircle given its center, azimuth, and radius
function calculateSemicircleCoordinates(center, azimuth, radius) {
	console.log(azimuth);
    let antennaAzimuth = (90 - azimuth) % 360;
    if (antennaAzimuth < 0) {
        antennaAzimuth += 360;
    }

    const segments = 120;
    const startAngle = (antennaAzimuth - 60) * (Math.PI / 180);
    const endAngle = (antennaAzimuth + 60) * (Math.PI / 180);

    const semicircleCoords = [];

    for (let i = 0; i <= segments; i++) { // Half the number of segments for a semicircle
        const angle = startAngle + (i / segments) * (endAngle - startAngle);

        const x = center[0] + radius * Math.cos(angle);
        const y = center[1] + radius * Math.sin(angle);
        semicircleCoords.push([x, y]);
    }

    semicircleCoords.push(center);
    return semicircleCoords;
}

    function createOrUpdateCircles(responseObj) {
        responseObj.towers_in_polygon.forEach((tower) => {
            const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
            const azimuth = parseFloat(tower.azimuth);
            const circleCoords = calculateSemicircleCoordinates(lonLat, azimuth, 1000);
            const circleFeature = new Feature({
                geometry: new Circle(circleCoords),
            });
            circleSource.addFeature(circleFeature);
        });
    }
</script>

<main class="main">
    <div class="map">
        <div class="map-container" bind:this={mapContainer} />
        <div class="btn">
            <button on:click={getTowersInCircle}>show</button>
            <button on:click={clearMap}>Clear</button>

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
</style>
