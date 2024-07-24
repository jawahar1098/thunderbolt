<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";

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
    try {
      const response = await fetch(`${basepath()}/call_details`, {
        method: "POST",
        body: contacts_of_mobileNumber,
      });

      if (response.ok) {
        data = await response.json();
        console.log(data);
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
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
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

<div
  style="margin-left: 2vh;
width: 91%;"
>
  <!-- {#if showProgress}
      <div class="position-absolute top-50 start-50 translate-middle p-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    {/if} -->

  {#if gotResult}
    <div class="table-container">
      <table>
        <thead style="position: sticky;">
          <tr>
            <th style="width: 4%;">SOURCE NUMBER</th>
            <th style="width: 4%;">DESTINATION NUMBER</th>
            <th style="width: 5%;">NICKNAME</th>
            <th style="width: 5%;">CALLDATE</th>
            <th style="width: 5%;">CALL TIME</th>
            <th style="width: 5%;">CALL TYPE</th>
            <th style="width: 5%;">DURATION</th>
            <th style="width: 5%;">IMEI</th>
            <th style="width: 5%;">CELLID</th>
            <th style="width: 5%;">PROVIDER</th>
            <th style="width: 5%;">ROAMING</th>
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
              <td>{tblD["cellId"]}</td>
              <td>{tblD["provider"]}</td>
              <td>{tblD["roaming"]}</td>
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
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: -1%; */
    /* margin-left: 5%; */
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
    width: 100%;
    max-height: 63vh;
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
</style>
