<script>
    // @ts-nocheck
    import { postRequest } from "$lib/req_utils";
    import { createEventDispatcher, afterUpdate } from "svelte";
    import { basepath } from "$lib/config";
  
    export let propData;
    $: number = propData.number;
    $: startDate = propData.startdate;
    $: endDate = propData.enddate;
    $: mode = propData.mode;
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
  
    
    function scrollview() {
      console.log(propData.number, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      mode = propData.mode;
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
     function contacts_of_mobileNumber(currentPage) {
      gotResult = false;
      showProgress = true;
      const contacts_of_mobileNumber = new FormData();
      contacts_of_mobileNumber.append("number", number);
      contacts_of_mobileNumber.append("mode", mode);
      if (startDate) contacts_of_mobileNumber.append("fromdate", startDate);
      if (endDate) contacts_of_mobileNumber.append("todate", endDate);
      contacts_of_mobileNumber.append("page", currentPage);
      contacts_of_mobileNumber.append("items_per_page", itemsPerPage);
  
      
      const url = `${basepath()}/tower_lookup`;
      postRequest(fetch, url, contacts_of_mobileNumber)
           
        // fetch(url,{
        //   method:'post',
        //   body:contacts_of_mobileNumber
        // })
        .then(res => res.json())
        .then(data => {

        tableData = data["data_dict"];
        final_result = tableData;
        filteredResults = [...final_result];
        if (tableData.length > 0) {
          showProgress = false;
          tableHeader = data["headers"];
          gotResult = true;
          dispatch("updateData", filteredResults);
        }
        total_pages = data["totalpages"];
  
        page_count = Math.ceil(total_pages / 4) + 1;
  
        showTablePage = true;
        showProgress = false;
      });
  
      //   if (response.ok) {
      //     data = await response.json();
      //     console.log(data);
      //   } else {
      //     console.error("Failed to submit form");
      //   }
      // } catch (error) {
      //   console.error("Error submitting form:", error);
      // }
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
        // mode != propData.mode
      ) {
        return;
      } else {
        contacts_of_mobileNumber(currentPage);
        number = "";
        startDate = "";
        endDate = "";
        // mode = "";
      }
    });
  </script>
  
  <div class="whole-container">
    
    {#if gotResult}
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
              <th style="width: 7%;">DESTINATION NUMBER</th>
              <th style="width: 5%;"> NICKNAME </th>
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
              <th style="width: 10%;">ADDRESS</th>
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
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("address", event)}
                />
              </th>
            </tr>
          </thead>
          <tbody>
            {#each filteredResults as tblD}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <td>{tblD["source_number"]}</td>
                <td>
                  <a
                    href="/cdat/profile?value={tblD['destination_number']}"
                    target="_blank">{tblD["destination_number"]}</a
                  ></td
                >
                <td>{tblD["nickname"]}</td>
                <td>{tblD["calldate"]}</td>
                <td>{tblD["calltime"]}</td>
                <td>{tblD["call_type"]}</td>
                <td>{tblD["duration"]}</td>
                <td
                  ><a
                    href="/cdat/hyperlink?mode=imei&number={tblD['imei']}"
                    target="_blank">{tblD["imei"]}</a
                  ></td
                >
                <td>{tblD["cellid"]}</td>
                <td>{tblD["provider"]}</td>
                <td>{tblD["roaming"]}</td>
                <td>{tblD["user_address"]}</td>
                <td>{tblD["latitude"]}</td>
                <td>{tblD["longitude"]}</td>
                <td>{tblD["azimuth"]}</td>
                <td>{tblD["address"]}</td>
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
      {/if}
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
    {/if}
  </div>
  
  <style>
    .whole-container {
      width: 100%;
      height: 83vh;
    }
    table {
      width: 94%;
      table-layout: fixed;
      text-align: center;
      border-collapse: collapse;
      /* margin-top: 1%; */
      margin-left: 5%;
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
    }
    .table-container {
      max-height: 66vh;
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
  
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 2%;
    }
  
    tbody tr:hover {
      background-color: #d0e4f1;
    }
    a {
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
    .btn {
      background-color: #3498db;
      color: white;
      border: none;
    }
    img {
      width: 23%;
    }
    .heading {
      margin-left: 5%;
      color: #296b97;
    }
  
    .pagination {
      margin-top: 1%;
      /* margin-left: 5%; */
      display: flex;
      justify-content: center;
    }
  
    .view {
      margin-right: 1%;
    }
    .button {
      padding: 8px 15px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      width: 7vw;
      /* margin-left: 10px; */
    }
  </style>
  