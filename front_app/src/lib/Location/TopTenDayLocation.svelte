<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { basepath } from "$lib/config";
    // import { onMount } from "svelte";
    import * as XLSX from "xlsx";
   export let number = "";
   console .log(number)
   export let startDate = "";
   console.log(startDate)
   export let endDate = "";
   console.log(endDate)
  let tableData;
  let tableHeader ;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let data;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();



  // Refer day_and_night_location_between_dates flask endpoint, completed
async function top_ten_day_location() {
  gotResult = false
  showProgress = true;
  const top_ten_day_location = new FormData();
  top_ten_day_location.append("number", number);
  top_ten_day_location.append("mode","Top10DayLoc");
  top_ten_day_location.append("from_date", startDate);
  top_ten_day_location.append("to_date", endDate)
 
      try {
  const response = await fetch(`${basepath()}/location`,
      {
      method: "POST",
      body: top_ten_day_location,
      }
  );

  if (response.ok) {
      data = await response.json();
      console.log(data)
      if (data['headers']==="No Data") {
        showProgress = false
        data_found = "No Data Matched With Database"
      }else{
        
        tableData = data["data_dict"];
        final_result = tableData;
        filteredResults = [...final_result]; 
        showProgress = false;
        tableHeader = data["headers"];
        gotResult = true;   
        dispatch('updateData', filteredResults);
        console.log(tableData,tableHeader)
      }
    
  } else {
      console.error("Failed to submit form");
  }
  } catch (error) {
  console.error("Error submitting form:", error);
  }
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
        if (filterValue && !item[field].toString().toLowerCase().includes(filterValue)) {
          return false;
        }
      }
      return true;
    });
    filteredResults = filteredData;
  }

  onMount(() => {
    top_ten_day_location();
  });

</script>

  {#if gotResult}
    <div class="table-container">          
      <div class="justify-center mt-3" style="margin-left: 6%;">
        <h2>Table For Top 10 Data</h2>
      </div>
        <table>
          <thead>
            <tr>
              <th style="width: 5%;">PHONE NUMBER</th>
              <!-- <th style="width: 5%;">NICKNAME </th> -->
              <th style="width: 5%;"> CELL ID </th>
              <th style="width: 5%;"> total calls</th>
              <!-- <th style="width: 14%;"> User address</th> -->
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="search">
                <input placeholder="search" on:input={(event) => handleColumnSearch('source_number', event)}/>
              </td>
              <td class="search">
                <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('nickname', event)}/> -->
              </td>
              <td class="search">
                <input placeholder="search" on:input={(event) => handleColumnSearch('tower_id', event)}/>
              </td>
              <td class="search">
                <input placeholder="search" on:input={(event) => handleColumnSearch('total_calls', event)}/>
              </td>
              <td class="search">
                <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('user_address', event)}/> -->
              </td>
            </tr>
              {#each filteredResults as tblD}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <td>{tblD['source_number']}</td>
                <!-- <td>{tblD['nickname']}</td> -->
                <td>{tblD['tower_id']}</td>
                <td>{tblD['total_calls']}</td>
                <!-- <td>{tblD['user_address']}</td> -->
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
        <div style="margin-top: 3%; text-align:center; font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif">
          <span>{data_found}</span>
        </div>
        {/if}
    <style>
      table {
        width: 94%;
        table-layout: fixed;
        text-align: center;
        border-collapse: collapse;
        /* margin-top: 2%; */
        margin-left: 5%;
        box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2);
      }
    
      th, td {
        border: 0.5px black;
        text-align: left;
        text-overflow: ellipsis;
        text-align: center;
        padding: 5px;
      }
    
      thead th {
        position: sticky;
        top: 0;
        background-color: black;
        border: 1px;
        color: rgb(118, 214, 57);
        height: 15px 10px;
      }
      tbody {
        width: 5%;
      }
      tbody td {
          border: 1px solid rgba(0, 0, 0, 0.1);
        }
      .table-container {
        max-height: 90vh; 
        overflow-y: auto;
        overflow-x: auto;
        position: sticky ;
        z-index: 1;
        top: 0; 
    
      }
      .search input {
        width: 100%;
        box-sizing: border-box;
      }
    
      tbody tr:hover {
        background-color: rgb(236, 226, 226);
      }
              
    </style>