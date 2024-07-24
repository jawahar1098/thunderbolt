<script>
  // @ts-nocheck

  import { base } from "$app/paths";
  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import * as XLSX from "xlsx";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.name;

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
  function nickname_search() {
    gotResult = false;
    const nickname_search = new FormData();
    nickname_search.append("number", number);
    nickname_search.append("mode", "NicknameSearch");

    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/search`, {
    //     method: "POST",
    //     body: nickname_search,
    //   });
    const url = `${basepath()}/search`;
    postRequest(fetch,url,nickname_search)
    .then(data => {

        console.log(data);
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
        }
      })
  }

  afterUpdate(() => {
    if (number != propData.name) {
      return;
    } else {
      nickname_search();
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
    a.download = "nick.xlsx";
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
    <div class="flex justify-center mt-3">
      <h2 class="heading">NICKNAME</h2>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 5%;"> MSISDN</th>
            <th style="width: 7%;">NICKNAME </th>
            <th style="width: 5%;">NAME</th>
            <th style="width: 5%;">PROVIDER</th>
            <th style="width: 5%;">CIRCLE</th>
            <th style="width: 14%;">LOCAL ADDRESS</th>
            <th style="width: 14%;">PERMANENT ADDRESS</th>
            <th style="width: 5%;">ACTIVATION DATE</th>
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
                on:input={(event) => handleColumnSearch("nickname", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("name", event)}
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
                on:input={(event) => handleColumnSearch("circle", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("local_address", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("permanent_address", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("activation_date", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
          
          {#each filteredResults as tblD}
            <tr class="border-bottom hover-bg-gray-100">
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["msisdn"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["nickname"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["name"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["provider"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["circle"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["local_address"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["permanent_address"]}</td
              >
              <td class="border-right px-2 py-1 font-medium text-ellipsis"
                >{tblD["activation_date"]}</td
              >
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
    width: 98%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: -1%; */
    margin-left: 1%;
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
