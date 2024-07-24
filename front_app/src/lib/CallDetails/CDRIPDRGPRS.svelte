<script>
  // @ts-nocheck
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";

  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let data = {};
  let showTablePage = false;
  let tableDataCdr;
  let tableHeader;
  let tableDataIpdr;
  let tableHeaderIpdr;
  let tableDataGprs;
  let tableHeaderGprs;
  let tableData;
  let showProgress = false;
  let gotResult = false;
  let final_result = [];
  let final_result1 = [];
  let final_result2 = [];
  let columnFilters = {};
  let filteredResults = [];
  let filteredResults1 = [];
  let filteredResults2 = [];
  let data_found = "No Data Yet";
  const dispatch = createEventDispatcher();

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed
    function contacts_of_mobileNumber() {
    gotResult = false;
    const contacts_of_mobileNumber = new FormData();
    contacts_of_mobileNumber.append("number", number);
    if (startDate) contacts_of_mobileNumber.append("fromdate", startDate);
    if (endDate) contacts_of_mobileNumber.append("todate", endDate);
    contacts_of_mobileNumber.append("mode", "IpdrGprsCdr");
    contacts_of_mobileNumber.append("page", currentPage);
    contacts_of_mobileNumber.append("items_per_page", itemsPerPage);
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/call_details`, {
    //     method: "POST",
    //     body: contacts_of_mobileNumber,
    //   });
    const url = `${basepath()}/call_details`;
    postRequest(fetch,url,contacts_of_mobileNumber)
    .then(data => {
        tableDataCdr = data["cdr_data"];
        tableDataIpdr = data["ipdr_data"];
        tableDataGprs = data["gprs_data"];
        final_result = tableDataCdr;
        final_result1 = tableDataIpdr;
        final_result2 = tableDataGprs;
        filteredResults = [...final_result];
        filteredResults1 = [...final_result1];
        filteredResults2 = [...final_result2];

        showProgress = false;
        gotResult = true;
        dispatch("updateData", filteredResults);
      } )
  }
  function got_to_page(pagenum) {
    currentPage = pagenum;
    contacts_of_mobileNumber();
  }
  let pagesToShow = 5; // Adjust this value to change the number of pages shown

  afterUpdate(() => {
    console.log("updated.....", propData);
    if (number != propData.number) {
      return;
    } else {
      contacts_of_mobileNumber();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  function calculateIndexes(currentPage, page_count) {
    let halfPagesToShow = Math.floor(pagesToShow / 2);
    let startIndex = currentPage - halfPagesToShow;
    let endIndex = currentPage + halfPagesToShow;

    if (startIndex < 1) {
      endIndex += Math.abs(startIndex) + 1;
      startIndex = 1;
    }

    if (endIndex > page_count) {
      startIndex -= endIndex - page_count;
      endIndex = page_count;
    }

    return { startIndex, endIndex };
  }

  function downloadDatacdr() {
    const wb = XLSX.utils.book_new();
    const dataArray = data.cdr_data.map((item) => {
      const formattedItem = {};
      data.cdr_headers.forEach((header) => {
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
    a.download = "cdr.xlsx";
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

  function downloadDataipdr() {
    const wb = XLSX.utils.book_new();
    const dataArray = data.ipdr_data.map((item) => {
      const formattedItem = {};
      data.ipdr_headers.forEach((header) => {
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

  function downloadDatagprs() {
    const wb = XLSX.utils.book_new();
    const dataArray = data.gprs_data.map((item) => {
      const formattedItem = {};
      data.gprs_headers.forEach((header) => {
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
    a.download = "gprs.xlsx";
    a.click();
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

  function handleColumnSearch1(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters1();
  }

  function applyFilters1() {
    const filteredData = final_result1.filter((item) => {
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
    filteredResults1 = filteredData;
  }

  function handleColumnSearch2(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters2();
  }

  function applyFilters2() {
    const filteredData = final_result2.filter((item) => {
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
    filteredResults2 = filteredData;
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

  <div class="excel_btn" style="margin-left: 5%; margin-top: 1%">
    <button class="excel" on:click={() => downloadDatacdr(filteredResults)}
      >CDR Excel</button
    >
    <button class="excel" on:click={() => downloadDataipdr(filteredResults)}
      >IPDR Excel</button
    >
    <button class="excel" on:click={() => downloadDatagprs(filteredResults)}
      >GPRS Excel</button
    >
  </div>

  {#if gotResult}
    <div class="cdr_container">
      <h3 class="heading">CDR DATA</h3>
      <div class="table-container">
        {#if filteredResults.length > 0}
          <table>
            <thead style="position: sticky;">
              <tr>
                <th style="width: 5%">SOURCE NUMBER</th>
                <th style="width: 6%">DESTINATION NUMBER</th>
                <th style="width: 5%">NICKNAME</th>
                <th style="width: 5%">CALL DATE</th>
                <th style="width: 12%">ADDRESS</th>
                <th style="width: 5%">CALL TYPE</th>
                <th style="width: 5%">DURATION</th>
                <th style="width: 4%">IMEI</th>
                <th style="width: 5%">CELL ID</th>
                <th style="width: 5%">PROVIDER</th>
                <th style="width: 5%">ROAMING</th>
                <th style="width: 5%">LATITUDE</th>
                <th style="width: 5%">LONGITUDE</th>
                <th style="width: 5%">AZIMUTH</th>
                <th style="width: 12%">USER ADDRESS</th>
              </tr>
              <tr>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("source_number", event)}
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
                    on:input={(event) => handleColumnSearch("address", event)}
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
                    on:input={(event) =>
                      handleColumnSearch("user_address", event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              {#each filteredResults as tblD}
                <tr>
                  <td>{tblD["source_number"]}</td>
                  <td
                    ><a
                      href="/cdat/profile?value={tblD['destination_number']}"
                      target="_blank">{tblD["destination_number"]}</a
                    ></td
                  >
                  <td>{tblD["nickname"]}</td>
                  <td>{tblD["calldate"]}</td>
                  <td>{tblD["address"]}</td>
                  <td>{tblD["call_type"]}</td>
                  <td>{tblD["duration"]}</td>
                  <td>{tblD["imei"]}</td>
                  <td>{tblD["cellid"]}</td>
                  <td>{tblD["provider"]}</td>
                  <td>{tblD["roaming"]}</td>
                  <td>{tblD["latitude"]}</td>
                  <td>{tblD["longitude"]}</td>
                  <td>{tblD["azimuth"]}</td>
                  <td>{tblD["user_address"]}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {:else}
          <div class="no_data" style="height: 20vh;">
            <img src="/nodata.png" alt="" style="width: 5%;" />
            <p class="nodata">No cdr data !!!!!!</p>
          </div>
        {/if}
      </div>
    </div>

    <div class="ipdr_container">
      <h3 class="heading">IPDR DATA</h3>
      {#if filteredResults1.length > 0}
        <div class="table-container">
          <table>
            <thead style="position: sticky;">
              <tr>
                <th style="width: 5%">Msisdn</th>
                <th style="width: 5%">Source IP</th>
                <th style="width: 5%">Source Port</th>
                <th style="width: 5%">Destination IP</th>
                <th style="width: 5%">Destination Port</th>
                <th style="width: 5%">CGID</th>
                <th style="width: 5%">Start Time</th>
                <th style="width: 5%">End Time</th>
                <th style="width: 5%">Home Circle</th>
                <th style="width: 5%">provider</th>
              </tr>
              <tr>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch1("msisdn", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("source_ip", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("source_port", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("destination_ip", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("destination_port", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch1("cgid", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("start_time", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch1("end_time", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch1("home_roaming_circle", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch1("provider", event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              {#each filteredResults1 as tblD}
                <tr>
                  <td>{tblD["msisdn"]}</td>
                  <td>{tblD["source_ip"]}</td>
                  <td>{tblD["source_port"]}</td>
                  <td>{tblD["destination_ip"]}</td>
                  <td>{tblD["destination_port"]}</td>
                  <td>{tblD["cgid"]}</td>
                  <td>{tblD["start_time"]}</td>
                  <td>{tblD["end_time"]}</td>
                  <td>{tblD["home_roaming_circle"]}</td>
                  <td>{tblD["provider"]}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <div class="no_data" style="height: 20vh;">
          <img src="/nodata.png" alt="" style="width: 10%;" />
          <p class="nodata">No ipdr data !!!!</p>
        </div>
      {/if}
    </div>

    <div class="gprs_container">
      <h3 class="heading">GPRS DATA</h3>
      {#if filteredResults2.length > 0}
        <div class="table-container">
          <table>
            <thead style="position: sticky;">
              <tr>
                {#each data.gprs_headers as tblH}
                  <th>
                    {tblH.toUpperCase().replace(/_/g, " ")}
                  </th>
                {/each}
              </tr>
              <tr>
                <th>
                  <input
                    class="input"
                    placeholder="Column"
                    on:input={(event) => handleColumnSearch2(tblH, event)}
                  />
                </th>
              </tr>
            </thead>
            <tbody>
              {#each filteredResults2 as tblD}
                <tr>
                  {#each data.gprs_headers as tblH}
                    <td
                      class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >
                      {tblD[tblH]}
                    </td>
                  {/each}
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <div class="no_data" style="height: 20vh;">
          <img src="/nodata.png" alt="" style="width: 10%;" />
          <p class="nodata">No gprs data !!!!</p>
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
      <img src="/nodata.png" alt="" style="width: 23%;" />
      <p class="nodata">No data Matched in Data Base</p>
    </div>
  {/if}
</div>

<style>
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
    font-size: 14px;
  }
  .cdr_container {
    height: 28vh;
  }
  .ipdr_container {
    height: 28vh;
  }
  .gprs_container {
    height: 28vh;
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
    max-height: 24vh;
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
  a {
    color: black;
  }
  .no_data {
    color: #161c2057;
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: center;
    /* height: 25vh; */
    justify-content: center;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }

  .heading {
    margin-left: 5%;
    color: #296b97;
    font-size: 1.5rem;
  }

  .excel {
    background-color: #296b97;
    color: white;
    border: none;
    height: 5vh;
    border-radius: 5px;
  }

  .excel_btn {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-right: 20px;
  }
</style>
