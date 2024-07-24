<script>
  // @ts-nocheck
  
      import { onMount } from 'svelte';
      import { basepath } from "$lib/config";
      import Summaryipdr from '$lib/ipdrsummary/Summaryipdr.svelte';
      import Country from '$lib/ipdrsummary/Country.svelte';
      import { count } from 'd3';
      import Device from '$lib/ipdrsummary/Device.svelte';
      import AppData from '$lib/ipdrsummary/AppData.svelte';
      import Isp from '$lib/ipdrsummary/Isp.svelte';
      import Vpn from '$lib/ipdrsummary/Vpn.svelte';
      import Voip from '$lib/ipdrsummary/Voip.svelte';
      import Matchedcall from '$lib/ipdrsummary/Matchedcall.svelte';
      import { userDetailsStore } from '$lib/datastore.js';
      import { postRequest } from '$lib/req_utils';

    
      let number = ''; 
      let summary_of_app;
      let summary_of_country;
      let summary_of_iptype;
      let summary_of_vpn;
      let country_data;
      let device;
      let vpn_data;
      let app_data;
      let foreign_isp_data;
      let india_isp_data;
      let all_vpn;
      let voip_data;
      let matched_call;
    
      let mode = 'summary';
    
      
       function fetchData() {
        const fetchData = new FormData();
        fetchData.append("number",number);
        fetchData.append("mode","summary_ipdr")
        // fetch(`${basepath()}/call_details`, {
        //   method: 'POST',
         
        //   body: fetchData
        // })

        const url = `${basepath()}/call_details`;
        postRequest(fetch,url,fetchData)
        .then(response =>response.json())
        .then(data => {
          console.log(data)
            all_vpn = data.allvpn
            summary_of_app = data.summary_app
            summary_of_country = data.summary_country
            summary_of_vpn = data.summary_vpn
            summary_of_iptype = data.summary_iptype
            country_data = data.country
            vpn_data = data.vpn
            app_data = data.app
            voip_data = data.voip
            matched_call = data.matchedcall
            device = data.device
            india_isp_data = data.isp_india
            foreign_isp_data = data.foreign_isp
            
        })
          
      }
    
      // onMount(() => {
      //   fetchData();
      // });
      let userDetails;
            userDetailsStore.subscribe(value => {
            userDetails = value;
            });
            onMount(() => {
            // beware of truthy and falsy values
            if (localStorage.getItem("userAuth")==="true"){
            userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
            }
            else{
            goto('/');
            }
        });
  

  
  
    
    </script>
    <div class="main">
    <div class="input-container">
      <div class="input-row">
        <label style="margin-left:4" for="" class="input-label">IPDR Summary </label>
      <input
        type="text"
        placeholder="Search Here"
        class="input-field"
        bind:value={number}
      />
      <button class="btn_1" on:click={fetchData}>Search</button>
      </div>
      
    </div>
    
    <div class="ipdr_body">
      <div class="tabs">
        <button id='button' class={mode === 'summary' ? 'active' : ''} on:click={() => mode = 'summary'}>Summary</button>
        <button id='button' class={mode === 'country' ? 'active' : ''} on:click={() => mode = 'country'}>Country</button>
        <button id='button' class={mode === 'vpn' ? 'active' : ''} on:click={() => mode = 'vpn'}>VPN</button>
        <button id='button' class={mode === 'app' ? 'active' : ''} on:click={() => mode = 'app'}>App</button>
        <button id='button' class={mode === 'device' ? 'active' : ''} on:click={() => mode = 'device'}>Device</button>
        <button id='button' class={mode === 'voip' ? 'active' : ''} on:click={() => mode = 'voip'}>VOIP</button>
        <button id='button' class={mode === 'isp' ? 'active' : ''} on:click={() => mode = 'isp'}>ISP</button>
        <button id='button' class={mode === 'matchedcall' ? 'active' : ''} on:click={() => mode = 'matchedcall'}>Matched Calls</button>
    
      </div>
    
      {#if mode === 'summary'}
        {#if summary_of_app || summary_of_country || summary_of_iptype || summary_of_vpn }
          <Summaryipdr {summary_of_app} {summary_of_country} {summary_of_iptype} {summary_of_vpn}/>
        {:else}
          <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    
      {#if mode === 'country'}
        {#if country_data}
          <Country {country_data} {number} />
        {:else}
          <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    
      {#if mode === 'isp'}
      {#if foreign_isp_data || india_isp_data}
        <Isp {foreign_isp_data} {india_isp_data} {number}/>
       {:else}
        <p>Loading Summary...</p>
      {/if}
      {/if}
    
    
    
      {#if mode === 'app'}
        {#if app_data}
        <AppData {app_data} {number}/>
        {:else}
          <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    
      {#if mode === 'device'}
      {#if device}
      <Device {device} {number}/>
      {:else}
        <p class ="container">Loading Summary...</p>
      {/if}
      {/if}
    
      {#if mode === 'vpn'}
        {#if all_vpn}
        <Vpn {all_vpn} {number}/>
        {:else}
          <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    
      {#if mode === 'voip'}
        {#if voip_data}
        <Voip {voip_data} {number}/>
        {:else}
        <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    
      {#if mode === 'matchedcall'}
        {#if matched_call}
        <Matchedcall {matched_call} {number}/>
        {:else}
        <p class ="container">Loading Summary...</p>
        {/if}
      {/if}
    </div>
  </div>
  <style>
    .main {
      margin-left: 4%;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 5px;
    }
  
    .active {
      /* background-color: #4CAF50; */
      /* background: linear-gradient(25deg, rgb(158, 215, 159), rgb(232, 222, 222)); */
      background: radial-gradient(circle at 0.7% 1%, rgb(215, 248, 247) 0%, rgb(102, 188, 239) 100.2%);
      color: white;
    }
  
    .input-container {
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
      margin-top: 5px;
    }
    .input-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    label {
      color: #296b97;
    }
  
    .btn_1 {
      padding: 8px 15px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      width: 10vw;
    }
    .btn_1:hover {
      background: #a5c2d5;
      color: white;
    }
  
    .input-label {
      display: flex;
      align-items: center;
      /* margin-left: 60px; */
      /* border-radius: 20px; */
    }
  
    .input-field {
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 74vw;
    }
    .input_filed:hover {
      background-color: aliceblue;
    }
  
    .ipdr_body {
      /* margin-left: 160px; */
      margin-top: 1vh;
      width: 100%;
    }
    .tabs{
      display: flex;
      justify-content: center;
      gap: 4px;
    }
  
    #button {
      height: 40px;
      width: 10%;
      font-size: 20px;
      border: none;
      /* transform: skew(18deg); */
    }
  
    #button:hover {
      background: radial-gradient(circle at 0.7% 1%, rgb(215, 248, 247) 0%, rgb(102, 188, 239) 100.2%);
      color: white;
    }
  
    .container {
      margin-top: 200px;
      display: flex;
      text-align: center;
      justify-content: center;
      font-size: 22px;
    }
  </style>
  