<!-- <h1>multiple_number_analysis</h1> -->
<script>
  // @ts-nocheck
  import CommonContacts from "./common_contacts.svelte";
  import Location from "./multi_location.svelte";
  import InternalCalling from "./internal_calling.svelte";
  import Handsets from "./common_number_analysis.svelte";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import { onMount } from "svelte";
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
  // const dispatch = createEventDispatcher();
  let activeTab = 0;
  const tabData = [
    { label: "profile" },
    { label: "common contacts" },
    { label: "location" },
    { label: "Internal calling" },
    { label: "Handsets" },
  ];
  function switchTab(index) {
    activeTab = index;
  }

  function cdr_analysis() {
    gotResult = false;
    showProgress = true;
    console.log("cdr number", number);
    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "analysis_profile");
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
          console.log(final_result, "///////////////////");
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
  <div class="nav">
    <div class="nav-tab">
      {#each tabData as tab, index (tab.label)}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
          class="tab"
          on:click={() => switchTab(index)}
          class:active={index === activeTab}
        >
          {tab.label}
        </div>
      {/each}
    </div>
  </div>
  <div class="body__container">
    {#if tabData[activeTab].label === "profile"}
      <p class="tab-heading">CDR Information</p>
      <div class="info">
        <!-- <div class="container"> -->
        {#each final_result as resultList}
          {#each resultList as item}
            <div class="info__container">
              <p class="detail">{item.source_number}'s cdr detail</p>
              <div class="content">
                <!-- <div class="content_info"> -->
                <!-- <p class="content__heading">Number</p> -->
                <!-- <p class="content__detail">{item.source_number}</p> -->
                <!-- </div> -->
                <div class="content_info">
                  <p class="content__heading">Nick Name</p>
                  <p class="content__detail">{item.nickname}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">Start Date</p>
                  <p class="content__detail">{item.start_date}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">End Date</p>
                  <p class="content__detail">{item["end_date"]}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">Provider</p>
                  <p class="content__detail">{item["total_provider"]}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">incoming calls</p>
                  <p class="content__detail" id="address">
                    {item["incoming_calls"]}
                  </p>
                </div>
                <div class="content_info">
                  <p class="content__heading">outgoing calls</p>
                  <p class="content__detail" id="address">
                    {item["outgoing_calls"]}
                  </p>
                </div>
                <div class="content_info">
                  <p class="content__heading">total present dates</p>
                  <p class="content__detail">{item["total_present_dates"]}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">only sms</p>
                  <p class="content__detail" id="address">{item["only_sms"]}</p>
                </div>
                <div class="content_info">
                  <p class="content__heading">one to one calls</p>
                  <p class="content__detail" id="address">
                    {item["one_to_one_call"]}
                  </p>
                </div>
                <div class="content_info">
                  <p class="content__heading">transaction calls</p>
                  <p class="content__detail" id="address">
                    {item["no_transaction_calls"]}
                  </p>
                </div>
                <div class="content_info">
                  <p class="content__heading">silent days</p>
                  <p class="content__detail" id="address">
                    {item["silent_days_count"]}
                  </p>
                </div>
                <div class="content_info">
                  <p class="content__heading">total duration</p>
                  <p class="content__detail" id="address">
                    {item["total_duration"]}
                  </p>
                </div>
                <div
                  class="content_info"
                  style="width: 45vw;
                height: 13vh;"
                >
                  <p class="content__heading">Local Address</p>
                  <p class="content__detail" style="width: auto;">
                    {item["local_address"]}
                  </p>
                </div>
                <div
                  class="content_info"
                  style="width: 45vw;
                height: 13vh;"
                >
                  <p class="content__heading">Permanent Address</p>
                  <p class="content__detail" style="width: auto;">
                    {item["permanent_address"]}
                  </p>
                </div>

                <div class="content_info" style=" height: 13vh;">
                  <p class="content__heading">roaming state</p>
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

                <div class="content_info" style=" height: 13vh;">
                  <p class="content__heading">imei</p>
                  <div class="grid-container">
                    <table style="border-collapse: separate;">
                      <tbody>
                        {#each Array(Math.ceil(item["total_imei"].length / 2)) as _, row}
                          <tr>
                            {#each Array(2) as _, col}
                              {#if item["total_imei"][row * 2 + col]}
                                <td>{item["total_imei"][row * 2 + col]}</td>
                              {/if}
                            {/each}
                          </tr>
                        {/each}
                      </tbody>
                    </table>
                  </div>
                </div>
                <!-- <div class="content_info">
                <p class="header">cdat count</p>
                <div class="grid-container">
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
              </div> -->
                <div class="content_info" style="height: 22vh; width:45vw;">
                  <p class="content__heading">total calls</p>
                  <div class="grid-container" style="width: 43.5vw;">
                    <table style="border-collapse: separate;">
                      <tbody>
                        {#each Array(Math.ceil(item["unique_destination_number_count"].length / 8)) as _, row}
                          <tr>
                            {#each Array(8) as _, col}
                              {#if item["unique_destination_number_count"][row * 8 + col]}
                                <td
                                  >{item["unique_destination_number_count"][
                                    row * 8 + col
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
            </div>
          {/each}
        {/each}
        <!-- </div> -->
      </div>
    {/if}
    {#if tabData[activeTab].label === "common contacts"}
      <CommonContacts {propData} />
    {/if}
    {#if tabData[activeTab].label === "location"}
      <Location {propData} />
    {/if}
    {#if tabData[activeTab].label === "Internal calling"}
      <InternalCalling {propData} />
    {/if}
    {#if tabData[activeTab].label === "Handsets"}
      <Handsets {propData} />
    {/if}
  </div>
</div>

<style>
  .main_container {
    width: 100%;
    height: 95vh;
    margin-top: 5vh;
  }

  .nav {
    width: 93%;
    display: flex;
    justify-content: center;
  }
  .nav-tab {
    border: 1px solid#d4ebf7;
    display: flex;
    width: 50%;
    margin: 1%;
    background-color: white;
    color: #15abfc;
    height: 5vh;
  }
  .tab {
    cursor: pointer;
    display: flex;
    justify-content: center;
    border: 1px solid #d4ebf7;
    width: 100%;
    align-items: center;
  }
  .tab-heading {
    font-size: 2em;
    text-transform: initial;
    display: flex;
    justify-content: center;
    color: #d4ebf7;
  }
  .active {
    font-weight: bold;
    background-color: #15abfc;
    color: white;
  }
  .main_container .body__container {
    width: 100%;
    height: 79%;
    /* display: flex; */
    /* margin: 1.4vh; */
  }
  .info__container {
    width: 48%;
    /* height: 53vh; */
    margin: 1vh;
  }
  .content {
    display: flex;
    flex-wrap: wrap;
  }
  .content_info {
    top: 2rem;
    /* left: 27px; */
    display: flex;
    position: relative;
    padding: 1em;
    background-color: #ffffff;
    width: 27em;
    height: 6em;
    flex-direction: column;
    justify-content: center;
  }
  .info {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    height: 50vh;
    overflow-y: scroll;
  }

  .content__heading {
    color: #296b97;
    margin-bottom: 0px;
    text-transform: capitalize;
  }
  .content__detail {
    color: black;
    width: 21vw;
    border: 1px solid #d4ebf7;
    padding-top: 2vh;
    padding-right: 2vh;
    padding-bottom: 2vh;
    padding-left: 4vh;
  }
  .container {
    display: flex;
    overflow: scroll;
  }
  .grid-container {
    max-height: 200px;
    overflow-y: auto;
    width: 21vw;
  }
  .grid-container table {
    width: 100%;
  }
  .grid-container table tbody tr td {
    background: #d4ebf7;
    border-collapse: separate;
  }
  .detail {
    font-size: 20px;
    color: #296b97;
    margin-left: 14px;
    text-transform: capitalize;
    font-style: italic;
  }
</style>
