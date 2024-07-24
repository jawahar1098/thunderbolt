<script>
  // @ts-nocheck
  
    import { onMount, onDestroy } from "svelte";
    import Chart from 'chart.js/auto';
    import Map from "ol/Map";
    import "ol/ol.css";
    import View from "ol/View";
    import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
    import { OSM,XYZ, Vector as VectorSource } from "ol/source";
    import { fromLonLat,  transform } from "ol/proj";
    import {Style, Stroke, Fill, } from "ol/style";
    import { basepath } from "$lib/config";
    import { userDetailsStore } from '$lib/datastore.js';
    import GeoJSON from "ol/format/GeoJSON";
    import { goto } from "$app/navigation";
    import 'flatpickr/dist/flatpickr.css';
    import { getRequest, postRequest } from "$lib/req_utils";

    let mapContainer;
    let map;
    let vectorLayer;
    let circleLayer; // New vector layer for circles
    let vectorSource;
    let circleSource = new VectorSource();
    let PolygonSource = new VectorSource();
    let showlatlong;
    let Nexus = '';
    let vigor = '';
    let CDAT = '';
    let Ticketing = '';
    let Analysis = '';
    let Database = '';
    // let personlayer

    let userDetails;

    userDetailsStore.subscribe(value => {
    userDetails = value;
    // console.log("value",value)
    });

    onMount(() => {
    // beware of truthy and falsy values
    if (localStorage.getItem("userAuth")==="true"){
    userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
    }
    else{
    goto('/');
    }
    })

    let getdata = JSON.parse(localStorage.getItem('userDetails'))
    console.log(getdata)

    Nexus = getdata.Model && getdata.Model.includes('NEXUS');
    console.log(Nexus)

    vigor = getdata.Model && getdata.Model.includes('VIGOR');
    console.log(vigor)

    CDAT = getdata.Model && getdata.Model.includes('CDAT');
    console.log(CDAT)

    Ticketing = getdata.Model && getdata.Model.includes('TICKETING');
    console.log(Ticketing)

    Analysis = getdata.Model && getdata.Model.includes('ANALYSIS');
    console.log(Analysis)

    Database = getdata.Model && getdata.Model.includes('DATABASE');
    console.log(Database)
    
    onMount(() => {
    // report()
    const indianStatesGeoJSONPath = "/India_states.geojson";
    vectorSource = new VectorSource({
    format: new GeoJSON(),
    url: indianStatesGeoJSONPath,
    });

    const vectorLayer = new VectorLayer({
    source: vectorSource,
    style: function (feature) {
        const color = feature.get("color") || "#0000ff"; // Default to blue if no color is specified
        return new Style({
        stroke: new Stroke({
            color: color,
            width: 2,
        }),
        });
    },
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

    PolygonSource = new VectorLayer({
        source: circleSource,
        style: new Style({
        stroke: new Stroke({
            color: "green",
            width: 1,
        }),
        fill: new Fill({
            color: "rgba(255, 0, 0, 0.1)",
        }),
        }),
    });
    // map = new Map({
    //     target: mapContainer,
    //     layers: [
    //     new TileLayer({
    //         source: new OSM({
    //         attributions: [],
    //         }),
    //     }),
    //     vectorLayer,
    //     PolygonSource,
    //     circleLayer, // Add the circle layer to the map
    //     ],
    //     view: new View({
    //     center: fromLonLat([77.4533, 21.8903]),
    //     zoom: 4.8,
    //     }),
    // });
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
    });
    
    let VoipCallsCount = 0;
    let vpnsUsed = 0;
    let bpartycount = 0;
    let dayLocationCount = 0;
    let nightLocationCount = 0;

    onMount(async () => {
        
        const url = basepath() + "/dashboardCount"
        getRequest(fetch, url )
        .then(data => {
          VoipCallsCount = data.VoipCount;
          vpnsUsed = data.VPNCount;
          bpartycount = data.MatchedCount;
        })

        const ur = basepath() + "/daylocation"
        getRequest(fetch,url)
        .then(locationData =>{
          dayLocationCount = locationData.daycount;
          nightLocationCount = locationData.nightcount;
          
        }).catch(error => {

          console.error("Error fetching data:", error);
        })
        
        
    });
    let cdrdata_count; 
    let sdrdata_count;
    let suspect_count;
    let cellidchart_count;
    let gprs_count;
    let phonearea_count;
    let towerdata_count;
    
    onMount(() => {
      dashboard();
    })

    function dashboard() {
        const url = basepath() + "/dashboardcounts"
        getRequest(fetch,url)
        .then(data => {
            if (data) {
            console.log(data, "Data");
            cdrdata_count = data.cdrdata_count
            sdrdata_count = data.sdrdata_count
            suspect_count= data.suspect_count
            cellidchart_count =data.cellidchart_count
            gprs_count = data.gprs_count
            phonearea_count =data.phonearea_count
            towerdata_count = data.towerdata_count
            

            } 
        })
        .catch((err) => {
            console.error("Fetch error:", err);
        })
    }
    let pie1;
    let data = {
    labels: [],
    datasets: [{
        data: [],
        backgroundColor: ['#FF6347', '#40E0D0', '#FFD700'],
        hoverBackgroundColor: ['#FF4500', '#00CED1', '#FFA500'],


        borderAlign: 'center'
    }]
    };
    const createChart = async () => {
    try {
       const url = `${basepath()}/vigor`
        getRequest(fetch,url)
       .then(fetchedData => {
          data.labels = Object.keys(fetchedData);
          data.datasets[0].data = Object.values(fetchedData);
        })

        const ctx = document.getElementById('myPie').getContext('2d');

        if (pie1) {
        pie1.destroy();
        }

        pie1 = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
            legend: {
                position: 'right',
                align: 'center',
                labels: {
                boxWidth: 20,
                padding: 10,
                },
            },
            },
        },
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    };
    onMount(createChart);

    onDestroy(() => {
    if (pie1) {
        pie1.destroy();
    }
    });

    onMount(() => {
      report();
    })
    
    let cases =[];
    let Total_raise;
    let Total_approval;
    let Total_pending;
    let Total_closed;
    let Total_under_process;
    let Total_analysis_approval;
    let Total_analysis_pending;
    let Total_analysis_raise;
    let showticket=false

    function report() {
      const body =  {
            team : userDetails.team,
            module : userDetails.modules,
            designation : userDetails.designation,
            role : userDetails.role,
            email : userDetails.email
        }
        const url = basepath() + '/report2'
        postRequest(fetch,url, body)
        .then(response => {
        console.log(response)
        cases = response
        console.log(cases,'//////////////////////////////////////////////')
        Total_raise=cases['Total_raise'];
        Total_approval=cases['Total_approval'];
        Total_pending=cases['Total_pending'];
        Total_closed=cases['Total_close'];
        Total_under_process=cases['Total_under_process'];
        Total_analysis_raise = cases['Total_analysis_raise'];
        Total_analysis_approval = cases['Total_analysis_approval'];
        Total_analysis_pending = cases['Total_analysis_pending'];
        
        })
    }
</script>

<main>
  <div class="row1">
    {#if getdata.Model.length >= 2}
      {#if Ticketing === true || Ticketing === ""}
        <div class="col-4">
          <h2>Ticketing Stats</h2>
          <table class="ticket_table table-hover">
            <thead class="thead-dark">
              <tr>
                <th>Types</th>
                <th>Data</th>
                <th>Analysis</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Raised</td>
                <td>{Total_raise}</td>
                <td>{Total_analysis_raise}</td>
              </tr>
              <tr>
                <td>Approved</td>
                <td>{Total_approval}</td>
                <td>{Total_analysis_approval}</td>
              </tr>
              <tr>
                <td>Pending</td>
                <td>{Total_pending}</td>
                <td>{Total_analysis_pending}</td>
              </tr>
              <tr>
                <td>Closed</td>
                <td>{Total_closed}</td>
                <td>{Total_closed}</td>
              </tr>
              <tr> </tr>
            </tbody>
          </table>
          <div class="text-end">
            <button class="btn" on:click={() => goto("/ticketing/Dashboard")}
              >Detailed View</button
            >
          </div>
        </div>
      {/if}

      <!-- {#if Database === true || Database === ""}
        <div class="col-4">
          <h2>Db Stats</h2>
          <div class="d-flex">
            <div class="mailshow">
              <table class="tabledatabase1">
                <thead>
                  <tr>
                    <th>Mails</th>
                    <th>Airtel</th>
                    <th>Jio</th>
                    <th>Cellone</th>
                    <th>Vodafone</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>CDR</td>
                    <td>23</td>
                    <td>52</td>
                    <td>12</td>
                    <td>10</td>
                  </tr>
                  <tr>
                    <td>Imei CDR</td>
                    <td>23</td>
                    <td>52</td>
                    <td>12</td>
                    <td>10</td>
                  </tr>
                  <tr>
                    <td>IPDR</td>
                    <td>23</td>
                    <td>52</td>
                    <td>12</td>
                    <td>10</td>
                  </tr>
                  <tr>
                    <td>Cellids</td>
                    <td>23</td>
                    <td>52</td>
                    <td>12</td>
                    <td>10</td>
                  </tr>
                  <tr>
                    <td>SDR</td>
                    <td>23</td>
                    <td>52</td>
                    <td>12</td>
                    <td>10</td>
                  </tr>
                </tbody>
              </table>
              <div>Database lastupdated : 25/08/2024 08:05</div>
            </div>
            <div class="text-end">
              <button class="btn" on:click={() => goto("/database")}
                >Detailed View</button
              >
            </div>
          </div>
        </div>
      {/if} -->
      {#if CDAT === true || CDAT === ""}
        <div class="col-4">
          <h2>Cdat Stats</h2>
          <table class="tabledatabase1">
            <tr>
              <th>Data Type</th>
              <th>Count</th>
            </tr>
            <tr>
              <td>Cdr Data</td>
              <td>{cdrdata_count}</td>
            </tr>
            <!-- <tr>
              <td>Sdr Data</td>
              <td>{sdrdata_count}</td>
            </tr> -->
            <tr>
              <td>Suspect Data</td>
              <td>{suspect_count}</td>
            </tr>
            <tr>
              <td>CellId Data</td>
              <td>{cellidchart_count}</td>
            </tr>
            <tr>
              <td>Tower Data</td>
              <td>{towerdata_count}</td>
            </tr>
            <tr>
              <td>PhoneArea Data</td>
              <td>{phonearea_count}</td>
            </tr>
            <!-- <tr>
              <td>Gprs Data</td>
              <td>{gprs_count}</td>
            </tr> -->
          </table>
          <div class="text-end">
            <button class="btn" on:click={() => goto("/cdat")}
              >Detailed View</button
            >
          </div>
        </div>
      {/if}
    {/if}
  </div>
  <div class="row2">
    {#if Nexus === true || Nexus === ""}
      <div class="col-4">
        <h2>Nexus Stats</h2>
        <table class="tabledatabase1">
          <tr>
            <th>Data Type</th>
            <th>Count</th>
          </tr>
          <tr>
            <td>Voipcalls</td>
            <td>{VoipCallsCount}</td>
          </tr>
          <tr>
            <td>Day Location</td>
            <td>{dayLocationCount}</td>
          </tr>
          <tr>
            <td>Night Location</td>
            <td>{nightLocationCount}</td>
          </tr>
          <tr>
            <td>Vpn Usde</td>
            <td>{vpnsUsed}</td>
          </tr>
          <tr>
            <td>B-party Count</td>
            <td>{bpartycount}</td>
          </tr>
        </table>
        <div class="text-end">
          <button class="btn" on:click={() => goto("/nexus")}
            >Detailed View</button
          >
        </div>
      </div>
    {/if}
    {#if vigor === true || vigor === ""}
      <div class="col-4">
        <h2>Vigor Stats</h2>
        <div class="cards">
          <div class="pie1">
            <canvas id="myPie"></canvas>
          </div>
        </div>
        <div class="text-end">
          <button class="btn" on:click={() => goto("/vigor")}
            >Detailed View</button
          >
        </div>
      </div>
    {/if}
    <div class="col-4">
      <!-- {#if getdata.Model.length < 2} -->
      <h2>Map View</h2>
      <div class="map-container" bind:this={mapContainer}>
        <div class="showlatlong text-end">
          {showlatlong || ""}
        </div>
        <button class="extend-button" on:click={() => goto("/dashboard/main")}
          >Extend Map</button
        >
      </div>
      <!-- {/if} -->
    </div>
  </div>
</main>

<style>
  .btn {
    width: 100%;
    height: 7%;
    margin: 1rem 0rem 0rem 0rem;
  }
  .col-4 {
    border-radius: 7px !important;
    box-shadow: 0px 0px 4px #0d6efd !important;
  }
  main {
    display: flex;
    flex-direction: column;
    margin-left: 4%;
    height: 70vh;
    width: 96%;
    margin-top: 2%;
    padding: 0em 1em 0em 1em;
  }
  .ticket_table {
    margin-left: 10px;
    width: 98%;
    height: 75%;
    border: 1px solid rgba(170, 115, 115, 0.1);
  }
  .ticket_table th,
  .ticket_table td {
    border: 1px solid rgba(170, 170, 170, 0.3);
  }
  .ticket_table tr:hover {
    background-color: rgb(236, 226, 226);
  }
  .ticket_table th {
    background-color: #0d6dfdab;
    color: #fff;
    font-style: italic;
  }
  .row1 {
    display: flex;
    gap: 20px;
  }
  .row2 {
    margin-top: 1px;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  .tabledatabase1 {
    width: 100%;
    height: 35vh;
    table-layout: fixed;
    text-align: center;
    padding: 5px;
    text-wrap: wrap;
    word-break: break-word;
    font-family: Georgia, "Times New Roman", Times, serif;
    font-style: italic;
    font-weight: 3rem;
  }
  .tabledatabase1 th,
  .tabledatabase1 td {
    border: 1px solid rgba(170, 170, 170, 0.3);
  }
  .tabledatabase1 th {
    background-color: #0d6dfdab;
    color: #fff;
  }
  .tabledatabase1 tr:hover {
    background-color: rgb(236, 226, 226);
  }
  .map-container {
    height: 34vh;
    width: 46vw;
    cursor: pointer;
  }
  button {
    width: 25%;
    margin: 0rem 0rem 0rem 0rem;
    border-radius: 5px;
    background: #0d6efd;
    color: #fff;
    border: none;
  }
  button:hover {
    color: black;
    background-color: white;
  }
  .extend-button {
    position: absolute;
    bottom: 10px;
    left: 14px;
    padding: 7px;
    background-color: #0d6efd;
    color: #fff;
    border: none;
    cursor: pointer;
  }
  .extend-button:hover {
    background-color: white;
    color: black;
  }
  .pie1 {
    width: 55%;
    height: 55%;
    margin-left: 30%;
    margin-bottom: 2%;
  }
  table {
    width: 30vw;
  }
  .col-4 {
    background-color: rgb(192, 223, 223);
    margin-top: 20px;
    flex: 1;
    padding: 0 10px;
    border: 1px;
    border-radius: 5%;
    background-color: transparent;
    box-shadow: 0px 0px 10px rgb(46, 44, 44);
    height: 45vh;
    position: relative;
  }
  h2 {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 2rem;
    font-weight: bold;
    /* margin: 20px 0; */
    color: black;
    text-align: center;
    font-style: italic;
  }
  .text-end {
    position: absolute;
    bottom: 10px;
    right: 10px;
    border-radius: 10%;
  }
</style>