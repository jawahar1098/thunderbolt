<script>
  // @ts-nocheck

  import "../../../gantt-default.css";
  import { onMount, getContext } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM, XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, LineString } from "ol/geom";
  import { Icon, Style, Stroke, Text, Fill } from "ol/style";
  import { fromLonLat } from "ol/proj";
  import Overlay from "ol/Overlay";
  import {
    SvelteGantt,
    SvelteGanttDependencies,
    SvelteGanttTable,
    MomentSvelteGanttDateAdapter,
  } from "svelte-gantt";
  import { time } from "../../../utils";
  import moment from "moment";
  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  //variables for map
  let mapContainer;
  let map;
  let USER_NUMBERS;
  let lineLayer;
  let Date;
  let dates_of_suspect = [];
  let locationCount = {};
  let towerData = [];
  let overlay;
  const colors = ["blue", "green", "orange", "yellow"];
  // Variable to store clicked marker data
  let clickedNumberData = [];
  let showSidebar = false;

  //variables for gantt
  const currentStart = time("00:00");
  const currentEnd = time("24:00");

  let options2 = getContext("options");

  export const data = {
    rows: [],
    tasks: [],
    dependencies: [],
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
    headers: [{ unit: "hour", format: "H:mm" }],
    fitWidth: true,
    minWidth: 1000,
    from: currentStart,
    to: currentEnd,
    tableHeaders: [
      { title: "Label", property: "label", width: 140, type: "tree" },
    ],
    tableWidth: 240,
    ganttTableModules: [SvelteGanttTable],
    ganttBodyModules: [SvelteGanttDependencies],
  };
  let gantt;

  async function sendNumberToFlask(event) {
    locationCount = {};
    event.preventDefault();

    const userNumbers = USER_NUMBERS.trim().split(",");

    if (userNumbers.length >= 0) {
      // try {
      //   const response = await fetch(`${basepath()}/get_common_link`, {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({ numbers: userNumbers, date: Date }),
      //   });

        // if (!response.ok) {
        //   throw new Error("Network response was not ok");
        // } else {
        //   console.log("entered...");
        //   const data = await response.json();
        const url = `${basepath()}/get_common_link`;
        postRequest(fetch,url,JSON.stringify({ numbers: userNumbers, date: Date }))
        .then(data => {
          towerData = data;
          console.log(towerData, "-----------------------");
          dates_of_suspect = data["common_dates"];
          if (data) {
            // Update the mapContainer height based on the selected date
            const mapContainerHeight = Date ? "75vh" : "75vh";
            mapContainer.style.height = mapContainerHeight;
          }
          data.rows = userNumbers.map((number, index) => ({
            id: index + 1,
            label: number,
            classes: `background-color: ${colors[index % colors.length]};`,
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
                const toTime = time(entry.tower_time).add(
                  entry.tower_duration,
                  "minutes"
                );
                let label;
                if (entry.tower_duration === 0) {
                  label = "0"; 
                } else {
                  label = entry.tower_duration; 
                }

                tasks.push({
                  id: tasks.length + 1,
                  resourceId: index + 1,
                  label: label, 
                  from: fromTime,
                  to: toTime,
                  classes: colors[index % colors.length],
                  enableDragging: false,
                });
              });
            }
          });

          // Update the gantt with the new tasks
          options.tasks = tasks;
          options.headers = [{ unit: "hour", format: "H:mm" }];
          if (Date) {
            options.headers.unshift({ unit: "day", format: Date });
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
                  geometry: new Point(fromLonLat([longitude, latitude])),
                });

                feature.set("number", number);
                feature.set("latitude", latitude);
                feature.set("longitude", longitude);
                feature.set("area", area);
                feature.set("time", time);

                const textStyle =
                  USER_NUMBERS.split(",").length === 1
                    ? new Text({
                        text: numberIndex.toString(),
                        offsetY: -30,
                        fill: new Fill({
                          color: "#000",
                        }),
                        font: "bold 14px Arial",
                      })
                    : null;

                feature.setStyle(
                  new Style({
                    image: new Icon({
                      src: "/man.png",
                      scale: 0.2,
                      rotation: rotation,
                      offset: [0, -15],
                      color: getMarkerColor(number),
                    }),
                    text: textStyle,
                  })
                );

                lineLayer.getSource().addFeature(feature);
                numberIndex++;
              }
            });
          }
        })
       
    } 
  }

  onMount(() => {
    window.gantt = gantt = new SvelteGantt({
      target: document.getElementById("example-gantt"),
      props: options,
    });
    // -------------------------------------------------------online map integration----------------------------------------------------------------------//
    // map = new Map({
    //   target: mapContainer,
    //   layers: [
    //     new TileLayer({
    //       source: new OSM({
    //         attributions: [],
    //       }),
    //     }),
    //   ],
    //   view: new View({
    //     center: fromLonLat([78.9629, 20.5937]),
    //     zoom: 5,
    //   }),
    // });
                // Offline MaP integration 
    map = new Map({
    	target: mapContainer,
    	layers: [
    		new TileLayer({
    			source: new XYZ({
    				url: 'http://10.50.50.150:8082/tile/{z}/{x}/{y}.png'
    			}),
    		}),
    		// vectorLayer,
    		// circleLayer,
    	],
    	view: new View({
    		center: [0, 0],
    		zoom: 2
    	})
    });

    lineLayer = new VectorLayer({
      source: new VectorSource(),
      style: new Style({
        stroke: new Stroke({
          color: "blue",
          width: 2,
        }),
      }),
    });

    map.addLayer(lineLayer);
    // Add click event listener to the map
    map.on("click", handleMapClick);
  });

  function getMarkerColor(number) {
    const index = USER_NUMBERS.split(",").indexOf(number);
    if (index !== -1) {
      return colors[index % colors.length];
    }
    return "#000000";
  }

  function calculateRotation(latitude, longitude, number) {
    const location = `${latitude}_${longitude}`;
    if (
      locationCount[location] &&
      locationCount[location].numbers.includes(number)
    ) {
      return 0;
    }
    if (locationCount[location]) {
      locationCount[location].count++;
      locationCount[location].numbers.push(number);
    } else {
      locationCount[location] = {
        count: 1,
        numbers: [number],
      };
    }
    const rotation =
      (locationCount[location].count - 1) * (30 * (Math.PI / 180));
    return rotation;
  }

  function handleMapClick(event) {
    console.log("Map clicked!");
    const clickedFeature = map.forEachFeatureAtPixel(
      event.pixel,
      (feature) => feature
    );
    console.log(clickedFeature);

    if (clickedFeature) {
      const clickedNumber = clickedFeature.get("number");
      clickedNumberData = []; // Clear the data before updating

      for (const number in towerData) {
        if (towerData[number] && number === clickedNumber) {
          towerData[number].forEach((item) => {
            clickedNumberData.push({
              number,
              latitude: parseFloat(item.tower_latitude),
              longitude: parseFloat(item.tower_longitude),
              tower_id: item.cell_id,
              time: item.tower_time,
              area: item.area_description,
            });
          });
        }
      }
      console.log(`Clicked Number Data for Number:`, clickedNumberData);

      // Assuming you have a variable to control the visibility of the sidebar, e.g., showSidebar
      showSidebar = true;
    } else {
      // Clicked outside of a feature, close the sidebar
      clickedNumberData = [];
      // Assuming you have a variable to control the visibility of the sidebar, e.g., showSidebar
      showSidebar = false;
    }
  }
