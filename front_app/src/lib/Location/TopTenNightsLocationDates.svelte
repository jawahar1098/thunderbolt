<script>
  // @ts-nocheck

  import { createEventDispatcher, onMount, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  import { basepath } from "$lib/config";
  // import { onMount } from "svelte";
  import * as XLSX from "xlsx";
  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let data = {};
  let showTablePage = false;
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  export let startDate;
  export let endDate;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  // Refer day_and_night_location_between_dates flask endpoint, completed
  function top_10_night_location_between_dates() {
    gotResult = false;
    showProgress = true;
    const top_10_night_location_between_dates = new FormData();
    top_10_night_location_between_dates.append("number", number);
    top_10_night_location_between_dates.append("from_date", startDate);
    top_10_night_location_between_dates.append("to_date", endDate);
    top_10_night_location_between_dates.append("mode", "Top10NightLocWithDate");
    // try {
    //   const response = await fetch(`${basepath()}/location`, {
    //     method: "POST",
    //     body: top_10_night_location_between_dates,
    //   });
    const url = `${basepath()}/location`;
    postRequest(fetch,url,top_10_night_location_between_dates)
    .then(data => {

        console.log(data);
        if (data["headers"] === "No Data") {
          showProgress = false;
          data_found = "No Data Matched With Database";
        } else {
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          showProgress = false;
          tableHeader = data["headers"];
          gotResult = true;
          dispatch("updateData", filteredResults);
        }
      } )
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      top_10_night_location_between_dates();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters();
  }

  function applyFilters() {
    const filteredData = final_result.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        if (
          filterValue &&
          !item[field].toString().toLowerCase().includes(filterValue)
        ) {
          return false;
        }
      }
      return true;
    });
    filteredResults = filteredData;
  }
</script>

{#if gotResult}
  <div class="justify-center mt-3" style="margin-left: 6%;">
    <h2 class="heading">NIGHT LOCATION - TOP 10</h2>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 5%;">PHONE NUMBER</th>
          <th style="width: 5%;"> FIRST CALL </th>
          <th style="width: 5%;"> LAST CALL </th>
          <th style="width: 5%;"> TOTAL CALLS</th>
          <th style="width: 5%;"> CELL ID </th>
          <th style="width: 14%;"> AREA DESCRIPTION</th>
          <!-- <th style="width: 5%;">NICKNAME </th>
          <th style="width: 14%;"> User address</th> -->
          <th style="width: 3%;">STATE</th>
          <th style="width: 3%;">LAT</th>
          <th style="width: 3%;">LONG</th>
          <th style="width: 3%;">AZM</th>
          
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("source_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("first_call", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("last_call", event)}
            />
          </th>
          <!-- <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("nickname", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("user_address", event)}
            />
          </th> -->
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_calls", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("tower_id", event)}
            />
          </th>
          
          
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("site_address", event)}
            />
          </th>
          <th class="search">
            <!-- <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("site_address", event)}
            /> -->
          </th>
          <th class="search">
            <!-- <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("site_address", event)}
            /> -->
          </th>
          <th class="search">
            <!-- <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("site_address", event)}
            /> -->
          </th>
          <th class="search">
            <!-- <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("site_address", event)}
            /> -->
          </th>
        </tr>
      </thead>
      <tbody>
        
        {#each filteredResults as tblD}
          <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
            <td>{tblD["source_number"]}</td>
            <td>{tblD["first_call"]}</td>
            <td>{tblD["last_call"]}</td>
            <!-- <td>{tblD["nickname"]}</td>
            <td>{tblD["user_address"]}</td> -->
            <td>{tblD["total_calls"]}</td>
            <td style="text-align: left;">{tblD["tower_id"]}</td>
            <td style="text-align: left;">{tblD["site_address"]}</td>
            <td>000</td>
            <td>000</td>
            <td>000</td>
            <td>000</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else if showProgress}
  <div class="position-absolute top-50 start-50 translate-middle p-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{:else}
  <div class="no_data">
    <img src="/nodata.png" alt="" />
    <p class="nodata">{data_found}!!!!!!!!</p>
  </div>
{/if}

<style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 5%;
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2); */
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 6px;
    text-wrap: wrap;
  }

  thead{
    position: sticky;
    top: -1px;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    color: white;
    text-transform: uppercase;
  }
  tbody {
    height: 73%;
                        
                      }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 79vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }


  tbody tr:hover {
    background-color: #d0e4f1;
  }
  a {
    color: black;
  }
  .no_data {
    color: #161c2057;
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: center;
    height: 85vh;
    justify-content: center;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }

  .heading {
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
</style>
