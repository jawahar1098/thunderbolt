<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import * as XLSX from "xlsx";

  let loopCount = "";
  export let startDate = "";
  export let number = "";
  export let endDate = "";
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let data = {};
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "No Data Yet";
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];

  async function contacts_of_mobileNumber() {
    gotResult = false;
    console.log(loopCount, number);
    const contacts_of_mobileNumber = new FormData();
    contacts_of_mobileNumber.append("number", number);
    contacts_of_mobileNumber.append("loopcount", loopCount);
    contacts_of_mobileNumber.append("fromdate", startDate);
    contacts_of_mobileNumber.append("todate", endDate);
    contacts_of_mobileNumber.append("mode", "loopcalls");
    showProgress = true;
    try {
      const response = await fetch(`${basepath()}/call_details`, {
        method: "POST",
        body: contacts_of_mobileNumber,
      });

      if (response.ok) {
        data = await response.json();
        console.log(data);
        if (data["data_dict"] === "No Data") {
          data_found = "No Data Matched In Database";
          showProgress = false;
        } else {
          showProgress = false;
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          tableHeader = data["headers"];
          gotResult = true;
          total_pages = data["totalpages"];
          page_count = total_pages / 10;
        }
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  onMount(() => {
    contacts_of_mobileNumber();
  });

  function got_to_page(pagenum) {
    currentPage = pagenum;
    contacts_of_mobileNumber();
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
</script>

<div class="relatieve h-[100vh] w-[100vw]">
  {#if showProgress}
    <div class="absolute top-[50%] left-[50%] p-10">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {/if}
  <div class="col-start-6 mr-10 col-span-3 flex justify-end">
    <button
      class="px-2 py-1 flex-end text-lg bg-green-900 hover:bg-green-600 text-white"
      on:click={() => downloadData(filteredResults)}>Download Excel</button
    >
  </div>
  <div class="table-container">
    {#if gotResult}
      <div
        class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between w-full px-5"
      >
        <div class="flex flex-col p-2 h-[80vh ] overflow-y-auto">
          <table
            class="table-auto border text-center text-sm font-light dark:border-neutral-500"
          >
            <thead class="font-medium bg-base-content dark:border-neutral-500">
              <tr>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >SOURCE NUMBER
                  <!-- <br><input class="input input-sm" placeholder="PHONE " on:input={(event) => handleColumnSearch('source_number', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >DESTINATION NUMBER
                  <!-- <br><input class="input input-sm" placeholder="OTHER" on:input={(event) => handleColumnSearch('destination_number', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >NICKNAME
                  <!-- <br> <input class="input input-sm" placeholder="NICKNAME" on:input={(event) => handleColumnSearch('Nickname', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >CALLDATE
                  <!-- <br> <input class="input input-sm" placeholder="CALLDATE" on:input={(event) => handleColumnSearch('calldate', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >CALLTIME
                  <!-- <br> <input class="input input-sm" placeholder="CALLTIME" on:input={(event) => handleColumnSearch('calltime', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >CALL TYPE
                  <!-- <br> <input class="input input-sm" placeholder="CALL TYPE" on:input={(event) => handleColumnSearch('Call_type', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >DURATION
                  <!-- <br> <input class="input input-sm" placeholder="DURATION" on:input={(event) => handleColumnSearch('Duration', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >IMEI
                  <!-- <br> <input class="input input-sm" placeholder="IMEI" on:input={(event) => handleColumnSearch('IMEI', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >CELLID
                  <!-- <br><input class="input input-sm" placeholder="CELLID" on:input={(event) => handleColumnSearch('CellId', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >PROVIDER
                  <!-- <br><input class="input input-sm" placeholder="PROVIDER" on:input={(event) => handleColumnSearch('Provider', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >ROAMING
                  <!-- <br><input class="input input-sm" placeholder="ROAMING" on:input={(event) => handleColumnSearch('Roaming', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >Address
                  <!-- <br><input class="input input-sm" placeholder="Address" on:input={(event) => handleColumnSearch('Address', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >LATITUDE
                  <!-- <br> <input class="input input-sm" placeholder="LATITUDE" on:input={(event) => handleColumnSearch('Latitude', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >LONGITUDE
                  <!-- <br> <input class="input input-sm" placeholder="LONGITUDE" on:input={(event) => handleColumnSearch('Longitude', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >AZIMUTH
                  <!-- <br> <input class="input input-sm" placeholder="AZIMUTH" on:input={(event) => handleColumnSearch('azimuth', event)}/> -->
                </th>
                <th
                  scope="col"
                  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[110px]"
                  >USER ADDRESS
                  <!-- <br> <input class="input input-sm" placeholder="USER ADDRESS" on:input={(event) => handleColumnSearch('user_address', event)}/> -->
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("source_number", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("destination_number", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Nickname", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("calldate", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("calltime", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Call_type", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Duration", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("IMEI", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("CellId", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Provider", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Roaming", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Address", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Latitude", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("Longitude", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) => handleColumnSearch("azimuth", event)}
                  />
                </td>
                <td>
                  <input
                    class="border-r border-b px-4 py-1 dark:border-neutral-500 w-[122px]"
                    placeholder="search"
                    on:input={(event) =>
                      handleColumnSearch("user_address", event)}
                  />
                </td>
              </tr>
              {#each filteredResults as tblD}
                <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                  <!-- {#each tableHeader as tblH}
                 <td
                   class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                 >
                   {tblD[tblH]}
                 </td>
                 {/each} -->

                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["source_number"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["destination_number"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Nickname"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["calldate"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["calltime"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Call_type"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Duration"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["IMEI"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["CellId"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Provider"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Roaming"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Address"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Latitude"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["Longitude"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["azimuth"]}</td
                  >
                  <td
                    class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                    >{tblD["user_address"]}</td
                  >
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-4 flex justify-center">
        <button
          class="btn btn-sm btn-secondary"
          on:click={() => got_to_page(1)}
          disabled={currentPage === 1}>First</button
        >

        {#each Array.from( { length: pagesToShow } ).slice(calculateIndexes(currentPage, page_count).startIndex - 1, calculateIndexes(currentPage, page_count).endIndex) as _, index}
          <button
            class="btn btn-sm btn-primary"
            on:click={() =>
              got_to_page(
                calculateIndexes(currentPage, page_count).startIndex + index
              )}
            >{calculateIndexes(currentPage, page_count).startIndex +
              index}</button
          >
        {/each}

        <button
          class="btn btn-sm btn-secondary ml-2"
          on:click={() => got_to_page(page_count)}
          disabled={currentPage === page_count}>Last</button
        >
      </div>
    {:else}
      <div class="w-25 flex justify-center mt-20">
        <span>{data_found}</span>
      </div>
    {/if}
  </div>
</div>

<style>
  button {
    border: 2px solid;
  }
  .table-container {
    margin-top: 2%;
    margin-bottom: 2%;
    margin-left: 2%;
    margin-right: 2%;
    overflow-x: auto;
    max-height: 700px;
    position: relative;
  }
  .input-sm {
    font-size: 0.8em;
    width: 80px;
    color: black;
  }

  table {
    width: 100%;
    table-layout: fixed;
    /* border-color: black; */
    text-align: center;
    border-collapse: collapse;
  }

  th,
  td {
    /* border: 1px solid black;
    padding: 8px; */
    text-align: center;
    text-wrap: wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
    border-collapse: collapse;
  }

  th {
    /* background-color: #121212;
    color: rgb(115, 112, 112); */
    padding: 15px;
    position: sticky;
    top: 0;
    z-index: 1;
    text-align: center;
  }
</style>
