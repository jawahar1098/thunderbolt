<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
  import Roaming from "./roaming_data.svelte";
  import Location from "./location_data.svelte";
  import { postRequest } from "$lib/req_utils";

  export let propData;
  console.log("Propdataaaaaaaaaaaaaaaaaa", propData);
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let data = {};
  let data1 = {};
  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";
  let final_result = [];
  let final_result1 = [];
  let tableData;
  let tableHeader;
  let formattedData;
  let datad;

  const rows = [];
  const rowSize = 5;

  let columnFilters = {};
  let filteredResults = [];
  const dispatch = createEventDispatcher();

  function cdr_analysis() {
    gotResult = false;
    showProgress = true;
    console.log("cdr number", number);
    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "profile");
    profile_num.append("startDate", startDate);
    profile_num.append("endDate", endDate);

    // try {
    //   // console.log(contacts_of_mobileNumber,"datas sent tobackend");
    //   const response = await fetch(`${basepath()}/profile_num`, {
    //     method: "POST",
    //     body: profile_num,
    //   });
    const url = `${basepath()}/profile_num`;
    postRequest(fetch,url,profile_num)
    .then(data => {

        console.log(data);
        if (data.data_dict === "No data Matched") {
          showProgress = false;
          datafound = "No Data Matched In Database";
          console.log(datafound, "-----------------");
        } else {
          gotResult = true;
          showProgress = false;
          final_result = data.data_dict;
        }
        showProgress = false;
      } )
  }

  afterUpdate(() => {
    console.log("updated---------,", propData);
    if (number != propData.number) {
      return;
    } else {
      cdr_analysis();
      number = "";
    }
  });
</script>

