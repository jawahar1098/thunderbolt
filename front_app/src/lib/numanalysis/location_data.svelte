<script>
  // @ts-nocheck

  import { onMount } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM,XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point } from "ol/geom";
  import { fromLonLat } from "ol/proj";
  import { basepath } from "$lib/config";
  import { afterUpdate } from "svelte";

  let mapContainer;
  let map;
  let vectorLayer;
  export let propData;
  console.log("Propdataaaaaaaaaaaaaaaaaa", propData);
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let currentPage = 1;
  let itemsPerPage = 0;

  let data = {};
  let showProgress = false;
  let gotResult = false;
  let data_found = "Not Data Yet";
  let currentTooltip;
  let clickedNumberData = [];
  let showSidebar = false;

  function removeTooltip() {
    if (currentTooltip && currentTooltip.parentNode === mapContainer) {
      mapContainer.removeChild(currentTooltip);
      currentTooltip = null;
    }
  }

  async function total_locations() {
    gotResult = false;
    const total_locations = new FormData();
    total_locations.append("number", number);
    if (startDate) total_locations.append("from_date", startDate);
    if (endDate) total_locations.append("to_date", endDate);
    total_locations.append("mode", "TotalLocation");
    total_locations.append("page", currentPage);
    total_locations.append("items_per_page", itemsPerPage);
    showProgress = true;
    try {
      const response = await fetch(`${basepath()}/location`, {
        method: "POST",
        body: total_locations,
      });

      if (response.ok) {
        data = await response.json();
        //   console.log(data);
        if (data["headers"] === "No Data") {
          showProgress = false;
          data_found = "No Data Matched With Database";
        } else {
          addPointsToMap(data);
          console.log("Location data came to frontend:", data);
        }
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      total_locations();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  onMount(() => {
    map = new Map({
      target: mapContainer,
      layers: [
        new TileLayer({
          source: new OSM({
            attributions: [],
          }),
        }),
      ],
      view: new View({
        center: fromLonLat([78.9629, 20.5937]),
        zoom: 5,
      }),
    });

    // map = new Map({
    //     target: mapContainer,
    //     layers: [
    //       new TileLayer({
    //         source: new XYZ({
    //           url: 'http://10.50.50.150:8082/tile/{z}/{x}/{y}.png'
    //         }),
    //       }),

    //     ],
    //     view: new View({
    //     center: fromLonLat([78.9629, 20.5937]),
    //     zoom: 5,
    //   }),
    //   });

    total_locations();
    map.on("click", handleMapClick);
  });

  function addPointsToMap(data) {
    console.log("entered intp addPointsTo Map", data.data_dict.latitude);
    const vectorSource = new VectorSource();

    data.data_dict.forEach((item) => {
      console.log("entered into coordinates");
      const firstcall = item.first_call;
      const lastcall = item.last_call;
      const nickname = item.nickname;
      const site_address = item.site_address;
      const source_number = item.source_number;
      const tower_id = item.tower_id;
      const total_calls = item.total_calls;
      const user_address = item.user_address;
      if (item.latitude && item.longitude) {
        const point = new Point(
          fromLonLat([parseFloat(item.longitude), parseFloat(item.latitude)])
        );
        // console.log("coordinates", point);
        const feature = new Feature({
          geometry: point,
        });
        feature.set("firstcall", firstcall);
        feature.set("lastcall", lastcall);
        feature.set("nickname", nickname);
        feature.set("site_address", site_address);
        feature.set("source_number", source_number);
        feature.set("tower_id", tower_id);
        feature.set("total_calls", total_calls);
        feature.set("user_address", user_address);

        vectorSource.addFeature(feature);
      }
    });

    vectorLayer = new VectorLayer({
      source: vectorSource,
    });

    map.addLayer(vectorLayer);
    // Function to handle map click event
    map.on("click", function () {
      removeTooltip();
    });

    map.on("singleclick", (event) => {
      removeTooltip();
      console.log("Single click event");
      map.forEachFeatureAtPixel(event.pixel, (feature) => {
        console.log("Feature clicked:", feature);
        if (feature) {
          const firstCall = feature.get("firstcall");
          const lastCall = feature.get("lastcall");
          const tooltip = document.createElement("div");
          tooltip.className = "tooltip";
          tooltip.innerHTML = `First Call: ${firstCall}, Last Call: ${lastCall}`;
          Object.assign(tooltip.style, {
            position: "absolute",
            backgroundColor: "white",
            padding: "5px",
            borderRadius: "4px",
            border: "1px solid #cccccc",
            whiteSpace: "nowrap",
            left: `${event.pixel[0] + 10}px`,
            top: `${event.pixel[1] - 20}px`,
            zIndex: "1000",
          });
          mapContainer.appendChild(tooltip);
          currentTooltip = tooltip;
          console.log("Tooltip:", currentTooltip);
          setTimeout(() => {
            removeTooltip();
          }, 5000);
        }
      });
    });
  }
  afterUpdate(() => {
    removeTooltip();
  });
  function handleMapClick(event) {
    console.log("Map clicked!");
    const clickedFeature = map.forEachFeatureAtPixel(
      event.pixel,
      (feature) => feature
    );
    console.log(clickedFeature);

    if (clickedFeature) {
      clickedNumberData = [];
      clickedNumberData.push({ "First Call": clickedFeature.get("firstcall") }); // Push as key-value pairs
      clickedNumberData.push({ "Last Call": clickedFeature.get("lastcall") });
      clickedNumberData.push({" Nickname": clickedFeature.get("nickname") });
      clickedNumberData.push({
        "site address": clickedFeature.get("site_address"),
      }); // Push as key-value pairs
      clickedNumberData.push({
        "source number": clickedFeature.get("source_number"),
      });
      clickedNumberData.push({ "tower id": clickedFeature.get("tower_id") });
      clickedNumberData.push({
        "total calls": clickedFeature.get("total_calls"),
      });
      clickedNumberData.push({
        "user address": clickedFeature.get("user_address"),
      });
      console.log(clickedNumberData, "clickednumberdata");
      showSidebar = true;
    } else {
      clickedNumberData = [];
      showSidebar = false;
    }
  }
</script>

<div class="map-container" bind:this={mapContainer} />
{#if showSidebar === true}
  <div class="sidebar">
   
      {#each clickedNumberData as item}
      {#each Object.entries(item) as [key, value]}
      <div class="side_container">
        <p class="side_header" style="word-break: break-word; margin:0;">{key}</p>
        <p class="side_value" style="word-break: break-word; margin:0;">{value}</p>
      </div>
      {/each}
    {/each}
    
    
  </div>
{/if}

<style>
  .map-container {
    height: 74vh;
    width: 100%;
    position: relative; /* Ensure the container is positioned relatively */
    overflow: auto; /* Allow overflow for scrolling */
  }
  .sidebar {
    width: 28%;
    height: 63.4vh;
    position: absolute;
    right: 10px;
    border-radius: 25px;
    margin-top: 24px;
    top: 0;
    background: white;
    display: flex;
    flex-direction: column;
  }
  .side_container{
    /* display: flex; */
    font-size: 14px;
    padding: 10px;

  }
  .side_header{
    color: #296b97;
    text-transform: capitalize;
  }
  .side_value{
    margin-left: 5px;
    display: flex;
    
    justify-content: center;
  }
  
</style>
