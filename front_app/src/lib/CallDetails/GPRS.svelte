<script>
  // @ts-nocheck
  import { createEventDispatcher, afterUpdate } from "svelte";

  import * as XLSX from "xlsx";
  import { onMount } from "svelte";
  import { postRequest } from "$lib/req_utils";
  import { basepath } from "$lib/config";

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
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed
    function gprs_info() {
    gotResult = false;
    const gprs_info = new FormData();
    gprs_info.append("number", number);
    gprs_info.append("mode", "gprsdetails");
    gprs_info.append("page", currentPage);
    gprs_info.append("items_per_page", itemsPerPage);
    showProgress = true;
    // try {
    //   const response = await fetch(
    //     `http://${window.location.hostname}:5005/call_details`,
    //     {
    //       method: "POST",
    //       body: gprs_info,
    //     }
    //   );
    const url = `${basepath()}/call_details`;
    postRequest(fetch,url,gprs_info)
    .then(data => {

        tableHeader = data["headers"];
        if (tableHeader === "No Data") {
          showProgress = false;
          data_found = "No Matches in Database";
        } else {
          showProgress = false;
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          gotResult = true;
          dispatch("updateData", filteredResults);
          total_pages = data["totalpages"];
          page_count = total_pages / 10;
        }
      } )
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      gprs_info();
      number = "";
      startDate = "";
      endDate = "";
    }
  });
  function got_to_page(pagenum) {
    currentPage = pagenum;
    gprs_info();
  }
  let pagesToShow = 5; // Adjust this value to change the number of pages shown

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

  function downloadData() {
    const wb = XLSX.utils.book_new();
    const dataArray = tableData.map((item) => {
      const formattedItem = {};
      tableHeader.forEach((header) => {
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
    a.download = "GPRS.xlsx";
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
    const filteredData = filteredResults.filter((item) => {
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
</script>

<div class="relatiev">
  {#if showProgress}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {/if}
  {#if gotResult}
    <div class="table-container">
      <div
        class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between w-full px-5"
      >
        <div class="flex flex-col p-2">
          <table
            class="table-auto border text-center text-sm font-light dark:border-neutral-500"
          >
            <thead class="font-medium bg-base-content dark:border-neutral-500">
              <tr>
                <th>Source Number</th>
                <th>IP Address</th>
                <th>Cell Id</th>
                <th>imei</th>
                <th>imsi</th>
                <th>Downlink Vol</th>
                <th>Uplink Vol</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Romaing</th>
              </tr>
              <tr>
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("source_number", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("ip_address", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("cgid", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("imei", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("imsi", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("downlink_vol", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("uplink_vol", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("start_time", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("end_time", event)}
                  /></th
                >
                <th class="search"
                  ><input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("roaming", event)}
                  /></th
                >
              </tr>
            </thead>
            <tbody>
              {#each filteredResults as tblD}
                <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                  {#each tableHeader as tblH}
                    <td
                      class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500"
                    >
                      {tblD[tblH]}
                    </td>
                  {/each}
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
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
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 2%;
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
    /* width: 5vw; */
  }
  .table-container {
    max-height: 90vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
  }
  .search {
    /* width: 100%;
      box-sizing: border-box; */
    background-color: #5cb2eb;
    border: 1px solid #a5c2d5;
    /* border-bottom: none; */
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
    background-color: rgb(236, 226, 226);
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
</style>
