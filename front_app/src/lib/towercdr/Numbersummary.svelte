<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";

  // export let selectedValues;
  export let propData;
  console.log(propData, "inside summary");
  $: selectedValues = propData.selectedValues;

  let final_result = [];
  let showProgress = true;
  let gotResult = false;
  let columnFilters = {};
  let data_found = "no data yet";
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  function handleSubmit() {
    gotResult = false;
    showProgress = true;

    const summary_tower = new FormData();
    summary_tower.append("mode", "summary");
    console.log(summary_tower, "in summary");
    // try {
    //   const response = await fetch(`${basepath()}/tower_analysis_2`, {
    //     method: "POST",
    //     body: JSON.stringify({ value: selectedValues, mode: "summary" }),
    //   });
    //   const data = await response.json();
    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({ value: selectedValues, mode: "summary" }))
    .then(data => {

      console.log(data);
      if (data.status === "failure") {
        gotResult = false;
        showProgress = false;
        data_found = `No Data Matched`;
      } else {
        final_result = data.result;
        console.log(final_result);
        filteredResults = [...final_result];
        gotResult = true;
        showProgress = false;
        dispatch("updateData", filteredResults);
      }
    })
  }

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
  // handleSubmit()

  afterUpdate(() => {
    if (selectedValues != propData.selectedValues) {
      return;
    } else {
      handleSubmit();
      selectedValues = "";
    }
  });
</script>

{#if showProgress}
  <div class="position-absolute top-50 start-50 translate-middle p-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{:else if gotResult}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Phone </th>
          <th>Destination </th>
          <th>Nickname </th>
          <th>First Call</th>
          <th>Last Call</th>
          <th>Incoming</th>
          <th>Outgoing</th>
          <th>Total Calls</th>
          <th>Total Duration</th>
          <th>Address</th>
        </tr>
        <tr>
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("source_number", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("destination_number", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("nickname", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("first_call", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("last_call", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_in", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_out", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_calls", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("duration", event)}
            /></th
          >
          <th class="search"
            ><input
              placeholder="search"
              on:input={(event) => handleColumnSearch("address", event)}
            /></th
          >
        </tr>
      </thead>

      <tbody>
        {#each filteredResults as tblD}
          <tr>
            <td>{tblD["source_number"]}</td>
            <td>{tblD["destination_number"]}</td>
            <td>{tblD["nickname"]}</td>
            <td>{tblD["first_call"]}</td>
            <td>{tblD["last_call"]}</td>
            <td>{tblD["call_in"]}</td>
            <td>{tblD["call_out"]}</td>
            <td>{tblD["total_calls"]}</td>
            <td>{tblD["duration"]}</td>
            <td>{tblD["address"]}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else}
  <div class="no_data">
    <img src="/nodata.png" alt="" />
    <p class="nodata">No data Matched in Data Base!!!!!!!!</p>
  </div>
{/if}

<style>
  table {
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    /* margin-left: 5%; */
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

  thead {
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
  }
  .table-container {
    max-height: 80vh;
    margin-top: 4vh;
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

  thead tr {
    border: none;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
  /* a {
    color: black;
  } */
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
</style>