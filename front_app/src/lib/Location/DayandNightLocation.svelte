<script>
    // @ts-nocheck

  import { createEventDispatcher ,afterUpdate} from 'svelte';
  import { basepath } from "$lib/config";
  import { postRequest } from '$lib/req_utils';
  export let propData;
	$: number = propData.number;
	$: startDate = propData.startdate;
	$: endDate = propData.enddate;
    let total_pages = 0
    let page_count = 0
    let currentPage = 1;
    let itemsPerPage = 10; 
    let data = {};
    let showTablePage = false;
    let tableHeader;
    let showProgress = false;
    let gotResult = false;
    let data_found = "No Data Yet";
    let tableDataDay = "";
    let tableDataNight = "";
    let final_result = [];
    let final_result1 ='';
    let filteredResults1 = '';
    let daylocation;
    let nightlocation;
    
    let columnFilters = {};
    let filteredResults = '';
    const dispatch = createEventDispatcher();

  

    // Refer day_and_night_location_between_dates flask endpoint, completed
  function day_and_night_location_between_dates() {
    gotResult = false
    const day_and_night_location_between_dates = new FormData();
    day_and_night_location_between_dates.append("number", number);
    if (startDate) day_and_night_location_between_dates.append("from_date", startDate);
    if (endDate) day_and_night_location_between_dates.append("to_date", endDate);
    day_and_night_location_between_dates.append("mode","DayNightMapping")
    day_and_night_location_between_dates.append("page", currentPage); 
    day_and_night_location_between_dates.append("items_per_page", itemsPerPage); 
    showProgress = true;
    //     try {
    // const response = await fetch(`${basepath()}/location`,
    //     {
    //     method: "POST",
    //     body: day_and_night_location_between_dates,
    //     }
    // );
    const url = `${basepath()}/location`;
    postRequest(fetch,url,day_and_night_location_between_dates)
    .then(data => {

        console.log(data)
        if (data['headers']==="No Data") {
          showProgress = false
          data_found = "No Data Matched With Database"
        }else{
          
          tableDataDay = data["day_data"];
          final_result = tableDataDay;
          filteredResults = [...final_result];
          tableDataNight = data["night_data"];
          final_result1 = tableDataNight;
          filteredResults1 = [...final_result1];

          daylocation = final_result.map(item => ({...item, timing: 'day'}));
          nightlocation = final_result1.map(item => ({...item, timing: 'night'}));
          let combinedData = [...daylocation, ...nightlocation];
          // filteredResults1 = [...final_result];
          showProgress = false;
          tableHeader = data["headers"];
          gotResult = true;
          dispatch('updateData', combinedData);
          // dispatch('updateData', filteredResults1);

        }
        total_pages = data['totalpages']
        page_count = total_pages / 10
            showTablePage=true;
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
        if (filterValue && !item[field].toString().toLowerCase().includes(filterValue)) {
          return false;
        }
      }
      return true;
    });
    filteredResults = filteredData;
  }

  function handleColumnSearch1(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters1();
  }

  function applyFilters1() {
    const filteredData = final_result1.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        if (filterValue && !item[field].toString().toLowerCase().includes(filterValue)) {
          return false;
        }
      }
      return true;
    });
    filteredResults1 = filteredData;
  }


const columnFilters1 = {};

  
  afterUpdate(() => {
		if (number != propData.number) {
			return
		} else {
			day_and_night_location_between_dates();
			number = ""
			startDate = ""
			endDate = ""

		}
	})

</script>

