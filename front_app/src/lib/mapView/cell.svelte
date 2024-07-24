<script>
// @ts-nocheck

  import { onMount, afterUpdate } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, LineString, Polygon } from "ol/geom";
  import { Icon, Style, Stroke, Text, Fill } from "ol/style";
  import { fromLonLat } from "ol/proj";
    import { basepath } from "$lib/config";

  let mapContainer;
  let map;
  let USER_NUMBER;
  let from_date = "";
  let to_date = "";
  let userData = [];
  let lineLayer;
  let semiCircleLayer;
  let Type = "";
  let fromDate = "";
  let toDate = "";
  let toDateValue;
  let fromDateValue;
  let requestData = {};
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
    //     center: [0, 0],
    //     zoom: 2,
    //   }),
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
          document.body.appendChild(tooltip);

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

  async function sendNumberToFlask(event) {
    event.preventDefault();
    const userNumber = USER_NUMBER.trim();
    fromDateValue = from_date.trim();
    toDateValue = to_date.trim();
    const type = Type.trim();
    console.log(fromDate, toDate);
    if (userNumber && fromDateValue && toDateValue) {
      requestData = {
        userNumber,
        fromDate: fromDateValue,
        toDate: toDateValue,
        type,
      };
    } else {
      requestData = {
        userNumber,
        type,
      };
    }
    console.log(requestData);

    if (userNumber) {
      try {
        const response = await fetch(
          `${basepath()}/cell_tower_tracking`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
          }
        );

        console.log("Response:", response);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        } else {
          const data = await response.json();
          console.log(data);

          userData = [];
          lineLayer.getSource().clear();
          semiCircleLayer.getSource().clear();
          console.log(data.cell_ids["tower_date"]);

          data.cell_ids.sort((a, b) => {
            const dateComparison = a.tower_date.localeCompare(b.tower_date);
            if (dateComparison === 0) {
              return a.tower_time.localeCompare(b.tower_time);
            }
            return dateComparison;
          });

          // data.cell_ids.sort((a, b) => {
          //   const timestampA = new Date(a.timestamp).getTime();
          //   const timestampB = new Date(b.timestamp).getTime();
          //   return timestampA - timestampB;
          // });

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

            feature.setStyle(
              new Style({
                image: new Icon({
                  src: "tower.png",
                  scale: 0.05,
                }),
              })
            );

            userData.push(feature);

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
            padding: [20, 20, 20, 20],
          });

          const vectorLayer = new VectorLayer({
            source: new VectorSource({
              features: userData,
            }),
          });

          map.addLayer(vectorLayer);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    } else {
      alert("Please enter a valid user name.");
    }
  }
</script>

<main class="main">
  <form>
    <input type="text" bind:value={USER_NUMBER} />
    <input type="date" bind:value={from_date} />
    <input type="date" bind:value={to_date} />
    <select name="Types" bind:value={Type}>
      <option value="cdr">CDR</option>
      <option value="ipdr">IPDR</option>
    </select>
    <button on:click={(event) => sendNumberToFlask(event)}>Show</button>
  </form>
  <div class="map-container" bind:this={mapContainer} />
</main>

<style>
  .map-container {
    height: 75vh;
    width: 100%;
  }
</style>