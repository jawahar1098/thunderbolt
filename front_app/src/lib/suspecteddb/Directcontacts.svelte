<script>
    // @ts-nocheck

    import { onMount } from "svelte";
    import { createEventDispatcher,afterUpdate} from 'svelte';
    import * as XLSX from "xlsx";
    import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

    export let propData;
    $: number = propData.number;
    let total_pages = 0
    let page_count = 0
    let currentPage = 1;
    let itemsPerPage = 5; 
    let data = {};
    let showTablePage = false;
    let tableData;
    let tableHeader;
    let showProgress = false;
    let gotResult = false;
    let datafound  = 'Not Data Yet'
    let urlParamValue = '';
    let dest_num= '';
    let parammode = '';
    let HomeContentHeading = 'cdatContacts';
    let final_result = [];
    let columnFilters = {};
    let filteredResults = [];
    const dispatch = createEventDispatcher();



    
  

// Refer direct_contacts flask endpoint, completed
 function direct_contacts() {
  gotResult = false
    const direct_contact_data = new FormData();
    direct_contact_data.append("number", number);
    direct_contact_data.append("mode", "cdatContacts");
    direct_contact_data.append("page", currentPage); 
    direct_contact_data.append("items_per_page", itemsPerPage); 
    showProgress = true;
    const url = `${basepath()}/profile_num`;
    postRequest(fetch,url,direct_contact_data)
    .then(data => {

      console.log(data['data_dict'])
      if (data['status'] === "failure"){
        showProgress = false;
        
        datafound = "No Data Matched In Database"
        
        
      }else{
        tableData = data["data_dict"]
        tableHeader = data["headers"];
        final_result = tableData;
        filteredResults = [...final_result]; 
        showProgress = false;
        gotResult = true;
        dispatch('updateData', filteredResults);
        total_pages = data['totalpages']
        page_count = total_pages / 6
        showTablePage=true;
      }
    })
  
    }
  
  afterUpdate(() => {
		if (number != propData.number) {
			return
		} else {
			direct_contacts();
			number = ""

		}
	})

  function downloadData() {
  const wb = XLSX.utils.book_new();
  const dataArray = tableData.map(item => {
    const formattedItem = {};
    tableHeader.forEach(header => {
      formattedItem[header] = item[header];
    });
    return formattedItem;
  });
  const ws = XLSX.utils.json_to_sheet(dataArray);
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
  const excelData = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
  const blob = new Blob([s2ab(excelData)], { type: "application/octet-stream" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "data.xlsx";
  a.click();
}

function s2ab(s) {
  const buf = new ArrayBuffer(s.length);
  const view = new Uint8Array(buf);
  for (let i = 0; i < s.length; i++) {
    view[i] = s.charCodeAt(i) & 0xff;
  }
  return buf;
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

  
    <!-- <div class="w-full mt-2 mx-3 p-2 grid grid-cols-6 items-center" style="display: flex; align-items: center; gap: 2px;">
    <div class="col-span-4 flex items-center">
      <label for="" class="mt-3 mx-5">Mobile No: </label>
      <div class="flex items-center space-x-2">
      <input class="me-4" id="mobileNumber"  type="text" placeholder="Enter Mobile No" size="10" bind:value={number}/>
      <button class="btn btn-success" on:click={direct_contacts}>Search</button>
      <button class="btn btn-primary" on:click={() => downloadData(filteredResults)}>Download Excel</button>
    </div>
    </div>
    <div class="flex-grow"></div>
    <button class="px-2 py-1 text-lg bg-green-900 hover:bg-green-600 text-white" on:click={() => downloadData(filteredResults)}>Download Excel</button> -->

  <!-- </div> -->

    {#if gotResult}
    <div class="justify-center mt-3">
      <h2 class="heading">DIRECT CONTACTS</h2>
    </div>
    <div class="table-container">
        <table>
          <thead>
            <tr>
              <th  style="width: 4%;">PHONE</th>
              <th  style="width: 4%;">OTHER</th>
              <th  style="width: 7%;">OTHER NICKNAME</th>
              <th  style="width: 14%;">OTHER ADDRESS</th>
              <!-- <th  style="width: 4%;"> CAT </th> -->
              <th  style="width: 4%;">INCOMING</th>
              <th  style="width: 4%;">OUTGOING</th>
              <th  style="width: 4%;">TOTAL CALLS</th>
              <th  style="width: 4%;">DURATION</th>
              <th  style="width: 4%;">FIRST CALL</th>
              <th  style="width: 4%;">LAST CALL</th>
              <!-- <th  style="width: 4%;">IO NAME</th> -->
              <th  style="width: 4%;">MODULE</th>
            </tr>
            <tr>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('source_number', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('destination_number', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('nickname', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('address', event)}/>
              </th>
              <!-- <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('cat', event)}/>
              </th> -->
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('call_in', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('total_calls', event)}/>
              </th>
              <th class="search">
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[110px]" placeholder="search" on:input={(event) => handleColumnSearch('duration', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('first_call', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('last_call', event)}/>
              </th>
              
              <!-- <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('io_name', event)}/>
              </th> -->
              <!-- need to add a module values -->
              <th class="search">
                <!-- <input  placeholder="search" on:input={(event) => handleColumnSearch('io_name', event)}/> -->
              </th>
            </tr>
          </thead>
          <tbody>
            
            {#each filteredResults as item}
            <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
              <td>{item['source_number']}</td>
              <td> <a href="/cdat/profile?value={item['destination_number']}" target="_blank"> {item['destination_number']} </a></td>
              <td>{item['nickname']}</td>
              <td>{item['address']}</td>
              <!-- <td>{item['cat']}</td> -->
              <td><a href="/cdat/hyperlink?number={item['source_number']}&mode=call_in&dest_number={item['destination_number']}&fromdate=&todate=&state=" target="_blank">{item['call_in']}</a></td>
              <td><a href="/cdat/hyperlink?number={item['source_number']}&mode=call_out&dest_number={item['destination_number']}&fromdate=&todate=&state=" target="_blank">{item['call_out']}</a></td>
              <td><a href="/cdat/hyperlink?number={item['source_number']}&mode=total_calls&dest_number={item['destination_number']}&fromdate=&todate=&state=" target="_blank">{item['total_calls']}</a></td>
              <td>{item['duration']}</td>
              <td>{item['first_call']}</td>
              <td>{item['last_call']}</td>
              <!-- <td>{item['io_name']}</td> -->
              <td>000</td>
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
      <p class="nodata">{datafound}!!!!!!!!</p>
    </div>
    {/if}
</div>

<style>
  table {
    width: 98%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 1%;
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
    height: 5vh;
  }
  .table-container {
    max-height: 82vh;
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
    width: 85%;
  }

  .heading {
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
  a{
    color: black;
  }
</style>