<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  // export let selectedValues;
  $: selectedValues = propData.selectedValues;
  $: startDate = propData.startDate;
  $: endDate = propData.endDate;
  console.log(propData, "----propdata---");
  let result;
  let filteredResults = [];
  let gotResult = false;
  let showProgress = true;
  let columnFilters = {};
  let data_found = "Not Data Yet";
  const dispatch = createEventDispatcher();

  function handleSubmit() {
    gotResult = false;
    showProgress = true;
    console.log(selectedValues);

    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({
    //     value: selectedValues,
    //     mode: "call_detials",
    //     fromdate: startDate,
    //     todate: endDate,
    //   }),
    // })

    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({
        value: selectedValues,
        mode: "call_detials",
        fromdate: startDate,
        todate: endDate,
      }))

      .then((res) => res.json())
      .then((data) => {
        console.log("inside call details");
        if (data.status === "success") {
          console.log(" status ", result);
          result = data.call_details;
          console.log(result, "----final result----");
          filteredResults = [...result];
          gotResult = true;
          showProgress = false
          dispatch("updateData", filteredResults);
        } else {
          gotResult = false;
          showProgress = false
          data_found = `No Data Matched`;
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      })
      .finally(() => {
        showProgress = false;
      });
  }
  console.log(gotResult, "---gotresults");

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters();
  }

  function applyFilters() {
    const filteredData = result.filter((item) => {
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

  afterUpdate(() => {
    if (selectedValues != propData.selectedValues) {
      return;
    } else {
      handleSubmit();
      selectedValues = "";
      startDate = "";
      endDate = "";
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
          <th>Source Number </th>
          <th>Destination Number </th>
          <th>Date </th>
          <th>Time </th>
          <th>Call type </th>
          <th>Duration </th>
          <th>Roaming </th>
          <th>IMEI </th>
          <th>IMSI </th>
          <th>First CellID </th>
          <th>Last CellID </th>
        </tr>
        <tr>
          <th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("source_number", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) =>
                handleColumnSearch("destination_number", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("date", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("time", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("call_type", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("duration", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("roaming", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("imei", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("imsi", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("first_cgid", event)}
            />
          </th><th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("last_cgid", event)}
            />
          </th></tr
        >
      </thead>

      <tbody>
        {#each filteredResults as tblD}
          <tr>
            <td>{tblD["source_number"]}</td>
            <td>{tblD["destination_number"]}</td>
            <td>{tblD["date"]}</td>
            <td>{tblD["time"]}</td>
            <td>{tblD["call_type"]}</td>
            <td>{tblD["duration"]}</td>
            <td>{tblD["roaming"]}</td>
            <td>{tblD["imei"]}</td>
            <td>{tblD["imsi"]}</td>
            <td>{tblD["first_cgid"]}</td>
            <td>{tblD["last_cgid"]}</td>
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
