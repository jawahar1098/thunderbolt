<script>
    // @ts-nocheck

    import { basepath } from "$lib/config";
    import { createEventDispatcher, afterUpdate } from "svelte";
    import { postRequest } from "$lib/req_utils";

    export let number;

    let final_result = [];
    let showProgress = false;
    let gotResult = false;
    let columnFilters = {};
    let data_found = "no data yet";
    let filteredResults = [];
    const dispatch = createEventDispatcher();

     function handleSubmit() {
      gotResult = false;
      
      const summary_tower = new FormData();
      summary_tower.append("mode", 'numbersummary');
      summary_tower.append("numbers", number);
        console.log(summary_tower,"in summary")
      // try {
      //   const response = await fetch(`${basepath()}/tower_analysis`, {
      //     method: "POST",
      //     body: summary_tower
          
      //   });
      const url = `${basepath()}/tower_analysis`;
      postRequest(fetch,url,summary_tower)

      .then(data => {       
         console.log(data)
        if (data.status === "failure"){
          gotResult = false;
          data_found = `No Data Matched`
        }else {
        final_result = data.result;
        console.log(final_result);
        filteredResults = [...final_result]; 
        gotResult = true;
        dispatch("updateData", filteredResults);
        }
      } )
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
    handleSubmit()

    // afterUpdate(() => {
    //   if (selectedValues != propData.selectedValues){
    //     return
    //   } else {
    //     handleSubmit();
    //     selectedValues = ""
    //   }

    // })
    </script>
<main>
  <div class="relatieve h-[100vh] w-[100vw]">
    {#if showProgress}
    <div class="absolute top-[50%] left-[50%] p-10">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    {/if}
    
    
  <div class="table-container">
    {#if gotResult}
      <div class="custom-border">
          <h3 style="text-align:center;">Tower Data Summary</h3>
        <table>
          <thead>
            <tr>
              <th scope="col"  class="border-r border-b py-2 text-dark-100 dark:border-neutral-500 [w-50px]">Phone </th>
              <th scope="col"  class="border-r border-b py-2 text-dark-100 dark:border-neutral-500 [w-50px]">Destination </th>
              <th scope="col"  class="border-r border-b py-2 text-dark-100 dark:border-neutral-500 [w-50px]">Nickname </th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">First Call</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Last Call</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Incoming</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Outgoing</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Total Calls</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Total Duration</th>
              <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]">Address</th>
            </tr>
            <tr>
              <th class="search"><input class="[w-50px]" placeholder="search"  on:input={(event) => handleColumnSearch('source_number', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('destination_number', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('nickname', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('first_call', event)} /></th>  
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('last_call', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('call_in', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('call_out', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('total_calls', event)} /></th>
              <th class="search"><input placeholder="search"  on:input={(event) => handleColumnSearch('duration', event)} /></th>
              <th class="search"><input placeholder="search" on:input={(event) => handleColumnSearch('address', event)} /></th>
          </tr>
          </thead>
  
          <tbody>
            
            {#each filteredResults as tblD}
              <tr>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500 [w-50px]">{tblD['source_number']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['destination_number']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['nickname']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['first_call']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['last_call']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_in']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_out']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['total_calls']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['duration']}</td>
                  <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['address']}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      {:else}
      <div class="no_data">
        <img src="/nodata.png" alt="" />
        <p class="nodata">No data Matched in Data Base!!!!!!!!</p>
      </div>
      {/if}
  </div>
  </div>

  </main>
  <style>
    main {
      margin-top: 55px;
      margin-left: 6%;
    }
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
  
  .table-container {
    max-height: 90vh; 
    overflow-y: auto;
    overflow-x: auto;
    position: sticky ;
    z-index: 1;
    top: 0; 
    width: 100vw;
    margin-left: -7%;
    
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }
  
  tbody td {
      border: 1px solid rgba(0, 0, 0, 0.1);
      word-break: break-word;

    }
    tbody tr:hover {
      background-color: rgb(236, 226, 226);
    }

    .nodata {
    font-size: 1.2em;
    margin: 0;
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
            
    </style>