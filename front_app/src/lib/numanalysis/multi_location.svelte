<script>
  // @ts-nocheck

  import { onMount } from "svelte";

  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";

  export let propData;
  console.log("Propdataaaaaaaaaaaaaaaaaa", propData);
  $: number = propData.number;
  // $: startDate = propData.startdate;
  // $: endDate = propData.enddate;
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

  async function common_meeting_points() {
    const common_meeting_points = new FormData();
    common_meeting_points.append("number", number);
    common_meeting_points.append("mode", "meeting_point");
    common_meeting_points.append("fromdate", startDate);
    common_meeting_points.append("todate", endDate);
    common_meeting_points.append("page", currentPage);
    common_meeting_points.append("items_per_page", itemsPerPage);
    showProgress = true;
    try {
      const response = await fetch(`${basepath()}/analysis`, {
        method: "POST",
        body: common_meeting_points,
      });

      if (response.ok) {
        data = await response.json();
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
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }
  afterUpdate(() => {
    console.log("updated---------,", propData);
    if (number != propData.number) {
      return;
    } else {
        common_meeting_points();
      number = "";
    }
  });
  function got_to_page(pagenum) {
    currentPage = pagenum;
    common_meeting_points();
  }
</script>

<div class="common_container">
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
    /* margin-top: 55px; */
    height: 59vh;
    width: 100%;
  }
 
 
 
  table {
    width: 94.5%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    /* margin-left: 5%; */
  }
 

  .sub-table:hover {
    background-color: rgb(254 226 226);
  }

  .sub:hover {
    background-color: rgb(219 234 254);
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
    height: 5vh;
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
</style>