<div class="main_container">
  {#if gotResult}
    <div class="cdr_container">
      {#each final_result as item}
        <div class="info__container">
          <!-- <div class="contentx"> -->
          <div class="content_info">
            <p class="content__heading">Number</p>
            <p class="content__detail">
              {item["source_number"]}
            </p>
          </div>
          <div class="content_info">
            <p class="content__heading">nickname</p>
            <p class="content__detail">{item["nickname"]}</p>
          </div>
          <div class="content_info">
            <p class="content__heading">Start Date</p>
            <p class="content__detail" id="call_start_date">
              {item["start_date"]}
            </p>
          </div>
          <div class="content_info">
            <p class="content__heading">End Date</p>
            <p class="content__detail" id="call_end_date">{item["end_date"]}</p>
          </div>

          <div class="content_info">
            <p class="content__heading">provider</p>
            <p class="content__detail">{item["total_provider"]}</p>
          </div>
          <div class="content_info" style="height: 13vh;">
            <p class="content__heading">Local Address</p>
            <p
              class="content__detail"
              id="blur"
              style="height: 6em; overflow: scroll;"
            >
              {item["local_address"]}
            </p>
          </div>
          <div class="content_info" style="height: 13vh;">
            <p class="content__heading">Permanant Address</p>
            <p
              class="content__detail"
              id="address"
              style="height: 6em; overflow: scroll;"
            >
              {item["permanent_address"]}
            </p>
          </div>
        </div>

        <!-- </div> -->
      {/each}
    </div>
  {:else if showProgress}
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  {:else}
    <div class="no_data">
      <img src="/nodata.png" alt="" />
      <p class="nodata">No data Found!!!!!!!!</p>
    </div>
  {/if}
  <div class="mainParent">
    <div>
      <div class="heading" id="header01">CDR DETAILS</div>
      {#each final_result as item}
        <div id="content01" class="content">
          <div class="data_info">
            <p class="header">incoming calls</p>
            <p class="details" id="address">{item["incoming_calls"]}</p>
          </div>
          <div class="data_info">
            <p class="header">outgoing calls</p>
            <p class="details" id="address">{item["outgoing_calls"]}</p>
          </div>
          <div class="data_info">
            <p class="header">total present dates</p>
            <p class="details">{item["total_present_dates"]}</p>
          </div>
          <div class="data_info">
            <p class="header">only sms</p>
            <p class="details" id="address">{item["only_sms"]}</p>
          </div>
          <div class="data_info">
            <p class="header">one to one calls</p>
            <p class="details" id="address">{item["one_to_one_call"]}</p>
          </div>
          <div class="data_info">
            <p class="header">transaction calls</p>
            <p class="details" id="address">{item["no_transaction_calls"]}</p>
          </div>
          <div class="data_info">
            <p class="header">silent days</p>
            <p class="details" id="address">{item["silent_days_count"]}</p>
          </div>
          <div class="data_info">
            <p class="header">total duration</p>
            <p class="details" id="address">{item["total_duration"]}</p>
          </div>
          <div class="data_info">
            <p class="header">roaming state</p>
            <!-- <p class="details" id="address">{item["roaming_state"]}</p> -->
            <div class="grid-container">
              <table style="border-collapse: separate;">
                <tbody>
                  {#each Array(Math.ceil(item["roaming_state"].length / 3)) as _, row}
                    <tr>
                      {#each Array(3) as _, col}
                        {#if item["roaming_state"][row * 3 + col]}
                          <td>{item["roaming_state"][row * 3 + col]}</td>
                        {/if}
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>

          <div class="data_info">
            <p class="header">imei</p>
            <div class="grid-container">
              <table style="border-collapse: separate;">
                <tbody>
                  {#each Array(Math.ceil(item["total_imei"].length / 3)) as _, row}
                    <tr>
                      {#each Array(3) as _, col}
                        {#if item["total_imei"][row * 3 + col]}
                          <td>{item["total_imei"][row * 3 + col]}</td>
                        {/if}
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
          <div class="data_info">
            <p class="header">cdat count </p>
            <!-- <p class="details" id="address">{item["cdat_count"]}</p> -->
            <div class="grid-container">
              <p>Total Count : {item["cdat_count"].length}</p>
              <table style="border-collapse: separate;">
                <tbody>
                  {#each Array(Math.ceil(item["cdat_count"].length / 4)) as _, row}
                    <tr>
                      {#each Array(4) as _, col}
                        {#if item["cdat_count"][row * 4 + col]}
                          <td>{item["cdat_count"][row * 4 + col]}</td>
                        {/if}
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
          <div class="data_info">
            <p class="header">total calls</p>
            <!-- <p class="details" id="address">
              {item["unique_destination_number_count"]}
            </p> -->
            <div class="grid-container">
              <table style="border-collapse: separate;">
                <tbody>
                  {#each Array(Math.ceil(item["unique_destination_number_count"].length / 4)) as _, row}
                    <tr>
                      {#each Array(4) as _, col}
                        {#if item["unique_destination_number_count"][row * 4 + col]}
                          <td
                            >{item["unique_destination_number_count"][
                              row * 4 + col
                            ]}</td
                          >
                        {/if}
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      {/each}
    </div>
    <div>
      <div class="heading" id="header02">LOCATION DETAILS</div>
      <div id="content02" class="content"><Location {propData} /></div>
    </div>
    <div>
      <div class="heading" id="header03">ROAMING DETAILS</div>
      <div id="content03" class="content"><Roaming {propData} /></div>
    </div>
  </div>
</div>

<style>
  .main_container {
    width: 100%;
    display: flex;
    flex-direction: row;
    padding: 0;
    height: 100vh;
    margin: 0.5em;
    background-color: #f3f5f78f;
  }
  .cdr_container {
    width: 23%;
    border: 1px solid #f3f5f75e;
    /* overflow: scroll;
    overflow-x: auto;
    overflow-y: auto; */
    background-color: white;
    border-radius: 12px;

    height: 79vh;
  }
  .data_info {
    display: flex;
    word-break: break-all;
    justify-content: center;
    align-items: center;
    padding-left: 10px;
    padding-right: 10px;
    /* width: 50%; */
    /* margin: -2px; */
  }
  .cdr_data {
    height: 78vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .details {
    width: 24vw;
    display: flex;
    justify-content: end;
  }
  .header {
    text-transform: uppercase;
    color: #296b97;
    word-break: break-word;
    width: 10vw;
  }
  .mainParent {
    height: 79vh;
    width: 70%;
    /* background: #f3f5f78f; */
    /* color: #949292; */
    overflow-y: scroll;
    border: 1px solid #f3f5f78f;
    margin-left: 4px;
    background-color: white;
    /* border-radius: 12px; */
  }

  .heading {
    position: sticky;
    padding: 0.5em;
    background-color: #5cb2eb;
    color: white;
    text-align: center;
    z-index: 2;
  }
  #header01 {
    top: 0;
  }
  #header02 {
    top: 0;
  }
  #header03 {
    top: 0;
  }

  .content {
    top: 0;
    height: 74vh;
  }
  .content {
    position: relative; /* Ensure content is positioned relatively */
    z-index: 1; /* Ensure content appears above the map */
  }
  #content01 {
    display: flex;
    flex-wrap: wrap;
    padding: 10px;
    width: 100%;
  }
  #content01 .data_info {
    display: flex;
    word-break: break-all;
    /* justify-content: space-between; */
    align-items: flex-start;
    padding-left: 10px;
    padding-right: 10px;
    width: 50%;
  }
  #content01 .data_info .header {
    width: 12vw;
    text-transform: uppercase;
    color: #296b97;
  }
  #content01 .data_info .details {
    width: 24vw;
  }
  #content01 .data_info .grid-container {
    max-height: 200px;
    overflow-y: auto;
    width: 24vw;
  }
  #content01 .data_info .grid-container table {
    width: 100%;
  }
  #content01 .data_info .grid-container table tbody tr td {
    background: #d4ebf7;
    border-collapse: separate;
  }
  .info__container {
    width: 99%;
    height: 70%;
    margin: 1vh;
  }

  .content_info {
    top: 0;
    display: flex;
    position: relative;
    padding: 1em;
    width: 27em;
    height: 6em;
    flex-direction: column;
    justify-content: center;
    padding: 5px;
  }

  .content__heading {
    /* color: #d54544; */
    color: #296b97;
    margin-bottom: 0px;
    text-transform: capitalize;
  }
  .content__detail {
    color: black;
    width: 21vw;
    border: 1px solid #d4ebf7;
    padding-top: 2vh;
    /* padding-right: 2vh; */
    padding-bottom: 2vh;
    /* padding-left: 4vh; */
    display: flex;
    justify-content: center;
  }
</style>
