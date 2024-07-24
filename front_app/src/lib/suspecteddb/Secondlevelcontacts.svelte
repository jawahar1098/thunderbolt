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
    let HomeContentHeading = 'SecondLevel';
    let final_result = [];
    let columnFilters = {};
    let filteredResults = [];
    const dispatch = createEventDispatcher();
  
  
  
    
  
  // Refer direct_contacts flask endpoint, completed
  function direct_contacts() {
    gotResult = false
    const direct_contacts = new FormData();
    direct_contacts.append("number", number);
    direct_contacts.append("mode", "SecondLevel");
    direct_contacts.append("page", currentPage); 
    direct_contacts.append("items_per_page", itemsPerPage); 
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/profile_num`, {
    //     method: "POST",
    //     body: direct_contacts,
    //   });

    const url = `${basepath()}/profile_num`;
    postRequest(fetch,url,direct_contacts)
    .then(data => {
  
        console.log(data)
        if (data['data_dict'] === "Not data Matched"){
          showProgress = false;
  
          datafound = "No Data Matched In Database"
  
  
        }else{
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result]; 
          tableHeader = data["headers"];
          showProgress = false;
          gotResult = true;
          dispatch('updateData', filteredResults);
          total_pages = data['totalpages']
          page_count = total_pages / 6
          showTablePage=true;
        }
      } )
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
    {#if gotResult}
    <div class="justify-center mt-3">
      <h2 class="heading">SECOND LEVEL CONTACTS</h2>
    </div>
  
    <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 4%;">OTHER</th>
              <th style="width: 4%;">CDAT PHONE</th>
              <th style="width: 7%;">NICKNAME</th>
              <!-- 0px;"> CAT </th> -->
              <th style="width: 4%;">INCOMING</th>
              <th style="width: 4%;">OUTGOING</th>
              <!-- need to add -->
              <th style="width: 4%;">TOTAL CALLS</th>
              <th style="width: 4%;">DURATION</th>

              <!-- <th>  CALL </th> -->
              <!-- <th> DUR </th> -->
              <th style="width: 4%;">First Call</th>
              <th style="width: 4%;">Last Call</th>
              <th style="width: 14%;">ADDRESS</th>

              <th style="width: 14%;">MODULE</th>

              <!-- <th  style="width: 120px;">IO NAME</th> -->

              

  
              <!-- <th >PHONE</th>
              <th >OTHER</th>
              <th > NICKNAME </th>
              <th >CALL IN</th>
              <th > CALL OUT</th>
              <th > DURATION</th>
              <th>First Call </th>
              <th>Last Call</th>
              <th >Address</th> -->
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
                <input  placeholder="search" on:input={(event) => handleColumnSearch('call_in', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/>
              </th>
              <th class="search">
                <!-- <input  placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/> -->
              </th> 
              <th class="search">
                <!-- <input  placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/> -->
              </th>
              <th class="search">
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[250px]" placeholder="search" on:input={(event) => handleColumnSearch('first_call', event)}/>
              </th>
              <th class="search">
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[250px]" placeholder="search" on:input={(event) => handleColumnSearch('last_call', event)}/>
              </th>
              <th class="search">
                <input  placeholder="search" on:input={(event) => handleColumnSearch('address', event)}/>
              </th>
              <th class="search">
                <!-- <input  placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/> -->
              </th>
            </tr>
          </thead>
          <tbody>
           
            {#each filteredResults as item}
            <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
              <td>{item['source_number']}</td>
              <td> <a href="/cdat/profile?value={item['destination_number']}" target="_blank"> {item['destination_number']} </a></td>
              <td>{item['nickname']}</td>
              <!-- <td>{item['cat']}</td> -->
              <td><a href="/cdat/hyperlink?number={item['source_number']}&mode=call_in&dest_number={item['destination_number' ]}&fromdate=&todate=&state=" target="_blank">{item['call_in']}</a></td>
              <td><a href="/cdat/hyperlink?number={item['source_number']}&mode=call_out&dest_number={item['destination_number' ]}&fromdate=&todate=&state=" target="_blank">{item['call_out']}</a></td>
              <td>000</td>
              <td>000</td>
              <td>{item['first_call']}</td>
              <td>{item['last_call']}</td>
              <td>{item['address']}</td>
              <td>000</td>
              <!-- <td>{item['io_name']}</td> -->
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
    tbody td {
      border: 1px solid rgba(0, 0, 0, 0.1);
      word-break: break-word;
      height: 5vh;
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