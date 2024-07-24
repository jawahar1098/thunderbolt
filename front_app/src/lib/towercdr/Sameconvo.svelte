<script>
  // @ts-nocheck
  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  // export let selectedValues;
  $: selectedValues = propData.selectedValues;
  $: startDate = propData.startDate;
  $: endDate = propData.endDate;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let gotResult = false;
  let showProgress = true;
  const dispatch = createEventDispatcher();
  let exportData1 = [];

  function handleSubmit() {
    gotResult = false;
    showProgress = true;
    console.log(selectedValues);

    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({
    //     value: selectedValues,
    //     mode: "sameconvo",
    //     fromdate: startDate,
    //     todate: endDate,
    //   }),
    // })
    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({
        value: selectedValues,
        mode: "sameconvo",
        fromdate: startDate,
        todate: endDate,
      }))
      .then((res) => res.json())
      .then((data) => {
        if (data.status !== "failure") {
          final_result = data.unique_common_groups;
          filteredResults = [...final_result];
          console.log(filteredResults);
          gotResult = true;
          // dispatch("updateData", filteredResults);
        } else {
          gotResult = false;
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      })
      .finally(() => {
        showProgress = false;
      });
  }

  function handleSearchChange(key, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    const [objectKey, propertyKey] = key.split(".");

    if (!columnFilters[objectKey]) {
      columnFilters[objectKey] = {};
    }
    columnFilters[objectKey][propertyKey] = filterValue;
    console.log(columnFilters, "-----------------------------------------");

    applyFilters();
  }

  function applyFilters() {
    if (Object.keys(columnFilters).length === 0) {
      // No filters applied, show all data
      filteredResults = [...final_result];
    } else {
      const filteredData = final_result.filter((item) => {
        for (const field in columnFilters) {
          const filterValue = columnFilters[field];
          if (
            filterValue &&
            !item[field]?.toString().toLowerCase().includes(filterValue)
          ) {
            return false;
          }
        }
        return true;
      });
      filteredResults = filteredData;
    }
  }

  function exportToXLSXIN(filteredData) {
    exportData1 = [
      [
        "S No",
        "Source number",
        "Destination number",
        "Imei",
        "Site Name",
        "Cell Id",
      ],
    ];
    exportData1 = exportData1.concat(
      filteredData.map((item, index) => {
        const sitenames = item.common_sitenames
          .map((site) => site.sitename)
          .join(", ");
        const cellids = item.common_sitenames
          .map((site) => site.cellids)
          .join(", ");

        return [
          index + 1,
          item.same_convo.source_number,
          item.same_convo.destination_number,
          item.same_convo.imei,
          sitenames,
          cellids,
        ];
      })
    );

    const ws = XLSX.utils.aoa_to_sheet(exportData1);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, "downloaded_data.xlsx");
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
  <div class="right">
    <button class="btn1" on:click={() => exportToXLSXIN(filteredResults)}
      >Download Excel</button
    >
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th colspan="3">Same Convo</th>
          <th colspan="2">Common Sitenames</th>
        </tr>
        <tr>
          <th>Source Number</th>
          <th>Destination Number</th>
          <th>Imei</th>
          <th>Site Name</th>
          <th>Cell id</th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleSearchChange("same_convo.source_number", event)}
            />
          </th>

          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleSearchChange("same_convo.destination_number", event)}
            />
          </th>

          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleSearchChange("same_convo.imei", event)}
            />
          </th>

          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleSearchChange("common_sitenames.sitename", event)}
            />
          </th>

          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleSearchChange("common_sitenames.cellids", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
        {#each filteredResults as result, i}
          {#each result.common_sitenames as site, j}
            <tr>
              {#if j === 0}
                <td rowspan={result.common_sitenames.length}
                  >{result.same_convo.source_number}</td
                >
                <td rowspan={result.common_sitenames.length}
                  >{result.same_convo.destination_number}</td
                >
                <td rowspan={result.common_sitenames.length}
                  >{result.same_convo.imei}</td
                >
              {/if}
              <td>{site.sitename}</td>
              <td>{site.cellids}</td>
            </tr>
          {/each}
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
    max-height: 76vh;
    margin-top: 1vh;
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

  .right{
    display: flex;
    justify-content: right;
    margin-top: 1vh;
  }
  .btn1{
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 10vw;
  }
</style>
