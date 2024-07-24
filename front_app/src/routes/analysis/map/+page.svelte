<script>
  // @ts-nocheck

  import { onMount, onDestroy } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM,XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, Polygon } from "ol/geom";
  import { fromLonLat, toLonLat, transform } from "ol/proj";
  import { Style, Stroke, Fill, Icon } from "ol/style";
  import { Draw, Modify, Select } from "ol/interaction";
  import { basepath } from "$lib/config";
  import Overlay from "ol/Overlay";
  import { writable, get } from "svelte/store";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export const bookmarkedTowers = writable([]);
  export const fetchedData = writable([]);

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
  let PolygonSource = new VectorSource();
  let towerKeys = [];
  let cellid = [];
  let cdrData = null;
  let selectedCdrData = null;
  let azimuth = [];
  let fileupload = null;
  let currentTowers = [];
  let Polygons = [];
  let isDrawing = false;
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

    PolygonSource = new VectorLayer({
      source: circleSource,
      style: new Style({
        stroke: new Stroke({
          color: "green",
          width: 2,
        }),
        fill: new Fill({
          color: "rgba(255, 0, 0, 0.1)",
        }),
      }),
    });


  // this code block is for online map
    // map = new Map({
    //   target: mapContainer,
    //   layers: [
    //     new TileLayer({
    //       source: new OSM({
    //         attributions: [],
    //       }),
    //     }),
    //     vectorLayer,
    //     PolygonSource,  
    //     circleLayer, // Add the circle layer to the map
    //   ],
    //   view: new View({
    //     center: fromLonLat([78.9629, 20.5937]),
    //     zoom: 5,
    //   }),
    // });

    // this code block is for offline map 

      map = new Map({
        target: mapContainer,
        layers: [
          new TileLayer({
            source: new XYZ({
              url: 'http://10.50.50.150:8082/tile/{z}/{x}/{y}.png'
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



    map.on("pointermove", function (event) {
      if (event.dragging) {
        return;
      }
      const coordinate = map.getEventCoordinate(event.originalEvent);
      const lonLat = coordinate
        ? transform(coordinate, "EPSG:3857", "EPSG:4326")
        : null;
      // console.log(lonLat);
      showlatlong = lonLat;
    });

    drawInteraction = new Draw({
      source: vectorSource,
      type: "Polygon",
      active: true, // Make sure the draw interaction is active initially
    });

    // Event listener for the drawend event
    drawInteraction.on("drawend", (event) => {
      const feature = event.feature;
      const geometry = feature.getGeometry();
      const coordinatesArray = geometry.getCoordinates();
      Polygons.push(coordinatesArray);
      coordinates = coordinatesArray[0].map((coord) => toLonLat(coord));

      // Convert coordinates to lon-lat format
      coordinates = coordinatesArray[0].map((coord) => {
        const lonLatCoordinate = toLonLat(coord);
        return {
          longitude: lonLatCoordinate[0],
          latitude: lonLatCoordinate[1],
        };
      });
      console.log(coordinates);
      sendCoordinatesToFlask();
      // vectorSource.clear()
      // map.removeInteraction(drawInteraction);
      drawInteraction.setActive(false);
      isDrawing = false;
    });
    map.addInteraction(drawInteraction);
    drawInteraction.setActive(false);

    modifyInteraction = new Modify({ source: vectorSource });
    map.addInteraction(modifyInteraction);
    selectInteraction = new Select();
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

  });
  onDestroy(() => {
    unsubscribe();
  });

  const unsubscribe = bookmarkedTowers.subscribe((value) => {
    console.log("Updated bookmarkedTowers:", value);
  });

  function activateDrawInteraction() {
    drawInteraction.setActive(true);
  }

  function bookmarkTower(tower, markbookmark) {
    console.log(tower);
    bookmarkedTowers.update((currentTowers) => {
      const towerName = tower.areadescription;
      const towerCoordinates = [tower.lat, tower.long];

      // Check if the tower already exists in the bookmarked towers
      const towerExists = currentTowers.some(
        (currentTower) =>
          currentTower.name === towerName &&
          currentTower.coordinates[0] === towerCoordinates[0] &&
          currentTower.coordinates[1] === towerCoordinates[1]
      );

      if (!towerExists) {
        const newTower = {
          name: tower.areadescription,
          coordinates: towerCoordinates,
        };

        markbookmark.style.background = "red";
        console.log("Bookmarking tower:", newTower);
        return [...currentTowers, newTower];
      } else {
        markbookmark.style.background = "white";

        console.log("Tower already added:", towerName);
        return currentTowers;
      }
    });
  }

  function sendbookmarkstoFlask() {
    let towers = [];
    const unsubscribe = bookmarkedTowers.subscribe((value) => {
      towers = value;
    });
    unsubscribe();
    console.log(bookmarkedTowers);
    // try {
    //   const response = await fetch(`${basepath()}/bookmarkdata`, {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({ data: towers }),
    //   });
    //   if (!response.ok) {
    //     throw new Error("Network response was not ok");
    //   }
    //   const responseData = await response.json();
    const url = `${basepath()}/bookmarkdata`;
    postRequest(fetch,url,JSON.stringify({ data: towers }))
    .then(data => {
      console.log("Sent Bookmarked data", responseData);
    } )
  }

  async function sendCoordinatesToFlask() {
    try {
      // Make sure coordinates are not empty before sending

      if (coordinates.length === 0) {
        alert("No coordinates to send.");
        return;
      }
      console.log(coordinates);

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
      } 
      
      else if (coordinates.length > 0) {
        console.log("coordinates sent from Svelte to Flask");
      }
      const responseText = await response.text();
      const responseObj = JSON.parse(responseText);
      console.log(responseObj);

      if (responseObj && responseObj.towers_in_polygon) {
        const towersWithProviders = responseObj.towers_in_polygon.map(
          (tower) => ({
            ...tower,
            providerName: tower.provider,
          })
        );

        fetchedData.set(towersWithProviders);
      }

      if (!responseObj.towers_in_polygon) {
        console.error("Invalid response format:", responseObj);
        return;
      }
      // vectorSource.clear();
      // circleSource.clear();

      const providerTower = {
        airtel: [],
        jio: [],
        vodafone: [],
        cellone: [],
      };

      responseObj.towers_in_polygon.forEach((tower) => {
        const provider = tower.provider;
        console.log(provider);

        if (provider === "AIRTEL") {
          console.log();
          const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
          const feature = new Feature({
            geometry: new Point(
              fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])
            ),
            city: tower.tower_key,
            azimuth: tower.azimuth,
            coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
            name: tower.areadescription,
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: "../airtel.png",
                scale: 0.3,
              }),
            })
          );
          console.log(feature);
          vectorSource.addFeature(feature);

          var element = document.createElement("div");
          element.innerHTML = `${tower.areadescription}</br>${tower.lat},${tower.long}`;

          element.className = "tower-label";
          element.style.fontSize = "8px";
          element.style.fontWeight = "bold";
          element.style.display = "flex";
          element.style.flexDirection = "column";
          element.style.alignItems = "flex-start";
          element.style.border = "1px solid";
          element.style.padding = "5px";

          const bookmarkImage = document.createElement("img");
          bookmarkImage.src = "../bookmark.png";
          bookmarkImage.className = "bookmark-img";
          bookmarkImage.style.width = "25px";
          bookmarkImage.style.height = "25px";
          bookmarkImage.textContent = "Bookmark";
          bookmarkImage.addEventListener("click", () => bookmarkTower(tower));
          element.appendChild(bookmarkImage);

          var overlay = new Overlay({
            element: element,
            positioning: "bottom-center",
            stopEvent: false,
            offset: [0, -50],
          });

          overlay.setPosition(fromLonLat(lonLat));
          map.addOverlay(overlay);
          return feature;
        } else if (provider === "CELLONE") {
          console.log();
          const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
          const feature = new Feature({
            geometry: new Point(
              fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])
            ),
            city: tower.tower_key,
            azimuth: tower.azimuth,
            coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
            name: tower.areadescription,
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: "../cellone.png",
                scale: 0.3,
              }),
            })
          );
          console.log(feature);
          vectorSource.addFeature(feature);

          var element = document.createElement("div");
          element.innerHTML = `${tower.areadescription}</br>${tower.lat},${tower.long}`;

          element.className = "tower-label";
          element.style.fontSize = "8px";
          element.style.fontWeight = "bold";
          element.style.display = "flex";
          element.style.flexDirection = "column";
          element.style.alignItems = "flex-start";
          element.style.border = "1px solid";
          element.style.padding = "5px";

          const bookmarkImage = document.createElement("img");
          bookmarkImage.src = "bookmark.png";
          bookmarkImage.className = "../bookmark-img";
          bookmarkImage.style.width = "25px";
          bookmarkImage.style.height = "25px";
          bookmarkImage.textContent = "Bookmark";
          bookmarkImage.addEventListener("click", () => bookmarkTower(tower));
          element.appendChild(bookmarkImage);

          var overlay = new Overlay({
            element: element,
            positioning: "bottom-center",
            stopEvent: false,
            offset: [0, -50],
          });

          overlay.setPosition(fromLonLat(lonLat));
          map.addOverlay(overlay);
          return feature;
        } else if (provider === "jio") {
          console.log();
          const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
          const feature = new Feature({
            geometry: new Point(
              fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])
            ),
            city: tower.tower_key,
            azimuth: tower.azimuth,
            coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
            name: tower.areadescription,
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: "../jio.png",
                scale: 0.3,
              }),
            })
          );
          console.log(feature);
          vectorSource.addFeature(feature);

          var element = document.createElement("div");
          element.innerHTML = `${tower.areadescription}</br>${tower.lat},${tower.long}`;

          element.className = "tower-label";
          element.style.fontSize = "8px";
          element.style.fontWeight = "bold";
          element.style.display = "flex";
          element.style.flexDirection = "column";
          element.style.alignItems = "flex-start";
          element.style.border = "1px solid";
          element.style.padding = "5px";

          const bookmarkImage = document.createElement("img");
          bookmarkImage.src = "../bookmark.png";
          bookmarkImage.className = "bookmark-img";
          bookmarkImage.style.width = "25px";
          bookmarkImage.style.height = "25px";
          bookmarkImage.textContent = "Bookmark";
          bookmarkImage.addEventListener("click", () =>
            bookmarkTower(tower,bookmarkImage)
          );
          element.appendChild(bookmarkImage);

          var overlay = new Overlay({
            element: element,
            positioning: "bottom-center",
            stopEvent: false,
            offset: [0, -50],
          });

          overlay.setPosition(fromLonLat(lonLat));
          map.addOverlay(overlay);
          return feature;
        } else if (provider === "VODAFONE") {
          console.log();
          const lonLat = [parseFloat(tower.long), parseFloat(tower.lat)];
          const feature = new Feature({
            geometry: new Point(
              fromLonLat([parseFloat(tower.long), parseFloat(tower.lat)])
            ),
            city: tower.tower_key,
            azimuth: tower.azimuth,
            coordinates: [parseFloat(tower.long), parseFloat(tower.lat)],
            name: tower.areadescription,
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: "../voda.png",
                scale: 0.1,
              }),
            })
          );
          console.log(feature);
          vectorSource.addFeature(feature);

          var element = document.createElement("div");
          element.innerHTML = `${tower.areadescription}</br>${tower.lat},${tower.long}`;

          element.className = "tower-label";
          element.style.fontSize = "8px";
          element.style.fontWeight = "bold";
          element.style.display = "flex";
          element.style.flexDirection = "column";
          element.style.alignItems = "flex-start";
          element.style.border = "1px solid";
          element.style.padding = "5px";

          const bookmarkImage = document.createElement("img");
          bookmarkImage.src = "../bookmark.png";
          bookmarkImage.className = "bookmark-img";
          bookmarkImage.style.width = "25px";
          bookmarkImage.style.height = "25px";
          bookmarkImage.textContent = "Bookmark";
          bookmarkImage.addEventListener("click", () =>
            bookmarkTower(tower, bookmarkImage)
          );
          element.appendChild(bookmarkImage);

          var overlay = new Overlay({
            element: element,
            positioning: "bottom-center",
            stopEvent: false,
            offset: [0, -50],
          });

          overlay.setPosition(fromLonLat(lonLat));
          map.addOverlay(overlay);
          return feature;
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
    } catch (error) {
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

  let file;

  function handlefileupload(event) {
    file = event.target.files[0];
    // console.log(file);
    const reader = new FileReader();

    reader.onload = () => {
      const arrayBuffer = reader.result;
      const workbook = XLSX.read(arrayBuffer, { type: "array" });

      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];

      const records = XLSX.utils.sheet_to_json(sheet);

      records.forEach((towerRecord) => {
        const towerData = { ...towerRecord };
        ploatmaps(towerData, "../tower.png");
      });
    };
    reader.readAsArrayBuffer(file);
  }

  function ploatmaps(towerData) {
    console.log(towerData, "Tower Data");
    const lonLat = [parseFloat(towerData.long), parseFloat(towerData.lat)];
    let provider = towerData.provider;

    if (typeof provider === "string" && provider.trim() !== "") {
      provider = provider.toUpperCase();
    } else {
      provider = "Unknown";
    }
    let Iconsrc;
    switch (provider) {
      case "AIRTEL":
        Iconsrc = "../airtel.png";
        break;
      case "CELLONE":
        Iconsrc = "../cellone.png";
        break;
      case "JIO":
        Iconsrc = "../jio.png";
        break;
      case "VODAFONE":
        Iconsrc = "../voda.png";
        break;
      default:
        Iconsrc = "../tower.png";
    }
    const feature = new Feature({
      geometry: new Point(
        fromLonLat([parseFloat(towerData.long), parseFloat(towerData.lat)])
      ),
      azimuth: towerData.azimuth,
      coordinates: [parseFloat(towerData.long), parseFloat(towerData.lat)],
      name: towerData.areadescription,
    });

    feature.setStyle(
      new Style({
        image: new Icon({
          src: Iconsrc,
          scale: 0.1,
        }),
      })
    );
    console.log(feature);
    vectorSource.addFeature(feature);

    var element = document.createElement("div");
    element.innerHTML = `${towerData.areadescription}</br>${towerData.lat},${towerData.long}`;

    element.className = "tower-label";
    element.style.fontSize = "8px";
    element.style.fontWeight = "bold";
    element.style.display = "flex";
    element.style.flexDirection = "column";
    element.style.alignItems = "flex-start";
    element.style.border = "1px solid";
    element.style.padding = "5px";

    const bookmarkImage = document.createElement("img");
    bookmarkImage.src = "../bookmark.png";
    bookmarkImage.className = "bookmark-img";
    bookmarkImage.style.width = "25px";
    bookmarkImage.style.height = "25px";
    bookmarkImage.textContent = "Bookmark";
    bookmarkImage.addEventListener("click", () =>
      bookmarkTower(towerData, bookmarkImage)
    );
    element.appendChild(bookmarkImage);

    var overlay = new Overlay({
      element: element,
      positioning: "bottom-center",
      stopEvent: false,
      offset: [0, -50],
    });

    overlay.setPosition(fromLonLat(lonLat));
    map.addOverlay(overlay);

    return feature;
    vectorSource.clear();
  }

  function downloadData() {
    const towers = get(fetchedData);

    const data = towers.map((tower) => {
      return {
        areadescription: tower.areadescription,
        provider: tower.providerName,
        lat: tower.lat,
        long: tower.long,
      };
    });

    if (data.length === 0) {
      console.error("No data available for download.");
      return;
    }

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(data);

    XLSX.utils.book_append_sheet(wb, ws, "Towers");

    const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tower_data.xlsx";
    a.click();
  }

  function downloadBookmarkedData() {
    const bookmarkedTowersArray = get(bookmarkedTowers);

    if (bookmarkedTowersArray.length === 0) {
      console.error("No bookmarked data available for download.");
      return;
    }

    const data = bookmarkedTowersArray.map((tower) => {
      return {
        areadescription: tower.name,
        provider: tower.providerName,
        lat: tower.coordinates[0],
        long: tower.coordinates[1],
      };
    });

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(data);

    XLSX.utils.book_append_sheet(wb, ws, "Bookmarked Towers");

    const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "bookmarked_towers.xlsx";
    a.click();
  }

  function handleSelectChange(event) {
    const selectedAction = event.target.value;

    switch (selectedAction) {
      case "submit":
        sendbookmarkstoFlask();
        break;
      case "downloadexcell":
        downloadData();
        break;
      case "bookmarkdata":
        downloadBookmarkedData();
        break;
      default:
        console.log("No action selected");
    }
  }
