<script>
        import Previewmodal from '$lib/modal/Previewmodal.svelte';
    import Numbersummary from '$lib/towercdr/Numbersummary.svelte';


    export let data;
    export let number;
    console.log(data,"---------")

    let summary_of_app = data.data_dict[0].ipdr_profile.summary_app;
    let summary_of_vpn = data.data_dict[0].ipdr_profile.summary_vpn;
    let summary_of_iptype = data.data_dict[0].ipdr_profile.summary_iptype;
    let summary_of_country = data.data_dict[0].ipdr_profile.summary_country;

    let mode;
    let show_modal = false;

    function renderdata(val){
        console.log(number,mode,"in profile")
        show_modal = true
        mode = val
    }

 
    

</script>
<dialog id="my_modal_4" class="modal fixed inset-0 z-50 overflow-y-auto">
    <div class="modal-box w-11/12 max-w-7xl mx-auto bg-white shadow-lg rounded-md p-6">
      <h3 class="font-bold text-2xl mb-4">Hello!</h3>
      <p class="mb-4">Click the button below to close</p>
      <Numbersummary {number} />
  
      <div class="modal-action flex justify-end mt-4">
        
      </div>
    </div>
    <div>
        <form method="dialog">
            <!-- if there is a button, it will close the modal -->
            <button class="btn px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Close</button>
          </form>
    </div>
  </dialog>
  
