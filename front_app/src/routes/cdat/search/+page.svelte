<script>
       // @ts-nocheck

  import Cellidsearch from "$lib/search/Cellidsearch.svelte";
  import Imsisearch from "$lib/search/Imsisearch.svelte";
  import Nicknamesearch from "$lib/search/Nicknamesearch.svelte";
  import PhoneImsi from "$lib/search/PhoneImsi.svelte";
  import Singleaddress from "$lib/search/Singleaddress.svelte";
  import CommonContactsMulti from "$lib/CallDetails/CommonContactsMulti.svelte";
  import NumberSearch from "$lib/analysis/numberSearch.svelte";
  import NameSearch from "$lib/analysis/nameSearch.svelte";
  import DateTarget from "$lib/analysis/dateTarget.svelte";
  import RoamingDetails from "$lib/analysis/roamingDetails.svelte";
  import Activeperiod from "$lib/analysis/activeperiod.svelte";
  import * as XLSX from "xlsx";
  import { userDetailsStore } from '$lib/datastore.js';
  import { onMount } from "svelte";
  import Rechargehistory from "$lib/analysis/rechargehistory.svelte";
  import Smpoa from "$lib/analysis/smpoa.svelte";
  import AlternateNumber from "$lib/analysis/alternateNumber.svelte";
  import AddressSearch from "$lib/analysis/addressSearch.svelte";


  let number = "";
  let endDate =  "";
  let startDate= "";
  let mode = "";
  let name = "";
  let address;
  let dataDownload = [];
  let isSubmitted = false;
  let selectedmode = "";
  let propData;

  function handlesubmit() {
    propData = {}
    isSubmitted = true;
    mode = selectedmode;
    console.log(mode)
    propData['number'] = number
    propData['startdate'] = startDate
    propData['enddate'] = endDate
    propData['name'] = name
    propData['address'] = address
    console.log(propData)
  }

  function updateDataForDownload(newData) {
      console.log(newData)
      dataDownload = newData['detail'];
  }

  function downloadData() {
    if (Array.isArray(dataDownload) && dataDownload.length > 0) {
        const ws = XLSX.utils.json_to_sheet(dataDownload);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
        if (mode === "Cellidsearch"){
        XLSX.writeFile(wb, `${mode}.xlsx`);
      }else{
        XLSX.writeFile(wb, `${number}_${mode}.xlsx`);
        }
    } else {
        console.error("Invalid data format for XLSX export:", dataDownload);
    }
  }

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
<main>
  <div class="input-container">
    <div class="input-row">
          <select name="" placeholder="Select Mode" id="filter_type" bind:value={selectedmode}>
            <option value="" disabled>Mode</option>
            <option value="Singleaddress">Single Address</option>
            <option value="AddressSearch">Bulk Address</option>      
            <option value="NumberSearch">Address Search</option>
            <option value="CommonCantacts">Common Contacts</option>
            <option value="Cellidsearch">CellID Search</option>
            <option value="Imsisearch">IMSI Search</option>
            <option value="PhoneImsi">Phone To IMSI</option>
            <option value="Nicknamesearch">NickName Search</option>
            <option value="NameSearch">Name Search</option>
            <option value="DateTarget">Date Target</option>
            <option value="RoamingDetails">Roaming Details</option>
            <option value="Activeperiod">Active Period</option>
            <option value="RechargeHistory">RechargeHistory</option>
            <option value="sm_poa">SMPOA</option>
            <option value="alternate_number">Alternate Number</option>
          </select>
          {#if selectedmode === 'AddressSearch'}
            <input class="input-field" type = "text" placeholder="Enter Address" bind:value={address}/>
          {:else if selectedmode === 'CommonCantacts' || selectedmode === 'NumberSearch' || selectedmode === 'RoamingDetails'}
            <input class="input-field" type="text" placeholder="Enter Number" bind:value={number}/>
            <input class="date-input" type="date" placeholder="Enter StartDate" bind:value={startDate}/>
            <input class="date-input" type="date" placeholder="Enter EndDate" bind:value={endDate}/>
          {:else if selectedmode === 'Nicknamesearch' || selectedmode === 'NameSearch'}
            <input class="input-field" type="text" placeholder="Enter Name" bind:value={name}/>
          {:else if selectedmode === 'DateTarget' || selectedmode === 'Activeperiod' || selectedmode === 'Cellidsearch' || selectedmode === 'Imsisearch' || selectedmode === 'PhoneImsi' || selectedmode === 'Singleaddress'}
            <input class="input-field" type="text" placeholder="Enter Number" bind:value={number}/>
          {:else if selectedmode === "RechargeHistory"}
        <input  class="input-field"   type="text"  placeholder="Enter Number"  bind:value={number} />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "sm_poa"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "alternate_number"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
          {/if}
          <button class="submit" on:click={handlesubmit}>Submit</button>
          <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
      </div>  
  </div>
  <div>
    {#if mode === "PhoneImsi"}
      <PhoneImsi {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "Imsisearch"}
      <Imsisearch {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "Singleaddress"}
      <Singleaddress {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "Cellidsearch"}
       <Cellidsearch {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "Nicknamesearch"}
      <Nicknamesearch {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "CommonCantacts"}
      <CommonContactsMulti {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "NumberSearch"}
      <NumberSearch {propData}  on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "DateTarget"}
      <DateTarget {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "RoamingDetails"}
      <RoamingDetails {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "Activeperiod"}
      <Activeperiod {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "NameSearch"}
      <NameSearch {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "RechargeHistory"}
      <Rechargehistory {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "sm_poa"}
      <Smpoa {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "alternate_number"}
      <AlternateNumber {propData} on:updateData={updateDataForDownload} />
    {/if}
    
    {#if mode === "AddressSearch"}
    <AddressSearch {propData} on:updateData={updateDataForDownload} />
  {/if}
  </div>
</main>

<style>
  main {
    margin-left: 4%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
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
  }
  .input-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .date-input {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 12vw;
  }

  .input-field {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 18vw;
  }
  #filter_type {
    margin-right: 10px;
      flex-grow: 1;
      background-color: white;
      border: none;
      font-size: 1.2em;
      color: #296b97;
      height: 4vh;
      border-radius: 3px;

  }
  .submit,.download-button {
    flex-grow: 0;
  }
  .submit {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 10vw;
  }
  .download-button {
    background-color: #3498db;
    padding: 8px 15px;
    color: white;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    /* margin: 4px 2px; */
    transition-duration: 0.4s;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    /* position: absolute;
              right: 20px; */
    border-radius: 50%;
  }
</style>


  