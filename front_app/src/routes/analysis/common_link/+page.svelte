<script>
  // @ts-nocheck

  import { onMount } from "svelte";

  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  let number = "";
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let data = {};
  let startDate;
  let endDate;
  let tableData;
  let tableHeader;
  let showProgress = false;
  let gotResult = false;
  let data_found = "Give your inputs";
  // let listnumber = number.split(",")

  function common_meeting_points() {
    const common_meeting_points = new FormData();
    common_meeting_points.append("number", number);
    common_meeting_points.append("mode", "meeting_point");
    common_meeting_points.append("fromdate", startDate);
    common_meeting_points.append("todate", endDate);
    common_meeting_points.append("page", currentPage);
    common_meeting_points.append("items_per_page", itemsPerPage);
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/analysis`, {
    //     method: "POST",
    //     body: common_meeting_points,
    //   });
  
    const url = `${basepath()}/analysis`;
    postRequest(fetch,url,common_meeting_points)
    .then(data => {

      // if (response.ok) {
      //   data = await response.json();
        console.log(data);
        tableData = data["data_dict"];
        if (tableData.length > 0) {
          showProgress = false;
          tableHeader = data["headers"];
          gotResult = true;
        } else {
          data_found =
            "There is no common meeting point for given source numbers";
          showProgress = false;
        }
        total_pages = data["totalpages"];
        page_count = total_pages / 10;
      } )
  }
  function got_to_page(pagenum) {
    currentPage = pagenum;
    common_meeting_points();
  }
</script>

<div class="common_container">
  <!-- {#if showProgress}
    <div class="absolute top-[50%] left-[50%] p-10">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {/if} -->

  <div class="input_container">
    <div class="input-row">
      <label for="" class="">CDR Common Visiting point </label>
      <input
        type="text"
        placeholder="Search Here"
        class="input-field"
        bind:value={number}
      />
      <label for="fromDate">From Date</label>
      <input
        class="date-input"
        id="fromDate"
        type="date"
        bind:value={startDate}
      />
      <label for="toDate">To Date:</label>
      <input class="date-input" id="toDate" type="date" bind:value={endDate} />
      <button class="submit" on:click={common_meeting_points}>Search</button>
    </div>
  </div>

  {#if gotResult}
    <div class="table_container">
      <div>
        <table>
          <thead>
            <tr>
              <th style="width: 5%;">Date</th>
              <th style="width: 5%;">State</th>
              <th style="width: 5%;">Location</th>
              <th style="width: 15%;">Source Number and Cellid</th>
            </tr>
          </thead>
          <tbody>
            {#each tableData as tbld}
              <tr>
                <td>{tbld["date"]}</td>
                <td>{tbld["state"]}</td>
                <td>{tbld["location"]}</td>
                <td style="padding: 0px;">
                  {#each tbld["entry"] as surce}
                    <tr class="sub-table">
                    <!-- class="border-b hover:bg-red-100 dark-border-neutral-500" -->
                      <td style="width: 18vw;">{surce["source_number"]}</td>
                      <td style="padding: 0px;">
                        {#each surce["cellid_data"] as sr}
                          <tr class="sub">
                            <td style="width:20vw;">{sr["cellid"]}</td>
                            <td style="padding: 0px;">
                              {#each sr["time"] as t}
                                <tr>
                                  <td style="width:10vw;">{t}</td>
                                </tr>
                              {/each}
                            </td>
                          </tr>
                        {/each}
                      </td>
                    </tr>
                  {/each}
                </td>
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
      <p class="nodata">{data_found}!!!!!!!!</p>
    </div>
  {/if}
</div>

<style>
  .common_container {
    /* margin-left: 4%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 55px;
    height: 92vh;
    width: 100%;
  }
  .input_container {
    background-color: #d4ebf7;
    padding: 10px;
    width: calc(100% - 40px);
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    border-radius: 8px;
    height: 7vh;
    justify-content: center;
    margin-left: 4%;
  }
  .input-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    /* width: 98%; */
  }

  label {
    color: #296b97;
  }

  .input-field {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 24vw;
  }
  .date-input {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 15vw;
  }

  table {
    width: 94.5%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 5%;
  }
  .submit {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 10vw;
    /* position: absolute;
            right: 20px;
            top: 20px */
  }

  .sub-table:hover{
    background-color: rgb(254 226 226);
  }

  .sub:hover{
    background-color: rgb(219 234 254);;
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
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table_container {
    max-height: 78vh;
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
