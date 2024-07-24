<script>
// @ts-nocheck

    import * as XLSX from 'xlsx';
    import { onMount } from 'svelte';
    export let voip_data;
    export let number;
    console.log(voip_data)
    let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
    let exportData = [];

    onMount(() => {
    // Prepare the data for export, including headers
    exportData = [['S No', 'Source IP', 'Destination IP', 'MSISDN','Start_Time','End_Time','Duration','Vendor','Cell ID','Roaming','IpInfo']];
    exportData = exportData.concat(
      voip_data.map((item, index) => [
        index + 1,
        item['source_ip'],
        item['destination_ip'],
        item['msisdn'],
        item['start_time'],
        item['end_time'],
        // item['same_handshake'],
        item['duration'],
        item['vendor'],
        // item['app'],
        item['cellid'],
        item['roaming'],
        item['ipinfo']
      ])
    );
  });

  function exportToXLSX() {
    const ws = XLSX.utils.aoa_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, `${number}_voip_data.xlsx`); 
   }

   function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column.toLowerCase()] = filterValue;
    applyFilters();
  }

  function applyFilters() {
    const filteredData = voip_data.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        if (filterValue && !item[field].toString().toLowerCase().includes(filterValue)) {
          return false;
        }
      }
      return true;
    });
    filteredResults = filteredData;
  }


</script>

<div>
  <div
    class="excel_btn"
    style="margin-left: 5%; margin-top: 1%"
  >
    <button class='excel' on:click={exportToXLSX}>Export Voip</button></div>

    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 5px;">
      {#if voip_data.length !== 0}
        <div class="table-container">
          <table>
            <thead>
              <tr>
                  <th >S No </th>
                  <th >Source IP </th>
                  <th >Destination IP </th>
                  <th >MSISDN</th>
                  <th >Start Time</th>
                  <th >End Time</th>
                  <!-- <th >Same handshake</th> -->
                  <th >Duration</th>
                  <th >Vendor</th>
                  <!-- <th >App</th> -->
                  <th >Cell ID</th>
                  <th >Roaming</th>
                  <th >IpInfo</th>
              </tr>
              <tr>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('S NO', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('source_ip', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('destination_ip', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('msisdn', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('start_time', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('end_time', event)}/>
                </th>
                <!-- <td class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('same_handshake', event)}/>
                </td> -->
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('duration', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('vendor', event)}/>
                </th>
                <!-- <td class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('app', event)}/>
                </td> -->
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('cellid', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('roaming', event)}/>
                </th>
                <th class="search">
                  <input  placeholder="search" on:input={(event) => handleColumnSearch('ipinfo', event)}/>
                </th>
              </tr>

            </thead>
            <tbody>
              
             
             
              {#each filteredResults.length > 0 ? filteredResults : voip_data as tblD,i}
              <tr class="border-bottom hover-bg-gray-100">
                <td >{i+1}</td>
                <td >{tblD['source_ip']}</td>
                <td >{tblD['destination_ip']}</td>
                <td >{tblD['msisdn']}</td>
                <td >{tblD['start_time']}</td>
                <td >{tblD['end_time']}</td>
                <!-- <td >{tblD['same_handshake']}</td> -->
                <td >{tblD['duration']}</td>
                <td >{tblD['vendor']}</td>
                <!-- <td >{tblD['app']}</td> -->
                <td >{tblD['cellid']}</td>
                <td >{tblD['roaming']}</td>
                <td >{tblD['ipinfo']}</td>
              </tr>
              {/each}
            </tbody>
          </table>
        </div>
        {:else}
        <div class="no_data">
          <p class="nodata"><b> No VOIP Data Available for this {number} </b></p>
        </div>
        
        {/if}
      </div>
</div>

<style>
  table {
    width: 98%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
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
    top: -0.5px;
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
    max-height: 90vh;
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
    margin-bottom: 0.5vh;
  }
</style>
