<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { writable } from "svelte/store";
  import { basepath } from "$lib/config";
  import { onMount,onDestroy } from "svelte";
  import { table_data,current_page } from '../../cdr_between_dates';


  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 4;
  let data = {};
  let showTablePage = false;
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;

  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let pagination = true;
  const dispatch = createEventDispatcher();

  // onMount(() => {
  //   contacts_of_mobileNumber(currentPage);
  // });


// FOR LAZY LOADING


let loading = false;
// const table_data = writable([]);

let scrollContainer;
let allDataRecieved = false;


$: {
    if (scrollContainer) {
      console.log('Scroll container is now defined, adding event listener');
      scrollContainer.addEventListener('scroll', handleScroll);

      onDestroy(() => {
        scrollContainer.removeEventListener('scroll', handleScroll);
        console.log('Event listener removed');
      });
    } else {
      console.log('Scroll container is still undefined');
    }
  }

  onMount(() => {
    console.log('Component mounted');
    if (scrollContainer) {
      console.log('Scroll container is defined, adding event listener');
      scrollContainer.addEventListener('scroll', handleScroll);
    } else {
      console.log('Scroll container is undefined at mount');
    }
  });

  onDestroy(() => {
    if (scrollContainer) {
      scrollContainer.removeEventListener('scroll', handleScroll);
    }
  });





  function handleScroll() {
    console.log("scrolling started")
    const { scrollTop, scrollHeight, clientHeight } = scrollContainer;
    console.log(`Scrolled: scrollTop=${scrollTop}, scrollHeight=${scrollHeight}, clientHeight=${clientHeight}`);
    if (scrollTop + clientHeight >= scrollHeight - 50) {
      console.log('Near bottom - implement logic to fetch more data here');
      contacts_of_mobileNumber(); 



    }
  }


  function scrollview() {
    console.log(propData.number, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
    number = propData.number;
    startDate = propData.startdate;
    endDate = propData.enddate;
    currentPage = false;
    itemsPerPage = false;
    gotResult = false;
    showProgress = true;
    pagination = false;
    contacts_of_mobileNumber(currentPage);
  }
  function pageview() {
    number = propData.number;
    startDate = propData.startdate;
    endDate = propData.enddate;
    currentPage = 1;
    itemsPerPage = 4;
    gotResult = false;
    showProgress = true;
    pagination = true;

    contacts_of_mobileNumber(currentPage); // Pass currentPage as an argument
  }

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed


  // async function contacts_of_mobileNumber(currentPage) {
  //   gotResult = false;
  //   showProgress = true;
  //   const contacts_of_mobileNumber = new FormData();
  //   contacts_of_mobileNumber.append("number", number);
  //   contacts_of_mobileNumber.append("mode", "CdrBetweenDates");
  //   contacts_of_mobileNumber.append("fromdate", startDate);
  //   contacts_of_mobileNumber.append("todate", endDate);
  //   contacts_of_mobileNumber.append("page", currentPage);
  //   contacts_of_mobileNumber.append("items_per_page", itemsPerPage);

  //   try {
  //     // console.log(contacts_of_mobileNumber,"datas sent tobackend");
  //     const response = await fetch(`${basepath()}/call_details`, {
  //       method: "POST",
  //       body: contacts_of_mobileNumber,
  //     });

  //     if (response.ok) {
  //       data = await response.json();
  //       console.log(data);
  //       tableData = data["data_dict"];
  //       final_result = tableData;
  //       filteredResults = [...final_result];
  //       if (tableData.length > 0) {
  //         showProgress = false;
  //         tableHeader = data["headers"];
  //         gotResult = true;
  //         dispatch("updateData", filteredResults);
  //       }
  //       total_pages = data["totalpages"];

  //       page_count = Math.ceil(total_pages / 4) + 1;

  //       showTablePage = true;
  //       showProgress = false;
  //     } else {
  //       console.error("Failed to submit form");
  //     }
  //   } catch (error) {
  //     console.error("Error submitting form:", error);
  //   }
  // }

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
    console.log(filteredResults, "--filter results--");
  }
  function handlePageClick(newPage) {
    if (newPage >= 0 && newPage < page_count) {
      currentPage = newPage;
      itemsPerPage = 4;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      contacts_of_mobileNumber(currentPage);
    }
  }

  function handleNextClick() {
    if (currentPage + 1 < page_count) {
      currentPage += 1;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      contacts_of_mobileNumber(currentPage);
    }
  }

  function handlePrevClick() {
    if (currentPage - 1 >= 0) {
      currentPage -= 1;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      contacts_of_mobileNumber(currentPage);
    }
  }
  afterUpdate(() => {
    if (
      number != propData.number ||
      startDate != propData.startdate ||
      endDate != propData.enddate
    ) {
      return;
    } else {
      contacts_of_mobileNumber(currentPage);
      number = "";
      startDate = "";
      endDate = "";
    }
  });



