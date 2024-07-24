<script>
// @ts-nocheck

  import * as XLSX from "xlsx";
  import { onMount } from "svelte";
  export let foreign_isp_data;
  export let india_isp_data;
  export let number;
  console.log(india_isp_data, foreign_isp_data);
  let exportData1 = [];
  let exportData2 = [];
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];

  onMount(() => {
    exportData1 = [["S No", "IP", "Vendor", "Usage"]];
    exportData1 = exportData1.concat(
      india_isp_data.map((item, index) => [
        index + 1,
        item["ip"],
        item["vendor"],
        item["usage"],
      ])
    );
  });

  function exportToXLSXIN() {
    const ws = XLSX.utils.aoa_to_sheet(exportData1);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, `${number}_indian_isp.xlsx`);
  }

  onMount(() => {
    exportData2 = [["S No", "IP", "Country", "Vendor", "Usage"]];
    exportData2 = exportData2.concat(
      foreign_isp_data.map((item, index) => [
        index + 1,
        item["ip"],
        item["country"],
        item["vendor"],
        item["usage"],
      ])
    );
  });
  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters();
  }
  function applyFilters() {
    filteredResults = india_isp_data.filter((item) => {
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
  }

  function exportToXLSX() {
    const ws = XLSX.utils.aoa_to_sheet(exportData2);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, `${number}_foreign_isp.xlsx`);
  }

  function HandleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    ApplyFilters();
  }
  function ApplyFilters() {
    filteredResults = foreign_isp_data.filter((item) => {
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
  }
</script>

<div class="row">
  <div class="float-left" style="width: 50%;">
    <div
      style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 5px; flex-direction: column;"
    >
      {#if india_isp_data.length !== 0}
        <div class="header">
          <h3 class="heading"><b>INDIAN ISP</b></h3>
          <div class="excel_btn" style="margin-left: 5%; margin-top: 1%">
            <button class="excel" on:click={exportToXLSXIN}>Export INDIA</button
            >
          </div>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>S No </th>
                <th>Ip </th>
                <th>Vendor </th>
                <th>Usage </th>
                <!-- <th >Start_Time </th> -->
                <!-- <th >End_Time </th> -->
              </tr>
              <tr>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("S.No", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("ip", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("vendor", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("usage", event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              
              {#each filteredResults.length > 0 ? filteredResults : india_isp_data as tblD, i}
                <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                  <td>{i + 1}</td>
                  <td>{tblD["ip"]}</td>
                  <td>{tblD["vendor"]}</td>
                  <td>{tblD["usage"]}</td>
                  <!-- <td >{tblD['start_time']}</td> -->
                  <!-- <td >{tblD['end_time']}</td> -->
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <p class="container">
          <b>No Indian ISP Data Available for this {number} </b>
        </p>
      {/if}
    </div>
  </div>
  <div class="float-right" style="width: 50%;">
    <div
      style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 5px;flex-direction: column;"
    >
      {#if foreign_isp_data.length !== 0}
      <div class="header">
        <h3 class="heading"><b>FOREIGN ISP</b></h3>
        <div class="excel_btn" style="margin-left: 5%; margin-top: 1%">
          <button class="excel" on:click={exportToXLSX}>Export FOREIGN</button
          >
        </div>
  
      </div>
     
        <div class="table-container">
         
          <table>
            <thead>
              <tr>
                <th>S No </th>
                <th>Ip </th>
                <th>Country </th>
                <th>Vendor </th>
                <th>Usage </th>
                <!-- <th >Start_Time </th> -->
                <!-- <th >End_Time </th> -->
              </tr>
              <tr>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => HandleColumnSearch("S.No", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => HandleColumnSearch("ip", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => HandleColumnSearch("country", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => HandleColumnSearch("vendor", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => HandleColumnSearch("usage", event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              
              {#each filteredResults.length > 0 ? filteredResults : foreign_isp_data as tblD, i}
                <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                  <td>{i + 1}</td>
                  <td>{tblD["ip"]}</td>
                  <td>{tblD["country"]}</td>
                  <td>{tblD["vendor"]}</td>
                  <td>{tblD["usage"]}</td>
                  <!-- <td >{tblD['start_time']}</td> -->
                  <!-- <td >{tblD['end_time']}</td> -->
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <div class="no_data">
          <p class="nodata">
            <b> No FOREIGN ISP Data Available for this {number} </b>
          </p>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  table {
    width: 98%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 0%;
    margin-left: 1%;
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2); */
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
    border: none;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    color: white;
    text-transform: uppercase;
  }
  /* tbody {
              
            } */
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 74vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
  }
  .header{
    display: flex;
    display: flex;
    width: 100%;
    justify-content: space-between;
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }
  .search {
    /* width: 100%;
                box-sizing: border-box; */
    background-color: #5cb2eb;
    /* border: 1px solid #a5c2d5; */
    /* border-bottom: none; */
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
  a {
    color: black;
  }
  .no_data {
    margin-top: 2vh;
    color: #296b97;
    display: flex;
    justify-content: center;
    width: 100%;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }

  .heading {
    margin-left: 5%;
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 1%;
  }
  .excel {
    background-color: #296b97;
    color: white;
    border: none;
    height: 5vh;
    border-radius: 5px;
  }

  .excel_btn {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-right: 20px;
  }
  .row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    top: unset;
    margin-top: 2vh;
  }
</style>
