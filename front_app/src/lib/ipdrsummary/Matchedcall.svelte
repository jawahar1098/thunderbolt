<script>
// @ts-nocheck

    import * as XLSX from 'xlsx';
    import { onMount } from 'svelte';
    export let matched_call;
    export let number;
    console.log(matched_call)
    let final_result = [];
    let columnFilters = {};
    let filteredResults = [];
    let exportData = [];

    onMount(() => {
    exportData = [['S No', 'Caller1', 'Caller2', 'calltime','Destination_Ip','Source_Ip']];
    exportData = exportData.concat(
      matched_call.map((item, index) => [
        index + 1,
        item['caller1'],
        item['caller2'],
        item['calltime'],
        item['destination_ip'],
        item['source_ip']
      ])
    );
  });

  function exportToXLSX() {
    const ws = XLSX.utils.aoa_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, `${number}_matchedcall_data.xlsx`); 
   }

   function handleColumnSearch(column, event) {
      const filterValue = event.target.value.trim().toLowerCase();
      columnFilters[column] = filterValue;
      applyFilters();
    }
    function applyFilters() {
        filteredResults = matched_call.filter((item) => {
          for (const field in columnFilters) {
            const filterValue = columnFilters[field];
            if (filterValue && !item[field].toString().toLowerCase().includes(filterValue)) {
              return false;
            }
          }
          return true;
        });
      }
</script>

<div>
  <div
    class="excel_btn"
    style="margin-left: 5%; margin-top: 1%"
  >
  <button class='excel' on:click={exportToXLSX}>Export Matched_call</button>
  </div>

    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 5px;">
      {#if matched_call.length !== 0}
        <div class="table-container">
          <table>
            <thead>
              <tr>
                  <th >S No </th>
                  <!-- <th >Msisdn</th> -->
                  <th >Caller1 </th>
                  <th >Caller2</th>
                  <th >Calltime</th>
                  <th >Destination IP</th>
                  <th >Source IP</th>
              </tr>
              <tr>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('S.No', event)}/>
                </th>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('caller1', event)}/>
                </th>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('caller2', event)}/>
                </th>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('calltime', event)}/>
                </th>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('destination_ip', event)}/>
                </th>
                <th class="search">
                  <input placeholder="search" on:input={(event) => handleColumnSearch('source_ip', event)}/>
                </th>
              </tr>

            </thead>
            <tbody>
              


              {#each filteredResults.length > 0 ? filteredResults : matched_call as tblD,i}
              <tr class="border-bottom hover-bg-gray-100">
                <!-- {#each tblD as val} -->
                <td >{i+1}</td>
                <!-- <td >{tblD['MSISDN']}</td> -->
                <td >{tblD['caller1']}</td>
                <td >{tblD['caller2']}</td>
                <td >{tblD['calltime']}</td>
                <td >{tblD['destination_ip']}</td>
                <td >{tblD['source_ip']}</td>
      
              </tr>
              {/each}
            </tbody>
          </table>
        </div>
        {:else}
        <div class="no_data">
          <p class="nodata"><b> No Matched Call Data Available for this {number} </b></p>
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
    margin-top: 1%;
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

  thead th {
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
    border: 1px solid #a5c2d5;
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
</style>
