<script>
    // @ts-nocheck

    import { createEventDispatcher } from "svelte";
    import { basepath } from "$lib/config";
    import Bpartysummary from "$lib/towercdr/Bpartysummary.svelte";
    import { postRequest } from "$lib/req_utils";

    let results = [];
    let number;
    let filetype;
    let mode;
    let user;
    let rf_data;
    let rfid
    let showresult = false;
    let getdata = JSON.parse(localStorage.getItem('userDetails'))

    let formdata = new FormData()
    formdata.append('user', getdata['email'])
    postRequest(fetch,`${basepath()}/getnotifications`,formdata)
    .then(data => {
        console.log(data);
        results = data;
    });

    function updatedata(c_n, c_t, type, c_u,data,rf_id) {
        
            console.log("ins",data,rf_id);
            showresult = false;
            mode = type;
            number = c_n;
            filetype = c_t;
            user = c_u;
            rfid = rf_id
            if (mode === 'device'){

                rf_data = data[0].imei
            }
            if(mode === 'incoming'){
                rf_data = data
            }
            if (mode === 'bparty'){

            rf_data = data
            }
            if(mode === 'outgoing'){
                rf_data = data
            }
            if(mode === 'only_sms'){
                rf_data = data
            }
            if(mode === 'vpn'){
                rf_data = data
            }
            if(mode === 'foreign_isp'){
                rf_data = data
            }
            if(mode === 'shared_device'){
                rf_data = data
            }
            if(mode === 'silent_days'){
                rf_data = data
            }
            updateseenstat(rf_id)
            console.log(number, filetype, user,mode);
            console.log(rf_data)
            // document.getElementById("my_modal_4").setAttribute("open", true);
            showresult = true;
        
    }
    function updateseenstat(rf_id){
        const formdata = new FormData()
        formdata.append('rfid',rf_id)
        formdata.append('user',getdata['email'])
        postRequest(fetch,`${basepath()}/updateseen`,formdata)

    }
    
    
