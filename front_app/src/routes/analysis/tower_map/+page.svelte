<script>
  // @ts-nocheck

  import { onMount, afterUpdate } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM,XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, LineString, Polygon } from "ol/geom";
  import { Style, Stroke, Fill, Icon, Text } from "ol/style";
  import { fromLonLat } from "ol/proj";
  import { basepath } from "$lib/config";

  let mapContainer;
  let map;
  let USER_NUMBER;
  let from_date = "";
  let to_date = "";
  let vectorLayer;
  let circleLayer;
  let userData = [];
  let lineLayer;
  let semiCircleLayer;
  let Type = "";
  let fromDate = "";
  let toDate = "";
  let toDateValue;
  let fromDateValue;
  let requestData = {};
  let labels = { first: "First", last: "Last" };
  let totalPages;
  let currentPageDataStart;
  let currentPageDataEnd;
  let totalDataCount;
  let currentPage = 1;
  let items_per_page = 10;
  let total = 0;
  let pagination = false;

  function createSemiCircleGeometry(center, radius, azimuthAngle) {
    const centerLon = center[0];
    const centerLat = center[1];
    let compassAngle = (90 - azimuthAngle) % 360;
    if (compassAngle < 0) {
      compassAngle += 360;
    }
    const startAngle = (compassAngle - 60) * (Math.PI / 180);
    const endAngle = (compassAngle + 60) * (Math.PI / 180);
    const numPoints = 100;
    const angleIncrement = (endAngle - startAngle) / (numPoints - 1);
    const semiCircleCoordinates = [];
    for (let i = 0; i < numPoints; i++) {
      const angle = startAngle + i * angleIncrement;
      const lon = centerLon + radius * Math.cos(angle);
      const lat = centerLat + radius * Math.sin(angle);
      semiCircleCoordinates.push([lon, lat]);
    }
    semiCircleCoordinates.push([centerLon, centerLat]);
    const semiCircle = new Polygon([semiCircleCoordinates]);
    return semiCircle;
  }

  onMount(() => {
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

    // Offline map 

    map = new Map({
    	target: mapContainer,
    	layers: [
    		new TileLayer({
    			source: new XYZ({
    				url: 'http://10.50.50.150:8082/tile/{z}/{x}/{y}.png'
    			}),
    		}),
    		
    	],
    	view: new View({
    		center: [0, 0],
    		zoom: 2
    	})
    });


    lineLayer = new VectorLayer({
      source: new VectorSource(),
      style: function (feature) {
        return new Style({
          stroke: new Stroke({
            color: "blue",
            width: 2,
          }),
          text: new Text({
            text: feature.get("tower_time") + "\n" + feature.get("date"),
            offsetY: -20,
            fill: new Fill({
              color: "black",
            }),
          }),
        });
      },
    });
    semiCircleLayer = new VectorLayer({
      source: new VectorSource(),
    });
    vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: userData,
      }),
    });

    map.addLayer(vectorLayer);
    map.addLayer(lineLayer);
    map.addLayer(semiCircleLayer);
    map.on("singleclick", (event) => {
      map.forEachFeatureAtPixel(event.pixel, (feature) => {
        if (feature) {
          console.log("Feature Properties:", feature.getProperties());
          // Show tooltip
          const towerTime = feature.get("tower_time");
          const azimuth = feature.get("azimuth");
          const tooltip = document.createElement("div");
          tooltip.className = "tooltip";
          tooltip.innerHTML = `Tower Time: ${towerTime}`;
          tooltip.style.position = "absolute";
          tooltip.style.backgroundColor = "white";
          tooltip.style.padding = "5px";
          tooltip.style.borderRadius = "4px";
          tooltip.style.border = "1px solid #cccccc";
          tooltip.style.whiteSpace = "nowrap";
          tooltip.style.left = `${event.pixel[0] + 10}px`;
          tooltip.style.top = `${event.pixel[1] - 20}px`;

          const centerLonLat = feature.getGeometry().getCoordinates();
          const radius = 100;

          if (feature.get("azimuth")) {
            const semiCircleGeometry = createSemiCircleGeometry(
              centerLonLat,
              radius,
              azimuth
            );
            const semiCircleFeature = new Feature({
              geometry: semiCircleGeometry,
            });

            semiCircleFeature.setStyle(
              new Style({
                fill: new Fill({
                  color: "rgba(0, 0, 255, 0.2)",
                }),
                stroke: new Stroke({
                  color: "blue",
                  width: 2,
                }),
              })
            );

            semiCircleLayer.getSource().addFeature(semiCircleFeature);
          } else {
            const semiCircleGeometry = createSemiCircleGeometry(
              centerLonLat,
              radius,
              azimuth
            );
            const semiCircleFeature = new Feature({
              geometry: semiCircleGeometry,
            });

            semiCircleFeature.setStyle(
              new Style({
                fill: new Fill({
                  color: "rgba(0, 0, 255, 0.2)",
                }),
                stroke: new Stroke({
                  color: "blue",
                  width: 2,
                }),
              })
            );
            const startPoint = centerLonLat;
            const endPoint = [
              centerLonLat[0] + radius * Math.cos((azimuth * Math.PI) / 180),
              centerLonLat[1] + radius * Math.sin((azimuth * Math.PI) / 180),
            ];
            const lineFeature = new Feature({
              geometry: new LineString([startPoint, endPoint]),
              tower_time: feature.get("tower_time"),
            });

            lineLayer.getSource().addFeature(lineFeature);
            semiCircleLayer.getSource().addFeature(semiCircleFeature);
          }
        }
      });
    });
  });

  afterUpdate(() => {
    const tooltips = document.querySelectorAll(".tooltip");
    tooltips.forEach((tooltip) => {
      tooltip.remove();
    });
  });

  async function sendNumberToFlask(page) {
    const userNumber = USER_NUMBER.trim();
    fromDateValue = from_date.trim();
    toDateValue = to_date.trim();
    const type = Type.trim();

    if (userNumber && fromDateValue && toDateValue) {
      requestData = {
        userNumber,
        fromDate: fromDateValue,
        toDate: toDateValue,
        type,
        page: page,
        items_per_page: items_per_page,
      };
    } else {
      requestData = {
        userNumber,
        type,
        page: page,
        items_per_page: items_per_page,
      };
    }

    if (userNumber) {
      try {
        const response = await fetch(`${basepath()}/cell_tower`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        } else {
          const data = await response.json();
          console.log(data, "-------------");
          total = data.totalpages;
          if (total > items_per_page) {
            pagination = true;
          }

          userData = [];
          vectorLayer.getSource().clear(); // Clear the vectorLayer source
          lineLayer.getSource().clear();
          semiCircleLayer.getSource().clear();

          data.cell_ids.sort((a, b) => {
            const dateComparison = a.tower_date.localeCompare(b.tower_date);
            if (dateComparison === 0) {
              return a.tower_time.localeCompare(b.tower_time);
            }
            return dateComparison;
          });

          data.cell_ids.forEach((cell, index) => {
            const lonLat = [
              parseFloat(cell.tower_longitude),
              parseFloat(cell.tower_latitude),
            ];
            const feature = new Feature({
              geometry: new Point(fromLonLat(lonLat)),
              tower_time: cell.tower_time,
              azimuth: cell.azimuth,
              date: cell.tower_date,
            });
            const textStyle = new Text({
              text: `${cell.tower_time}\n${cell.tower_date}`,
              offsetY: -30,
              fill: new Fill({
                color: "#000",
              }),
              font: "bold 14px Arial",
            });

            feature.setStyle(
              new Style({
                image: new Icon({
                  src: "/tower.png",
                  scale: 0.05,
                }),
                text: textStyle,
              })
            );

            userData.push(feature);
            vectorLayer.getSource().addFeature(feature);

            if (index > 0) {
              const prevCell = data.cell_ids[index - 1];
              const prevLonLat = [
                parseFloat(prevCell.tower_longitude),
                parseFloat(prevCell.tower_latitude),
              ];

              const lineFeature = new Feature({
                geometry: new LineString([
                  fromLonLat(prevLonLat),
                  fromLonLat(lonLat),
                ]),
                tower_time: cell.tower_time,
                date: cell.tower_date,
              });

              lineLayer.getSource().addFeature(lineFeature);
            }
          });

          const extent = userData.reduce((extent, feature) => {
            return extent
              ? extent.concat(feature.getGeometry().getExtent())
              : feature.getGeometry().getExtent();
          }, null);

          map.getView().fit(extent, {
            padding: [0, 0, 0, 0],
          });
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    } else {
      alert("Please enter a valid user name.");
    }

    totalDataCount = total;
    currentPage = page;
    currentPageDataStart = (currentPage - 1) * items_per_page + 1;
    currentPageDataEnd = Math.min(currentPage * items_per_page, totalDataCount);
    totalPages = Math.ceil(totalDataCount / items_per_page);
  }
</script>

<main class="main">
  <form on:submit|preventDefault>
    <input class="number" id="blur" type="text" bind:value={USER_NUMBER} />
    <input class="date" type="date" bind:value={from_date} />
    <input class="date" type="date" bind:value={to_date} />
    <select
      class="form-select"
      aria-label="Default select example"
      name="Types"
      bind:value={Type}
    >
      <option value="cdr">CDR</option>
      <option value="ipdr">IPDR</option>
    </select>
    <button
      type="button"
      class="btn btn-success"
      on:click={() => sendNumberToFlask(currentPage)}>Show</button
    >
  </form>
  <div class="map-container" bind:this={mapContainer} />
</main>
<!-- {#if pagination}
  <div class="footer">
    <div class="shownumber">
      <button
        class="btn"
        on:click={() => sendNumberToFlask(1)}
        disabled={currentPage === 1}>{labels.first}</button
      >
      <button
        class="btn"
        on:click={() => sendNumberToFlask(currentPage - 1)}
        disabled={currentPage === 1 || currentPage === totalPages}
        >{currentPage === 1 || currentPage === totalPages
          ? ""
          : currentPage - 1}</button
      >
      <button
        class="btn"
        on:click={() => sendNumberToFlask(currentPage + 1)}
        disabled={currentPage === totalPages}
        >{currentPage === totalPages ? "" : currentPage + 1}</button
      >
      <button
        class="btn"
        on:click={() => sendNumberToFlask(totalPages)}
        disabled={currentPage === totalPages}>{labels.last}</button
      >
    </div>
  </div>
{/if} -->

<style>
  .main {
    /* display: flex; */
    /* align-items: flex-start; */
    margin-left: 3%;
    width: 95vw;
    margin-top: 50px;
  }
  .map-container {
    height: 87vh;
    width: 100%;
  }
  form {
    margin: 1vh;
    display: flex;
    justify-content: center;
    gap: 0.5vw;
  }
  .footer {
    display: flex;
    justify-content: center;
    margin-top: 2vh;
  }
  select {
    width: 8vw;
    border: 2px solid rgb(51, 7, 121);
    color: rgb(51, 7, 121);
  }
  .number {
    height: 4vh;
    width: 20vw;
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

  #blur {
    /* filter: blur(4px); */
  }
</style>
