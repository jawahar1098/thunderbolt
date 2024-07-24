<script>
  
    import { onMount } from 'svelte';
    import {basepath} from "$lib/config"
        let dashboard_data = [];
        let cdr = [];
        let sdr = [];
        let suspect = [];
        let cellid = [];
        let phonearea = [];
    
        function dashboard(){
            
                fetch(basepath()+'/dashboard_data',{
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(datas => {
                  console.log(datas)
                    dashboard_data = datas.data
                    cdr = dashboard_data.last_updated_cdr
                    sdr = dashboard_data.last_updated_sdr
                    suspect = dashboard_data.last_updated_suspect
                    cellid = dashboard_data.last_updated_cellid
                    phonearea=dashboard_data.last_updated_phone_area
                })
                .catch((err)=>{
                  console.log(err)
                })
        }
     onMount(()=>{
        dashboard()
     }
     )
  </script>
  
  <main>
        <div class="container">
            <div class="card l-bg-cherry" style="margin-top: 20px;">
              <h3 style="margin-top: 25px;">Total Count Cdr</h3>
              <p style="font-size: large;"><b>{dashboard_data.total_unique_source_count_cdr}</b></p>
                <div class="card-statistic-3 p-4">
                    <div class="card-icon card-icon-large"><i class="bi bi-telephone-forward-fill"></i></div>
                </div>
            </div>
  
  
          <div class="card l-bg-green-dark" style="margin-top: 20px;">
              <h3 style="margin-top: 35px;">Imei Count Cdr</h3>
              <p style="font-size: large;"><b>{dashboard_data.imei_count_cdr}</b></p>
          <div class="card-statistic-3 p-4">
              <div class="card-icon card-icon-large"><i class="bi bi-device-ssd-fill"></i></div>
          </div>
        </div>
  
  
        <div class="card l-bg-orange-dark" style="margin-top: 20px;">
          <h3 style="margin-top: 25px;">Last Update Cdr</h3>
          <p style="font-size:large"><b>{cdr.latest_as_on_date}</b></p>
          <div class="card-statistic-3 p-4">
              <div class="card-icon card-icon-large"><i class="bi bi-activity"></i></div>
          </div>
        </div>
        <div class="card l-bg-cherry-2" style="margin-top: 20px;">
          <h3 style="margin-top: 25px;">Total Count Phonearea</h3>
          <p style="font-size:large"><b>{dashboard_data.total_unique_source_count_phonearea}</b></p>
          <div class="card-statistic-3 p-4">
           <div class="card-icon card-icon-large"><i class="bi bi-phone-vibrate-fill"></i></div>
         </div>
        </div>
  
  
    </div>
  
  <div style="margin-right: 90px; margin-top:130px" class="container">
      <div class="row">
          <div class="col-md-3 col-sm-6">
              <div class="counter">
                  <div class="counter-icon">
                      <i class="bi bi-tablet-fill"></i>
                  </div>
                  <span class="counter-value">{dashboard_data.total_unique_source_count_sdr}</span>
                  <h2>Total Source Count SDR</h2>
              </div>
          </div>
          <div class="col-md-3 col-sm-6">
              <div class="counter blue">
                  <div class="counter-icon">
                      <i class="bi bi-database-fill"></i>
                  </div>
                  <span class="counter-value">{sdr.latest_as_on_date}</span>
                  <h2>Last Updated Sdr</h2>
              </div>
          </div>
          <div class="col-md-3 col-sm-6">
              <div class="counter ">
                  <div class="counter-icon">
                      <i class="bi bi-clipboard2-data-fill"></i>
                  </div>
                  <span class="counter-value">{suspect.latest_as_on_date}</span>
                  <h2>Last Updated suspect</h2>
              </div>
          </div>
          <div class="col-md-3 col-sm-6">
              <div class="counter blue">
                  <div class="counter-icon">
                      <i class="bi bi-pie-chart-fill"></i>
                  </div>
                  <span class="counter-value">{cellid.latest_as_on_date}</span>
                  <h2>Last Updated CellId</h2>
              </div>
          </div>
      </div>
  </div>
  
  
  
  </main>
  
<style>
     .container{
      
      display: flex;
      margin-left: 400px;
      margin-top: 20px;
  
  }
  
  .card .card-statistic-3 .card-icon-large .bi, .card .card-statistic-3 .card-icon-large .bi, .card .card-statistic-3 .card-icon-large .bi, .card .card-statistic-3 .card-icon-large .bi {
     font-size: 50px;
     margin-right: 12px;
     margin-top: -initial ;
     height: 300px;
     overflow: hidden;
     
  }
  
  .card .card-statistic-3 .card-icon {
     text-align: center;
     line-height: 50px;
     margin-left: 15px;
     color: #000;
     position: absolute;
     right: -5px;
     top: 50px;
     opacity: 0.1;
  }
  
  
  .l-bg-cherry {
     background: linear-gradient(to right, #c899b6, rgb(235, 211, 225)) ;
     color: #fff;
     height: 150px;
     width: 250px;
     border-radius: 20px;
    
  }
  .l-bg-green-dark {
     background: linear-gradient(to right, #82ccc5, #92cea9) ;
     color: #fff;
     height: 150px;
     margin-left: 20px;
     width: 250px;
     border-radius: 20px;
  }
  
  .l-bg-orange-dark {
     background: linear-gradient(to right, #bf8698, #db627c) ;
     color: #fff;
     height: 150px;
     margin-left: 20px;
     width: 250px;border-radius: 20px;
  
  }
  
  .l-bg-cherry-2 {
     background: linear-gradient(to right, #d2aedc, rgb(222, 170, 170));
     color: #fff;
     height: 150px;
     width: 250px;
     margin-left: 20px;border-radius: 20px;
  }
  
  h3 {
      text-align: center ;
      color:black;
      font-size: 25px;
      font-family: 'Algerian';
  }
  
  p{
      text-align: center;
  }
  
  .container{
      margin-top: 20px;
      
  }
  
  .counter{
      color: #f27f21;
      font-family: 'Open Sans', sans-serif;
      text-align: center;
      height: 250px;
      width: 250px;
      padding: 30px 25px 25px;
      margin: 0 auto;
      border: 3px solid #f27f21;
      border-radius: 20px 20px;
      position: relative;
      z-index: 1;
      margin-right: 20px;
  }
  .counter:before,
  .counter:after{
      content: "";
      background: #f3f3f3;
      border-radius: 20px;
      box-shadow: 4px 4px 2px rgba(0,0,0,0.2);
      position: absolute;
      left: 15px;
      top: 15px;
      bottom: 15px;
      right: 15px;
      z-index: -1;
  }
  .counter:after{
      background: transparent;
      width: 100px;
      height: 100px;
      border: 15px solid #f27f21;
      border-top: none;
      border-right: none;
      border-radius: 0 0 0 20px;
      box-shadow: none;
      top: auto;
      left: -10px;
      bottom: -10px;
      right: auto;
  }
  .counter .counter-icon{
      font-size: 35px;
      line-height: 35px;
      margin: 0 0 15px;
      transition: all 0.3s ease 0s;
  }
  .counter:hover .counter-icon{ transform: rotateY(360deg); }
  .counter .counter-value{
      color: #555;
      font-size: 15px;
      font-weight: 600;
      line-height: 20px;
      margin: 0 0 20px;
      display: block;
      transition: all 0.3s ease 0s;
  }
  .counter:hover .counter-value{ text-shadow: 2px 2px 0 #d1d8e0; }
  .counter h2{
      font-size: 17px;
      font-weight: 700;
      text-transform: uppercase;
      margin: 0 0 15px;
  }
  .counter.blue{
      color: #4accdb;
      border-color: #4accdb;
  }
  .counter.blue:after{
      border-bottom-color: #4accdb;
      border-left-color: #4accdb;
  }


  @media screen and (max-width:990px){
      .counter{ margin-bottom: 40px; }
  }
</style>





































<!-- <script>
    import { onMount } from 'svelte';
    import { basepath } from '$lib/config';
  
    let dashboardData = null;
  
    onMount(async () => {
      fetch(`${basepath()}/dashboard_data`)
      .then(response =>response.json())
      .then(data => {
        console.log(data)
          dashboardData = data.data;
        });
    })

    function displayValue(value) {
        if (value && typeof value === 'object' && !Array.isArray(value)) {
        let formattedValues = [];
        for (const [key, val] of Object.entries(value)) {
            formattedValues.push(`${key.replace(/_/g, ' ')} = ${val}`);
        }
        return formattedValues.join('<br>');
        }
        return value;
    }
</script>
  
<main class="container">
    <h1 style="font-family: bold">CDAT DASHBOARD</h1>
    {#if dashboardData}
    <div class="container1">
        <div class="col-md-3 col-sm-6">
            <div class="counter orange">
                <div class="counter-icon">
                    <i class="bi bi-telephone-outbound-fill"></i>
                </div>
                <h5 class="title">IMEI Count CDR</h5>
                <span class="text">{dashboardData.imei_count_cdr}</span>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="counter green">
                <div class="counter-icon">
                    <i class="bi bi-telephone-outbound-fill"></i>
                </div>
                <h5 class="title">Total Source Count CDR</h5>
                <span class="text">{dashboardData.total_unique_source_count_cdr}</span>
            </div>
        </div>
        <br>
        <div class="col-md-3 col-sm-6">
            <div class="counter pink">
                <div class="counter-icon">
                    <i class="bi bi-telephone-outbound-fill"></i>  
                </div>
                <h5 class="title">Total Source Count SDR</h5>
                <span class="text">{dashboardData.total_unique_source_count_sdr}</span>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="counter gray">
                <div class="counter-icon">
                    <i class="bi bi-person-exclamation"></i>
                </div>
                <h5 class="card-title">Total Count(Phonearea)</h5>
                <p class="card-text">{displayValue(dashboardData.total_unique_source_count_phonearea)}</p>
            </div>
        </div>
    </div>

    <div class="container2">
        <div class="col-md-4 col-sm-6">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last Updated Sdr</h5>
                    <p class="card-text">{displayValue(dashboardData.last_updated_sdr)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last Updated suspect</h5>
                    <p class="card-text">{displayValue(dashboardData.last_updated_suspect)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Last Updated CellId</h5>
                    <p class="card-text">{displayValue(dashboardData.last_updated_cellid)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last Activation Dates by State Sdr</h5>
                    <p class="card-text">{displayValue(dashboardData.last_activation_dates_by_state_sdr)}</p>
                </div>
            </div>
        </div>
    </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Total Records</h5>
                    <p class="card-text">{@html displayValue(dashboardData.total_records_all_collections)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last updated Cdr</h5>
                    <p class="card-text">{displayValue(dashboardData.last_updatd_cdr)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last Updated Phonearea</h5>
                    <p class="card-text">{displayValue(dashboardData.last_updated_phone_area)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-6 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Last Activation Dates by State CellId</h5>
                    <p class="card-text">{@html displayValue(dashboardData.last_activation_dates_by_state_cellidchart)}</p>
                </div>
            </div>
        </div>
        <div class="col-lg-6 col-md-2 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">State Wise Cell-TowerId Counts</h5>
                    <p class="card-text">{@html displayValue(dashboardData.state_wise_cell_towerid_counts_cellidchart)}</p>
                </div>
            </div>
        </div>
    {:else}
    <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        </div>
    {/if}
</main>

<style>
    main {
        background-color: rgb(219, 215, 210);
        width: 100vw;
        height: 100vh;
        margin-left: 100px;
    }
    .counter{
        color: #eb3b5a;
        font-family: 'Muli', sans-serif;
        width: 200px;
        height: 200px;
        text-align: center;
        border-radius: 100%;
        padding: 77px 32px 40px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    .counter:before,
    .counter:after{
        content: "";
        background: #fff;
        width: 80%;
        height: 80%;
        border-radius: 100%;
        box-shadow: -5px 5px 5px rgba(0,0,0,0.3);
        transform: translateX(-50%)translateY(-50%);
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: -1;
    }
    .counter:after{
        background: linear-gradient(45deg,#B81242 49%, #D74A75 50%);
        width: 100%;
        height: 100%;
        box-shadow: none;
        transform: translate(0);
        top: 0;
        left: 0;
        z-index: -2;
        clip-path: polygon(50% 50%, 50% 0, 100% 0, 100% 100%, 0 100%, 0 50%);
    }
    .counter .counter-icon{
        color: #fff;
        background: linear-gradient(45deg,#B81242 49%, #D74A75 50%);
        font-size: 33px;
        line-height: 70px;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        position: absolute;
        top:  0;
        left: 0;
        z-index: 1;
        transition: all 0.3s;
    }
    .counter .counter-icon i.bi{
        transform: rotateX(0deg);
        transition: all 0.3s ease 0s;
    }
    .counter:hover .counter-icon i.bi{ transform: rotateX(360deg); }
    .counter h3{
        font-size: 17px;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0 0 3px;
    }
    .counter .counter-value{
        font-size: 30px;
        font-weight: 700;
    }
    .counter.orange{ color: #F38631; }
    .counter.orange:after,
    .counter.orange .counter-icon{
        background: linear-gradient(45deg,#F38631 49%,#F8A059 50%);
    }
    .counter.green{ color: #88BA1B; }
    .counter.green:after,
    .counter.green .counter-icon{
        background: linear-gradient(45deg,#88BA1B 49%,#ACD352 50%);
    }
    .counter.blue{ color: #5DB3E4; }
    .counter.blue:after,
    .counter.blue .counter-icon{
        background: linear-gradient(45deg,#5DB3E4 49%,#7EBEE1 50%);
    }
    @media screen and (max-width:990px){
        .counter{ margin-bottom: 40px; }
    }
</style>
  

<!-- <script>
    import { onMount } from 'svelte';
    import { basepath } from '$lib/config';

    let dashboardData = null;

    onMount(async () => {
      fetch(`${basepath()}/dashboard_data`)
      .then(response => response.json())
      .then(data => {
        dashboardData = data.data;
      });
    });

    function displayValue(value) {
      if (value && typeof value === 'object' && !Array.isArray(value)) {
        let formattedValues = [];
        for (const [key, val] of Object.entries(value)) {
          formattedValues.push(`${key.replace(/_/g, ' ')} = ${val}`);
        }
        return formattedValues.join('<br>');
      }
      return value;
    }
</script>

<style>
  .card-body {
    max-height: 300px;
    overflow-y: scroll;
  }
</style>

<main class="container my-3">
  <h1 style="text-align: center;">CDAT DASHBOARD</h1>
  {#if dashboardData}
    <div class="row" style="margin-top: 10px;">
      {#each Object.entries(dashboardData) as [key, value]}
        <div class="col-lg-4 col-md-6 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{key.replace(/_/g, ' ')}</h5>
              <p class="card-text">{@html displayValue(value)}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {/if}
</main> -->

 -->
