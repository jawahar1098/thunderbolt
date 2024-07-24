<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";
  import { onMount } from "svelte";
  export let number;
  export let dest_number;
  export let fromdate;
  export let todate;
  export let state;
  console.log(fromdate, todate);
  let showProgress = false;
  let gotResult = false;
  let filteredResults = [];
  let datafound = "no data yet";
  let final_result = [];
  let data = {};
  let mode = "";
  let columnFilters = {};
  let callin;

  let tableData;
  let exportData = [];
  onMount(() => {
    // Prepare the data for export, including headers
    exportData = [
      [
        "source Number",
        "Destination Number",
        "nickname",
        "call Date",
        "call type",
        "imei",
        "cellid",
        "provider",
        "roaming",
        "address",
        "latitude",
        "longitude",
        "azimuth",
        "user address",
      ],
    ];
  });
  function exportToXLSX() {
    const ws = XLSX.utils.aoa_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, `${number}_${dest_number}_${fromdate}_${todate}_${state}_call_in.xlsx`);
  }

  function hyper_callin() {
    gotResult = false;
    showProgress = true;
    const call_in = new FormData();
    call_in.append("number", number);
    call_in.append("dest_num", dest_number);
    call_in.append("fromdate", fromdate);
    call_in.append("todate", todate);
    call_in.append("state", state);
    call_in.append("mode", "call_in");

    const url = `${basepath()}/hyperlink`
    postRequest(fetch,url,call_in)
      .then((data) => {
        if (data.data_dict === "Not data Matched") {
          showProgress = false;
          datafound = "No Data Matched In Database";
        } else {
          callin = data.data_dict[0]["call_in"];
          tableData = data["data_dict"];
          final_result = tableData;
          filteredResults = [...final_result];
          console.log(filteredResults);
          gotResult = true;
          exportData = [
            [
              "source Number",
              "Destination Number",
              "nickname",
              "call Date",
              "call type",
              "imei",
              "cellid",
              "provider",
              "roaming",
              "address",
              "latitude",
              "longitude",
              "azimuth",
              "user address",
            ],
            ...final_result.map((item) => [
              item["source_number"],
              item["destination_number"],
              item["nickname"],
              item["calldate"],
             
              item["call_type"],
              item["imei"],
              item["cellid"],
              item["provider"],
              item["roaming"],
              item["address"],
              item["latitude"],
              item["longitude"],
              item["azimuth"],
              item["user_address"],
            ]),
          ];
        }
      });
  }
  hyper_callin();
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
  onMount(() => {
    // Prepare the data for export, including headers
    exportData = [["S.No", "D.No", "Nickname", "calldate"]];
    exportData = exportData.concat(
      app_data.map((item, index) => [
        item["source_number"],
        item["destination_number"],
        item["nickname"],
        item["calldate"],
      ])
    );
  });

 
</script>

{#if gotResult}
  <!-- Another table starts -->
  <div class="header">
    <h4 class="heading"
    >
      Call In of {number} from {dest_number}
    </h4>
    <button class="download-button" on:click={exportToXLSX}>Download</button>
  </div>
   
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 7%;">SOURCE NUMBER</th>
            <th style="width: 7%;">DESTINATION NUMBER</th>
            <th style="width: 5%;">nickname</th>
            <th style="width: 5%;">calldate</th>
            <th style="width: 5%;">call_type</th>
            <th style="width: 5%;">imei</th>
            <th style="width: 5%;">cellid</th>
            <th style="width: 5%;">provider</th>
            <th style="width: 5%;">roaming</th>
            <th style="width: 10%;">address</th>
            <th style="width: 5%;">latitude</th>
            <th style="width: 5%;">longitude</th>
            <th style="width: 5%;">azimuth</th>
            <th style="width: 10%;">user address</th>
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
                on:input={(event) => handleColumnSearch("call_type", event)}
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
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.source_number}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.destination_number}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.nickname}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.calldate}</td
              >
              <!-- <td>{item.calltime}</td> -->
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.call_type}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.imei}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.cellid}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.provider}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.roaming}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.address}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.latitude}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.longitude}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.azimuth}</td
              >
              <td style="max-width: 200px; word-wrap: break-word;"
                >{item.user_address}</td
              >
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  <!-- </div> -->
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

  .header{
    margin-top: 1vh;
    margin-left: 10vh
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
    background-color: black;
    border: 1px;
    color: rgb(118, 214, 57);
    height: 15px 10px;
    text-transform: uppercase;
  }
  tbody {
    width: 5%;
    word-break: break-word;
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    max-width: 200px;
    word-wrap: break-word;
  }
  .table-container {
    max-height: 90vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    margin-top: 6vh;
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
    word-break: break-word;
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
  .download-button {
    background-color: #3498db;
    /* padding: 8px 15px; */
    color: white;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    /* margin: 4px 2px; */
    transition-duration: 0.4s;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    width: 5%;
    /* position: absolute;
            right: 20px; */
    border-radius: 45%;
  }
</style>
