<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
    import { postRequest } from "$lib/req_utils";
  import { sum } from "d3";
  import {afterUpdate} from "svelte";


  export let propData;
  $: number = propData.number
  let summary_of_app; 
  let summary_of_vpn; 
  let summary_of_iptype; 
  let summary_of_country; 
  let showdata = [];

  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";

  function profile_num() {
    gotResult = false;
    showProgress = true;
    console.log("ipdr number", number);

    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "ipdrprofile");
    showProgress = true;
    const url = `${basepath()}/profile_num`
    postRequest(fetch, url, profile_num)
      .then((data) => {
        console.log(data,"ipdr");
        if (data.summary === "no data") {
          gotResult = false;
          showProgress = false;
          datafound = "No Data Matched In Database";
          console.log(datafound,"-----------------")
        }
        else{
          showdata = []
          gotResult = true;
          showdata.push(data);
          summary_of_vpn = data.summary_vpn;

        }
        
        })
      

      .catch((err) => {
        console.log(err);
      });
  }

  afterUpdate(()=> {
    if(number != propData.number){
    return
    }
    else{
      profile_num()
      gotResult = false
      number =""
    }
  })
 
</script>

<main>
  <!-- <h1>IPDR</h1> -->
  {#if gotResult}
  <div>
    <h1 class="header">IPDR Profile</h1>
    <div class="ipdrpro flex">
          {#each showdata as item}
          <div class="count_details">
            <label for="" class="font-bold">Device Used</label>
            <p>{item.device.length}</p>
          </div>

          <div class=" w-1/1">
            <div class="count_details">
                <label for="" class="font-bold">VPN Used</label>
            
              <p class="font-bold">
                {item.allvpn.length}
              </p>
            </div>
          </div>

          <div class="count_details">
            <label for="" class="font-bold">Apps used</label>
            <p>{item.app.length}</p>
          </div>
          <div class="count_details">
            <label for="" class="font-bold">Country Visited</label>
            <p>{item.country.length}</p>

            
          </div>
          <div class="count_details">
            <label for="" class="font-bold">Foreign Isp</label>
            <p>{item.foreign_isp.length}</p>
            
          </div>
          <div class="count_details">
            <label for="" class="font-bold">Indian Isp</label>
            <p>{item.isp_india.length}</p>
            
          </div>
          {/each}
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
    <p class="nodata">No data Found in IPDR PROFILE!!!!!!!!</p>
  </div>
  {/if}
</main>

<style>
  main {
    width: 100%;
  }
  .header {
    background-color: #3498db;
    color: #fff;
    padding: 5px;
    display: flex;
    width: 99%;
    justify-content: center;
    height: 6vh;
  }
  .count_details {
    display: flex;
    justify-content: space-between;
    margin: 1rem;
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

  .container {
    color: red;
  }
</style>
