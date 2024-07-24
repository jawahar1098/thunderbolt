<script>
  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import Map from "ol/Map";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, LineString } from "ol/geom";
  import { Icon, Style, Stroke, Text, Fill } from "ol/style";
  import { fromLonLat } from "ol/proj";
  import Overlay from "ol/Overlay";
  import * as XLSX from "xlsx";
  import { each } from "highcharts";
  import { split } from "postcss/lib/list";
  import { tree } from "d3";
  import { postRequest } from "$lib/req_utils";

  // export let key_location;
  // export let sitename;
  // export let startDate;
  // export let endDate ;
  export let selectedValues;
  export let casename;
  export let casetype;
  export let user;
  let mapContainer;
  let map;
  let final_result = [];
  let ind_num_val = [];
  let result = [];
  let zero_dur_num = [];
  let cdat_source = [];
  let cdat_imei = [];
  let cdat_des_in_phone = [];
  let cdat_src_in_des = [];
  let vigor_num = [];
  let sidedata = false;
  let selectedTower = [];
  let isLoading = false;

  let gotResult = false;
  let showprogress = false;
  let userDetails = JSON.parse(localStorage.getItem("userDetails"));
  console.log(ind_num_val, "==============");
  let showValue = false;
  let tooltipValue = "";

  function showsCard(data) {
    showValue = true;
    console.log(data, "==============");
    tooltipValue = data.map((item) => {
      let tooltip = "";
      if (item.source_numbers) {
        if (Array.isArray(item.source_numbers)) {
          tooltip += `Source Number\n`;
          for (let i = 0; i < item.source_numbers.length; i++) {
            tooltip += `${item.source_numbers[i]}\n`;
          }
        } else {
          tooltip.split(",");
          tooltip += `Source Number: ${item.source_numbers} count :${item.count}\n`;
        }
      }
      if (item.imeis) {
        if (Array.isArray(item.imeis)) {
          tooltip += `IMEI: \n${item.imeis.join("\n")}\n`;
        } else {
          tooltip += `IMEI: \n${item.imeis || 0}\n`;
        }
      }
      if (item.destination_numbers) {
        if (Array.isArray(item.destination_numbers)) {
          tooltip += `Destination Number: \n${item.destination_numbers.join(
            "\n"
          )}\n`;
        } else {
          tooltip += `Destination Number: \n${item.destination_numbers}\n`;
        }
      }
      return tooltip.replace(/,/g, ""); // Remove commas from the entire tooltip
    });
  }

  // function showsCard(data) {
  //   showValue = true;
  //   console.log(data, "==============");
  //   tooltipValue = data.map((item) => {
  //     let tooltip = "";
  //     if (item.source_numbers) {
  //       if (Array.isArray(item.source_numbers)) {
  //         tooltip += `Source Number\n`;
  //         for (let i = 0; i < item.source_numbers.length; i++) {
  //           tooltip += `${item.source_numbers[i].split(",")}\n`;
  //         }
  //       } else {
  //         tooltip += `Source Number: ${item.source_numbers.split(",")}`;
  //         if (item.count) {
  //           tooltip += ` count: ${item.count}`;
  //         }
  //         tooltip += "/n";
  //       }
  //     }
  //     if (item.imeis) {
  //       if (Array.isArray(item.imeis)) {
  //         tooltip += `IMEI: \n${item.imeis.join("\n")}\n`;
  //       } else {
  //         tooltip += `IMEI: \n${item.imeis}\n`;
  //       }
  //     }
  //     if (item.destination_numbers) {
  //       if (Array.isArray(item.destination_numbers)) {
  //         tooltip += `Destination Number: \n${item.destination_numbers.join(
  //           "\n"
  //         )}\n`;
  //       } else {
  //         tooltip += `Destination Number: \n${item.destination_numbers}\n`;
  //       }
  //     }
  //     return tooltip.replace(/,/g, ""); // Remove commas from the entire tooltip
  //   });
  // }

  function hideCard() {
    showValue = false;
  }

  function getcasedata() {
    gotResult = false;
    isLoading = true;
    // fetch(`${basepath()}/getcasedata`, {
    //   method: "post",
    //   body: JSON.stringify({
    //     casename: casename,
    //     casetype: casetype,
    //     // itemsper_page: 50,
    //     // pagenumber: currentPage,
    //     mode: "detailed_view",
    //     user: user,
    //   }),
    // })

    const url = `${basepath()}/getcasedata`;
    postRequest(fetch,url,JSON.stringify({
        casename: casename,
        casetype: casetype,
        // itemsper_page: 50,
        // pagenumber: currentPage,
        mode: "detailed_view",
        user: user,
      }))
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        result = data.distinct_sdi[0];
        cdat_source = data.cdat_source[0];
        cdat_des_in_phone = data.cdat_des_in_phone[0];
        cdat_imei = data.cdat_imei[0];
        cdat_src_in_des = data.cdat_src_in_des[0];
        // cdatnumber_for_imei = data.cdatnumber_for_imei[0];
        vigor_num = data.vigor_num[0];
        zero_dur_num = data.zero_dur_num[0];

        addFeaturesToMap();
        // console.log(result.lat, "zero");
        gotResult = true;
        isLoading = false;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        isLoading = false; // Set isLoading to false in case of error
      });
  }

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

    if (casename !== "") {
      getcasedata();
    }
  });
  function addFeaturesToMap() {
    let vectorSource = new VectorSource();

    result.forEach((item) => {
      if (item.lat !== undefined && item.long !== undefined) {
        let latitude = parseFloat(item.lat);
        let longitude = parseFloat(item.long);

        let feature = new Feature({
          geometry: new Point(fromLonLat([longitude, latitude])),
        });

        feature.setStyle(
          new Style({
            image: new Icon({
              src: "/airtel.png",
              scale: 0.15,
            }),
          })
        );

        vectorSource.addFeature(feature);

        var element = document.createElement("div");
        element.innerHTML = `
                <div style="font-size:10px;font-weight:600;font-family:'Raleway'">Site Name: ${item.sitename}</div>
                <div style="display:flex;justify-content:space-evenly">
                    <img src="/incomingcall.svg" alt="source number" style="width: 10%;background:transparent" />
                    <div style="font-size:16px;color:green">${item.source_numbers.length}</div>
                    <img src="/device.svg" alt="source number" style="width: 10%;background:transparent" />
                    <div style="font-size:16px;color:blue">${item.imeis.length}</div>
                    <img src="/outgoingcall.svg" alt="source number" style="width: 10%;background:transparent" />
                    <div style="font-size:16px;color:red">${item.destination_numbers.length}</div>
                </div>
            `;
        element.className = "tower-label";
        element.style.width = "18em";
        element.style.wordBreak = "break-all";
        element.style.fontSize = "10px";
        element.style.fontWeight = "bold";
        element.style.display = "flex";
        element.style.flexDirection = "column";
        element.style.alignItems = "flex-start";
        element.style.border = "1px solid black";
        element.style.borderRadius = "3px";
        element.style.background = "transparent";
        element.style.padding = "3px";
        element.style.cursor = "pointer";

        var overlay = new Overlay({
          element: element,
          positioning: "bottom-center",
          stopEvent: false,
          offset: [0, -50],
        });

        overlay.setPosition(fromLonLat([longitude, latitude]));

        element.addEventListener("click", () => {
          selectedTower = item;
          sidedata = true;
        });

        map.addOverlay(overlay); // Add overlay to the map for every feature
      }
    });

    let vectorLayer = new VectorLayer({
      source: vectorSource,
    });

    map.addLayer(vectorLayer);

    // Add event listener for zoom change
    let overlays = map.getOverlays().getArray();
    overlays.forEach((overlay) => {
      overlay.getElement().style.display = "none";
    });

    // Add event listener for zoom change
    map.on("moveend", function () {
      let zoom = map.getView().getZoom();
      let overlays = map.getOverlays().getArray();
      console.log(overlays, zoom);
      overlays.forEach((overlay) => {
        if (zoom <= 6) {
          overlay.getElement().style.display = "none"; // Hide the overlays when zoomed out
        } else if (zoom >= 6) {
          overlay.getElement().style.display = "flex"; // Show the overlays when zoomed in
        }
      });
    });
  }

  $: towerDetails = updateTowerDetails(selectedTower);

  function updateTowerDetails(item) {
    if (sidedata) {
      const sourceNumbers = Array.isArray(item.source_numbers)
        ? item.source_numbers.join(" ").replace(",", " ")
        : item.source_numbers;
      console.log(sourceNumbers, "source");
      const imeiNumbers = Array.isArray(item.imeis)
        ? item.imeis.join(" ").replace(",", " ")
        : item.imeis;
      console.log(imeiNumbers, "imeis");
      const destinationNumbers = Array.isArray(item.destination_numbers)
        ? item.destination_numbers.join(" ").replace(",", " ")
        : item.destination_numbers;
      console.log(destinationNumbers, "destination");

      return {
        sitename: item.sitename,
        sourceNumbers: sourceNumbers,
        imeiNumbers: imeiNumbers,
        destinationNumbers: destinationNumbers,
      };
    } else {
      return {
        sitename: "Alternative Site Name",
        sourceNumbers: "Alternative Source Number",
        imeiNumbers: "Alternative IMEI Number",
        destinationNumbers: "Alternative Destination Number",
      };
    }
  }
