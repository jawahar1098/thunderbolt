<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let data;
  let urlParamValue;
  let parammode;
  let dest_num;
  let HomeContentHeading;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  // Refer day_and_night_location_between_dates flask endpoint, completed
  function cellid_search() {
    gotResult = false;
    const cellid_search = new FormData();
    cellid_search.append("number", number);
    cellid_search.append("mode", "CellidData");

    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/search`, {
    //     method: "POST",
    //     body: cellid_search,
    //   });

      const url = `${basepath()}/search`;
      postRequest(fetch,url,cellid_search)
      .then(data => {

        console.log(data);
        if (data["headers"] === "No Data") {
          showProgress = false;
          data_found = "No Data Matched With Database";
        } else {
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          showProgress = false;
          tableHeader = data["headers"];
          gotResult = true;
          dispatch("updateData", filteredResults);
          HomeContentHeading = "cellidpage";
          console.log(tableData, tableHeader);
        }
      })
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      cellid_search();
      number = "";
    }
  });

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
</script>

<div class="relatieve">
  {#if gotResult}
    <div class="justify-center mt-3">
      <h2 class="heading" style="margin-left: 2%;">Cell_ID Data</h2>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 5%;">CELLTOWERID</th>
            <th style="width: 5%;">BTS ID</th>
            <th style="width: 5%;"> AREADESCRIPTION</th>
            <th style="width: 14%;">SITE ADDRESS</th>
            <th style="width: 5%;">LATITUDE</th>
            <th style="width: 5%;">LONGITUDE</th>
            <th style="width: 5%;">AZIMUTH</th>
            <th style="width: 5%;">OPERATOR</th>
            <th style="width: 5%;">STATE</th>
            <th style="width: 5%;">OTYPE</th>
            <th style="width: 5%;">LAST UPDATED</th>
          </tr>
          <tr>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("celltowerid", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("bts_id", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("areadescription", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("siteaddress", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("lat", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("long", event)}
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
                on:input={(event) => handleColumnSearch("operator", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("state", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("otype", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("lastupdate", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as item}
            <tr class="border-bottom hover-bg-gray-100">
              {#each tableHeader as header}
                {#if parammode === "total_calls" || HomeContentHeading === "cellidpage"}
                  {#if header === "call_count"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                    >
                      <a
                        href="/search/cellidSearch?value={number}&mode=total_calls"
                        target="_blank">{item[header]}</a
                      >
                    </td>
                  {:else if header === "cdat_count" || header === "call_in" || header === "call_out" || header === "total_calls"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                    >
                      <a
                        href="/search/cellidSearch?value={item[
                          'source_number'
                        ]}&mode={header}&dest_number={item[
                          'destination_number'
                        ]}"
                        target="_blank">{item[header]}</a
                      >
                    </td>
                  {:else if header === "destination_number" || header === "cellid"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                      ><a
                        href="/search/cellidSearch?value={item[
                          header
                        ]}&mode=dest_num"
                        target="_blank">{item[header]}</a
                      ></td
                    >
                  {:else if header === "imei"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                      ><a
                        href="/search/cellidSearch?value={item[
                          header
                        ]}&mode=imei"
                        target="_blank">{item[header].length}</a
                      ></td
                    >
                    <!-- {/if} -->
                  {:else}
                    <td class="border-right px-2 py-1 font-medium text-ellipsis"
                      >{item[header]}</td
                    >
                  {/if}
                {:else if parammode === "imei" || parammode === "call_out" || parammode === "call_in" || parammode === "total_calls"}
                  {#if header === null}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                    ></td>
                  {:else if header === "cdat_count" || header === "call_in" || header === "call_out" || header === "total_calls"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                      ><a
                        href="/search/cellidSearch?value={item[
                          'source_number'
                        ]}&mode={header}&dest_number={item[
                          'destination_number'
                        ]}"
                        target="_blank">{item[header]}</a
                      ></td
                    >
                  {:else if header === "imei"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                    >
                      <a
                        href="/search/cellidSearch?value={item[
                          header
                        ]}&mode=imei"
                        target="_blank">{item[header]}</a
                      ></td
                    >
                  {:else if header === "destination_number"}
                    <td
                      class="border-right px-2 py-1 font-medium text-ellipsis text-danger"
                    >
                      <a
                        href="/search/cellidSearch?value={item[
                          header
                        ]}&mode=dest_num"
                        target="_blank">{item[header]}</a
                      ></td
                    >
                  {:else}
                    <td class="border-right px-2 py-1 font-medium text-ellipsis"
                      >{item[header]}</td
                    >
                  {/if}
                {/if}
              {/each}
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
      <p class="nodata">{data_found}!!!!!!!!</p>
    </div>
  {/if}
</div>

<style>
  table {
    width: 97%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 1%;
    margin-left: 2%;
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
