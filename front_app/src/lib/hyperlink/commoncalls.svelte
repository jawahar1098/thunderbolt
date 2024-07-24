<script>
  // @ts-nocheck

  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  export let number;
  export let dest_number;
  let showProgress = false;
  let gotResult = false;
  let filteredResults = [];
  let datafound = "no data yet";
  let final_result = [];
  let totalcalls;
  let data = {};
  let columnFilters = {};
  let tableData;

  function common_contacts_url() {
    gotResult = false;
    showProgress = true;
    const common_contacts = new FormData();
    common_contacts.append("number", number);
    common_contacts.append("dest_num", dest_number);
    common_contacts.append("mode", "common_contacts");


    const url = `${basepath()}/call_details`;
    postRequest(fetch,url,common_contacts)

    // fetch(`${basepath()}/call_details`, {
    //   method: "POST",
    //   body: common_contacts,
    // })
      .then((response) => response.json())
      .then((data) => {
        console.log(data, "-data--");
        if (data.data_dict === "Not data Matched") {
          showProgress = false;
          datafound = "No Data Matched In Database";
        } else {
          totalcalls = data["data_dict"];
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          console.log(filteredResults);
          gotResult = true;
        }
      });
  }

  common_contacts_url();
  // onMount(() => {
  //   const urlParams = new URLSearchParams($page.url.search);
  //    number = urlParams.get('value');
  //    mode = urlParams.get('mode');

  //   if (number && mode) {
  //     common_contacts_url();
  //   }
  // })
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
    console.log(filteredResults, "--filter results--");
  }
</script>

{#if gotResult}
  <!-- Another table starts -->
  <div class="flex justify-center mt-3">
    <h4
      style="margin-top: 1%; text-align:center; font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif"
    >
      Summary of {number}
    </h4>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 7%;">Source number</th>
          <th style="width: 7%;">Destination number</th>
          <th style="width: 5%;">nickname</th>
          <th style="width: 5%;">calldate</th>
          <th style="width: 5%;">calltime</th>
          <th style="width: 5%;">call_type</th>
          <th style="width: 5%;">duration</th>
          <th style="width: 5%;">imei</th>
          <th style="width: 5%;">cellid</th>
          <th style="width: 5%;">provider</th>
          <th style="width: 5%;">roaming</th>
          <th style="width: 10%;">address</th>
          <th style="width: 5%;">latitude</th>
          <th style="width: 5%;">longitude</th>
          <th style="width: 5%;">azimuth</th>
          <th style="width: 10%;">user_address</th>
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
              on:input={(event) => handleColumnSearch("calldate", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("calltime", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_type", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("duration", event)}
            />
          </th>

          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("imei", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("cellid", event)}
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
              on:input={(event) => handleColumnSearch("roaming", event)}
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
              on:input={(event) => handleColumnSearch("latitude", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("longitude", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("azimuth", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("user_address", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
        {#each filteredResults as item}
          <tr>
            <td>{item.source_number}</td>
            <td>{item.destination_number}</td>
            <td>{item.nickname}</td>
            <td>{item.calldate}</td>
            <td>{item.calltime}</td>
            <td>{item.call_type}</td>
            <td>{item.duration}</td>
            <td>{item.imei}</td>
            <td>{item.cellid}</td>
            <td>{item.provider}</td>
            <td>{item.roaming}</td>
            <td>{item.address}</td>
            <td>{item.latitude}</td>
            <td>{item.longitude}</td>
            <td>{item.azimuth}</td>
            <td>{item.user_address}</td>
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
    <p class="nodata">No calls!!!!!!!!</p>
  </div>
{/if}

<style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 2%; */
    margin-left: 5%;
    box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2);
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
    background-color: black;
    border: 1px;
    color: rgb(118, 214, 57);
    height: 15px 10px;
    text-transform: uppercase;
  }
  tbody {
    width: 5%;
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 90vh;
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
    background-color: rgb(236, 226, 226);
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
  .heading {
    margin-left: 5%;
    color: #296b97;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
</style>
