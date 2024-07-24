<script>
    // @ts-nocheck
  
    import { basepath } from "$lib/config";
    import { createEventDispatcher, afterUpdate } from "svelte";
    import { postRequest } from "$lib/req_utils";
  
    export let propData;
    $: number = propData.number;
    $: mode = propData.mode;
    let currentPage = 1;
    let datafound = "No Data Yet";
    let tableData;
    let tableHeader;
    let showProgress = false;
    let gotResult = false;
    let final_result = [];
    let columnFilters = {};
    let filteredResults = [];
    const dispatch = createEventDispatcher();
  
     function imei_search_data_fuc() {
      gotResult = false;
      const imei_search_data = new FormData();
      imei_search_data.append("number", number);
      imei_search_data.append("mode", mode);
      showProgress = true;
      
      const url = `${basepath()}/tower_lookup`;
      postRequest(fetch, url, imei_search_data)
          
        // fetch(url,{
        //   method:'post',
        //   body:imei_search_data
        // })
        .then(res => res.json())
        .then(data => {

        
          
        if (data["status"] === "success") {
          tableData = data["data_dict"] || [];
          final_result = tableData;
          filteredResults = [...final_result];
          showProgress = false;
          gotResult = true;
          dispatch("updateData", filteredResults);
          
        } else {
          showProgress = false;
          datafound = "No data matched in database";
        }
      });
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
          if (
            filterValue &&
            !item[field].toString().toLowerCase().includes(filterValue)
          ) {
            return false;
          }
        }
        return true;
      });
      filteredResults = filteredData;
    }
  
    afterUpdate(() => {
      console.log("updated.....", propData);
      if (number != propData.number) {
        return;
      } else {
        imei_search_data_fuc();
        number = "";
      }
    });
  </script>
  
  <div class="relatieve" style="margin-left: 4%;">
    {#if gotResult}
      <div class="flex justify-center mt-3">
        <h2 class="heading">IMEI summary</h2>
      </div>
      <div class="table-container">
        <div class="d-flex flex-column p-2">
          <table>
            <thead>
              <tr>
                <th style="width: 5%;">SOURCE NUMBER</th>
                <!-- <th style="width: 5%;">INCOMING</th> -->
                <!-- <th style="width: 5%;">OUTGOING</th> -->
                <!-- <th style="width: 5%;">DURATION</th> -->
                <!-- <th style="width: 5%;">TOTAL CALLS</th> -->
                <th style="width: 5%;">IMEI</th>
                <th style="width: 5%;">FIRST CALL</th>
                <th style="width: 5%;">LAST CALL</th>
              </tr>
              <tr>
                <td class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("sourcenumber", event)}
                  />
                </td>
                <!-- <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("call_in", event)}
                  />
                </th>
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("call_out", event)}
                  />
                </th>
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("duration", event)}
                  />
                </th>
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("total_calls", event)}
                  />
                </th> -->
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("imei_number", event)}
                  />
                </th>
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("first_call", event)}
                  />
                </th>
                <th class="search">
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[235px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("last_call", event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              {#each filteredResults as tblD}
                <tr class="border-bottom hover-bg-gray-100">
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["sourcenumber"]}</td
                  >
                  <!-- <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["call_in"]}</td
                  >
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["call_out"]}</td
                  >
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["duration"]}</td
                  >
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["total_calls"]}</td
                  > -->
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["imei_number"]}</td
                  >
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["first_call"]}</td
                  >
                  <td class="border-right px-2 py-1 font-medium text-ellipsis"
                    >{tblD["last_call"]}</td
                  >
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
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
      margin-top: 0%;
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
  
    thead {
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
      max-height: 80vh;
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
      margin-left: 1%;
      color: #296b97;
    }
    a {
      color: black;
    }
  </style>
  