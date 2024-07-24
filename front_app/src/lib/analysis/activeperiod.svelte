<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  
  export let propData;
  $: number = propData.number;
  let data = {};
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
    function active_inactive_period_fuc() {
    gotResult = false;
    showProgress = true;
    const active_inactive_period = new FormData();
    active_inactive_period.append("numbers", number);
    active_inactive_period.append("mode", "active_inactive_period");
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/tower_analysis`, {
    //     method: "POST",
    //     body: active_inactive_period,
    //   });

      const url = `${basepath()}/tower_analysis`;
      postRequest(fetch,url,active_inactive_period)
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
          gotResult = true;
        }
      } )
  }
  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      active_inactive_period_fuc();
      number = "";
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
        if (filterValue) {
          // If the filter is applied for a list field, check its length
          if (Array.isArray(item[field])) {
            if (item[field].length !== parseInt(filterValue)) {
              return false;
            }
          } else if (
            !item[field].toString().toLowerCase().includes(filterValue)
          ) {
            // If it's not a list, proceed with regular filtering
            return false;
          }
        }
      }
      return true;
    });
    filteredResults = filteredData;
    dispatch("updateData", filteredResults);
    console.log(filteredResults, "---column filter-- data");
  }
</script>

<div class="roaming_container">
  <!-- {#if showProgress}
    <div class="absolute top-[50%] left-[50%] p-10">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {/if} -->

  {#if gotResult}
    <div class="heading">
      <h2 >Active Period</h2>
    </div>
    <div class="table_container">
      <!-- <div class="name_container"> -->
      <table class="table_data">
        <thead class="font-medium bg-base-content dark:border-neutral-500">
          <tr>
            <!-- {#each tableHeader as tblH}
              <th
                scope="col"
                class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >
                {tblH.toUpperCase().replace(/_/g, " ")}
              </th>
              {/each} -->

            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >Source Number
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) => handleColumnSearch("source_number", event)}
              />
            </th>
            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
            >
              Sitename
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) => handleColumnSearch("sitename", event)}
              />
            </th>
            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
            >
              start Date
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) => handleColumnSearch("start_date", event)}
              />
            </th>
            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
            >
              End Date
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) => handleColumnSearch("end_date", event)}
              />
            </th>
            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >Active Dates
              <br />
              <input
                class="input input-sm"
                placeholder="search"
                on:input={(event) => handleColumnSearch("active_dates", event)}
              />
            </th>
            <th
              scope="col"
              class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[155px]"
              >InActive Dates
              <br /><input
                class="input input-sm"
                placeholder="search"
                on:input={(event) =>
                  handleColumnSearch("inactive_dates", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
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
                >{tblD["sitename"]}</td
              >
              <td
                class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                >{tblD["start_date"]}</td
              >
              <td
                class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                >{tblD["end_date"]}</td
              >
              <td
                class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                >{tblD["active_dates"]}</td
              >
              <td
                class="border-r px-4 py-2 font-medium text-ellipsis dark:border-neutral-500"
                >{tblD["inactive_dates"]}</td
              >
            </tr>
          {/each}
        </tbody>
      </table>
      <!-- </div> -->
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
    width: 90%;
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
    width: 96.3%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 0%;
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
