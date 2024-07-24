<script>

  // @ts-nocheck

  import DayandNightLocation from "$lib/Location/DayandNightLocation.svelte";
  import TopTenDaysLocation from "$lib/Location/TopTenDaysLocationBetweenDates.svelte";
  import TopTenNightsLocation from "$lib/Location/TopTenNightsLocationDates.svelte";
  import TotalLocation from "$lib/Location/TotalLocation.svelte";
  import * as XLSX from "xlsx";
  import { writable } from 'svelte/store';
  import { get } from 'svelte/store';
  import { userDetailsStore } from '$lib/datastore.js';
  import { onMount } from "svelte";

  




  let number = "";
  let startDate = "";
  let endDate = "";
  let mode = "";
  let showdata = false;
  let gotResult = false;
  let dataDownload = [];
  let isSubmitted = false;
  let selectedmode = "";
  let propData;



  function handlesubmit() {
    propData = {}
    isSubmitted = true;
    mode = selectedmode;
    propData['number'] = number
    propData['startdate'] = startDate
    propData['enddate'] = endDate;
  }

  function updateDataForDownload(newData) {
    console.log(newData)
    dataDownload = newData['detail'];
  }

  function downloadData() {
    // const data = get(dataDownload);
    if (Array.isArray(dataDownload) && dataDownload.length > 0) {
      const ws = XLSX.utils.json_to_sheet(dataDownload);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      // XLSX.writeFile(wb, "data.xlsx");
      XLSX.writeFile(wb, `${number}_${startDate}_${endDate}_${mode}.xlsx`);
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
      <!-- <label class=" input-label" for="mobileNumber">Enter Mobile Number</label> -->
      <input class="input-field" id="mobileNumber"  type="text" placeholder=" Enter  Mobile no" size="10" bind:value={number}/>
      <label for="fromDate">From Date:</label>
      <input class="date-input" id="fromDate" type="datetime-local" bind:value={startDate}/>
      <label for="toDate">To Date:</label>
      <input class="date-input" id="toDate" type="datetime-local" bind:value={endDate}/>         
      <!-- <label class="input-label" for="option">Mode</label> -->
      <select name="" id="filter_type" bind:value={selectedmode}>
        <option value="" disabled>Mode</option>
          <option value="TopTenDaysLocation">Top 10Days Location</option>
          <option value="TopTenNightLocation">TOP 10Night  Location</option>
          <option value="TotalLocation">Total Location</option>
          <option value="DayandNightLocation">Days and Nights Location</option>
          <!-- <option value="TotalLocation">Total Location</option> -->
      </select>
      <button class="submit" on:click={handlesubmit}>Submit</button>
      <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
  </div>
<div>
</main>

<div>
  {#if isSubmitted}
    
    {#if mode === "TopTenDaysLocation"}
      <TopTenDaysLocation {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "TopTenNightLocation"}
      <TopTenNightsLocation {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "TotalLocation"}
      <TotalLocation {propData} on:updateData = {updateDataForDownload}/>
    {/if}
    {#if mode === "DayandNightLocation"}
    <DayandNightLocation {propData} on:updateData = {updateDataForDownload}/>
    {/if}
  {/if}
</div>

<style>
  main {
    margin-left: 4%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 15px;
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
    /* box-shadow: 5px 5px gray; */
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

  .input-field {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 20vw;
  }
  .date-input {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 15vw;
  }
  #filter_type {
    /* margin-right: 10px;  */
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 17vw;
  }

  /* .select-state{
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 12vw;

  } */
  .submit {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 10vw;
    /* position: absolute;
            right: 20px;
            top: 20px */
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