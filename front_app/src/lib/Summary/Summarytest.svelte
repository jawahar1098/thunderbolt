
<script>
  import { onMount } from 'svelte';
  import * as XLSX from "xlsx";
  import { basepath } from "$lib/config";


  
  let showTablePage = false
  export let number = "";
  let data = {};
  let showProgress = false;
  let gotResult = false;
  let tableData;
  let tableHeader;
  let pagination = true;
  let currentPage = 1;
  let urlParamValue = '';
  let parammode = '';
  let dest_num = '';
  let itemsPerPage = 4;
  let bottomRightHomeContentHeading = "profile"
  let datafound  = 'Not Data Yet'
  let final_result = [];
    let columnFilters = {};
    let filteredResults = [];
    let data_2;

  console.log("asdfasdf in side summaru nwe")



async function hyperlink_route(number,dest_num,mode) {
  
  const profile_num = new FormData();
  profile_num.append("number", number);
  profile_num.append("mode", mode);
  profile_num.append('dest_num',dest_num)
  if (number){
    showProgress = true

  }

  try {
    const response = await fetch(
      `${basepath()}/hyperlink`,
      {
        method: "POST",
        body: profile_num,
      }
    );

    if (response.ok) {
      data = await response.json();
      console.log(data)
      
      if (data.data_dict === 'Not data Matched'){
        showProgress = false
        datafound = "No Data Matched In Database"
      }
      else{

        bottomRightHomeContentHeading = ""
        gotResult=true
      }
    } else {
      console.error("Failed to submit form",response);
    }
  } catch (error) {
    console.error("Error submitting form:", error);
  }
}

async function summary_mobile() {
  gotResult = false
  const summary_mobile = new FormData();
  summary_mobile.append("number", number);
  summary_mobile.append("mode", "summary_new");
  showProgress = true
  try {
    const response = await fetch(
      `${basepath()}/summary_of_mobile`,
      {
        method: "POST",
        body: summary_mobile,
      }
    );

    if (response.ok) {
      data = await response.json();
      console.log(data);
      final_result =  data.data2;
            filteredResults = [...final_result];
      if (data.data_dict === 'Not data Matched'){
        showProgress = false
        datafound = "No Data Matched In Database"
        
      }else{

        gotResult=true
      }
    } else {
      console.error("Failed to submit form",response);
    }
  } catch (error) {
    console.error("Error submitting form:", error);
  }
}

summary_mobile()
   
 function downloadData() {
  const secondTableData = data.data2;
  const secondTableHeader = data.header2;
  const wb = XLSX.utils.book_new();
  const dataArray = secondTableData.map(item => {
    const formattedItem = {};
    secondTableHeader.forEach(header => {
      formattedItem[header] = item[header];
    });
    return formattedItem;
  });
  const ws = XLSX.utils.json_to_sheet(dataArray);
  XLSX.utils.book_append_sheet(wb, ws, "SecondTableData");
  const excelData = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
  const blob = new Blob([s2ab(excelData)], { type: "application/octet-stream" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "second_table_data.xlsx";
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
    filteredResults = data.data2.filter((item) => {
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
  
<div class="flex items-center">
  <div class="flex-grow p-4 cursor-pointer">
      
  </div>
  <div class="col-start-6 mr-10 col-span-3 flex justify-end">
      <button class="px-2 py-1 flex-end text-lg bg-green-900 hover:bg-green-600 text-white" on:click={() => downloadData(filteredResults)}>Download Excel</button>
  </div>
</div>



  <div class="relatieve ">
   
    {#if gotResult}

    
    <div class="flex justify-center mt-3">
      <h4>Summary of {number}</h4>
    </div>
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between w-full px-5 ">
      <div class="flex flex-col p-2 ">
        <table  class="table-auto border text-center text-sm font-light dark:border-neutral-500">
          <thead class="font-medium bg-base-content dark:border-neutral-500">
            <tr>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">SOURCE NUMBER
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">DESTINATION NUMBER
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">NICKNAME
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">INCOMING 
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">OUTGOING
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">TOTAL CALLS
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">DURATION
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">FIRST CALL
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">LAST CALL
              </th>
              <th scope="col" class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[120px]">ADDRESS
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('source_number', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('destination_number', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('nickname', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('call_in', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('call_out', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('total_calls', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('duration', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('first_call', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('last_call', event)}/>
              </td>
              <td>
                <input class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[120px]" placeholder="search" on:input={(event) => handleColumnSearch('address', event)}/>
              </td>
            </tr>
            {#each filteredResults as item}
            <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                {#each data.header2 as header}
                {#if bottomRightHomeContentHeading }
                    {#if header === "call_count"}
                    <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=total_calls" target="_blank">{item[header]}</a></td>
                    {:else if header === "cdat_count" || header === "call_in" || header === "call_out" || header === "total_calls"}
          
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode={header}&dest_number={item["destination_number"]}" target="_blank">{item[header]}</a></td>
                    {:else if header === "destination_number" || header === "cellid"}
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item[header]}&mode=dest_num" target="_blank">{item[header]}</a></td>
                    {:else if header === "imei" }
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item[header]}&mode=imei" target="_blank">{item[header].length}</a></td>
                      <!-- {/if} -->
                      {:else}
                      <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 ">{item[header]}</td>
                    {/if}
                   
                  {:else if parammode === "imei" || parammode === 'call_out'}
                    {#if header === null}
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"></td>
                    {:else if header === "cdat_count" || header === "call_in" || header === "call_out" || header === "total_calls"}
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item['source_number']}&mode={header}&dest_number={item["destination_number"]}" target="_blank">{item[header]}</a></td>
                    {:else if header === "imei" || header === "destination_number" }
                        <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500 text-rose-600">
                          <a href="/home?value={item[header]}&mode=imei" target="_blank">{item[header]}</a></td>
                    {:else}
                      <td class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500">{item[header]}</td>
                    {/if}

                    {/if}
                {/each}
            </tr>
            {/each}
          </tbody>
        </table>
        
      </div>
      </div>
   
    {:else if showProgress}
    <div class="w-25 flex justify-center mt-20">
      
      <div class="absolute top-[50%] left-[50%] p-10">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
    </div>
    {:else}
    <div class="no_data">
      <img src="/nodata.png" alt="" />
      <p class="nodata">{datafound}</p>
    </div>
  {/if}
</div>

<style>
       
.input-sm {
  font-size: 0.8em;
  width: 100px; 
  color: black;

}

table {
  /* width: 100%; */
  table-layout: fixed;
  text-align: center;
  /* height: 200px; */
  /* position: fixed; */
}

th, td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}

thead {
      position: sticky;
      top: 0;
  }

  tbody {
      height: 100vh; 
      /* overflow-y: auto; */
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

  
</style> 