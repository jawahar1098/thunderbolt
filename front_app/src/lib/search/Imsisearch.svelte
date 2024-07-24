<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let data;
  let urlParamValue;
  let parammode;
  let dest_num;
  let HomeContentHeading;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  // Refer day_and_night_location_between_dates flask endpoint, completed
  function imsi_details() {
    gotResult = false;

    const imsi_details = new FormData();
    imsi_details.append("number", number);
    imsi_details.append("mode", "IMSI");

    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/imsi_details`, {
    //     method: "POST",
    //     body: imsi_details,
    //   });
    const url = `${basepath()}/imsi_details`;
    postRequest(fetch,url,imsi_details)
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
          HomeContentHeading = "imsipage";
          console.log(tableData, tableHeader);
        }
      })
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      imsi_details();
      number = "";
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
  <div class="flex justify-center mt-3">
    <h2 class="heading" style="margin-left: 2%;">IMSI Details</h2>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 5%;">IMSI </th>
          <th style="width: 5%;"> NICKNAME </th>
          <th style="width: 5%;">PHONE NUMBER</th>
          <th style="width: 5%;">INCOMING</th>
          <th style="width: 5%;">OUTGOING</th>
          <th style="width: 5%;">TOTAL CALLS</th>
          <th style="width: 5%;">DURATION</th>
          <th style="width: 5%;">FIRST CALL</th>
          <th style="width: 5%;">LAST CALL</th>
          <th style="width: 14%;">ADDRESS</th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("imsi", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("nickname", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("source_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_in", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_out", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_calls", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("dur", event)}
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
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("address", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
        
        {#each filteredResults as tblD}
          <tr class="border-bottom hover-bg-gray-100">
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["imsi"]}</td
>
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["nickname"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["source_number"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["call_in"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["call_out"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["total_calls"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["dur"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["first_call"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["last_call"]}</td
            >
            <td class="border-right px-2 py-1 font-medium text-ellipsis"
              >{tblD["address"]}</td
            >
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
    width: 96%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 2%;
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 5px;
    text-wrap: wrap;
  }

  thead{
    position: sticky;
    top: 0;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    color: white;
    text-transform: uppercase;
  }
  
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
    height: 5vh;
  }
  .table-container {
    max-height: 80vh;
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
    width: 85%;
  }

  .heading {
    margin-left: 1%;
    color: #296b97;
  }
  a {
    color: black;
  }
</style>