</script>

<!-- <div
  style="display: flex; flex-direction: column; width:37em;height: 43rem;
  margin: 10px;border:2px solid #d4ebf7;
  border-radius: 5px;"
>
  <div style="display:flex ;justify-content:space-evenly ;margin-top: 1rem;">
    <img
      src="/incomingcall.svg"
      alt="source number"
      style="width: 8%;
  height: 60%;"
    />
    <div>Source Number</div>
  </div>
  <div style="display:flex ;justify-content:space-evenly; margin-left:1rem;">
    <img
      src="/outgoingcall.svg"
      alt="source number"
      style="width: 8%;
  height: 60%;"
    />
    <div>Destination Number</div>
  </div>
  <div style="display:flex ;justify-content:space-evenly;">
    <img
      src="/device.svg"
      alt="source number"
      style="width: 8%;
  height: 60%;"
    />
    <div>Imei Number</div>
  </div> -->
<div style="width: 93vw;">
  <div style="width:96%;border:2px solid #d4ebf7;border-radius:5px;">
    <div style="display: flex;margin-top: 0.5rem; width: 32%;">
      <div style="display:flex; margin-left:1rem;">
        <img src="/incomingcall.svg" alt="source number" class="image" />
        <div style="padding-left: 0.7rem;">Source Number</div>
      </div>
      <div style="display:flex;">
        <img src="/outgoingcall.svg" alt="source number" class="image" />
        <div style="padding-left: 0.7rem;">Destination Number</div>
      </div>
      <div style="display:flex;">
        <img src="/device.svg" alt="source number" class="image" />
        <div style="padding-left: 0.7rem;">Imei Number</div>
      </div>
    </div>
    <div style="display: flex; width:99%;">
      <div class="map-container" bind:this={mapContainer}>
        {#if isLoading}
          <div class="loading-spinner"></div>
        {/if}
      </div>
      <div>
        {#if sidedata}
          <div class="site">
            <div
              style="font-size: 16px; font-weight: 600; font-family: Raleway; padding:0.5rem;height:5rem;"
            >
              Site Name
              <div class="data">
                <span>{towerDetails.sitename}</span>
              </div>
            </div>
          </div>
          <div class="source-datas">
            <div
              style="font-size: 16px; margin-top: 5px; padding:0.5rem;font-weight:600; font-family: Raleway"
            >
              Source Number:
            </div>
            <div class="data">
              {#each towerDetails.sourceNumbers.split(" ") as sourceNumbers}
                <span
                  style="padding: 0.2rem; margin: 0.2rem;background:#d4ebf7;height:fit-content;border-radius: 3px;"
                  >{sourceNumbers}</span
                >
              {/each}
            </div>
            <!-- Use selectedTower.sourceNumbers instead of selectedTower.source_numbers -->
          </div>
          <div class="imei-datas">
            <div
              style="font-size: 16px; padding: 0.5rem; overflow-y: scroll; font-family: Raleway; font-weight:600"
            >
              IMEI Number:
            </div>
            <div class="data">
              {#each towerDetails.imeiNumbers.split(" ") as imeiNumbers}
                <span
                  style="padding: 0.2rem; margin: 0.2rem;background:#d4ebf7;height:fit-content;border-radius: 3px;"
                  >{imeiNumbers}</span
                >
              {/each}
            </div>
            <!-- Use selectedTower.imeiNumbers instead of selectedTower.imeis -->
          </div>
          <div class="datas">
            <div
              style="font-size: 16px; padding: 0.5rem;font-weight:600; overflow-y: scroll; font-family: Raleway;"
            >
              Destination Number:
            </div>
            <div class="dest-data">
              {#each towerDetails.destinationNumbers.split(" ") as destination_numbers}
                <span
                  style="padding: 0.2rem; margin: 0.2rem;background:#d4ebf7 ; width:25%; height:fit-content;border-radius: 3px;"
                  >{destination_numbers}</span
                >
              {/each}
            </div>
            <!-- Use selectedTower.destinationNumbers instead of selectedTower.destination_numbers -->
          </div>
        {/if}
      </div>
    </div>
  </div>
  <div class="card">
    <div class="down-text">
      <p style="font-weight: 600; font-family:Raleway">CDR Matched Source</p>
      <p>
        There are <span
          class="text"
          on:mouseover={() => showsCard(cdat_source)}
          on:mouseout={hideCard}
          title={tooltipValue}
        >
          {#if cdat_source.length > 0}
            {#each cdat_source as source}
              {source.source_numbers.length}
            {/each}
          {:else}
            {0}
          {/if}
        </span>
        <span style="color: red;"> source number </span>
        are matched with the <span style="color: red;"> CDR Record </span>
      </p>
      <p style="font-weight: 600; font-family:Raleway">CDR Matched IMEI</p>
      <p>
        There are <span
          class="text"
          on:mouseover={() => showsCard(cdat_imei)}
          on:mouseout={hideCard}
          title={tooltipValue}
        >
          {#if cdat_imei.length > 0}
            {#each cdat_imei as cdat_imeis}
              {cdat_imeis.imeis.length}
            {/each}
          {:else}
            {0}
          {/if}
        </span>
        <span style="color: red;"> imei number </span>
        are matched with the <span style="color: red;"> CDR Record </span>
      </p>
      <p style="font-weight: 600; font-family:Raleway">CDR Zero Duration</p>
      <p>
        There are <span
          class="text"
          on:mouseover={() => showsCard(zero_dur_num)}
          on:mouseout={hideCard}
          title={tooltipValue}>{zero_dur_num.length}</span
        >
        <span style="color: red;"> Zero Duration Number </span>
        are matched with the <span style="color: red;"> CDR Record </span>
      </p>
      <p style="font-weight: 600; font-family:Raleway">
        CDR Soruce in Destination
      </p>
      <p>
        There are <span
          class="text"
          on:mouseover={() => showsCard(cdat_src_in_des)}
          on:mouseout={hideCard}
          title={tooltipValue}
        >
          {#if cdat_src_in_des.length > 0}
            {#each cdat_src_in_des as src_number}
              {src_number.destination_numbers.length}
            {/each}
          {:else}
            {0}
          {/if}
        </span>
        <span style="color: red;"> Source Number </span>
        are matched with the
        <span style="color: red;"> Destination Number of CDR Record </span>
      </p>
      <p style="font-weight: 600; font-family:Raleway">
        CDR Destination in Source
      </p>
      <p>
        There are <span
          class="text"
          on:mouseover={() => showsCard(cdat_des_in_phone)}
          on:mouseout={hideCard}
          title={tooltipValue}
        >
          {#if cdat_des_in_phone.length > 0}
            {#each cdat_des_in_phone as des_number}
              {des_number.source_numbers.length}
            {/each}
          {:else}
            {0}
          {/if}
        </span>
        <span style="color: red;"> Destination Number </span>
        are matched with the
        <span style="color: red;"> Source Number of CDR Record </span>
      </p>
    </div>
  </div>
</div>

<style>
  .image {
    width: 10%;
  }
  #destinationNumber {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
  }

  #imei {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
  }

  .data {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
    overflow-y: scroll;
    height: 5rem;
  }
  .dest-data {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
    overflow-y: scroll;
    height: 15rem;
  }
  /* CSS for each number within the destination number container */

  .down-text {
    font-family: "Raleway";
    margin-left: 1rem;
  }

  .text {
    font-size: 1.2rem;
    font-weight: 600;
    color: #296b97;
  }
  .site {
    margin: 0.5rem;
    width: 28rem;
    word-break: break-all;
    box-shadow: 0px 1px 3px #5cb2eb;
    border-radius: 5px;
    height: 5rem;
  }
  .datas {
    margin: 0.5rem;
    width: 28rem;
    word-break: break-all;
    box-shadow: 0px 1px 3px #5cb2eb;
    border-radius: 5px;
    height: 18rem;
  }
  .imei-datas {
    margin: 0.5rem;
    width: 28rem;
    word-break: break-all;
    box-shadow: 0px 1px 3px #5cb2eb;
    border-radius: 5px;
    height: 8rem;
  }
  .source-datas {
    margin: 0.5rem;
    width: 28rem;
    word-break: break-all;
    box-shadow: 0px 1px 3px #5cb2eb;
    border-radius: 5px;
    height: 10rem;
  }

  .map-container {
    margin: 1rem 0rem 0rem 1rem;
    width: 100%;
    height: 70vh;
  }
  .card {
    margin-top: 1rem;
    position: relative;
    background-color: #fff;
    width: 96%;
    padding: 10px;
    left: 0%;
    overflow-x: scroll;
    margin-bottom: 1rem;
  }

  .text:hover {
    cursor: pointer;
  }
  .loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-top: 4px solid #000;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    position: absolute;
    top: 38%;
    left: 50%;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
