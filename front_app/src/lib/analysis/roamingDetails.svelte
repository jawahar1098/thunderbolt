<script>
  // @ts-nocheck

  //   import { base } from "$app/paths";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  
  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let data = {};
  let showTablePage = false;
  let tableData;
  let tableData2;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let data_found_native = `No Native data found in database for ${propData.number}`;
  let data_found_roaming = `No roaming data found in database for ${propData.number}`;
  let final_result = [];
  let final_result2 = [];
  let columnFilters = {};
  let filteredResults = [];
  let filteredResults2 = [];
  const dispatch = createEventDispatcher();

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed
    function roaming_details_fuc() {
    gotResult = false;
    showProgress = true;
    const roaming_details = new FormData();
    roaming_details.append("numbers", number);
    if (startDate) roaming_details.append("fromdate", startDate);
    if (endDate) roaming_details.append("todate", endDate);
    roaming_details.append("mode", "roaming_details");
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/tower_analysis`, {
    //     method: "POST",
    //     body: roaming_details,
    //   });
    const url = `${basepath()}/tower_analysis`;
    postRequest(fetch,url,roaming_details)
    .then(data => {

        tableHeader = data["data_dict"];
        if (tableHeader === "No Data") {
          showProgress = false;
          data_found = "No Matches in Database";
        } else {
          // showProgress = false;
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          // native_dict
          tableData2 = data["native_dict"];
          final_result2 = tableData2;
          filteredResults2 = [...final_result2];
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
    if (number != propData.number) {
      return;
    } else {
      roaming_details_fuc();
      number = "";
      startDate = "";
      endDate = "";
    }
  });
</script>

{#if gotResult}
  <div class="native_container">
    <div class="heading">
      <h2>Native Location</h2>
    </div>
    {#if tableData2 !== "No Data"}
      <div class="table_container1" style="max-height: 18vh;">
        <table class="table_data">
          <thead>
            <tr>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
                >Source Number
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("source_number", event)}
                />
              </th>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >
                State
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("state", event)}
                />
              </th>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >
                Date of Activation
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("date_of_activation", event)}
                />
              </th>
             
            </tr>
          </thead>
          <tbody>
            {#each filteredResults2 as tblD}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["source_number"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["state"]}</td
                >
                <td
                  class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                  >{tblD["date_of_activation"]}</td
                >
                
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else}
      <div class="no_data" style="height: 18vh;">
        <img src="/nodata.png" alt="" style="width: 10%;" />
        <p class="nodata">{data_found_native}</p>
      </div>
    {/if}
  </div>

  <div class="roaming_container">
    <div class="heading">
      <h2>Roaming Location</h2>
    </div>
    {#if tableData !== "No Data"}
      <div class="table_container">
        <!-- <div class="flex flex-col p-2 h-[80vh ] overflow-y-auto"> -->
        <table class="table_data">
          <thead class="font-medium bg-base-content dark:border-neutral-500">
            <tr>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
                >Source Number
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("source_number", event)}
                />
              </th>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >
                State
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("state", event)}
                />
              </th>
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >
                Total Record
                <br /><input
                  class="input input-sm"
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("count", event)}
                />
              </th>
              <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
            >
              source
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("from", event)}
              />
            </th>
            </tr>
          </thead>
          <tbody>
            {#each filteredResults as tblD}
              <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                <td>{tblD["source_number"]}</td>
                <td>{tblD["state"]}</td>
                <td>{tblD["count"]}</td>
                <td>{tblD["from"]}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else}
      <div class="no_data" style="height: 38vh;">
        <img src="/nodata.png" alt="" style="width: 15%;" />
        <p class="nodata">{data_found_roaming}!!!!!!!!</p>
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
  <div class="no_data">
    <img src="/nodata.png" alt="" />
    <p class="nodata">{data_found}</p>
  </div>
{/if}

<style>
  .input-sm {
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
    padding: 6px;
    text-wrap: wrap;
  }
  .native_container {
    height: 20vh;
    width: 100%;
    margin-top: 8px;
  }
  .roaming_container {
    height: 65vh;
    width: 100%;
  }

  thead {
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
  tbody {
    height: 30%;
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table_container1 {
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    /* height: 0vh; */
  }
  .table_container {
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    height: 60vh;
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
    width: 23%;
  }

  .heading {
    margin-left: 5%;
    color: #296b97;
    /* margin-top: 3vh;
    margin-bottom: 1vh; */
    font-size: 1.5rem;
  }
</style>