<div class="relatieve h-[100vh] w-[100vw]">
    {#each data.data_dict as item}
          <div class="flex">
            <div class="profile-img w-2/12 p-2">
                <img src="propic.jpeg" alt="Profile Picture" class="profile-picture">
                <p id="number"><b>Number :</b>{item['number']}</p>
                <p id="name"><b>Name :</b>undefined</p>
                <h2 class="bg-blue-500 text-white p-4">Red Flag Indications</h2>
                <div class="flex items-center">
                    <label for="" class='font-bold px-5'>Red flag name:</label>
                    <p class="info-item" id="call_end_date">False</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Red flag name:</label>
                  <p class="info-item" id="call_end_date">True</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Red flag name:</label>
                  <p class="info-item" id="call_end_date">False</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Red flag name:</label>
                  <p class="info-item" id="call_end_date">True</p>
                </div>
          </div>
          <div class="flex">
          <!-- CDR Profile -->
              <div class="cdrpro w-/12">
                <h1 class="bg-blue-500 text-white p-4">CDR Profile</h1>
                {#each data.headers as header}

                    {#if header === "call_count"}
                    <label for="sidekey" class="font-bold p-5">Call Count:</label>
                    <a href="/home?value={number}&mode=total_calls" target="_blank">{item[header]}</a><br>
                    {:else if header === "call_in" || header === "call_out" || header === "total_calls"}
                    <label for="sidekey" class="font-bold">Call Count:</label>

                    <a href="/home?value={number}&mode={header}&dest_number={item["destination_number"]}" target="_blank">{header}: {item[header]}</a><br>
                    {:else if header === "destination_number"}
                    <label for="sidekey" class="font-bold">Destination Number:</label>

                    <a href="/home?value={item[header]}&mode=dest_num" target="_blank"> {item[header]}</a><br>
                    {:else if header === "cellid"}
                    <label for="sidekey" class="font-bold">Cell Id:</label>
                    <a href="/home?value={item[header]}&mode=cellidsearch" target="_blank">Cell ID: {item[header]}</a><br>
                    {:else if header === "imei"}
                    <label for="" class="font-bold p-5">IMEI:</label>
                    <a href="/home?value={number}&mode=imei&imei_num={item[header]}" target="_blank">
                      <span class="value">{item[header].length}</span>
                    </a>
                  
                    {:else if header === "total_contacts"}
                    <label for="" class="font-bold p-5 text-red-600">Total Contacts</label>
                      <a href="/home?value={number}&mode=total_contacts&dest_number={item[header]}" target="_blank">
                        <!-- <span class="key">Total Contacts <br></span> -->
                        <span class="value">{item[header].length}</span>
                      </a><br>
                    {:else if header === "cdat_count"}
                      <label for="" class="font-bold p-5">CDAT Count:</label>
                          <a class="text-red-900" href="/home?value={number}&mode=cdat_count" target="_blank">
                            <!-- <span class="key">CDAT Count <br></span> -->
                              <span class="value">{item[header].length}</span>
                          </a><br>
                      {:else if header === "other_states"}
                      <label for="sidekey" class="font-bold p-5">Other States :</label>
                      <a href="/home?value={number}&mode=other_states&states={item[header]}" target="_blank">
                          <span class="value">{item[header].length}</span>
                        </a>
                      <br>
                      {:else if header === "dest_count"}
                      <label for="sidekey" class="font-bold">Dest Count :</label>

                      <a href="/home?value={number}&mode=dest_count&dest_count={item[header]}" target="_blank">Destination Count {item[header].length}</a><br>
                  
                      {/if}
                {/each}
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Call Start Date :</label>
                  <p class="info-item" id="call_start_date">{item['call_start_date']}</p>
                </div>
                
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Call end date :</label>
                  <p class="info    import Summaryipdr from '$lib/ipdrsummary/Summaryipdr.svelte';
                  -item" id="call_end_date">{item['call_end_date']}</p>

                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>NICKNAME :</label>
                  <p class="info-item" id="nickname">{item['nickname']}</p>

                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>CAT :</label>
                  <p class="info-item" id="cat">{item['cat']}</p>
                </div>
                
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Org</label>
                  <p class="info-item" id="org">{item['org']}</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Module</label>
                  <p class="info-item" id="module">{item['module']}</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Last Updated</label>
                  <p class="info-item" id="last_updated">{item['last_updated']}</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Address</label>
                  <p class="info-item" id="address">{item['address']}</p>
                </div>
                <div class="flex items-center">
                  <label for="" class='font-bold px-5'>Io Name</label>
                  <p class="info-item" id="io_name">{item['io_name']}</p>

                </div>
                <div class="flex items-center">
                  <label for="" class="font-bold px-5">Caf:</label>
                  <p class="info-item" id="caf">{item['caf']}</p>  
                </div>
              </div>
              <!-- Tower profile -->

              <div class="towerpro 4/13">
                <h1 class="bg-red-500 text-white p-4">Tower Profile</h1>
                
                <div class="table-like-container">
                    <div class="table-row">
                        <div class="table-cell">
                          <label for="" class="font-bold">Imei:</label>
                        </div>
                        <div class="table-cell px-10">
                          <p class="info-item" id="caf">{item['tower_imei'].length}</p>
                        </div>
                    </div>

                    <div class="table-row">
                      <div class="table-cell">
                        <label for="" class="font-bold">Valid Contacts:</label>
                      </div>
                      <div class="table-cell px-10">
                        <p class="info-item" id="caf">{item['validUniqueCount']}</p>
                      </div>
                    </div>
                  
                    <div class="table-row">
                      <div class="table-cell">
                        <label for="" class="font-bold">Invalid Contacts:</label>
                      </div>
                      <div class="table-cell px-10">
                        <p class="info-item" id="caf">{item['notValidUniqueCount']}</p>
                      </div>
                    </div>
                  
                    <div class="table-row">
                      <div class="table-cell">
                        <label for="" class="font-bold">Dates Present:</label>
                      </div>
                      <div class="table-cell px-10">
                        <p class="info-item" id="caf">{item['dates_present']}</p>
                      </div>
                    </div>
                  
                    <div class="table-row">
                      <div class="table-cell">
                        <label for="" class="font-bold">Dates Difference:</label>
                      </div>
                      <div class="table-cell px-10">
                        <p class="info-item" id="caf">{item['date_difference']}</p>
                      </div>
                    </div>
                  
                    <div class="table-row">
                      <div class="table-cell">
                        <label for="" class="font-bold">Other Number:</label>
                      </div>
                      <div class="table-cell px-10">
                        <p class="info-item" id="caf">{item['other_number']}</p>
                      </div>
                    </div>
                  
                <div class="table-row">
                    <div class="table-cell">
                        <label for="" class="font-bold">Tower Present:</label>
                      </div>
                    <div class='has-tooltip table-cell px-10'>
                        <h2 class="bg-red-100 p-3 [w-100]"> {item['tower'].length}</h2>
                            <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                                <div class="overflow-x-auto">
                                    <table class="min-w-full bg-white border border-neutral-300 dark:border-neutral-700">
                                    <thead>
                                        <tr class="bg-primary dark:bg-primary-dark text-white">
                                        <th class="py-2 px-4">
                                            <input type="checkbox">
                                        </th>
                                        <th class="py-2 px-4">IP</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each item['tower'] as _t}
                                        <tr class="hover:bg-gray-100 text-r dark:hover:bg-gray-800">
                                        <td class="py-2 px-4">
                                            <input type="checkbox" name="" id="" bind:checked={_t.isSelected}>
                                        </td>
                                        <td class="py-2 px-4 text-left">{_t}</td>
                                        </tr>
                                        {/each}
                                    </tbody>
                                    </table>
                                </div>
                                <button class="hover:bg-purple-300 mx-10">Analyse Selected Towers</button>
                                
                            </span>
                        </div>                
                </div>
                <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Sectors Availabels Number:</label>
                    </div>
                    <div class="table-cell px-10">
                      <p class="info-item" id="">{item['sector'].length}</p>
                    </div>
                  </div>
                
                  <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Imei in CDR:</label>
                    </div>
                    
                    <div class='has-tooltip table-cell px-10'>
                        <h2 class="bg-red-100 p-3 [w-100]"> {item['imei_count_cdr'].length}</h2>
                            <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mr-80'>
                                <div class="overflow-x-auto">
                                    <table class="min-w-full bg-white border border-neutral-300 dark:border-neutral-700">
                                    <thead>
                                        <tr class="bg-primary dark:bg-primary-dark text-white">
                                        
                                        <th class="py-2 px-4">Imei</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each item['imei_count_cdr'] as _t}
                                        <tr class="hover:bg-gray-100 dark:hover:bg-gray-800">
                                        <td class="py-2 px-4 ">{_t}</td>
                                        </tr>
                                        {/each}
                                    </tbody>
                                    </table>
                                </div>
                                <!-- <button class="hover:bg-purple-300 mx-10">Analyse Selected Towers</button> -->
                                
                            </span>
                        </div>
                  </div>
                
                  <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Total calls:</label>
                    </div>
                    <div class="table-cell px-10">
                      <p class="info-item" id="caf">{item['total_call_count']}</p>
                    </div>

                  </div>
                
                  <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Ratio Call:</label>
                    </div>
                    <div class="table-cell px-10">
                      <p class="info-item" id="caf">{item['ratio_call']}</p>
                    </div>
                  </div>
                
                  <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Sms Ratio:</label>
                    </div>
                    <div class="table-cell px-10">
                      <p class="info-item" id="caf">{item['ratio_sms']}</p>
                    </div>
                  </div>
                
                  <div class="table-row">
                    <div class="table-cell">
                      <label for="" class="font-bold">Total Ratio:</label>
                    </div>
                    <div class="table-cell px-10">
                      <p class="info-item" id="caf">{item['ratio']}</p>
                    </div>
                  </div>
            </div>
            <div class="table-row">
                <div class="table-cell">
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onclick="my_modal_4.showModal()">Summary</button>

                    <!-- <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"><a href="#my_modal_8" class="">Summary</a> -->
                        <!-- </button> -->
                </div>
                <div class="table-cell px-4">
                    <button class="bg-green-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click="{()=>renderdata('towercdr')}">Tower CDR</button> 
                </div>
              </div>

            </div>
              
            </div>
          </div>
          <!-- IPDR DATA -->
        <div>
            <h1 class="bg-purple-500 text-white p-4">IPDR Profile</h1>
          <div class="ipdrpro flex">
            <div class="flex items-center w-1/1">
                <label for="" class='font-bold px-5'>Device Used</label>
                <div class='has-tooltip'>
                    <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                        <table class="dark:border-neutral-500">
                            <thead>
                                <th>Imei</th>
                                <th>Count</th>
                                <th>Start time</th>
                                <th>End Time</th>

                            </thead>
                            <tbody>
                                    {#each item.ipdr_profile.device  as v_p}
                                    <tr>
                                        <td>{v_p['_id']}</td>
                                        <td>{v_p['count']}</td>
                                        <td>{v_p['max_date']}</td>
                                        <td>{v_p['min_date']}</td>
    
                                    </tr>
                                    {/each}
                                </tbody>
                            </table>
                    </span>
                    {item.ipdr_profile.device.length}
                </div>             
             </div>

            <div class=" w-1/1">
                <div class='has-tooltip flex items-center'>
                        <h2 class="bg-red-100 p-3 [w-100]"> VPN Used - {item.ipdr_profile.allvpn.length}</h2>
                    <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                        <table class="dark:border-neutral-500">
                            <thead>
                                <th>Vpn Name</th>
                                <th>IP</th>
                                <th>Download Vol</th>
                                <th>Uplink Vol</th>
                                <th>Duration</th>
                                <th>Start time</th>
                                <th>End Time</th>
                            </thead>
                            <tbody>
                                    {#each item.ipdr_profile.allvpn  as v_p}
                                    <tr>
                                        <td>{v_p['VPN']}</td>
                                        <td>{v_p['VPN_IP']}</td>
                                        <td>{v_p['downlink_vol']}</td>
                                        <td>{v_p['uplink_vol']}</td>
                                        <td>{v_p['duration']}</td>
                                        <td>{v_p['start_time']}</td>
                                        <td>{v_p['end_time']}</td>

                                    </tr>
                                    {/each}
                                </tbody>
                            </table>
                    </span>
                </div>
                <div class="px-3">

                    {#if summary_of_vpn && summary_of_vpn.total_unique_vpn_count}
                    <p >
                        The highest count vpn - <b>{summary_of_vpn.highest_count_vpn.VPN}</b><br>
                        Total destination IP count - <b>{summary_of_vpn.highest_count_vpn.total_destination_ips_count_of_vpn}</b> -> <b>{summary_of_vpn.highest_count_vpn_ip}</b>.<br>
                        The lowest count vpn - <b>{summary_of_vpn.lowest_count_vpn.VPN}</b><br>
                        Total destination IP count of <b>{summary_of_vpn.lowest_count_vpn.total_destination_ips_count_of_vpn}</b> -> <b>{summary_of_vpn.lowest_count_vpn_ip}</b>.<br>
                        The total unique vpn count is <b>{summary_of_vpn.total_unique_vpn_count}</b>
                    </p>
                    {:else}
                    <p class="container">VPN Summary is not available.</p>
                    {/if}
                </div>
             
            </div>

               

            
          <div class="flex items-center w-1/1">
            <label for="" class='font-bold px-5'>Apps used</label>
            <div class='has-tooltip'>
                <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-20 mx-2'>
                    <table class="dark:border-neutral-500">
                        <thead>
                            <th>App Name</th>
                            <th>Unique Ip</th>
                            <th>Total Destination ip Vol</th>
                            
                        </thead>
                        <tbody>
                                {#each item.ipdr_profile.app  as a_p}
                                <tr>
                                    <td>{a_p['APP']}</td>
                                    <td>{a_p['count_of_unique_destination_ips_of_app']}</td>
                                    <td>{a_p['total_destination_ips_count_of_app']}</td>

                                </tr>
                                {/each}
                            </tbody>
                        </table>
                </span>
                {item.ipdr_profile.app.length}
                </div>
          </div>
          <div class="flex items-center w-1/1">
            <label for="" class='font-bold px-5'>Country Visited</label>
            
                <div class='has-tooltip'>
                    <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                        <table class="dark:border-neutral-500">
                            <thead>
                                <th>Country Name</th>
                                <th>Unique Ip</th>
                                <th>Number of times used</th>
                                
                            </thead>
                            <tbody>
                                    {#each item.ipdr_profile.country  as c_p}
                                    <tr>
                                        <td>{c_p['COUNTRY']}</td>
                                        <td>{c_p['count_of_unique_destination_ips_of_country']}</td>
                                        <td>{c_p['total_destination_ips_count_of_country']}</td>
    
                                    </tr>
                                    {/each}
                                </tbody>
                            </table>
                    </span>
                    {item.ipdr_profile.country.length}
                </div>          
            </div>
          <div class="flex items-center w-1/1">
            <label for="" class='font-bold px-5'>Foreign Isp</label>
            <div class='has-tooltip'>
                <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                    <table class="dark:border-neutral-500">
                        <thead>
                            <th>Country Name</th>
                            <th>ip</th>
                            <th>Usage</th>
                            <th>Vendor</th>
                            
                        </thead>
                        <tbody>
                                {#each item.ipdr_profile.foreign_isp  as c_p}
                                <tr>
                                    <td>{c_p['country']}</td>
                                    <td>{c_p['ip']}</td>
                                    <td>{c_p['usage']}</td>
                                    <td>{c_p['vendor']}</td>


                                </tr>
                                {/each}
                            </tbody>
                        </table>
                </span>
                {item.ipdr_profile.foreign_isp.length}
            </div>  
          </div>
          <div class="flex items-center w-1/1">
            <label for="" class='font-bold px-5'>Indian Isp</label>
            <div class='has-tooltip'>
                <span class='tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2'>
                    <table class="dark:border-neutral-500">
                        <thead>
                            <th>ip</th>
                            <th>Usage</th>
                            <th>Vendor</th>
                            
                        </thead>
                        <tbody>
                                {#each item.ipdr_profile.isp_india  as c_p}
                                <tr>
                                    <td>{c_p['ip']}</td>
                                    <td>{c_p['usage']}</td>
                                    <td>{c_p['vendor']}</td>


                                </tr>
                                {/each}
                            </tbody>
                        </table>
                </span>
                {item.ipdr_profile.isp_india.length}
            </div>  
          </div>
          </div>
        </div>

            {/each}

        
</div>



<style>

.tooltip {
  @apply invisible absolute;
}

.has-tooltip:hover .tooltip {
  @apply visible z-50;
}

</style>