</script>
<main>

  

    <div class="row">
      
        <!-- <div class=" notify col-4  my-5 ">
            {#each results as result}
            <div class="card mb-4">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        {#if result.seen === "0"}
                        <div
                        class="position-absolute top-0 end-0 p-2 bg-danger text-white rounded-start"
                        >
                        <button
                        on:click={() => { 
                            updatedata(
                                        result.number,
                                        result.filetype,
                                        result.redflagtype,
                                        result.user,
                                        result.data,
                                        result.rfid
                                        );
                                    }}
                                
                                class="redflagbutton bg-danger text-white rounded-start"
                                >
                                View Data</button
                                >
                            </div>
                        {:else}
                        <div
                        class="position-absolute top-0 end-0 p-2 bg-success text-white rounded-start"
                        >
                        <button
                        on:click={() => { 
                            updatedata(
                                        result.number,
                                        result.filetype,
                                        result.redflagtype,
                                        result.user,
                                        result.data,
                                        result.rfid
                                        );
                                    }}
                                
                                class="redflagbutton bg-success text-white rounded-start"
                                >
                                View Data</button
                                >
                            </div>
                        {/if}
                            {#if result.redflagtype === "bparty"}
                            <img
                            src="/bparty.png"
                            alt="not found"
                            class="rounded-circle me-4"
                            />
                            {:else if result.redflagtype === "Tower Track"}
                            <img
                            src="/towercon.jpeg"
                            alt="not found"
                            class="rounded-circle me-4"
                            />
                            {/if}
                            <div class="flex-grow-1">
                                <p class="text-dark">
                                    <span class="fw-bold">number:</span>
                                    {result.number}
                                </p>
                                <p class="text-dark">
                                    <span class="fw-bold">filetype:</span>
                                    {result.filetype}
                                </p>
                                <p class="text-dark">
                                    <span class="fw-bold">red flag:</span>
                                    {result.redflagtype}
                                </p>
                            <p class="text-secondary">{result.description}</p>
                        </div>
                        <div class="position-absolute bottom-0 end-0 p-2 bg-light">
                            Date: {result.timestamp} 
                        </div>
                    </div>
                </div>
            </div>
            {/each}
        </div> -->

        <div class="accordion" id="accordionExample">
            {#each results as result, i}
            <div class="accordion-item">
            {#if result.seen === '0'}
                <h2 class="accordion-header" id="headingOne">
                  <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne{i}" aria-expanded="true" aria-controls="collapseOne{i}" 
                          style="color: red; background-color: #e7f1ff; box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.125);"
                          on:click={() => { 
                            updatedata(
                              result.number,
                              result.filetype,
                              result.redflagtype,
                              result.user,
                              result.data,
                              result.rfid
                            );
                          }}>
                     <p><strong class="acc-name"> redflag : {result.redflagtype} </strong> {result.redflagtype} redflag found in {result.number} type {result.filetype} in {result.timestamp} </p>
                  </button>
                </h2>
              {:else}
                <h2 class="accordion-header" id="headingOne">
                  <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne{i}" aria-expanded="true" aria-controls="collapseOne{i}" 
                          style="color: green; background-color: #e7f1ff; box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.125);"
                          on:click={() => { 
                            updatedata(
                              result.number,
                              result.filetype,
                              result.redflagtype,
                              result.user,
                              result.data,
                              result.rfid
                            );
                          }}>
                    <p> <strong class="acc-name"> redflag : {result.redflagtype} </strong>  {result.redflagtype} found in {result.number} type {result.filetype} in {result.timestamp}  </p>
                  </button>
                </h2>
            {/if}
              
              <div id="collapseOne{i}" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                    <div class="d-flex align-items-center">
                        <div class="col-8 container">
                            {#if showresult && mode === "bparty"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">B Party</h3>
                                        <table>
                                            <thead>
                                                <th>Destination Number</th>
                                                <th>Incoming Count</th>
                                                <th>Outgoing Count</th>
                                                <th>Total calls</th>
                                                <th>Duration</th>
                                                <th>First Call</th>
                                                <th>last Call</th>
                                            </thead>
                                            <tbody>
                                                {#each rf_data as _rfd}
                                                    <tr>
                                                        <td>{_rfd.destination_number}</td>
                                                        <td>{_rfd.call_in}</td>
                                                        <td>{_rfd.call_out}</td>
                                                        <td>{_rfd.total_calls}</td>
                                                        <td>{_rfd.duration}</td>
                                                        <td>{_rfd.first_call}</td>
                                                        <td>{_rfd.last_call}</td>
                                                    </tr>
                                                {/each}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "device"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Imei</h3>
                                        {#each rf_data as _rfd}
                                            <p class="card-text">{_rfd}</p>
                                        {/each}
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "incoming"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Incoming</h3>
                                        <table>
                                            <thead>
                                                <th>Destination Number</th>
                                                <th>Calls</th>
                                            </thead>
                                            <tbody>
                                                {#each rf_data as _rfd}
                                                    <tr>
                                                        <td>{_rfd.destination_number}</td>
                                                        <td>{_rfd.total_record}</td>
                                                    </tr>
                                                {/each}
                                            </tbody>
                
                                            </table>
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "outgoing"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Outgoing</h3>
                                        <table>
                                            <thead>
                                                <th>Destination Number</th>
                                                <th>Calls</th>
                                            </thead>
                                            <tbody>
                                                {#each rf_data as _rfd}
                                                    <tr>
                                                        <td>{_rfd.destination_number}</td>
                                                        <td>{_rfd.total_record}</td>
                                                    </tr>
                                                {/each}
                                            </tbody>
                
                                            </table>
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "vpn"}
                            <div class="container">
                                    <div class="card devicediv">
                                        <div class="card-body">
                                            <h3 class="card-title">VPN</h3>
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>VPN</th>
                                                        <th>Uplink Usage</th>
                                                        <th>Downlink Usage</th>
                                                        <th>IP Count</th>
                                                        <th>Usage Count</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {#each rf_data as td}
                                                    <tr>
                                                        <td>{td['vpn']}</td>
                                                        <td>{td['downlink_vol']}</td>
                                                        <td>{td['uplink_vol']}</td>
                                                        <td>{td['count_of_unique_destination_ips_of_vpn']}</td>
                                                        <td>{td['total_destination_ips_count_of_vpn']}</td>
                                                    </tr>
                                                    {/each}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                            </div>
                            {:else if showresult && mode === "foreign_isp"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Foreign ISP</h3>
                                        <table>
                                            <thead>
                                                <tr>
                                                  <th>Destination Ip</th>
                                                  <th>Vendor</th>
                                                  <th>Country</th>
                                                  <th>Downlink_Usage</th>
                                                  <th>Uplink_Usage</th>
                                                  <th>Total Record</th>
                                                </tr>
                                              </thead>
                                            <tbody>
                                                {#each rf_data as td}
                                                <tr>
                                                    <td>{td["ip"]}</td>
                                                    <td>{td["vendor"]}</td>
                                                    <td>{td["country"]}</td>
                                                    <td>{td["downlink_vol"]}</td>
                                                    <td>{td["uplink_vol"]}</td>
                                                    <td>{td["count"]}</td>                
                                                </tr>
                                                {/each}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "shared_device"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Shared Device</h3>
                                        <table>
                                            <thead>
                                                <tr>
                                                  <th>IMEI</th>
                                                  <th>Source Number</th>
                                                </tr>
                                              </thead>
                                            <tbody>
                                                {#each rf_data as result, i}
                                                    {#each result.source_numbers as site, j}
                                                        <tr>
                                                        {#if j === 0}
                                                            <td rowspan={result.source_numbers.length}>{result.imei}</td>
                                                        {/if}
                                                        <td>{site}</td>
                                                        </tr>
                                                    {/each}
                                                {/each}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            {:else if showresult && mode === "silent_days"}
                            <div class="container">
                                <div class="card devicediv">
                                    <div class="card-body">
                                        <h3 class="card-title">Silent Days</h3>
                                        <table>
                                            <thead>
                                                <tr>
                                                  <th>Source Number</th>
                                                  <th>Start date</th>
                                                  <th>End date</th>
                                                  <th>Inactive Days</th>
                                                </tr>
                                              </thead>
                                            <tbody>
                                                {#each rf_data as td}
                                                <tr>
                                                    <td>{td["source_number"]}</td>
                                                    <td>{td["start_date"]}</td>
                                                    <td>{td["end_date"]}</td>
                                                    <td>{td["inactive_dates"].length}</td>
                
                                                    
                                                </tr>
                                                {/each}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            {/if}
                        </div>
          </div>
                </div>
              </div>
            </div>
            {/each}
        </div>

          
          
        
        
        

        
        
    </div>
</main>
    


<style>
    main{
        margin-left: 5%;
    }
    img {
        width: 5rem;
        height: 5rem;
    }
    .redflagbutton {
        border: none;
    }
    .acc-name{
        margin-right:30px;
    }
    .devicediv{
        margin: 2%;
        height: 25vh;
        overflow-y: scroll;
    }

    .card-body {
        margin-bottom: 0.5rem;
    }

    .card {
        width: 80%;
    }
    .alert {
        margin: 4%;
    }
    .notify{
        height:100vh;
        overflow: auto;
    }
    .grid-container {
    width: 50%;
    height: 20vh;
    overflow-y: scroll;
  }

  .grid-container table {
    width: 100%;
    margin: 0;
  }
  .grid-container table tbody tr td {
    background: #d4ebf7;
    border-collapse: separate;
  }

  .accordion {
    margin-top: 1rem;

  }
  h2 {
    text-align: center;
  }
  
  
</style>