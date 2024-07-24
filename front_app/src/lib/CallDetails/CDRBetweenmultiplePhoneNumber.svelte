<script>
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
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let data_found = "No Data Yet";
  const dispatch = createEventDispatcher();

  // let listnumber = number.split(",")

  async function contacts_of_mobileNumber() {
    gotResult = false;
    const contacts_of_mobileNumber = new FormData();
    contacts_of_mobileNumber.append("number", number);
    if (startDate) contacts_of_mobileNumber.append("fromdate", startDate);
    if (endDate) contacts_of_mobileNumber.append("todate", endDate);
    contacts_of_mobileNumber.append("mode", "CdrBtwmultipleNumber");
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

        if (data.status !== "failure") {
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          if (tableData.length > 0) {
            showProgress = false;
            tableHeader = data["headers"];
            gotResult = true;
            dispatch("updateData", filteredResults);
          } else {
            showProgress = false;
            gotResult = false;
            data_found = "Give valid data";
          }
        } else {
          data_found = "No Data Matched in Database";
          showProgress = false;
          gotResult = false;
        }
        total_pages = data["totalpages"];
        page_count = total_pages / 10;
      } )
  }

  afterUpdate(() => {
    if (
      number != propData.number ||
      startDate != propData.startdate ||
      endDate != propData.enddate
    ) {
      return;
    } else {
      contacts_of_mobileNumber();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  function got_to_page(pagenum) {
    currentPage = pagenum;
    contacts_of_mobileNumber();
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
  <!-- {#if showProgress}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {/if} -->

  {#if gotResult}
    <div class="flex justify-center mt-3">
      <h2 class="heading">CDR DETAILS BETWEEEN MULTIPLE NUMBERS</h2>
    </div>
    <div class="table-container">
      <table>
        <thead style="position: sticky;">
          <tr>
            <th style="width: 4.7%;">PHONE</th>
            <!-- <th style="width: 6%;">SOURCE NUMBER</th> -->
            <th style="width: 4.7%;">OTHER</th>
            <!-- <th style="width: 6%;">DESTINATION NUMBER</th> -->
            <th style="width: 5%;">OTHER NICKNAME</th>
            <!-- <th style="width: 5%;">NICKNAME</th> -->
            <th style="width: 8%;">OTHER ADDRESS</th>
            <th style="width: 4.2%;">CALLDATE</th>
            <th style="width: 4%;">CALL TIME</th>
            <th style="width: 3.5%;">CALL TYPE</th>
            <th style="width: 3%;">DURATION</th>
            <th style="width: 6.5%;">IMEI</th>
            <!-- added -->
            <th style="width: 6.5%;">IMSI</th>
            <th style="width: 5%;">CELLID</th>
            <th style="width: 8%;">AREA DESCRIPTION</th>

            <th style="width: 4%;">PROVIDER</th>
            <th style="width: 5%;">ROAMING</th>
            <th style="width: 4%;">LAT</th>
            <th style="width: 4%;">LONG</th>
            <th style="width: 3%;">AZM</th>
            <!-- <th style="width: 8%;">USER ADDRESS</th> -->
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
                on:input={(event) => handleColumnSearch("user_address", event)}
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
              <!-- <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("imei", event)}
              /> -->
            </th>

            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("cellId", event)}
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
           
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as tblD}
            <tr>
              <td
                ><a
                  href="/cdat/profile?value={tblD['source_number']}"
                  target="_blank">{tblD["source_number"]}</a
                ></td
              >
              <td
                ><a
                  href="/cdat/profile?value={tblD['destination_number']}"
                  target="_blank">{tblD["destination_number"]}</a
                ></td
              >
              <td>{tblD["nickname"]}</td>
              <td>{tblD["user_address"]}</td>

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
              <td>000000000000000</td>
              
              <td>{tblD["cellId"]}</td>
              <td>{tblD["address"]}</td>

              <td>{tblD["provider"]}</td>
              <td>{tblD["roaming"]}</td>
              <td>{tblD["latitude"]}</td>
              <td>{tblD["longitude"]}</td>
              <td>{tblD["azimuth"]}</td>
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
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: -1%;
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
  .heading {
    margin-left: 5%;
    color: #296b97;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
</style>
