<script>
// @ts-nocheck

    import * as XLSX from 'xlsx';
    import { onMount } from 'svelte';
    export let all_vpn;
    export let number;
    console.log(all_vpn)
    let exportData = [];
    let final_result = [];
    let columnFilters = {};
    let filteredResults = [];

    onMount(() => {
    exportData = [['S No', 'VPN', 'VPN IP', 'Downlink_Vol','Uplink_Vol','Start_Time','End_Time','Duration']];
    exportData = exportData.concat(
      all_vpn.map((item, index) => [
        index + 1,
        item['VPN'],
        item['VPN_IP'],
        item['downlink_vol'],
        item['uplink_vol'],
        item['start_time'],
        item['end_time'],
        item['duration']
      ])
    );
  });

  function exportToXLSX() {
    const ws = XLSX.utils.aoa_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, `${number}_vpn_data.xlsx`); 
   }

   function handleColumnSearch(column, event) {
      const filterValue = event.target.value.trim().toLowerCase();
      columnFilters[column] = filterValue;
      applyFilters();
    }
    function applyFilters() {
        filteredResults = all_vpn.filter((item) => {
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
  <button class='excel' on:click={exportToXLSX}>Export Vpn</button></div>

    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 5px;">
      {#if all_vpn.length !== 0}
        <div class="table-container">
          <table>
            <thead>
              <tr>
                  <th style="width: 60px;">S No </th>
                  <!-- <th >Msisdn</th> -->
                  <th style="width: 190px;">VPN </th>
                  <th style="width: 140px;">VPN IP </th>
                  <th style="width: 140px;">Downlink Vol</th>
                  <th style="width: 190px;">Uplink Vol</th>
                  <th style="width: 290px;">Start Time</th>
                  <th style="width: 290px;">End Time</th>
                  <th style="width: 160px;">Duration</th>
                </tr>
                <tr>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('S.No', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('VPN', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('VPN_IP', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('downlink_vol', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('uplink_vol', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('start_time', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('end_time', event)}/>
                  </th>
                  <th class="search">
                    <input placeholder="search" on:input={(event) => handleColumnSearch('duration', event)}/>
                  </th>
                </tr>

            </thead>
            <tbody>
             

              {#each filteredResults.length > 0 ? filteredResults : all_vpn as tblD,i}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <!-- {#each tblD as val} -->
                <td>{i+1}</td>
                <!-- <td >{tblD['MSISDN']}</td> -->
                <td>{tblD['VPN']}</td>
                <td>{tblD['VPN_IP']}</td>
                <td>{tblD['downlink_vol']}</td>
                <td>{tblD['uplink_vol']}</td>
                <td>{tblD['start_time']}</td>
                <td>{tblD['end_time']}</td>
                <td>{tblD['duration']}</td>
      
              </tr>
              {/each}
            </tbody>
          </table>
        </div>
        {:else}
        <div class="no_data">
          <p class="nodata"><b> No VPN Data Available for this {number} </b></p>
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
    max-height: 74vh;
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