</script>

<main class="main">
  <form class="header">
    <input type="text" bind:value={USER_NUMBERS} class="number" />
    <input type="date" name="date" id="" bind:value={Date} class="date" />
    <button on:click={sendNumberToFlask}>Show</button>
  </form>

  <div class="container">
    <div id="example-gantt" />
  </div>
  <div class="container-map">
    <div class="map-container" bind:this={mapContainer} />
    {#if showSidebar === true}
      <div class="sidebar">
        <table class="table-map">
          <div class="table-head">
            <thead>
              <tr>
                <th class="table-heading">Number</th>
                <th class="table-heading">Tower ID</th>
                <th class="table-heading">Area Description</th>
                <th class="table-heading">Time</th>
              </tr>
            </thead>
          </div>
          <div class="table-content">
            <tbody>
              {#each clickedNumberData as tower (tower)}
                <tr>
                  <td class="table-body">{tower.number}</td>
                  <td class="table-body">{tower.tower_id}</td>
                  <td class="table-body">{tower.area}</td>
                  <td class="table-body">{tower.time}</td>
                </tr>
              {/each}
            </tbody>
          </div>
        </table>
      </div>
    {/if}
  </div>
</main>

<style>
  .main {
    /* display: flex; */
    /* align-items: flex-start; */
    margin-left: 3%;
    width: 94vw;
    margin-top: 30px;
  }
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

  .container-map {
    height: 80vh;
    width: 100%;
    display: flex;
  }
  .map-container {
    height: 80vh;
    width: 100%;
  }
  .sidebar {
    width: 28%;
    height: 63.4vh;
    position: absolute;
    right: 10px;
    border-radius: 25px;
    margin-top: 8px;
  }

  *::-webkit-scrollbar {
    width: 5px;
  }
  *::-webkit-scrollbar-track {
    background: white;
  }

  *::-webkit-scrollbar-thumb {
    background-color: blue;
    border-radius: 20px;
    border: 3px solid rgb(173, 173, 172);
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
  .number {
    height: 4vh;
    width: 35vw;
    border-radius: 4px;
    border: 2px solid rgb(51, 7, 121);
    align-content: center;
    font-size: large;
  }
  .date {
    height: 4vh;
    width: 10vw;
    border-radius: 4px;
    border: 2px solid rgb(51, 7, 121);
    align-content: center;
    font-size: large;
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

  .table-map {
    color: black;
    overflow: auto;
  }

  .table-head {
    /* border: 1px solid black; */
    /* border-radius: 25px; */
    background-color: #6fa2c7;
    /* border-top-left-radius: 25px; */
    border-top-right-radius: 25px;
  }

  .table-heading {
    width: 6.85vw;
    padding: 2px;
    height: 6vh;
    font-size: 14px;
    border-left: 1px solid #00000029;
  }
  .table-content {
    overflow-y: scroll;
    scrollbar-width: thin;
    height: 57vh;
    background-color: white;
    border-bottom-left-radius: 25px;
  }
  .table-body {
    border: 1px solid #00000029;
    width: 7.8vw;
    padding: 2px;
    height: 6vh;
    font-size: 14px;
    text-align: center;
    word-break: break-word;
    overflow-y: auto;
  }
</style>
