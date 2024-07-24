<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";

  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let total_pages = 0;
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
  const dispatch = createEventDispatcher();

  // contacts_of_mobileNumber MOBILE HANDSET SEARCH,,mobile_handset_analysis flask endpoint, completed
   function contacts_of_mobileNumber() {
    gotResult = false;
    showProgress = true;
    const contacts_of_mobileNumber = new FormData();
    contacts_of_mobileNumber.append("number", number);
    if (propData.startdate)
      contacts_of_mobileNumber.append("fromdate", startDate);
    if (propData.enddate) contacts_of_mobileNumber.append("todate", endDate);
    contacts_of_mobileNumber.append("mode", "cdrIMEI");
    contacts_of_mobileNumber.append("page", currentPage);
    contacts_of_mobileNumber.append("items_per_page", itemsPerPage);
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/call_details`, {
    //     method: "POST",
    //     body: contacts_of_mobileNumber,
    //   });

      const url = `${basepath()}/call_details`;
      postRequest(fetch,url,contacts_of_mobileNumber)
      .then(data => {


        tableData = data["data_dict"];
        final_result = tableData;
        filteredResults = [...final_result];
        if (tableData.length > 0) {
          showProgress = false;
          tableHeader = data["headers"];
          total_pages = data["totalpages"];
          gotResult = true;
          dispatch("updateData", filteredResults);
        } else {
          showProgress = false;
          data_found = "no data matched in database";
        }
      })
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

  function formatcoordinate(value) {
    return Number(parseFloat(value).toFixed(4));
  }
</script>

<div class="relatieve">
  {#if gotResult}
  <div class="flex justify-center mt-3">
    <h2 class="heading">IMEI DETAILS</h2>
  </div>
  <div class="table-container">
   
      <table>
        <thead style="position: sticky;">
          <tr>
            <th style="width: 5%;">PHONE</th>
            <th style="width: 6%;">OTHER</th>
            <th style="width: 5%;">OTHER NICKNAME </th>
            <th style="width: 12%;">OTHER ADDRESS</th>

            <th style="width: 5%;">CALL DATE</th>
            <th style="width: 5%;"> CALL TIME</th>
            <th style="width: 5%;"> CALL TYPE</th>
            <th style="width: 5%;">DURATION</th>
            <th style="width: 5%;">IMEI</th>
            <th style="width: 5%;">IMSI</th>

            <th style="width: 5%;">CELL ID</th>
            <th style="width: 12%;">AREA DESCRIPTION</th>
            <th style="width: 5%;">PROVIDER</th>
            <th style="width: 5%;">ROAMING</th>
            <th style="width: 5%;">LAT</th>
            <th style="width: 5%;">LONG</th>
            <th style="width: 5%;">AZM</th>
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
                placeholder=" search "
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
                on:input={(event) => handleColumnSearch("user_address", event)}
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
              <!-- <input
                placeholder="search"
                on:input={(event) => handleColumnSearch("imei", event)}
              /> -->
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
                on:input={(event) => handleColumnSearch("address", event)}
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
            
          </tr>
        </thead>
        <tbody>
          {#each filteredResults as tblD}
            <tr>
             
              <td>{tblD["source_number"]}</td>
              <td
                ><a
                  href="/cdat/profile?value={tblD['destination_number']}"
                  target="_blank">{tblD["destination_number"]}</a
                ></td
              >
              <td>{tblD["nickname"]}</td>
              <td>{tblD["user_address"]}</td>

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
              <td>000000000000000</td>
              <td>{tblD["cellid"]}</td>
              <td>{tblD["address"]}</td>
              <td>{tblD["provider"]}</td>
              <td>{tblD["roaming"]}</td>
              <td>{formatcoordinate(tblD["latitude"])}</td>
              <td>{formatcoordinate(tblD["longitude"])}</td>
              <td>{tblD["azimuth"]}</td>
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
        <p class="nodata">{data_found}</p>
      </div>
    {/if}
</div>

<style>
  table {
    width: 93.8%;
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
    padding: 5px;
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
  /* tbody {
   
 } */
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 79vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    margin-top: 2vh;
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
