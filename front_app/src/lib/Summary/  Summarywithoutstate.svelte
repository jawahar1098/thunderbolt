<script>
  // @ts-nocheck

  import { createEventDispatcher, onMount, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  $: state = propData.state;
  let showProgress = false;
  export let state = "";
  let gotResult = false;
  let tableData;
  let tableHeader;
  let pagination = true;
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let showTablePage = false;
  let data = {};
  let datafound = "NO Data Yet";
  const dispatch = createEventDispatcher();

  // SUMMARY OF MOBILE NUMBER WITHIN A STATE, Refer summary_within_state flask endpoint, completed
  function summary_otherthan_state() {
    gotResult = false;
    showProgress = true;
    const summary_otherthan_state = new FormData();
    summary_otherthan_state.append("number", number);
    if (startDate) summary_otherthan_state.append("fromdate", startDate);
    if (endDate) summary_otherthan_state.append("todate", endDate);
    summary_otherthan_state.append("state", state);
    summary_otherthan_state.append("mode", "SummaryWithoutState");
    summary_otherthan_state.append("page", currentPage);
    summary_otherthan_state.append("items_per_page", itemsPerPage);

    // try {
    //   const response = await fetch(`${basepath()}/summary_for_state`, {
    //     method: "POST",
    //     body: summary_otherthan_state,
    //   });

    const url = `${basepath()}/summary_for_state`;
    postRequest(fetch,url,summary_otherthan_state)
    .then(data => {


        console.log(data["data_dict"]);
        if (data["data_dict"] === "Not data Matched") {
          showProgress = false;
          gotResult = false;
          datafound = "No Data Matched In Database";
        } else {
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          tableHeader = data["headers"];
          showProgress = false;
          gotResult = true;
          dispatch("updateData", filteredResults);
          total_pages = data["totalpages"];
          page_count = total_pages / 10;
          showTablePage = true;
        }
      } )
  }

  afterUpdate(() => {
    console.log("updated.....", propData);
    if (number != propData.number) {
      return;
    } else {
      summary_otherthan_state();
      number = "";
      startDate = "";
      endDate = "";
      state = "";
    }
  });

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

{#if showProgress}
  <div class="position-absolute top-50 start-50 translate-middle p-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{/if}

{#if gotResult}
  <div class="flex justify-center mt-3">
    <h4 class="heading">SUMMARY OTHER THAN STATE - {propData.number}</h4>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 4%;">PHONE</th>
          <th style="width: 4%;">OTHER</th>
          <th style="width: 4%;">OTHER NICKNAME </th>
          <th style="width: 15%;">OTHER ADDRESS</th>
          <th style="width: 4%;">STATE</th>
          <th style="width: 4%;">INCOMING</th>
          <th style="width: 4%;">OUTGOING</th>
          <th style="width: 4%;">TOTAL CALLS </th>
          <th style="width: 4%;">FIRSTCALL</th>
          <th style="width: 4%;">LASTCALL </th>
          <th style="width: 4%;">DURATION</th>
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
              on:input={(event) => handleColumnSearch("state", event)}
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
              on:input={(event) => handleColumnSearch("first_call", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("last_call", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("lduration", event)}
            />
          </th>
          
        </tr>
      </thead>
      <tbody>
        
        {#each filteredResults as item}
          <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
            <td>{item["source_number"]}</td>
            <td>
              <a
                href="/cdat/profile?value={item['destination_number']}"
                target="_blank"
              >
                {item["destination_number"]}
              </a></td
            >
            <td>{item["nickname"]}</td>
           
            <td>{item["address"]}</td>
            <td>{item["state"]}</td>
            <td
              ><a
                href="/cdat/hyperlink?number={propData.number}&mode=call_in&dest_number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state={item["state"]}"
                target="_blank">{item["call_in"]}</a
              ></td
            >
            <td
              ><a
                href="/cdat/hyperlink?number={propData.number}&mode=call_out&dest_number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state={item["state"]}"
                target="_blank">{item["call_out"]}</a
              ></td
            >
            <td
              ><a
                href="/cdat/hyperlink?number={propData.number}&mode=total_calls&dest_number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state={item["state"]}"
                target="_blank">{item["total_calls"]}</a
              ></td
            >
            <td>{item["first_call"]}</td>
            <td>{item["last_call"]}</td>
            <td>{item["duration"]}</td>
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
    <p class="nodata">{datafound}!!!!!!!!</p>
  </div>
{/if}

<style>
  .heading {
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
  table {
    width: 94.5%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 5%;
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
    top: -1px;
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
  }
  .table-container {
    max-height: 78vh;
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
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
</style>
