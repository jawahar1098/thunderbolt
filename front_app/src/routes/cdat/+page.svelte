<script>
  // @ts-nocheck

  //highcharts.js
  //highcharts-3d
  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import Highcharts from "highcharts";
  import highcharts3d from "highcharts/highcharts-3d";
  import { userDetailsStore } from '$lib/datastore.js';
  import { postRequest } from "$lib/req_utils";
  let userDetails;
  userDetailsStore.subscribe(value => {
  userDetails = value;
  });
  onMount(() => {
  // beware of truthy and falsy values
  if (localStorage.getItem("userAuth")==="true"){
  userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
  }
  else{
  goto('/');
  }
});

  import * as d3 from "d3";
  import { getRequest } from "$lib/req_utils";

  let dashboard_data = [];
  let cdr = [];
  let sdr = [];
  let suspect = [];
  let cellid = [];
  let phonearea = [];
  let number = "";

  let last_updated_cdr;
  let last_updated_sdr;
  let last_updated_cellid;
  let last_updated_suspect;
  let last_updated_phone_area;
  let cdrData = [];
  let loading = "false";
  let mapLoading = "false";
  let portfolio;
  let modes = [
    "Andhra Pradesh",
    "Arunanchal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Orissa",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Andaman and Nicobar Island",
    "Chandigarh",
    "Dadra and Nagar Haveli",
    "Daman and Diu",
    "Delhi",
    "Lakshadweep",
    "Puducherry",
    "Jammu and Kashmir",
  ];

  let selectOption = "Andhra Pradesh";

  function dashboard() {
    loading = true;
    // fetch(basepath() + "/dashboard_data", {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    // })

    const url = `${basepath()}/dashboard_data`;
    getRequest(fetch,url)
    
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((datas) => {
        if (datas.status === "success") {
          console.log(datas, "Data");

          const dashboardData = datas.data;
          console.log(dashboardData.last_updated_cellid, "DashBoard");
          last_updated_cdr = dashboardData.last_updated_cdr.as_on_date;
          last_updated_sdr = dashboardData.last_updated_sdr;
          last_updated_cellid = dashboardData.last_updated_cellid;
          last_updated_suspect =
            dashboardData.last_updated_suspect.as_on_datetime;
          last_updated_phone_area = dashboardData.last_updated_phone_area;

          const chartData = {
            cdr: datas.data.cdat_cdr,
            sdr: datas.data.cdat_sdr,
            suspect: datas.data.cdat_suspect,
            cellid: datas.data.cdat_cellidchart_sample,
            phonearea: datas.data.cdat_phonearea,
            towerdata: datas.data.cdat_towerdata,
          };

          loading = false;
        } else {
          console.error("Error in data retrieval:", datas.message);
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      });
  }

  function dashboardMap(selectOption) {
    mapLoading = true;
    // fetch(basepath() + "/tower_dashboard", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify(selectOption),
    // })

    const url = `${basepath()}/tower_dashboard`;
    postRequest(fetch,url,JSON.stringify(selectOption))

      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((datas) => {
        cdrData = datas;
        selectOption = "Andhra Pradesh";
        console.log(cdrData,'////////////////////////////');
        mapLoading = false;
      });
  }

  function pieChart() {
    // fetch(basepath() + "/pie-chart", {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    // })

    const url = `${basepath()}/pie-chart`;
    getRequest(fetch,url)

      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((datas) => {
        console.log(datas, "Data");

        const chartData = {
          cdr: datas.data.cdat_cdr,
          sdr: datas.data.cdat_sdr,
          suspect: datas.data.cdat_suspect,
          cellid: datas.data.cdat_cellidchart_sample,
          phonearea: datas.data.cdat_phonearea,
          towerdata: datas.data.cdat_towerdata,
        };

        create3DPieChart(chartData);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      });
  }

  function chartCount() {
    // fetch(basepath() + "/counts", {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    // })

    const url = `${basepath()}/counts`;
    getRequest(fetch,url)

      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((datas) => {
        console.log(datas, "Data count");

        const chartData = {
          cdr: datas.cdr_count,
          sdr: datas.sdr_count,
          suspect: datas.suspect_count,
          towerdata: datas.tower_count,
        };
        createPieChart(chartData);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      });
  }

  function drawIndiaMap(selectOption) {
    console.log(selectOption, "option");

    // Select the existing SVG element or create a new one if it doesn't exist
    const svg = d3.select("#india-map svg").empty()
      ? d3
          .select("#india-map")
          .append("svg")
          .attr("width", 800)
          .attr("height", 600)
      : d3.select("#india-map svg");

    // Remove existing elements in the SVG
    svg.selectAll("*").remove();

    const projection = d3.geoMercator().scale(1000).center([90, 25]);

    d3.json("states_india.geojson").then(function (india) {
      const path = d3.geoPath().projection(projection);
      svg
        .selectAll("path")
        .data(india.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("fill", (d) => {
          const stateName = d.properties.st_nm;
          return stateName === selectOption
            ? getColorBasedOnOption(selectOption)
            : "white";
        })
        .attr("stroke", "black");

      svg
        .selectAll("text")
        .data(india.features)
        .enter()
        .append("text")
        .attr("text-anchor", "middle")
        .style("font-size", "12px")
        .attr("class", "state-label")
        .attr("transform", function (d) {
          const centroid = path.centroid(d);
          return "translate(" + centroid[0] + "," + centroid[1] + ")";
        })
        .attr("dy", ".35em")
        .text(function (d) {
          return [d.properties.st_nm, d.properties.state_code];
        });
    });

    function getColorBasedOnOption(selectOption) {
      return "red"; // Replace with your logic to determine color based on the selected option
    }
  }

  function create3DPieChart(chartData) {
    Highcharts.chart("my3DPieChart", {
      chart: {
        type: "pie",
        options3d: {
          enabled: true,
          alpha: 45,
        },
      },
      title: {
        text: "Total Document Records",
      },
      plotOptions: {
        pie: {
          innerSize: 100,
          depth: 45,
        },
      },
      credits: { enabled: false },
      series: [
        {
          name: "Data Count",
          data: [
            ["CDR", chartData.cdr],
            ["SDR", chartData.sdr],
            ["Suspect", chartData.suspect],
            ["CellID", chartData.cellid],
            ["Phone Area", chartData.phonearea],
            ["Tower Data", chartData.towerdata],
          ],
        },
      ],
    });
  }

  function createPieChart(chartData) {
    Highcharts.chart("3DPieChart", {
      chart: {
        type: "pie",
        options3d: {
          enabled: true,
          alpha: 45,
        },
      },
      title: {
        text: "Total Unique Source Number Records",
      },
      plotOptions: {
        pie: {
          innerSize: 100,
          depth: 45,
        },
      },
      credits: { enabled: false },
      series: [
        {
          name: "Data Count",
          data: [
            ["CDR", chartData.cdr],
            ["SDR", chartData.sdr],
            ["Suspect", chartData.suspect],
            ["Tower Data", chartData.towerdata],
          ],
        },
      ],
    });
  }

  function handleOptionChange(event) {
    selectOption = event.target.value;
    dashboardMap(selectOption);
    drawIndiaMap(selectOption);
  }
  highcharts3d(Highcharts);
  highcharts3d(Highcharts);
  onMount(() => {
    dashboard();
    dashboardMap(selectOption);
    drawIndiaMap(selectOption);
    pieChart();
    chartCount();
  });

  
</script>

<div class="conts">
  <div class="cards">
    {#if !loading}
      <div class="cards-content l-bg-cherry">
        <div class="text">
          <div>Last Updated CDR</div>
          <div class="text-content">{last_updated_cdr || "No data Found"}</div>
        </div>
      </div>
      <div class="cards-content l-bg-green-dark">
        <div class="text">
          <div>Last Updated SDR</div>
          <div class="text-content">{last_updated_sdr || "No Data Found"}</div>
        </div>
      </div>
      <div class="cards-content l-bg-orange-dark">
        <div class="text">
          <div>Last Updated CellID</div>
          <div class="text-content">
            {last_updated_cellid || "No Data Found"}
          </div>
        </div>
      </div>
      <div class="cards-content l-bg-red-dark">
        <div class="text">
          <div>Last Updated Suspect</div>
          <div class="text-content">
            {last_updated_suspect || "No Data Found"}
          </div>
        </div>
      </div>
      <div class="cards-content l-bg-blue-dark">
        <div class="text">
          <div>Last Updated Phone Area</div>
          <div class="text-content">
            {last_updated_phone_area || "No data Found"}
          </div>
        </div>
      </div>
    {:else}
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    {/if}
  </div>
</div>
<div class="map">
  <div class="map-content">
    <div class="maps">
      <select
        id="color-selector"
        placeholder="DropDown"
        bind:value={selectOption}
        on:change={handleOptionChange}
      >
        <option value="Andhra Pradesh" disabled>Andhra Pradesh</option>
        {#each modes as mode}
          <option value={mode}>{mode}</option>
        {/each}
      </select>
      <div id="india-map" class="mapee" />
    </div>
    <div class="result-content">
      {#if !mapLoading}
        {#each cdrData as res}
          <div class="cards-text l-bg-cherry">
            <p>Total CDR Data</p>
            <p>{res["cdrData"]}</p>
            <p>
              {res.last_updated_cdr["as_on_date"] ||
                `No Data Found For this ${selectOption}`}
            </p>
          </div>
          <div class="cards-text l-bg-green-dark">
            <p>Total SDR Data</p>
            <p>{res["SDR Data"]}</p>
            <p>
              {res["last_updated_sdr"] ||
                `No Data Found For this ${selectOption}`}
            </p>
          </div>
          <div class="cards-text l-bg-orange-dark">
            <p>Total CellID Data</p>
            <p>{res["cellId Chart"]}</p>
            <p class="date-text">
              {res.last_updated_cellid ||
                `No Data Found For this ${selectOption}`}
            </p>
          </div>
          <div class="cards-text l-bg-red-dark">
            <p>Total Suspect Data</p>
            <p>{res["Suspect"]}</p>
            <p class="date-text">
              {res.last_updated_suspect["as_on_datetime"] ||
                `No Data Found For this ${selectOption}`}
            </p>
          </div>
          <div class="cards-text l-bg-blue-dark">
            <p>Total Phone Area</p>
            <p>{res["Phone Area"]}</p>
            <p>
              {res["last_updated_phone_area"] ||
                `No Data Found For this ${selectOption}`}
            </p>
          </div>
        {/each}
      {:else}
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      {/if}
    </div>
  </div>
  <div class="end-content">
    <div class="card-content">
      <div id="my3DPieChart" class="pie-chart"></div>
    </div>
    <div class="card-content">
      <div id="3DPieChart" class="pie-chart"></div>
    </div>
  </div>
</div>

<style>
  .cards-text p {
    margin: 0.3rem 0rem 0rem 1rem;
    font-size: 1rem;
    font-family: "Raleway";
  }

  .mapee {
    display: flex;
    justify-content: center;
    padding-top: 5rem;
  }
  .conts {
    position: absolute;
    left: 4%;
    width: calc(100% - 4%);
    /* top: 5%; */
  }
  .cards {
    display: flex;
    flex-wrap: wrap;
    margin: 0.5rem;
    justify-content: space-evenly;
  }
  .cards-content {
    width: 18%;
    height: 12vh;
    margin: 0.5rem;
    border-radius: 10px;
  }

  /* .l-bg-cherry {
    border: none !important;
    background: #ffffff;
  }
  .l-bg-green-dark {
    border: none !important;
    background-color: #c8fff9;
  }

  .l-bg-orange-dark {
    border: none !important;
    background: #ffb9ce;
  }

  .l-bg-red-dark {
    border: none !important;
    background: #ffbcbc;
  }
  .l-bg-blue-dark {
    border: none !important;
    background: #b1c9ff;
  } */
  .map {
    position: absolute;
    top: 20%;
    width: calc(100% - 4%);
    left: 4%;
    height: calc(100% - 20%);
    display: flex;
  }
  .map-content {
    width: 75%;
    height: 98%;
    display: flex;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgb(175, 175, 175);
    margin-left: 1rem;
  }
  .cards-content {
    box-shadow: 0px 0px 10px rgb(175, 175, 175);
    transition: all 1s ease;
  }
  .cards-content:hover {
    z-index: 1;
    box-shadow: 5px 0px 10px #0d6efd;
  }
  .card-content {
    width: 93%;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgb(175, 175, 175);
    padding: 1rem;
    height: 48%;
    display: flex;
    flex-direction: row;
    margin: 0rem 0rem 0.8rem 1rem;
  }
  .maps {
    width: 70%;
    height: 100%;
  }
  .result-content {
    width: 50%;
    height: 100%;
    padding-top: 4rem;
  }
  .date-text {
    font-size: 1rem;
  }
  select {
    margin: 0.5rem;
    width: 20%;
    font-size: 1rem;
    font-family: "Raleway";
    position: absolute;
    justify-content: center;
    left: 25%;
  }
  .text {
    font-size: 1.2rem;
    font-family: "Raleway";
    text-align: center;
    margin: 0.5rem;
    font-weight: 500;
  }
  .text-content {
    color: black;
    font-weight: 600;
    font-family: "Raleway";
    font-size: 1.1rem;
    padding: 0.5rem;
  }
  .pie-chart {
    width: 100% !important;
  }
  .cards-text {
    width: 90%;
    height: 15%;
    border: 1.5px solid rgb(175, 175, 175);
    margin: 0.7rem 0rem 0rem 1rem;
    box-shadow: 0px 0px 4px rgb(175, 175, 175);
    border-radius: 10px;
    transition: all 1s ease;
  }
  .cards-text:hover {
    z-index: 1;
    box-shadow: 5px 0px 10px #0d6efd;
  }
  .image {
    width: 6%;
  }
  .images {
    height: 50%;
  }
  .end-content {
    width: 30%;
  }
</style>
