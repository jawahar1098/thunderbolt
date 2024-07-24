<script>
  // @ts-nocheck

  //   import { base } from "$app/paths";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  export let propData;
  $: address = propData.address;

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
    function address_search_fun() {
    gotResult = false;
    showProgress = true;
    const address_search = new FormData();
    address_search.append("address", address);
    address_search.append("mode", "address_search");

    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/analysis`, {
    //     method: "POST",
    //     body: address_search,
    //   });
    const url = `${basepath()}/analysis`;
    postRequest(fetch,url,address_search)
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
        }
      } )
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
    a.download = "name.xlsx";
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
    if (address != propData.address) {
      return;
    } else {
      address_search_fun();
      address = "";
    }
  });
</script>

<div class="roaming_container">
  {#if gotResult}
    <div class="heading">
      <h2>Address Search</h2>
    </div>
    <div class="table_container">
      <div class="flex flex-col p-2 h-[80vh ] overflow-y-auto">
        <table class="table_data">
          <thead class="font-medium bg-base-content dark:border-neutral-500">
            <tr>
              <th scope="col" style="width: 5%;"
                >Name
                <br />
                <input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("name", event)}
                />
              </th>
              <th scope="col" style="width: 5%;"
                >Source Number
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("source_number", event)}
                />
              </th>
              <th scope="col" style="width: 5%;">
                Alternate Number
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("alternate_number", event)}
                />
              </th>
              <th scope="col" style="width: 5%;">
                Activate Date
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("date_of_activation", event)}
                />
              </th>
              <th scope="col" style="width: 10%;">
                Local Address
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("local_address", event)}
                />
              </th>
              <th scope="col" style="width: 10%;"
                >Permanent Address
                <br />
                <input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("permanent_address", event)}
                />
              </th>
              <th scope="col" style="width: 5%;"
                >State
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("state", event)}
                />
              </th>
              <!-- <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]">Match
                <br><input class="input input-sm" placeholder="Activation Date" on:input={(event) => handleColumnSearch('match', event)}/>
              </th> -->
            </tr>
          </thead>
          <tbody>
            {#each filteredResults as tblD}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["name"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["source_number"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["alternate_number"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["date_of_activation"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["local_address"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["permanent_address"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["state"]}</td
                >
                <!-- <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['match']}</td> -->
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
      <p class="nodata">{data_found}</p>
    </div>
  {/if}
</div>

<style>
  .input-sm {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }
  .roaming_container {
    width: 99%;
    margin-left: 15px;
    margin-top: 2vh;
  }
  table {
    width: 97%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: -1%;
    margin-left: 1%;
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2); */
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 6px;
    text-wrap: wrap;
  }

  thead {
    position: sticky;
    top: 0px;
    height: 10vh;
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
  }
  .table_container {
    max-height: 79vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
  }
  .heading {
    margin-left: 5%;
    color: #296b97;
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
