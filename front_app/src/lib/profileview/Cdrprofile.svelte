<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
    import { postRequest } from "$lib/req_utils";
  import { afterUpdate } from "svelte";

  let data;
  export let propData;
  $: number = propData.number;

  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";
  let showdata;

  function profile_num() {
    gotResult = false;
    console.log("cdr number", number);
    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "profile");
    showProgress = true;
    const url = `${basepath()}/profile_num`
    postRequest(fetch,url,profile_num)
      .then((data) => {
        console.log(data,"--------------------S");
        if (data.data_dict === "No data Matched") {
          // gotResult = false;
          showProgress = false;
          datafound = "No Data Matched In Database";
          console.log(datafound,"-----------------")
        } else {
          gotResult = true;
          showProgress = false;
          showdata = data.data_dict;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }

  afterUpdate(() => {
    console.log("updated---------,", propData);
    if (number != propData.number) {
      return;
    } else {
      profile_num();
      number = "";
    }
  });
</script>

<main>
  <!-- <h1>CDR</h1> -->
  {#if gotResult}
    <div class="cdrpro">
      <h1 class="header">CDR Profile</h1>
      {#each showdata as item}
        <div class="info-item">
          <div class="info">
            <label >Number</label>
            <p class="date_start " id="blur">
              {item["source_number"]}
            </p>
          </div>
          <div class="info">
            <label>Total Contacts</label>
            <p class="date_start" id="call_start_date">
              {item["unique_destination_number_count"].length}
            </p>
          </div>
          <div class="info">
            <label>Cdat Contact</label>
            <p class="date_start" id="call_start_date">
              
              {item["cdat_count"].length}
            </p>
          </div>
          <div class="info">
            <label>Other State</label>
            <p class="date_start" id="call_start_date">
              {item["roaming_state"].length}
            </p>
          </div>

          <div class="info">
            <label>Call Start Date</label>
            <p class="date_start" id="call_start_date">{item["start_date"]}</p>
          </div>

          <div class="info">
            <label>Call End Date</label>
            <p class="date_start" id="call_end_date">{item["end_date"]}</p>
          </div>
          <div class="info">
            <label>total_present_dates</label>
            <p id="address">{item["total_present_dates"]}</p>
          </div>
          <div class="info">
            <label>silent_days_count</label>
            <p id="address">{item["silent_days_count"]}</p>
          </div>
          <div class="info">
            <label>nickname</label>
            <p class="items" id="blur">{item["nickname"]}</p>
          </div>
          <div class="info">
            <label>provider</label>
            <p id="address">{item["total_provider"]}</p>
          </div>
          <div class="info">
            <label>incoming calls</label>
            <p id="address">{item["incoming_calls"]}</p>
          </div>
          <div class="info">
            <label>outgoing calls</label>
            <p id="address">{item["outgoing_calls"]}</p>
          </div>
          <div class="info">
            <label>sms count</label>
            <p id="address">{item["only_sms"]}</p>
          </div>
          <div class="info">
            <label>transaction calls</label>
            <p id="address">{item["no_transaction_calls"]}</p>
          </div>
          <div class="info">
            <label>one to one call</label>
            <p id="address">{item["one_to_one_call"]}</p>
          </div>
          <div class="info">
            <label>Local Address</label>
            <p class="items" id="blur">{item["local_address"]}</p>
          </div>
          <!-- <div class="info">
          <label>Permanant Address</label>
          <p class="items" id="address">{item['permanent_address']}</p>
        </div> -->
        </div>
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
</main>

<style>
  main {
    /* margin-left: 5%; */
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .cdrpro {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    /* justify-content: center; */

    /* margin: 5%; Full width */
  }
  /* #blur{
    filter: blur(4px);
  } */
  .header {
    background-color: #3498db;
    color: #fff;
    padding: 5px;
    display: flex;
    width: 99%;
    justify-content: center;
    height: 6vh;
  }

  .info-item {
    padding: 0rem;
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  /* .font-bold{
    background-color: #3498db;
  } */
  .info {
    display: flex;
    justify-content: space-between;
    font-size: 1em;
  }

  .date_start {
    width: 5.2vw;
    word-break: break-word;
    /* color: #3498db */
  }

  .items {
    margin-left: 12px;
    /* width: 20.2vw; */
    word-break: break-word;
    color: #3498db;
    width: 6vw;
  }
  a {
    color: #3498db;
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

  .pagination {
    margin-top: 2%;
    margin-left: 5%;
  }

  /* Add more styling as needed */
</style>
