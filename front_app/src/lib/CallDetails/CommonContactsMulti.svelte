<script>
  // @ts-nocheck
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  // export let number1 = "";
  // export let number2 = "";
  export let propData;
  $: number = propData.number;

  let data = {};
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let data_found = "No Data Yet";
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  function contacts_of_mobileNumber() {
    gotResult = false;
    const contacts_of_mobileNumber = new FormData();
    contacts_of_mobileNumber.append("number", number);
    contacts_of_mobileNumber.append("mode", "CommonContacts");
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/call_details`, {
    //     method: "POST",
    //     body: contacts_of_mobileNumber,
    //   });
        const url = `${basepath()}/call_details`;
        postRequest(fetch,url,contacts_of_mobileNumber)
        .then(data => {

        if (data["result"] === "no data") {
          data_found = `No common contact Matched for these numbers ${propData.number} In Database`;
          showProgress = false;
          gotResult = false;
          console.log(gotResult, "inside");
        } else {
          showProgress = false;
          tableData = data["result"];
          final_result = tableData;
          filteredResults = [...final_result];
          gotResult = true;
          dispatch("updateData", filteredResults);
          total_pages = data["totalpages"];
          page_count = total_pages / 10;
        }
      } )
  }

  afterUpdate(() => {
    console.log("updated.....", propData);
    if (number != propData.number) {
      return;
    } else {
      contacts_of_mobileNumber();
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
      <h2 class="heading">CDR DETAILS BETWEEEN MULTIPLE NUMBERS</h2>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Destination Number </th>
            <th> Source Numbers </th>
            <th> count </th>
          </tr>
          <tr>
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
                on:input={(event) =>
                  handleColumnSearch("source_numbers", event)}
              />
            </th>
            <th class="search">
              <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("count", event)}
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as tblD}
            <tr>
              <td
                ><a
                  href="/cdat/profile?value={tblD['destination_number']}"
                  target="_blank">{tblD["destination_number"]}</a
                ></td
              >
              <td>{tblD["source_numbers"]}</td>
              <td
                ><a
                  href="/cdat/hyperlink?dest_number={tblD[
                    'destination_number'
                  ]}&number={tblD['source_numbers']}&mode=hyper_contact"
                  target="_blank">{tblD["count"]}</a
                ></td
              >
            </tr>{/each}
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
      <p class="nodata">{data_found}</p>
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