{#if gotResult}
<div class="day_container">
  <div class="heading">
    <h2>DAY LOCATIONS - TOP 10</h2>
  </div>
  {#if tableDataDay.length > 0}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 5%;">PHONE NUMBER</th>
          <th style="width: 5%;">FIRST CALL</th>
            <th style="width: 5%;">LAST CALL</th>
            <th style="width: 5%;">TOTAL CALLS</th>
            <th style="width: 5%;">CELL ID</th>
            <th style="width: 14%;">AREA DESCRIPTION</th>
            <th style="width: 3%;">STATE</th>
            <th style="width: 3%;">LAT</th>
            <th style="width: 3%;">LONG</th>
            <th style="width: 3%;">AZM</th>

            <!-- <th style="width: 5%;">NICKNAME</th>
            <th style="width: 14%;">User address</th> -->
            
        </tr>
        <tr>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('source_number', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('first_call', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('last_call', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('total_calls', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('tower_id', event)}/>
          </th>
  
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/>
          </th>

          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>

          <!-- <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('nickname', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('user_address', event)}/>
          </th> -->
          
        </tr>
      </thead>
      <tbody>
          {#each filteredResults as tblD}
          <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
            <td>{tblD['source_number']}</td>
            <td>{tblD['first_call']}</td>
            <td>{tblD['last_call']}</td>
            <td>{tblD['total_calls']}</td>
            <td>{tblD['tower_id']}</td>
            <td>{tblD['site_address']}</td>
            <!-- <td>{tblD['nickname']}</td> -->
            <!-- <td>{tblD['user_address']}</td> -->
            
            <td>000</td>
            <td>000</td>
            <td>000</td>
            <td>000</td>
          </tr>
          {/each}
      </tbody>
    </table>
  </div>
  {:else}
  <div class="no_data" style="height: 38vh;">
    <img src="/nodata.png" alt="" style="width: 15%;"/>
    <p class="nodata">No day location data!!!!!!!!</p>
  </div>
  {/if}
</div>

<div class="night_container">
  <div class="heading">
    <h2>NIGHT LOCATIONS - TOP 10</h2>
  </div>
  {#if tableDataNight.length > 0}
  <div class="table-container">
    <table>
      <thead style="position: sticky;">
        <tr>
          <th style="width: 5%;">PHONE NUMBER</th>
          <th style="width: 5%;"> FIRST CALL </th>
            <th style="width: 5%;"> LAST CALL </th>
            <th style="width: 5%;"> TOTAL CALLS</th>
            <th style="width: 5%;"> CELL ID </th>
            <th style="width: 14%;"> AREA DESCRIPTION</th>
            <!-- <th style="width: 5%;">NICKNAME </th> -->
            <!-- <th style="width: 14%;"> User address</th> -->
            <th style="width: 3%;">STATE</th>
            <th style="width: 3%;">LAT</th>
            <th style="width: 3%;">LONG</th>
            <th style="width: 3%;">AZM</th>
           
        </tr>
        <tr>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('source_number', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('first_call', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('last_call', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('total_calls', event)}/>
          </th>

          <!-- <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('nickname', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('user_address', event)}/>
          </th> -->
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('tower_id', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch1('site_address', event)}/>
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('site_address', event)}/> -->
          </th>
        </tr>
      </thead>
      <tbody>
       
          {#each filteredResults1 as tblD}
          <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
              <td>{tblD['source_number']}</td>
              <td>{tblD['first_call']}</td>
              <td>{tblD['last_call']}</td>
              <td>{tblD['total_calls']}</td>
              <!-- <td>{tblD['nickname']}</td>
              <td>{tblD['user_address']}</td> -->
              <td>{tblD['tower_id']}</td>
              <td>{tblD['site_address']}</td>
              <td>000</td>
              <td>000</td>
              <td>000</td>
              <td>000</td>
          </tr>
          {/each}
      </tbody>
    </table>
  </div>
  
  {:else}
  <div class="no_data" style="height: 38vh;">
    <img src="/nodata.png" alt="" style="width: 15%;"/>
    <p class="nodata">No night location data!!!!!!!!</p>
  </div>
  
  {/if}
</div>


{:else if showProgress}
<div class="position-absolute top-50 start-50 translate-middle p-5">
<div class="spinner-border text-primary" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
</div>
{:else}
<div class="no_data" style="height: 85vh;">
  <img src="/nodata.png" alt="" style="width: 23%;"/>
  <p class="nodata">{data_found}!!!!!!!!</p>
</div>
{/if}

<style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: -1%; */
    margin-left: 5%;
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2); */
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 6px;
    text-wrap: wrap;
  }
  .day_container{
    height: 42vh;
    width: 100%;
    margin-top: 1vh;
  }
  .night_container{
    height: 42vh;
    width: 100%;
    margin-top: 1vh;
  }

  thead{
    position: sticky;
    top: -1px;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    color: white;
    text-transform: uppercase;
  }
  tbody {
    height: 30%;               
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 36vh;
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
    width: 23%;
  }

  .heading {
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
</style>
