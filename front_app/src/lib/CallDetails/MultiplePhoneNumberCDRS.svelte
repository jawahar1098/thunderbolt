<script>
  // @ts-nocheck

  import { createEventDispatcher,afterUpdate} from 'svelte';

  import { onMount } from "svelte";

  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
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
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  // let listnumber = number.split(",")

  function contacts_of_mobileNumber() {
  gotResult = false
  showProgress = true;
  const contacts_of_mobileNumber = new FormData();
  contacts_of_mobileNumber.append("number", number);
  if (startDate) contacts_of_mobileNumber.append("fromdate", startDate);
  if (endDate) contacts_of_mobileNumber.append("todate", endDate);
  contacts_of_mobileNumber.append("mode","multipleNumber")
  contacts_of_mobileNumber.append("page", currentPage); 
  contacts_of_mobileNumber.append("items_per_page", itemsPerPage); 
    // try {
    //   const response = await fetch(`${basepath()}/call_details`,
    //       {
    //       method: "POST",
    //       body: contacts_of_mobileNumber,
    //       }
    //   );

    const url = `${basepath()}/call_details`;
    postRequest(fetch,url,contacts_of_mobileNumber)
    .then(data => {


          if (data.status !== 'failure') {
            tableData = data["data_dict"];
            final_result = tableData;
            filteredResults = [...final_result]; 
            showProgress = false;
            tableHeader = data["headers"];
            gotResult = true;
            dispatch('updateData', filteredResults);
            
          }else{
            data_found = "No Data Matched in Database"
            showProgress = false;
            gotResult = false;

          }
          total_pages = data['totalpages']
          page_count = total_pages / 10
      })
}

afterUpdate(() => {
		console.log("updated.....", propData)
		if (number != propData.number || startDate != propData.startdate || endDate != propData.enddate) {
			return
		} else {
			contacts_of_mobileNumber();
			number = ""
			startDate = ""
			endDate = ""

		}
	})

function got_to_page(pagenum){
currentPage = pagenum
contacts_of_mobileNumber()
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
</script>

<div class="relatieve">
  <!-- {#if showProgress}
  <div class="position-absolute top-50 start-50 translate-middle p-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  {/if} -->

  {#if gotResult}
  <div class="flex justify-center mt-3">
    <h2 class="heading">MULTIPLE NUMBER CDR</h2>
  </div>
  <div class="table-container">
   
    <table>
      <thead style="position: sticky;">
        <tr>
          <th style="width: 3%;">PHONE</th>
          <th style="width: 3%;">OTHER</th>
          <th style="width: 5%;">OTHER NICKNAME</th>
          <th style="width: 16%;">OTHER ADDRESS</th>
          <th style="width: 3%;">CALL DATE</th>
          <!-- added -->
          <th style="width: 3%;">CALL TIME</th>

          <th style="width: 2%;">CALL TYPE</th>
          <th style="width: 2%;">DURATION</th>
          <th style="width: 5%;">IMEI</th>
          <th style="width: 5%;">IMSI</th>
          <th style="width: 5%;">CELL ID</th>
          <th style="width: 16%;">AREA DESCRIPTION</th>
          <th style="width: 3%;">PROVIDER</th>
          <th style="width: 2%;">ROAM</th>
          <th style="width: 3%;">LAT</th>
          <th style="width: 3%;">LONG</th>
          <th style="width: 2%;">AZM</th>
          
        </tr>
        <tr>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('source_number', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('destination_number', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('nickname', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('user_address', event)}/>
          </th>
          <!-- <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('user_address', event)}/>
          </th> -->
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('calldate', event)}/>
          </th>
          <!-- added call time -->
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('calldate', event)}/> -->
          </th>

          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('call_type', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('duration', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('imei', event)}/>
          </th>
          <th class="search">
            <!-- <input placeholder="search" on:input={(event) => handleColumnSearch('imei', event)}/> -->
          </th>

          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('cellid', event)}/>
          </th>
         
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('address', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('provider', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('roaming', event)}/>
          </th>
          
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('latitude', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('longitude', event)}/>
          </th>
          <th class="search">
            <input placeholder="search" on:input={(event) => handleColumnSearch('azimuth', event)}/>
          </th>
         
        </tr>
      </thead>
      <tbody>
        
        {#each filteredResults as tblD}
        <tr>
          <td>{tblD['source_number']}</td>
          <td ><a href="/cdat/profile?value={tblD['destination_number']}" target="_blank">{tblD["destination_number"]}</a></td>
          <td>{tblD['nickname']}</td>
          <td>{tblD['user_address']}</td>
          <td>{tblD['calldate']}</td>
          <td>{tblD['call_type']}</td>
          <!-- added call time statically -->
          <td>00</td>
          <td>{tblD['duration']}</td>
          <td><a href="/cdat/hyperlink?mode=imei&number={tblD['imei']}" target="_blank">{tblD["imei"]}</a></td>
          <!-- added imsi static value -->
          <td>000000000000000</td>
          <td>{tblD['cellid']}</td>
          <td>{tblD['address']}</td>
          <td>{tblD['provider']}</td>
          <td>{tblD['roaming']}</td>
          <td>{tblD['latitude']}</td>
          <td>{tblD['longitude']}</td>
          <td>{tblD['azimuth']}</td>
         
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
    <div class="no_data">
      <img src="/nodata.png" alt="" />
      <p class="nodata">{data_found}!!!!!!!!</p>
    </div>
    {/if}
</div>

<style>
  table {
      width: 94%;
      table-layout: fixed;
      text-align: center;
      border-collapse: collapse;
      /* margin-top: -1%; */
      margin-left: 5%;
      font-size: 12px;
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
      max-height: 80vh;
      overflow-y: auto;
      overflow-x: auto;
      position: sticky;
      z-index: 1;
      /* margin-top: 2vh; */
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
    a{
      color: black;
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
    margin-left: 5%;
    color: #296b97;
  }
  
  
  
  </style>
   