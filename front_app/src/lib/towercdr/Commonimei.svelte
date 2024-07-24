<script>
  // @ts-nocheck
  //search and style fixed in this page
  import { onMount } from "svelte";
  import * as XLSX from "xlsx";
  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  export let propData;
  // export let selectedValues;
  $: selectedValues = propData.selectedValues;
  $: startDate = propData.startDate;
  $: endDate = propData.endDate;
  let data = [];
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let mode;
  let gotResult = false;
  let showProgress = true;
  // let filteredResults = []
  const dispatch = createEventDispatcher();

  function handleSubmit() {
    gotResult = false;
    showProgress = true;
    console.log(selectedValues);

    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({
    //     value: selectedValues,
    //     mode: "common_imei",
    //     fromdate: startDate,
    //     todate: endDate,
    //   }),
    // })
    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({
        value: selectedValues,
        mode: "common_imei",
        fromdate: startDate,
        todate: endDate,
      }))
      .then((res) => res.json())
      .then((data) => {
        if (data.status !== "failure") {
          final_result = data.common_imei_numbers;
          filteredResults = [...final_result];
          console.log(final_result);
          showProgress = false;
          gotResult = true;
          dispatch("updateData", filteredResults);
        } else {
          gotResult = false;
          showProgress = false;
          console.log(showProgress, "--else-");
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      })
      .finally(() => {
        showProgress = false;
      });
  }

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    console.log("handle column search", columnFilters[column]);
    applyFilters();
  }

  function applyFilters() {
    console.log(columnFilters, "---------applyfilter------------");
    const filteredData = final_result.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        // console.log(filterValue,"----------------------------");
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
    console.log(filteredResults, "------------------------------");
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
          <th scope="col"> Tower </th>
          <th scope="col"> Numbers </th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("_id", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("common_numbers", event)}
            />
          </th>
        </tr>
      </thead>

      <tbody>
        {#each filteredResults as td}
          <tr>
            <td>{td["_id"]}</td>

            <td>
              <div class="grid-container">
                <table style="border-collapse: separate;">
                  <tbody>
                    {#each Array(Math.ceil(td["common_numbers"]
                          .split(",")
                          .map((num) => num.trim()).length / 5)) as _, row}
                      <tr>
                        {#each Array(5) as _, col}
                          {#if td["common_numbers"]
                            .split(",")
                            .map((num) => num.trim())[row * 5 + col]}
                            <td>
                              {#if td["common_numbers"]
                                .split(",")
                                .map((num) => num.trim())[row * 5 + col]}
                                {td["common_numbers"]
                                  .split(",")
                                  .map((num) => num.trim())[row * 5 + col]}
                              {:else}
                                <!-- Display nothing if the value is undefined -->
                              {/if}
                            </td>
                          {/if}
                        {/each}
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            </td>
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
  .grid-container {
    width: 100%;
    height: 34vh;
    overflow-y: scroll;
  }

  .grid-container table {
    width: 100%;
    margin: 0;
  }
  .grid-container table tbody tr td {
    background: #d4ebf7;
    border-collapse: separate;
  }
</style>