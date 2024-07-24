<script>
  // @ts-nocheck
  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  let total_pages = 0;
  let showTablePage = false;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let data = {};
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
    showProgress = true;

    const imei_search_data = new FormData();
    imei_search_data.append("number", number);
    imei_search_data.append("mode", "IMEIUsedInPHONE");
    imei_search_data.append("page", currentPage);
    imei_search_data.append("items_per_page", itemsPerPage);
    // try {
    //   const response = await fetch(`${basepath()}/imei_search`, {
    //     method: "POST",
    //     body: imei_search_data,
    //   });
    const url = `${basepath()}/imei_search`;
    postRequest(fetch,url,imei_search_data)
    .then(data => {
          console.log(data);
          tableData = data["data_dict"] || [];
          final_result = tableData;
          filteredResults = [...final_result];
          tableHeader = data["headers"] || [];

          if (data["data_dict"] !== "Not data Matched") {
            showProgress = false;
            gotResult = true;
            dispatch("updateData", filteredResults);
            total_pages = data["totalpages"] || 0;
            page_count = Math.ceil(total_pages / itemsPerPage);
          } else {
            showProgress = false;
            datafound = "No data matched in database";
          }
        } )
  }
  function got_to_page(pagenum) {
    currentPage = pagenum;
    imei_search_data_fuc();
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
    if (number != propData.number) {
      return;
    } else {
      imei_search_data_fuc();
      number = "";
    }
  });
</script>

<div class="relatieve">
  {#if gotResult}
  <div class="flex justify-center mt-3">
    <h2 class="heading">IMEI used in Phone</h2>
  </div>
    <div class="table-container">
      <div class="d-flex flex-column p-2">
        <table>
          <thead>
            <tr>
              <th style="width: 5%;">PHONE</th>
              <th style="width: 5%;">NICKNAME </th>
              <th style="width: 14%;">ADDRESS</th>
              <th style="width: 5%;">IMEI</th>
              <th style="width: 5%;">INCOMING</th>
              <th style="width: 5%;">OUTGOING</th>
              <th style="width: 5%;">TOTAL CALLS</th>
              <th style="width: 5%;">DURATION</th>
              <th style="width: 5%;">FIRST CALL</th>
              <th style="width: 5%;">LAST CALL</th>
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
                  on:input={(event) => handleColumnSearch("imei", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("call_in", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("call_out", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("total_calls", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("dur", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("first_call", event)}
                />
              </th>
              <th class="search">
                <input
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
                >{tblD["source_number"]}</td
              >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["nickname"]}</td
                >
                
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["address"]}</td
                >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["imei"]}</td
              >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["call_in"]}</td
                >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["call_out"]}</td
                >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["total_calls"]}</td
                >
                <td class="border-right px-2 py-1 font-medium text-ellipsis"
                  >{tblD["dur"]}</td
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
    padding: 8px;
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
  tbody {
    height: 73%;
                        
                      }
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
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
  a {
    color: black;
  }
</style>