async function contacts_of_mobileNumber() {

  number = propData.number;
  // startDate = propData.startdate;
  // endDate = propData.enddate;

  console.log(startDate,endDate)

  if (loading || allDataRecieved) return;

    loading = true;

    gotResult = false;
    showProgress = true;
    const contacts_of_mobileNumber1 = new FormData();
    contacts_of_mobileNumber1.append("number", number);
    contacts_of_mobileNumber1.append("mode", "CdrBetweenDates");
    contacts_of_mobileNumber1.append("fromdate", startDate);
    contacts_of_mobileNumber1.append("todate", endDate);
    contacts_of_mobileNumber1.append("page", $current_page);
    contacts_of_mobileNumber1.append("items_per_page", itemsPerPage);


    try {
      console.log(contacts_of_mobileNumber1,"datas sent tobackend");
      const response = await fetch(`${basepath()}/call_details`, {
        method: "POST",
        body: contacts_of_mobileNumber1,
      });

      if (response.ok) {
        data = await response.json();
        console.log(data)
        tableData = data["data_dict"];
        final_result = tableData;
        filteredResults = [...final_result];
        if (tableData.length > 0) {
          table_data.update(current => [...current, ...tableData]);
          current_page.update((value) => value + 1);

          console.log($table_data.length)

        } 
      
      } else {
        allDataRecieved = true;
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }finally {
    loading = false;
  }
  }



</script>

<!-- <div class="whole-container"> -->
  <!-- {#if showProgress}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {/if} -->
  <!-- {#if gotResult}
    <div class="header">
      <h2 class="heading">CDR DETAILS</h2>
      <div class="view">
        <button class="button" on:click={() => pageview()}>Page View</button>
        <button class="button" on:click={() => scrollview()}>Scroll View</button
        >
      </div>
    </div>
    <div class="table-container">
      <table>
        <thead style="position: sticky;">
          <tr>
            <th style="width: 6%;">SOURCE NUMBER</th>
            <th style="width: 7%;">OTHER NUMBER</th>
            <th style="width: 5%;"> NICKNAME </th>
            <th style="width: 10%;">ADDRESS</th>
            <th style="width: 5%;">CALLDATE</th>
            <th style="width: 6%;">CALLTIME</th>
            <th style="width: 5%;">CALL TYPE</th>
            <th style="width: 5%;">DURATION</th>
            <th style="width: 5%;">IMEI</th>
            <th style="width: 5%;">CELLID</th>
            <th style="width: 5%;">PROVIDER</th>
            <th style="width: 5%;">ROAMING</th>
            <th style="width: 10%;">USER ADDRESS</th>
            <th style="width: 5%;">LATITUDE</th>
            <th style="width: 5%;">LONGITUDE</th>
            <th style="width: 5%;">AZIMUTH</th>
          </tr>
          <tr>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("source_number", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("destination_number", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("nickname", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("address", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("calldate", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("calltime", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("call_type", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("duration", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("imei", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("cellid", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("provider", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("roaming", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("user_address", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("latitude", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("longitude", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("azimuth", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as tblD}
            <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
              <td>{tblD["source_number"]}</td>
              <td><a href="/cdat/profile?value={tblD['destination_number']}" target="_blank">{tblD["destination_number"]}</a></td>
              <td>{tblD["nickname"]}</td>
              <td>{tblD["address"]}</td>
              <td>{tblD["calldate"]}</td>
              <td>{tblD["calltime"]}</td>
              <td>{tblD["call_type"]}</td>
              <td>{tblD["duration"]}</td>
              <td><a href="/cdat/hyperlink?mode=imei&number={tblD['imei']}" target="_blank">{tblD["imei"]}</a></td>
              <td>{tblD["cellid"]}</td>
              <td>{tblD["provider"]}</td>
              <td>{tblD["roaming"]}</td>
              <td>{tblD["user_address"]}</td>
              <td>{tblD["latitude"]}</td>
              <td>{tblD["longitude"]}</td>
              <td>{tblD["azimuth"]}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    {#if pagination}
      <div class="pagination">
        {#if page_count > 1}
          <div class="pagination">
            <div class="flex items-center space-x-2">
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePageClick(1)}
                disabled={currentPage === 1}>FIRST</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePrevClick()}
                disabled={currentPage === 1}>{currentPage}</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handleNextClick()}
                disabled={currentPage + 1 >= page_count}
                >{currentPage + 1}</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePageClick(page_count - 1)}
                disabled={currentPage - 1 >= page_count}>LAST</button
              >
            </div>
          </div>
        {/if}
      </div>
    {/if} -->
    
<!--     
  {:else if showProgress}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {:else}
    <div class="no_data">
      <img src="/nodata.png" alt="" />
      <p class="nodata">No data Matched in Data Base!!!!!!!!</p>
    </div>
  {/if} -->


  {#if $table_data.length > 0}
      <h2 class="heading" style="margin: 100px 0px 10px 100px ">CDR DETAILS </h2>
    <div class="table-container">
      <table  id="cdr-table" style="margin-left: 100px;">
        <thead >
          <tr>
            <th style="width: 6%;">SOURCE NUMBER</th>
            <th style="width: 7%;">OTHER NUMBER</th>
            <th style="width: 5%;"> NICKNAME </th>
            <th style="width: 10%;">ADDRESS</th>
            <th style="width: 5%;">CALLDATE</th>
            <th style="width: 6%;">CALLTIME</th>
            <th style="width: 5%;">CALL TYPE</th>
            <th style="width: 5%;">DURATION</th>
            <th style="width: 5%;">IMEI</th>
            <th style="width: 5%;">CELLID</th>
            <th style="width: 5%;">PROVIDER</th>
            <th style="width: 5%;">ROAMING</th>
            <th style="width: 10%;">USER ADDRESS</th>
            <th style="width: 5%;">LATITUDE</th>
            <th style="width: 5%;">LONGITUDE</th>
            <th style="width: 5%;">AZIMUTH</th>
          </tr>
        </thead>
        <tbody bind:this={scrollContainer}>
          {#each $table_data as tblD}
            <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
              <td>{tblD["source_number"]}</td>
              <td><a href="/cdat/profile?value={tblD['destination_number']}" target="_blank">{tblD["destination_number"]}</a></td>
              <td>{tblD["nickname"]}</td>
              <td>{tblD["address"]}</td>
              <td>{tblD["calldate"]}</td>
              <td>{tblD["calltime"]}</td>
              <td>{tblD["call_type"]}</td>
              <td>{tblD["duration"]}</td>
              <td><a href="/cdat/hyperlink?mode=imei&number={tblD['imei']}" target="_blank">{tblD["imei"]}</a></td>
              <td>{tblD["cellid"]}</td>
              <td>{tblD["provider"]}</td>
              <td>{tblD["roaming"]}</td>
              <td>{tblD["user_address"]}</td>
              <td>{tblD["latitude"]}</td>
              <td>{tblD["longitude"]}</td>
              <td>{tblD["azimuth"]}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
{/if}

<!-- </div> -->

<style>


  .table-container {
  width: 100%;
  overflow: hidden;
}




#cdr-table {
    width: 100%;
    /* border-collapse: collapse; */
  }
  #cdr-table th, #cdr-table td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
  }
  #cdr-table th {
    background-color: #f2f2f2;
  }
  #cdr-table tr:nth-child(even) {
    background-color: #f2f2f2;
  }


#cdr-table {
  width: 100%;
  table-layout: fixed;
  /* border-collapse: collapse; */
}

#cdr-table thead th {
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

#cdr-table tbody {
  display: block;
  max-height: 600px;
  overflow-y: scroll;
}

#cdr-table thead,
#cdr-table tbody tr {
  display: table;
  width: 90%;
  table-layout: fixed;
}

#cdr-table tbody td {
  word-break: break-word;
}


#cdr-table th,
#cdr-table td {
  border: 1px solid #dee2e6;
  padding: .75rem; 
}

#cdr-table th:last-child,
#cdr-table td:last-child {
  border-right: none; 
}


</style>
