<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: selectedValues = propData.selectedValues;
  $: startDate = propData.startDate;
  $: endDate = propData.endDate;
  const dispatch = createEventDispatcher();

  let data = [];
  let final_result = [];
  let ind_num_val = [];
  let filteredResults = [];
  let columnFilters = {};
  let mode;
  let current_num;

  let gotResult = false;
  let data_found = "No data";
  let showProgress = true;
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 0;
  let itemsPerPage = 50;
  let pagination = false;
  let downexcel = false;
  let userDetails = JSON.parse(localStorage.getItem("userDetails"));
  console.log(ind_num_val, "==============");

  function handleSubmit() {
    gotResult = false;
    showProgress = true;

    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({
    //     value: selectedValues,
    //     mode: "formulaone",
    //     fromdate: startDate,
    //     todate: endDate,
    //   }),
    // })

    const url = `${basepath()}/analysis`;
    postRequest(fetch,url,SON.stringify({
        value: selectedValues,
        mode: "formulaone",
        fromdate: startDate,
        todate: endDate,
      }),)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          final_result = data.response;
          console.log(final_result, "--fhj");
          filteredResults = [...final_result];
          dispatch("updateData", filteredResults);
          gotResult = true;
          showProgress = false;
        } else {
          gotResult = false;
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      })
      .finally(() => {
        showProgress = false;
      });
  }
  function handleColumnSearch(column, event) {
    // console.log("----",column);
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
    console.log(filteredResults, "------------");
  }

  afterUpdate(() => {
    if (selectedValues != propData.selectedValues) {
      return;
    } else {
      handleSubmit();
      selectedValues = "";
      startDate = "";
      endDate = "";
    }
  });

  function setPage(p) {
    showprogress = true;
    if (p >= 0 && p < page_count) {
      currentPage = p;
      itemsPerPage = 50;
      gotResult = false;
      getcasedata();
    }
  }
  function formatDate(dateString) {
    if (!dateString) {
      return "Invalid Date";
    }

    const date = new Date(dateString);

    // Check if the date is invalid (NaN)
    if (isNaN(date.getTime())) {
      return "Invalid Date";
    }

    const year = date.getUTCFullYear();
    const month = (date.getUTCMonth() + 1).toString().padStart(2, "0");
    const day = date.getUTCDate().toString().padStart(2, "0");

    return `${day}-${month}-${year}`; // ${hours}:${minutes}:${seconds}`;
  }
</script>

{#if showProgress}
  <div class="position-absolute top-50 start-50 translate-middle p-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{:else if gotResult}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th> Source Number </th>
          <th> Nick name </th>
          <th> Full name </th>
          <th> date of Activation </th>
          <th> Address </th>
          <th> Alternal Number </th>
          <th> Destination Number </th>
          <th> Dates present </th>
          <th> Date Diff </th>
          <th> First call </th>
          <th> Last call </th>
          <th> Total calls </th>
          <th> valid Numbers </th>
          <th> Invalid Numbers </th>
          <th> Call in </th>
          <th> Call out </th>
          <th> Sms in </th>
          <th> Sms out </th>
          <th> incoming </th>
          <th> Outgoing </th>
          <th> provider </th>
          <th> Sector </th>
          <th> Tower </th>
          <th> state </th>
          <th> Imei </th>
          <th> Imei CDR </th>
          <th> Only sms </th>
          <th> Only incoming </th>
          <th> Only outgoing </th>
        </tr>
        <tr>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("source_number", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("nickname", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("fullname", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("date_of_activation", event)}
                />
              </th>

              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("local_address", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("alternate_number", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("other_number", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("dates_present", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("date_difference", event)}
                />
              </th><th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("max_date", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("min_date", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_call_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("validUniqueCount", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("notValidUniqueCount", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_callin_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_callout_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_smsin_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_smsout_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_in_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("total_out_count", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("provider", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("sector", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("tower", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("state", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("imei", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("imei_count_cdr", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) => handleColumnSearch("only_sms", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("only_incoming", event)}
                />
              </th>
              <th class="search"
                ><input
                  class="input input-sm"
                  placeholder="Search"
                  on:input={(event) =>
                    handleColumnSearch("only_outgoing", event)}
                />
              </th>
            </tr>
      </thead>
      <tbody>
        {#each filteredResults as tblD}
          <tr class="border border-gray-100">
            <td>{tblD["source_number"]}</td>
            <td>{tblD["nickname"]}</td>
            <td>{tblD["fullname"]}</td>
            <td>{tblD["date_of_activation"]}</td>
            <td>{tblD["local_address"]}</td>
            <td>{tblD["alternate_number"]}</td>
            <td>{tblD["other_number"]}</td>
            <td>{tblD["dates_present"]}</td>
            <td>{tblD["date_difference"]}</td>
            <td>{formatDate(tblD["max_date"])}</td>
            <td>{formatDate(tblD["min_date"])}</td>
            <td>{tblD["total_call_count"]}</td>
            <td>{tblD["validUniqueCount"].length}</td>
            <td>{tblD["notValidUniqueCount"].length}</td>
            <td>{tblD["total_callin_count"]}</td>
            <td>{tblD["total_callout_count"]}</td>
            <td>{tblD["total_smsin_count"]}</td>
            <td>{tblD["total_smsout_count"]}</td>
            <td>{tblD["total_in_count"]}</td>
            <td>{tblD["total_out_count"]}</td>
            <td>{tblD["provider"]}</td>
            <td>{tblD["sector"].length}</td>
            <td>{tblD["tower"].length}</td>
            <td>{tblD["state"].length}</td>
            <td>{tblD["imei"].length}</td>
            <td
              >{#if tblD["imei_count_cdr"] !== ""}{tblD["imei_count_cdr"][0]
                  .length}{:else}
                0
              {/if}</td
            >
            <td>{tblD["only_sms"].length}</td>
            <td>{tblD["only_incoming"].length}</td>
            <td>{tblD["only_outgoing"].length}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
 
{:else}
  <div class="no_data">
    <img src="/nodata.png" alt="" />
    <p class="nodata">No data Matched in Data Base!!!!!!!!</p>
  </div>
{/if}

<style>
  table {
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    /* margin-left: 5%; */
  }

  th{
    width: 6vw;
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
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 80vh;
    margin-top: 4vh;
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

  thead tr {
    border: none;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
  /* a {
    color: black;
  } */
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