</script>

<main class="main">
  <div class="map">
    <!-- <div class="showlatlong">
      {showlatlong}
    </div> -->
    <div class="nav">
      <input
        type="file"
        name="uploadFile"
        accept=".csv,.xlsx,.xls"
        id="fileupload"
        multiple
        required
        class="mt-1 p-2 border rounded-md"
        on:change={handlefileupload}
      />
      <select class="form-select"
      aria-label="Default select example" on:change={handleSelectChange}>
        <option value="" disabled selected>Select an action</option>
        <option value="submit">Save Data</option>
        <option value="downloadexcell">Download Excel</option>
        <option value="bookmarkdata">Download Bookmarked Data</option>
      </select>
      <button type="submit" on:click={activateDrawInteraction}
        >Draw Polygon</button
      >
    </div>
    <div class="showlatlong text-end">
      {showlatlong}
    </div>
    <div class="flex map-container" bind:this={mapContainer} />
    <!-- <div class="btn">
				<button on:click={sendCoordinatesToFlask}>Show</button>
				<button on:click={() => { clearMap(); reactivateDrawInteraction();}}>Clear</button>
			</div> -->
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
</main>

<style>
  .main {
    display: flex;
    align-items: flex-start;
    margin-left: 5%;
    width: 91vw;
    margin-top: 22px;
  }
  .showlatlong{
  }
  .map {
    height: 97vh;
    width: 100%;
  }

  .map-container {
    height: 85vh;
    width: 100%;
    cursor: pointer;
  }
  .nav{
	display: flex;
    justify-content: center;
    gap: 10px;
    margin: 1rem;
	align-items: center;
  }
  select {
    width: 10vw;
    border: 2px solid rgb(51, 7, 121);
    color: rgb(51, 7, 121);
	height: 5vh;
  }

  button {
    height: 5vh;
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
  input {
      height: 5vh;
      width: 20vw;
      border-radius: 4px;
      border: 2px solid rgb(51, 7, 121);
      align-content: center;
      font-size: large;
    }
</style>
