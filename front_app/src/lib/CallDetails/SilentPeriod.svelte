<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
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
  let data_found = "No Data Yet";
  let tableData;
  let showProgress = false;
  let gotResult = false;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

    function silent_period() {
    gotResult = false;
    showProgress = true;
    const silent_period = new FormData();
    silent_period.append("number", number);
    if (startDate) silent_period.append("fromdate", startDate);
    if (endDate) silent_period.append("todate", endDate);
    silent_period.append("mode", "silentPeriod");
    silent_period.append("page", currentPage);
    silent_period.append("items_per_page", itemsPerPage);
    // try {
    //   const response = await fetch(`${basepath()}/call_details`, {
    //     method: "POST",
    //     body: silent_period,
    //   });

    const url = `${basepath()}/call_details`;
    postRequest(fetch,url,silent_period)
    .then(data => {

        if (data.status === "failure") {
          showProgress = false;
          data_found = "No Data Matched With Database";
        } else {
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          showProgress = false;
          gotResult = true;
          dispatch("updateData", filteredResults);
          total_pages = data["totalpages"];
          page_count = total_pages / 10;
        }
      } )
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
      silent_period();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  function got_to_page(pagenum) {
    currentPage = pagenum;
    silent_period();
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
    <div class="flex justify-center mt-3">
      <h2 class="heading">SILENT PERIOD</h2>
    </div>
    <div class="table-container">
      <div>
        <div>
          <table>
            <thead style="position: sticky">
              <tr>
                <th style="width: 5%;">SOURCE NUMBER </th>
                <th style="width: 5%;">DESTINATION NUMBER </th>
                <th style="width: 5%;">NICKNAME </th>
                <th style="width: 5%;">Start Date </th>
                <th style="width: 5%;">End Date </th>
                <th style="width: 5%;">INCOMING </th>
                <th style="width: 5%;">OUTGOING </th>
                <th style="width: 5%;">TOTAL CALLS </th>
                <th style="width: 5%;">DURATION </th>
                <th style="width: 14%;">Address </th>
                <th style="width: 5%;">Silent Period </th>
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
                    on:input={(event) =>
                      handleColumnSearch("call_start_date", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("call_end_date", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("in", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("out", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("calls", event)}
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
                    on:input={(event) => handleColumnSearch("address", event)}
                  />
                </th>
                <th class="search">
                  <input
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("silent_period", event)}
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
                  <td>{tblD["call_start_date"]}</td>
                  <td>{tblD["call_end_date"]}</td>
                  <td
                    ><a
                      href="/cdat/hyperlink?number={propData.number}&mode=call_in&dest_number={tblD[
                        'destination_number'
                      ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                      target="_blank">{tblD["in"]}</a
                    ></td
                  >
                  <td
                    ><a
                      href="/cdat/hyperlink?number={propData.number}&mode=call_out&dest_number={tblD[
                        'destination_number'
                      ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                      target="_blank">{tblD["out"]}</a
                    ></td
                  >
                  <td
                    ><a
                      href="/cdat/hyperlink?number={propData.number}&mode=total_calls&dest_number={tblD[
                        'destination_number'
                      ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                      target="_blank">{tblD["calls"]}</a
                    ></td
                  >
                  <td>{tblD["dur"]}</td>
                  <td>{tblD["address"]}</td>
                  <td>{tblD["silent_period"]}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
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
      /* margin-top: -1%; */
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
    }
    .table-container {
      max-height: 80vh;
      overflow-y: auto;
      overflow-x: auto;
      position: sticky;
      z-index: 1;
      /* margin-top: 2vh; */
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
    a{
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
  
  
  
  </style>