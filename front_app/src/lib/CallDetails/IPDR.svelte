<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
  import { onMount } from "svelte";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;

  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 5;
  let data = {};
  let showTablePage = false;
  // @ts-ignore
  let tableData;
  // @ts-ignore
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  // @ts-ignore
  let final_result = [];
  let columnFilters = {};
  // @ts-ignore
  let filteredResults = [];
  let pagination = true;
  const dispatch = createEventDispatcher();

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
    ipdr_details(currentPage);
  }
  function pageview() {
    number = propData.number;
    startDate = propData.startdate;
    endDate = propData.enddate;
    currentPage = 1;
    itemsPerPage = 5;
    gotResult = false;
    showProgress = true;
    pagination = true;

    ipdr_details(currentPage); // Pass currentPage as an argument
  }

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed
   function ipdr_details(currentPage) {
    gotResult = false;
    showProgress = true;
    const ipdr_details = new FormData();
    ipdr_details.append("number", number);
    ipdr_details.append("mode", "ipdrdetails");
    ipdr_details.append("fromdate", startDate);
    ipdr_details.append("todate", endDate);
    ipdr_details.append("page", currentPage);
    ipdr_details.append("items_per_page", itemsPerPage);
    // showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/call_details`, {
    //     method: "POST",
    //     body: ipdr_details,
    //   });
      const url = `${basepath()}/call_details`;
      postRequest(fetch,url,ipdr_details)
      .then(data => {
  
        // @ts-ignore
        tableData = data["data_dict"];
        final_result = tableData;
        filteredResults = [...final_result];

        if (data["headers"] == "No Data") {
          showProgress = false;
          // @ts-ignore
        } else {
          tableHeader = data["headers"];
          gotResult = true;
          showProgress = false;
          dispatch("updateData", filteredResults);
        }
        // @ts-ignore
        total_pages = data["totalpages"];
        page_count = Math.ceil(total_pages / 5);
        showTablePage = true;
      })
  }

  afterUpdate(() => {
    console.log("updated.....", propData);
    if (
      number != propData.number ||
      startDate != propData.startdate ||
      endDate != propData.enddate
    ) {
      return;
    } else {
      ipdr_details(currentPage);
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  // @ts-ignore
  function downloadData() {
    const wb = XLSX.utils.book_new();
    // @ts-ignore
    const dataArray = tableData.map((item) => {
      const formattedItem = {};
      // @ts-ignore
      tableHeader.forEach((header) => {
        // @ts-ignore
        formattedItem[header] = item[header];
      });
      return formattedItem;
    });
    const ws = XLSX.utils.json_to_sheet(dataArray);
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    const excelData = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
    const blob = new Blob([s2ab(excelData)], {
      type: "application/octet-stream",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ipdr.xlsx";
    a.click();
  }

  // @ts-ignore
  function s2ab(s) {
    const buf = new ArrayBuffer(s.length);
    const view = new Uint8Array(buf);
    for (let i = 0; i < s.length; i++) {
      view[i] = s.charCodeAt(i) & 0xff;
    }
    return buf;
  }

  // @ts-ignore
  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    // @ts-ignore
    columnFilters[column] = filterValue;
    applyFilters();
  }

  function applyFilters() {
    // @ts-ignore
    const filteredData = final_result.filter((item) => {
      for (const field in columnFilters) {
        // @ts-ignore
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
  function handlePageClick(newPage) {
    if (newPage >= 0 && newPage < page_count) {
      currentPage = newPage;
      itemsPerPage = 5;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      ipdr_details(currentPage);
    }
  }

  function handleNextClick() {
    if (currentPage + 1 < page_count) {
      currentPage += 1;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      ipdr_details(currentPage);
    }
  }

  function handlePrevClick() {
    if (currentPage - 1 >= 0) {
      currentPage -= 1;
      number = propData.number;
      startDate = propData.startdate;
      endDate = propData.enddate;
      ipdr_details(currentPage);
    }
  }
</script>

<div class="whole-container">
  {#if gotResult}
    <div class="header">
      <h2 class="heading">IPDR DETAILS</h2>
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
            <th style="width: 4%;">Msisdn</th>
            <th style="width: 4%;">Source IP</th>
            <th style="width: 4%;">Source Port</th>
            <th style="width: 4%;">OTHER IP</th>
            <th style="width: 5%;">OTHER Port</th>
            <th style="width: 5%;">CGID</th>
            <th style="width: 4%;">Company</th>
            <th style="width: 4%;">Domain</th>
            <th style="width: 4%;">VPN</th>
            <th style="width: 4%;">START TIME</th>
            <th style="width: 4%;">END TIME</th>
            <th style="width: 4%;">DURATION</th>
            <th style="width: 4%;">Data Usage</th>
            <th style="width: 4%;">Com Type</th>
            <th style="width: 4%;">Home Circle</th>
            <th style="width: 4%;">provider</th>
          </tr>
          <tr>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("msisdn", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("source_ip", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("source_port", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("destination_ip", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("destination_port", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("cgid", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("company", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("domain", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("vpn", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("start_time", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("end_time", event)}
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
                on:input={(event) => handleColumnSearch("datausage", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("ip_type", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("home_circle", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("provider", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as tblD}
            <tr>
              <td
                ><a href="/cdat/profile?value={tblD['msisdn']}" target="_blank"
                  >{tblD["msisdn"]}</a
                ></td
              >
              <td>{tblD["source_ip"]}</td>
              <td>{tblD["source_port"]}</td>
              <td>{tblD["destination_ip"]}</td>
              <td>{tblD["destination_port"]}</td>
              <td
                ><a
                  href="/cdat/hyperlink?mode=cellid&number={tblD['cgid']}"
                  target="_blank">{tblD["cgid"]}</a
                ></td
              >
              <td>{tblD["company"]}</td>
              <td>{tblD["domain"]}</td>
              <td>{tblD["vpn"]}</td>
              <td>{tblD["start_time"]}</td>
              <td>{tblD["end_time"]}</td>
              <td>{tblD["duration"]}</td>
              <td>{tblD["datausage"]}</td>
              <td>{tblD["ip_type"]}</td>
              <td>{tblD["home_circle"]}</td>
              <td>{tblD["provider"]}</td>
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
      <p class="nodata">No Data Matched in Database!!!!!</p>
    </div>
  {/if}
</div>

<!-- <style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 2%; */
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
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 2%;
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

  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
    /* width: 5vw; */
  }
  .table-container {
    max-height: 84vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    margin-top: 2vh;
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
    width: 6vw;
    /* margin-left: 10px; */
  }
</style> -->

<style>
  .whole-container{
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
    max-height: 67vh;
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
    width: 6vw;
    /* margin-left: 10px; */
  }
</style>

